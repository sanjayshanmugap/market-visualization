"""
FastAPI Backend for Agentic Market Research Project
==================================================

REST API and WebSocket server for the market simulation UI.
Provides real-time market data, agent management, and simulation control.

Timeline: Month 5 - Human-in-the-Loop & Meta-Learning
Team: Team D - UX, Dashboards & Ops
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import asyncio
import json
import time
import logging
from datetime import datetime, timedelta
import uvicorn

# Import market simulation components
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core_engine import MarketSimulator, MarketConfig
from src.agents import AgentRegistry
from src.validation import FactChecker


# Pydantic models for API
class MarketDataRequest(BaseModel):
    symbol: str
    timeframe: str = "1m"


class AgentActionRequest(BaseModel):
    agent_id: str
    action_type: str
    parameters: Dict[str, Any]


class SimulationConfig(BaseModel):
    duration: float = 3600.0  # 1 hour
    time_step: float = 1.0
    agents: List[str] = []
    symbols: List[str] = ["AAPL", "GOOGL", "MSFT"]


class SimulationResponse(BaseModel):
    simulation_id: str
    status: str
    start_time: float
    duration: float
    agents: List[str]


# FastAPI app
app = FastAPI(
    title="Agentic Market Research API",
    description="API for multi-agent market simulation",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
market_simulator: Optional[MarketSimulator] = None
agent_registry: Optional[AgentRegistry] = None
fact_checker: Optional[FactChecker] = None
active_simulations: Dict[str, Dict] = {}
run_history: List[Dict[str, Any]] = []
# track last trade timestamp per symbol for WS broadcast
last_trade_ts: Dict[str, int] = {}
websocket_connections: List[WebSocket] = []

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    global market_simulator, agent_registry, fact_checker
    
    logger.info("Starting Agentic Market Research API")
    
    # Initialize market simulator
    now = datetime.utcnow()
    config = MarketConfig(
        simulation_id="backend_api",
        start_time=now,
        end_time=now + timedelta(minutes=10),
        symbols=["AAPL"],
        initial_prices={"AAPL": 100.0}
    )
    market_simulator = MarketSimulator(config)
    
    # Initialize agent registry
    agent_registry = AgentRegistry()
    
    # Initialize fact checker
    fact_checker = FactChecker()
    
    # Initialize last trade timestamps
    for sym in market_simulator.order_books.keys():
        last_trade_ts[sym] = 0

    # Start broadcaster task
    asyncio.create_task(broadcast_snapshots_task())

    logger.info("Application initialized successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down application")
    
    # Close all WebSocket connections
    for websocket in websocket_connections:
        await websocket.close()
    
    # Stop all active simulations
    for sim_id in list(active_simulations.keys()):
        await stop_simulation(sim_id)


# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")


manager = ConnectionManager()


# API Routes

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Agentic Market Research API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "active_simulations": len(active_simulations),
        "websocket_connections": len(manager.active_connections)
    }


@app.get("/api/market-data/{symbol}")
async def get_market_data(symbol: str):
    """Get market data for symbol"""
    if not market_simulator:
        raise HTTPException(status_code=500, detail="Market simulator not initialized")
    
    try:
        market_data = market_simulator.get_market_data(symbol)
        return market_data
    except Exception as e:
        logger.error(f"Error getting market data for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/market-data")
async def get_all_market_data():
    """Get market data for all symbols"""
    if not market_simulator:
        raise HTTPException(status_code=500, detail="Market simulator not initialized")
    
    try:
        all_data = market_simulator.get_all_market_data()
        return all_data
    except Exception as e:
        logger.error(f"Error getting all market data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/trades/{symbol}")
async def get_trades(symbol: str, lookback_seconds: int = 3600, limit: int = 200):
    """Get recent trades for a symbol"""
    if not market_simulator:
        raise HTTPException(status_code=500, detail="Market simulator not initialized")
    if symbol not in market_simulator.order_books:
        raise HTTPException(status_code=404, detail="Symbol not found")

    try:
        ob = market_simulator.order_books[symbol]
        now_ms = int(time.time() * 1000)
        since = now_ms - lookback_seconds * 1000
        # Prefer get_trades_since; fallback to get_trades
        if hasattr(ob, 'get_trades_since'):
            trades = ob.get_trades_since(since)
        elif hasattr(ob, 'get_trades'):
            trades = ob.get_trades()
        else:
            trades = []
        # Convert dataclasses to dicts if needed
        def to_dict(t):
            return {
                'buy_order_id': getattr(t, 'buy_order_id', None),
                'sell_order_id': getattr(t, 'sell_order_id', None),
                'price': getattr(t, 'price', 0.0),
                'quantity': getattr(t, 'quantity', 0),
                'timestamp': getattr(t, 'timestamp', 0),
            }
        items = [to_dict(t) for t in trades][-limit:]
        return {'symbol': symbol, 'trades': items}
    except Exception as e:
        logger.error(f"Error getting trades for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/simulation/start")
async def start_simulation(config: SimulationConfig):
    """Start a new simulation"""
    if not market_simulator:
        raise HTTPException(status_code=500, detail="Market simulator not initialized")
    
    try:
        # Generate simulation ID
        sim_id = f"sim_{int(time.time())}"
        
        # Start simulation
        simulation_task = asyncio.create_task(
            run_simulation(sim_id, config)
        )
        
        # Store simulation info
        active_simulations[sim_id] = {
            "task": simulation_task,
            "config": config,
            "start_time": time.time(),
            "status": "running"
        }
        
        # Broadcast simulation start
        await manager.broadcast(json.dumps({
            "type": "simulation_started",
            "simulation_id": sim_id,
            "config": config.dict()
        }))
        
        return SimulationResponse(
            simulation_id=sim_id,
            status="running",
            start_time=time.time(),
            duration=config.duration,
            agents=config.agents
        )
        
    except Exception as e:
        logger.error(f"Error starting simulation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/simulation/{sim_id}/stop")
async def stop_simulation(sim_id: str):
    """Stop a simulation"""
    if sim_id not in active_simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    try:
        simulation = active_simulations[sim_id]
        simulation["task"].cancel()
        simulation["status"] = "stopped"
        
        # Remove from active simulations
        del active_simulations[sim_id]
        
        # Broadcast simulation stop
        await manager.broadcast(json.dumps({
            "type": "simulation_stopped",
            "simulation_id": sim_id
        }))
        
        return {"message": "Simulation stopped", "simulation_id": sim_id}
        
    except Exception as e:
        logger.error(f"Error stopping simulation {sim_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/simulation/{sim_id}/status")
async def get_simulation_status(sim_id: str):
    """Get simulation status"""
    if sim_id not in active_simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    simulation = active_simulations[sim_id]
    return {
        "simulation_id": sim_id,
        "status": simulation["status"],
        "start_time": simulation["start_time"],
        "duration": time.time() - simulation["start_time"],
        "config": simulation["config"]
    }


@app.get("/api/simulation/history")
async def get_simulation_history():
    """Return recent simulation runs"""
    return {"history": run_history[-50:]}


@app.get("/api/agents")
async def get_agents():
    """Get all registered agents"""
    if not agent_registry:
        raise HTTPException(status_code=500, detail="Agent registry not initialized")
    
    try:
        agents = agent_registry.get_all_agents()
        return {"agents": agents}
    except Exception as e:
        logger.error(f"Error getting agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/agents/{agent_id}/action")
async def agent_action(agent_id: str, action: AgentActionRequest):
    """Execute agent action"""
    if not agent_registry:
        raise HTTPException(status_code=500, detail="Agent registry not initialized")
    
    try:
        # Get agent
        agent = agent_registry.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Execute action
        result = await execute_agent_action(agent, action)
        
        return {"result": result}
        
    except Exception as e:
        logger.error(f"Error executing agent action: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/fact-check/stats")
async def get_fact_check_stats():
    """Get fact checking statistics"""
    if not fact_checker:
        raise HTTPException(status_code=500, detail="Fact checker not initialized")
    
    try:
        stats = fact_checker.get_statistics()
        return stats
    except Exception as e:
        logger.error(f"Error getting fact check stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


# Helper functions

async def run_simulation(sim_id: str, config: SimulationConfig):
    """Run simulation in background"""
    try:
        logger.info(f"Starting simulation {sim_id}")
        
        # Run simulation
        results = market_simulator.run_simulation(
            duration_seconds=config.duration,
            time_step=config.time_step
        )
        
        # Update simulation status
        if sim_id in active_simulations:
            active_simulations[sim_id]["status"] = "completed"
            active_simulations[sim_id]["results"] = results
        
        # Append to run history
        summary = {
            'simulation_id': sim_id,
            'started_at': active_simulations.get(sim_id, {}).get('start_time'),
            'duration': config.duration,
            'agents': config.agents,
            'results': results,
        }
        run_history.append(summary)

        # Broadcast completion
        await manager.broadcast(json.dumps({
            "type": "simulation_completed",
            "simulation_id": sim_id,
            "results": results
        }))
        
        logger.info(f"Simulation {sim_id} completed")
        
    except asyncio.CancelledError:
        logger.info(f"Simulation {sim_id} cancelled")
    except Exception as e:
        logger.error(f"Simulation {sim_id} error: {e}")
        if sim_id in active_simulations:
            active_simulations[sim_id]["status"] = "error"
            active_simulations[sim_id]["error"] = str(e)


async def execute_agent_action(agent, action: AgentActionRequest):
    """Execute agent action"""
    # This would be implemented based on specific agent types
    # For now, return a placeholder
    return {
        "agent_id": action.agent_id,
        "action_type": action.action_type,
        "status": "executed",
        "timestamp": time.time()
    }


# Background broadcaster
async def broadcast_snapshots_task():
    while True:
        try:
            if market_simulator:
                for sym in market_simulator.order_books.keys():
                    snap = market_simulator.get_market_data(sym)
                    await manager.broadcast(json.dumps({
                        'type': 'snapshot',
                        'symbol': sym,
                        'data': snap,
                    }))

                    # broadcast new trades
                    ob = market_simulator.order_books[sym]
                    since = last_trade_ts.get(sym, 0)
                    trades = []
                    if hasattr(ob, 'get_trades_since'):
                        trades = ob.get_trades_since(since)
                    elif hasattr(ob, 'get_trades'):
                        trades = ob.get_trades()
                        # filter by timestamp > since if available
                        trades = [t for t in trades if getattr(t, 'timestamp', 0) > since]
                    if trades:
                        last_trade_ts[sym] = max(getattr(t, 'timestamp', 0) for t in trades)
                        for t in trades[-50:]:
                            await manager.broadcast(json.dumps({
                                'type': 'trade',
                                'symbol': sym,
                                'trade': {
                                    'buy_order_id': getattr(t, 'buy_order_id', None),
                                    'sell_order_id': getattr(t, 'sell_order_id', None),
                                    'price': getattr(t, 'price', 0.0),
                                    'quantity': getattr(t, 'quantity', 0),
                                    'timestamp': getattr(t, 'timestamp', 0),
                                }
                            }))
        except Exception as e:
            logger.error(f"Broadcaster error: {e}")
        await asyncio.sleep(1.0)


# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
