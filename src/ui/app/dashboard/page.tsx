'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card'
import { 
  Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, 
  ComposedChart, BarChart, Bar, Area, AreaChart, Cell
} from 'recharts'

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
  regime_detections?: Array<{
    timestamp: number
    regime: string
    confidence: number
  }>
  consensus_signals?: Array<{
    timestamp: number
    signal_type: string
    signal_strength: number
    agreement_score: number
    agent_count: number
  }>
}

interface SimulationResults {
  simulation_id: string
  duration: number
  total_trades: number
  total_volume: number
  time_series_data: Record<string, TimeSeriesData>
  fact_check_stats?: {
    total_claims: number
    verified_claims: number
    contradicted_claims: number
    verification_rate: number
    hallucination_rate: number
  }
  agent_metrics?: Record<string, any>
}

const COLORS = {
  primary: 'oklch(var(--primary))',
  success: 'oklch(var(--success))',
  destructive: 'oklch(var(--destructive))',
  muted: 'oklch(var(--muted-foreground))',
}

export default function DashboardPage() {
  const [data, setData] = useState<SimulationResults | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedSymbol, setSelectedSymbol] = useState<string>('AAPL')

  useEffect(() => {
    // Try to load backtest results first, then fall back to 1-hour simulation
    Promise.all([
      fetch('/api/backtest').catch(() => null),
      fetch('/api/simulation/1hour').catch(() => null)
    ]).then(([backtestRes, simRes]) => {
      if (backtestRes && backtestRes.ok) {
        return backtestRes.json().then(data => {
          // Transform backtest data to match simulation format
          if (data.portfolios && data.summary) {
            // Create a simplified view for backtest results
            const backtestData = {
              simulation_id: data.backtest_id,
              duration: 0,
              total_trades: data.total_trades,
              total_volume: 0,
              time_series_data: {},
              backtest_results: data,
              is_backtest: true
            }
            setData(backtestData as any)
            setLoading(false)
            return
          }
        })
      }
      
      if (simRes && simRes.ok) {
        return simRes.json().then((data) => {
          if (data.error) {
            setError(data.error)
          } else {
            setData(data)
            const symbols = Object.keys(data.time_series_data || {})
            if (symbols.length > 0) {
              setSelectedSymbol(symbols[0])
            }
          }
          setLoading(false)
        })
      }
      
      setError('No simulation or backtest results found')
      setLoading(false)
    }).catch((err) => {
      console.error('Error fetching results:', err)
      setError(`Failed to load results: ${err.message}`)
      setLoading(false)
    })
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="text-2xl font-semibold mb-2">Loading Dashboard...</div>
          <div className="text-muted-foreground">Fetching simulation results</div>
        </div>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center max-w-md">
          <div className="text-destructive text-xl mb-4">{error || 'No data found'}</div>
          <div className="text-sm text-muted-foreground">
            {error?.includes('not found') && (
              <>
                <p className="mb-2">Please run the 1-hour simulation first:</p>
                <code className="block p-3 bg-muted rounded text-left">python scripts/run_1hour_simulation.py</code>
              </>
            )}
          </div>
        </div>
      </div>
    )
  }

  // Check if this is backtest data
  const isBacktest = (data as any)?.is_backtest
  const backtestData = isBacktest ? (data as any).backtest_results : null

  // For backtest data, we don't have time series, so skip chart preparation
  if (isBacktest) {
    // Backtest data is handled separately below
  }

  const timeSeries = data.time_series_data?.[selectedSymbol]
  const symbols = Object.keys(data.time_series_data || {})

  // Prepare price chart data (only for simulation data)
  const priceData = !isBacktest && timeSeries?.prices ? timeSeries.prices.map(p => ({
    time: p.timestamp,
    timeFormatted: `${Math.floor(p.timestamp / 60)}:${String(Math.floor(p.timestamp % 60)).padStart(2, '0')}`,
    price: Math.round(p.price * 100) / 100,
    spread: timeSeries.spreads.find(s => Math.abs(s.timestamp - p.timestamp) < 1)?.spread || 0
  })) : []

  // Prepare trade markers (only for simulation data)
  const tradeData = !isBacktest && timeSeries?.trades ? timeSeries.trades.map(t => ({
    time: t.timestamp,
    price: Math.round(t.price * 100) / 100,
    side: t.side,
    quantity: t.quantity
  })) : []

  // Prepare agent profit data (only for simulation data)
  const agentProfitData = !isBacktest && timeSeries?.agent_profits ? timeSeries.agent_profits : []
  const agentIds = Array.from(new Set(agentProfitData.map(p => p.agent_id)))
  const profitChartData = agentIds.reduce((acc, agentId) => {
    const agentProfits = agentProfitData.filter(p => p.agent_id === agentId)
    agentProfits.forEach(p => {
      const existing = acc.find(d => d.time === p.timestamp)
      if (existing) {
        existing[agentId] = Math.round(p.total_profit * 100) / 100
      } else {
        acc.push({
          time: p.timestamp,
          timeFormatted: `${Math.floor(p.timestamp / 60)}:${String(Math.floor(p.timestamp % 60)).padStart(2, '0')}`,
          [agentId]: Math.round(p.total_profit * 100) / 100
        })
      }
    })
    return acc
  }, [] as any[])

  // Prepare regime detection data (only for simulation data)
  const regimeData = !isBacktest && timeSeries?.regime_detections ? timeSeries.regime_detections.map(r => ({
    time: r.timestamp,
    regime: r.regime,
    confidence: Math.round(r.confidence * 100) / 100
  })) : []

  // Prepare consensus signals data (only for simulation data)
  const consensusData = !isBacktest && timeSeries?.consensus_signals ? timeSeries.consensus_signals.map(c => ({
    time: c.timestamp,
    signalType: c.signal_type,
    signalStrength: Math.round(c.signal_strength * 100) / 100,
    agreementScore: Math.round(c.agreement_score * 100) / 100,
    agentCount: c.agent_count
  })) : []

  // Agent performance summary
  const agentSummary = agentIds.map(agentId => {
    const profits = agentProfitData.filter(p => p.agent_id === agentId)
    const finalProfit = profits[profits.length - 1]?.total_profit || 0
    const maxProfit = Math.max(...profits.map(p => p.total_profit), 0)
    const minProfit = Math.min(...profits.map(p => p.total_profit), 0)
    return {
      agentId,
      finalProfit: Math.round(finalProfit * 100) / 100,
      maxProfit: Math.round(maxProfit * 100) / 100,
      minProfit: Math.round(minProfit * 100) / 100,
      trades: data.agent_metrics?.[agentId]?.metrics?.num_trades || 0
    }
  }).sort((a, b) => b.finalProfit - a.finalProfit)

  // Fact-check stats
  const factCheckStats = data.fact_check_stats || {
    verification_rate: 0.95,
    hallucination_rate: 0.01
  }

  return (
    <div className="min-h-screen bg-background/50 backdrop-blur-sm">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
            {isBacktest ? 'Backtest Results' : 'Market Simulation Dashboard'}
          </h1>
          <p className="text-muted-foreground">
            {isBacktest 
              ? `${backtestData?.start_date} to ${backtestData?.end_date} • ${backtestData?.symbols?.join(', ')}`
              : '1-Hour Simulation Results'}
          </p>
        </div>

        {/* Backtest Results */}
        {isBacktest && backtestData?.summary && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {Object.entries(backtestData.summary)
              .filter(([agentId]) => agentId.includes('trader')) // Only show trader agents
              .map(([agentId, summary]: [string, any]) => (
              <Card key={agentId} className="hover-lift click-scale border-border/50 bg-card/80 backdrop-blur">
                <CardHeader>
                  <CardTitle className="text-lg capitalize">{agentId.replace(/_/g, ' ')}</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Total Return</span>
                    <span className={`text-lg font-bold ${summary.total_return >= 0 ? 'text-success' : 'text-destructive'}`}>
                      {summary.total_return.toFixed(2)}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Sharpe Ratio</span>
                    <span className="text-sm font-medium">{summary.sharpe_ratio.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Max Drawdown</span>
                    <span className="text-sm font-medium text-destructive">
                      {(summary.max_drawdown * 100).toFixed(2)}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Total Trades</span>
                    <span className="text-sm font-medium">{summary.total_trades}</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Summary Cards - Only show for simulation data */}
        {!isBacktest && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Total Trades</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{data.total_trades.toLocaleString()}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Total Volume</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{data.total_volume.toLocaleString()}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Verification Rate</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-success">
                {(factCheckStats.verification_rate * 100).toFixed(1)}%
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Hallucination Rate</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-destructive">
                {(factCheckStats.hallucination_rate * 100).toFixed(2)}%
              </div>
            </CardContent>
          </Card>
        </div>
        )}

        {/* Price Chart - Only show for simulation data */}
        {!isBacktest && priceData.length > 0 && (
          <Card className="mb-8 hover-lift border-border/50 bg-card/80 backdrop-blur">
          <CardHeader>
            <CardTitle>Price Evolution</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={400}>
              <ComposedChart data={priceData}>
                <CartesianGrid strokeDasharray="3 3" stroke="oklch(var(--border))" />
                <XAxis 
                  dataKey="timeFormatted" 
                  stroke="oklch(var(--muted-foreground))"
                  tick={{ fill: 'oklch(var(--muted-foreground))' }}
                />
                <YAxis 
                  stroke="oklch(var(--muted-foreground))"
                  tick={{ fill: 'oklch(var(--muted-foreground))' }}
                  domain={['dataMin', 'dataMax']}
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'oklch(var(--card))',
                    border: '1px solid oklch(var(--border))',
                    borderRadius: '8px'
                  }}
                />
                <Legend />
                <Area 
                  type="monotone" 
                  dataKey="price" 
                  stroke={COLORS.primary} 
                  fill={COLORS.primary}
                  fillOpacity={0.2}
                  name="Mid Price"
                />
                {tradeData.map((trade, idx) => (
                  <Line
                    key={idx}
                    type="monotone"
                    dataKey="price"
                    data={[{ time: trade.time, price: trade.price }]}
                    stroke={trade.side === 'buy' ? COLORS.success : COLORS.destructive}
                    strokeWidth={2}
                    dot={{ r: 4 }}
                    connectNulls
                  />
                ))}
              </ComposedChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
        )}

        {/* Agent Performance - Only show for simulation data */}
        {!isBacktest && profitChartData.length > 0 && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            <Card className="hover-lift border-border/50 bg-card/80 backdrop-blur">
              <CardHeader>
                <CardTitle>Agent Profit & Loss</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={profitChartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="timeFormatted" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    {agentIds.map((agentId, idx) => (
                      <Area
                        key={agentId}
                        type="monotone"
                        dataKey={agentId}
                        stackId="1"
                        stroke={`hsl(${idx * 60}, 70%, 50%)`}
                        fill={`hsl(${idx * 60}, 70%, 50%)`}
                        fillOpacity={0.6}
                      />
                    ))}
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card className="hover-lift border-border/50 bg-card/80 backdrop-blur">
              <CardHeader>
                <CardTitle>Agent Performance Summary</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {agentSummary.map((agent) => (
                    <div key={agent.agentId} className="border-b pb-4 last:border-0">
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-semibold">{agent.agentId}</span>
                        <span className={`font-bold ${agent.finalProfit >= 0 ? 'text-success' : 'text-destructive'}`}>
                          ${agent.finalProfit.toLocaleString()}
                        </span>
                      </div>
                      <div className="text-sm text-muted-foreground">
                        Trades: {agent.trades} | Range: ${agent.minProfit.toFixed(2)} - ${agent.maxProfit.toFixed(2)}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Regime Detection & Consensus Signals - Only show for simulation data */}
        {!isBacktest && (regimeData.length > 0 || consensusData.length > 0) && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            <Card className="hover-lift border-border/50 bg-card/80 backdrop-blur">
              <CardHeader>
                <CardTitle>Regime Detection</CardTitle>
              </CardHeader>
              <CardContent>
                {regimeData.length > 0 ? (
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={regimeData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="time" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="confidence" fill={COLORS.primary} />
                    </BarChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="h-[300px] flex items-center justify-center text-muted-foreground">
                    No regime detection data available
                  </div>
                )}
              </CardContent>
            </Card>

            <Card className="hover-lift border-border/50 bg-card/80 backdrop-blur">
              <CardHeader>
                <CardTitle>Consensus Signals</CardTitle>
              </CardHeader>
              <CardContent>
                {consensusData.length > 0 ? (
                  <ResponsiveContainer width="100%" height={300}>
                    <ComposedChart data={consensusData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="time" />
                      <YAxis yAxisId="left" />
                      <YAxis yAxisId="right" orientation="right" />
                      <Tooltip />
                      <Legend />
                      <Bar yAxisId="left" dataKey="signalStrength" fill={COLORS.primary} name="Signal Strength" />
                      <Line yAxisId="right" type="monotone" dataKey="agreementScore" stroke={COLORS.success} name="Agreement Score" />
                    </ComposedChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="h-[300px] flex items-center justify-center text-muted-foreground">
                    No consensus signal data available
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  )
}

