'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader } from '../../components/ui/card'
import { Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ComposedChart } from 'recharts'

interface TimeSeriesData {
  prices: Array<{ timestamp: number; price: number }>
  trades: Array<{ timestamp: number; price: number; quantity: number; side: string; agent_id: string }>
  spreads: Array<{ timestamp: number; spread: number }>
  agent_profits?: Array<{
    timestamp: number
    agent_id: string
    realized_profit: number
    unrealized_profit: number
    total_profit: number
    capital: number
    position: number
  }>
}

interface SimulationResults {
  experiment: string
  timestamp: number
  duration: number
  results: {
    duration: number
    total_trades: number
    total_volume: number
    time_series?: Record<string, TimeSeriesData>
    market_data: Record<string, any>
    agents: string[]
    agent_trades: Record<string, number>
    final_state: string
  }
}

export default function VisualizationPage() {
  const [data, setData] = useState<SimulationResults | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedSymbol, setSelectedSymbol] = useState<string | null>(null)

  useEffect(() => {
    fetch('/api/results/30min')
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          setError(data.error)
        } else {
          setData(data)
          // Set first symbol as default
          if (data.results?.time_series) {
            const symbols = Object.keys(data.results.time_series)
            if (symbols.length > 0) {
              setSelectedSymbol(symbols[0])
            }
          }
        }
        setLoading(false)
      })
      .catch((err) => {
        setError('Failed to load simulation results')
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-16">
        <div className="text-center text-muted-foreground">Loading visualization data...</div>
      </div>
    )
  }

  if (error || !data || !data.results?.time_series) {
    return (
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <div className="text-destructive mb-4">{error || 'No time-series data found'}</div>
          <div className="text-sm text-muted-foreground">
            {error?.includes('not found') && (
              <p>Please run the 30-minute simulation first:</p>
            )}
            <code className="block mt-2 p-2 bg-muted rounded">python scripts/run_30min_simulation.py</code>
          </div>
        </div>
      </div>
    )
  }

  const symbols = Object.keys(data.results.time_series)
  const timeSeries = selectedSymbol ? data.results.time_series[selectedSymbol] : null

  // Helper function to round to 2 decimal places
  const roundToTwoDecimals = (value: number): number => {
    return Math.round(value * 100) / 100
  }

  // Prepare chart data: create a combined dataset
  // First, create price line data (rounded to 2 decimal places)
  const priceData = timeSeries
    ? timeSeries.prices.map((p) => ({
        timestamp: p.timestamp,
        timeFormatted: formatTime(p.timestamp),
        price: roundToTwoDecimals(p.price),
        buyTrade: null as number | null,
        sellTrade: null as number | null,
      }))
    : []

  // Then, add trades to the nearest price point (rounded to 2 decimal places)
  if (timeSeries) {
    timeSeries.trades.forEach((trade) => {
      // Find the closest price point
      let closestIdx = 0
      let minDiff = Math.abs(priceData[0]?.timestamp - trade.timestamp)
      
      for (let i = 1; i < priceData.length; i++) {
        const diff = Math.abs(priceData[i].timestamp - trade.timestamp)
        if (diff < minDiff) {
          minDiff = diff
          closestIdx = i
        }
      }
      
      // Add trade to the closest price point (rounded to 2 decimal places)
      if (trade.side === 'buy') {
        priceData[closestIdx].buyTrade = roundToTwoDecimals(trade.price)
      } else {
        priceData[closestIdx].sellTrade = roundToTwoDecimals(trade.price)
      }
    })
  }

  const chartData = priceData

  // Calculate Y-axis domain with 0.5 intervals
  const prices = priceData.map((d) => d.price).filter((p) => p !== null && p !== undefined) as number[]
  
  // Default values if no price data
  let yMin = 0
  let yMax = 100
  let yTicks: number[] = []
  
  if (prices.length > 0) {
    const minPrice = Math.min(...prices)
    const maxPrice = Math.max(...prices)
    
    // Round down min and round up max to nearest 0.5, then add padding
    yMin = Math.floor(minPrice * 2) / 2 - 0.5
    yMax = Math.ceil(maxPrice * 2) / 2 + 0.5
    
    // Generate ticks at 0.5 intervals
    for (let tick = yMin; tick <= yMax; tick += 0.5) {
      yTicks.push(roundToTwoDecimals(tick))
    }
  }

  return (
    <div className="container mx-auto px-4 py-16 md:py-24 max-w-7xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Simulation Visualization</h1>
        <p className="text-muted-foreground">
          {data.experiment} • Duration: {data.duration}s • {new Date(data.timestamp * 1000).toLocaleString()}
        </p>
      </div>

      {/* Symbol Selector */}
      {symbols.length > 1 && (
        <div className="mb-6">
          <div className="flex gap-2 flex-wrap">
            {symbols.map((symbol) => (
              <button
                key={symbol}
                onClick={() => setSelectedSymbol(symbol)}
                className={`px-4 py-2 rounded-md border transition-all ${
                  selectedSymbol === symbol
                    ? 'border-primary bg-primary/10 text-primary'
                    : 'border-border bg-card hover:bg-accent/50'
                }`}
              >
                {symbol}
              </button>
            ))}
          </div>
        </div>
      )}

      {timeSeries && (
        <>
          {/* Price Chart with Trades */}
          <Card className="mb-8">
            <CardHeader>
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold">
                  Price & Trades - {selectedSymbol}
                </h2>
                <div className="text-sm text-muted-foreground">
                  {timeSeries.prices.length} price points • {timeSeries.trades.length} trades
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={500}>
                <ComposedChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="oklch(var(--border))" />
                  <XAxis
                    dataKey="timeFormatted"
                    stroke="oklch(var(--muted-foreground))"
                    style={{ fontSize: '12px' }}
                    angle={-45}
                    textAnchor="end"
                    height={80}
                  />
                  <YAxis
                    stroke="oklch(var(--muted-foreground))"
                    style={{ fontSize: '12px' }}
                    label={{ value: 'Price ($)', angle: -90, position: 'insideLeft' }}
                    domain={[yMin, yMax]}
                    ticks={yTicks.length > 0 ? yTicks : undefined}
                    allowDataOverflow={false}
                    tickFormatter={(value) => `$${value.toFixed(2)}`}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'oklch(var(--card))',
                      border: '1px solid oklch(var(--border))',
                      borderRadius: '8px',
                    }}
                    formatter={(value: any, name: string) => {
                      if (value === null) return null
                      if (name === 'price' || name === 'buyTrade' || name === 'sellTrade') {
                        return [`$${Number(value).toFixed(2)}`, name === 'price' ? 'Price' : name === 'buyTrade' ? 'Buy Trade' : 'Sell Trade']
                      }
                      return [value, name]
                    }}
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="price"
                    stroke="#6366F1"
                    strokeWidth={2}
                    dot={false}
                    name="Mid Price"
                  />
                  <Line
                    type="monotone"
                    dataKey="buyTrade"
                    stroke="#10B981"
                    strokeWidth={0}
                    dot={{ fill: '#10B981', r: 5 }}
                    name="Buy Trades"
                    connectNulls={false}
                  />
                  <Line
                    type="monotone"
                    dataKey="sellTrade"
                    stroke="#EF4444"
                    strokeWidth={0}
                    dot={{ fill: '#EF4444', r: 5 }}
                    name="Sell Trades"
                    connectNulls={false}
                  />
                </ComposedChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Trade Statistics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <Card>
              <CardHeader className="pb-2">
                <div className="text-sm text-muted-foreground">Total Trades</div>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-semibold">{timeSeries.trades.length}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <div className="text-sm text-muted-foreground">Buy Trades</div>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-semibold text-success">
                  {timeSeries.trades.filter((t) => t.side === 'buy').length}
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <div className="text-sm text-muted-foreground">Sell Trades</div>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-semibold text-destructive">
                  {timeSeries.trades.filter((t) => t.side === 'sell').length}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Agent Profit Chart */}
          {timeSeries.agent_profits && timeSeries.agent_profits.length > 0 && (
            <Card className="mb-8">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-semibold">Agent Profit & Loss</h2>
                  <div className="text-sm text-muted-foreground">
                    {new Set(timeSeries.agent_profits.map((p) => p.agent_id)).size} agents
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                  <ComposedChart data={prepareProfitChartData(timeSeries.agent_profits)}>
                    <CartesianGrid strokeDasharray="3 3" stroke="oklch(var(--border))" />
                    <XAxis
                      dataKey="timeFormatted"
                      stroke="oklch(var(--muted-foreground))"
                      style={{ fontSize: '12px' }}
                      angle={-45}
                      textAnchor="end"
                      height={80}
                    />
                    <YAxis
                      stroke="oklch(var(--muted-foreground))"
                      style={{ fontSize: '12px' }}
                      label={{ value: 'Profit ($)', angle: -90, position: 'insideLeft' }}
                      tickFormatter={(value) => `$${value.toFixed(2)}`}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'oklch(var(--card))',
                        border: '1px solid oklch(var(--border))',
                        borderRadius: '8px',
                      }}
                      formatter={(value: any, name: string) => {
                        return [`$${Number(value).toFixed(2)}`, name]
                      }}
                    />
                    <Legend />
                    {getAgentProfitLines(timeSeries.agent_profits)}
                  </ComposedChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          )}

          {/* Agent Profit Summary */}
          {timeSeries.agent_profits && timeSeries.agent_profits.length > 0 && (
            <Card>
              <CardHeader>
                <h2 className="text-xl font-semibold">Agent Profit Summary</h2>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {getAgentProfitSummary(timeSeries.agent_profits).map((agent) => (
                    <div key={agent.agent_id} className="border rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="font-semibold">{agent.agent_id}</h3>
                        <div className={`text-lg font-bold ${agent.totalProfit >= 0 ? 'text-success' : 'text-destructive'}`}>
                          ${agent.totalProfit.toFixed(2)}
                        </div>
                      </div>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        <div>
                          <div className="text-muted-foreground">Realized Profit</div>
                          <div className={`font-semibold ${agent.realizedProfit >= 0 ? 'text-success' : 'text-destructive'}`}>
                            ${agent.realizedProfit.toFixed(2)}
                          </div>
                        </div>
                        <div>
                          <div className="text-muted-foreground">Unrealized Profit</div>
                          <div className={`font-semibold ${agent.unrealizedProfit >= 0 ? 'text-success' : 'text-destructive'}`}>
                            ${agent.unrealizedProfit.toFixed(2)}
                          </div>
                        </div>
                        <div>
                          <div className="text-muted-foreground">Capital</div>
                          <div className="font-semibold">${agent.capital.toFixed(2)}</div>
                        </div>
                        <div>
                          <div className="text-muted-foreground">Position</div>
                          <div className="font-semibold">{agent.position}</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </>
      )}
    </div>
  )
}

function prepareProfitChartData(agentProfits: TimeSeriesData['agent_profits']): Array<Record<string, any>> {
  if (!agentProfits || agentProfits.length === 0) return []

  // Group by timestamp
  const timeMap = new Map<number, Record<string, any>>()
  const agentIds = new Set<string>()

  agentProfits.forEach((profit) => {
    agentIds.add(profit.agent_id)
    if (!timeMap.has(profit.timestamp)) {
      timeMap.set(profit.timestamp, { timestamp: profit.timestamp, timeFormatted: formatTime(profit.timestamp) })
    }
    const dataPoint = timeMap.get(profit.timestamp)!
    dataPoint[`${profit.agent_id}_profit`] = profit.total_profit
    dataPoint[`${profit.agent_id}_realized`] = profit.realized_profit
  })

  return Array.from(timeMap.values()).sort((a, b) => a.timestamp - b.timestamp)
}

function getAgentProfitLines(agentProfits: TimeSeriesData['agent_profits']) {
  if (!agentProfits || agentProfits.length === 0) return null

  const agentIds = Array.from(new Set(agentProfits.map((p) => p.agent_id)))
  const colors = ['#6366F1', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4']

  return (
    <>
      {agentIds.map((agentId, index) => (
        <Line
          key={agentId}
          type="monotone"
          dataKey={`${agentId}_profit`}
          stroke={colors[index % colors.length]}
          strokeWidth={2}
          dot={false}
          name={`${agentId} Total Profit`}
          connectNulls={false}
        />
      ))}
    </>
  )
}

function getAgentProfitSummary(agentProfits: TimeSeriesData['agent_profits']) {
  if (!agentProfits || agentProfits.length === 0) return []

  const agentMap = new Map<string, {
    agent_id: string
    realizedProfit: number
    unrealizedProfit: number
    totalProfit: number
    capital: number
    position: number
  }>()

  agentProfits.forEach((profit) => {
    if (!agentMap.has(profit.agent_id)) {
      agentMap.set(profit.agent_id, {
        agent_id: profit.agent_id,
        realizedProfit: 0,
        unrealizedProfit: 0,
        totalProfit: 0,
        capital: 0,
        position: 0,
      })
    }
    const agent = agentMap.get(profit.agent_id)!
    // Use latest values
    agent.realizedProfit = profit.realized_profit
    agent.unrealizedProfit = profit.unrealized_profit
    agent.totalProfit = profit.total_profit
    agent.capital = profit.capital
    agent.position = profit.position
  })

  return Array.from(agentMap.values()).sort((a, b) => b.totalProfit - a.totalProfit)
}

function formatTime(seconds: number): string {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

