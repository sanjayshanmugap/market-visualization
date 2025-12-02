# src/ui/web_interface.py

from typing import Dict, Any, Optional, List
import logging
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class WebInterfaceConfig:
    """
    Configuration for the web interface.
    """
    host: str = "localhost"
    port: int = 8000
    debug: bool = False
    auto_reload: bool = True

class WebInterface:
    """
    Web interface for the agentic market simulator.
    Provides real-time visualization and human-in-the-loop interaction.
    """
    def __init__(self, config: WebInterfaceConfig = None):
        self.config = config or WebInterfaceConfig()
        self.is_running = False
        self.connected_clients: List[str] = []
        logger.info(f"WebInterface initialized with config: {self.config}")

    def start(self) -> bool:
        """
        Starts the web interface server.
        """
        try:
            logger.info(f"Starting web interface on {self.config.host}:{self.config.port}")
            # TODO: Implement actual web server startup (FastAPI/Flask)
            self.is_running = True
            logger.info("Web interface started successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to start web interface: {e}")
            return False

    def stop(self) -> bool:
        """
        Stops the web interface server.
        """
        try:
            logger.info("Stopping web interface...")
            self.is_running = False
            self.connected_clients.clear()
            logger.info("Web interface stopped successfully")
            return True
        except Exception as e:
            logger.error(f"Error stopping web interface: {e}")
            return False

    def broadcast_market_update(self, update: Dict[str, Any]) -> None:
        """
        Broadcasts a market update to all connected clients.
        """
        if not self.is_running:
            logger.warning("Web interface not running, cannot broadcast update")
            return

        logger.debug(f"Broadcasting market update to {len(self.connected_clients)} clients")
        # TODO: Implement actual WebSocket broadcasting
        pass

    def send_agent_update(self, agent_id: str, update: Dict[str, Any]) -> None:
        """
        Sends an update for a specific agent to connected clients.
        """
        if not self.is_running:
            logger.warning("Web interface not running, cannot send agent update")
            return

        logger.debug(f"Sending agent update for {agent_id} to {len(self.connected_clients)} clients")
        # TODO: Implement actual WebSocket agent-specific updates
        pass

    def handle_human_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handles human input from the web interface.
        """
        logger.info(f"Handling human input: {input_data}")
        # TODO: Implement human input processing
        return {"status": "received", "timestamp": datetime.now().isoformat()}

    def get_market_state(self) -> Dict[str, Any]:
        """
        Returns the current market state for display.
        """
        logger.debug("Retrieving market state for web interface")
        # TODO: Implement actual market state retrieval
        return {
            "timestamp": datetime.now().isoformat(),
            "status": "running",
            "agents": [],
            "orders": [],
            "trades": []
        }

    def get_agent_state(self, agent_id: str) -> Dict[str, Any]:
        """
        Returns the current state of a specific agent.
        """
        logger.debug(f"Retrieving state for agent {agent_id}")
        # TODO: Implement actual agent state retrieval
        return {
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat(),
            "status": "active",
            "capital": 0.0,
            "holdings": {}
        }

    def add_client(self, client_id: str) -> None:
        """
        Adds a new client connection.
        """
        if client_id not in self.connected_clients:
            self.connected_clients.append(client_id)
            logger.info(f"Client {client_id} connected. Total clients: {len(self.connected_clients)}")

    def remove_client(self, client_id: str) -> None:
        """
        Removes a client connection.
        """
        if client_id in self.connected_clients:
            self.connected_clients.remove(client_id)
            logger.info(f"Client {client_id} disconnected. Total clients: {len(self.connected_clients)}")

    def is_healthy(self) -> bool:
        """
        Checks if the web interface is healthy.
        """
        return self.is_running and len(self.connected_clients) >= 0
