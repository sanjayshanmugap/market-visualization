'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader } from '../../components/ui/card'
import { Badge } from '../../components/ui/badge'

interface SimulationResults {
  experiment: string
  timestamp: number
  duration: number
  results: {
    duration: number
    total_trades: number
    total_volume: number
    market_data: Record<string, {
      symbol: string
      best_bid: number
      best_ask: number
      spread: number
      mid_price: number
      last_trade_price: number
      stats: {
        vwap: number
        volatility: number
        total_volume: number
        spread: number
        mid_price: number
      }
    }>
    agents: string[]
    agent_trades: Record<string, number>
    final_state: string
  }
  validation: {
    success: boolean
    criteria_met: {
      agents_trading: boolean
      fact_check: boolean
    }
    issues: string[]
  }
  fact_check_stats: {
    total_claims: number
    verified_claims: number
    contradicted_claims: number
    verification_rate: number
    hallucination_rate: number
    cache_size: number
  }
  success: boolean
}

export default function ResultsPage() {
  const [data, setData] = useState<SimulationResults | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('/api/results')
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          setError(data.error)
        } else {
          setData(data)
        }
        setLoading(false)
      })
      .catch((err) => {
        setError('Failed to load results')
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-16">
        <div className="text-center text-muted-foreground">Loading simulation results...</div>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="container mx-auto px-4 py-16">
        <div className="text-center text-destructive">{error || 'No results found'}</div>
      </div>
    )
  }

  const { results, validation, fact_check_stats, experiment, duration } = data
  const symbols = Object.keys(results.market_data)

  return (
    <div className="container mx-auto px-4 py-16 md:py-24 max-w-6xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">{experiment}</h1>
        <p className="text-muted-foreground">
          Duration: {duration}s • {new Date(data.timestamp * 1000).toLocaleString()}
        </p>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <Card>
          <CardHeader className="pb-2">
            <div className="text-sm text-muted-foreground">Total Trades</div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-semibold">{results.total_trades}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <div className="text-sm text-muted-foreground">Total Volume</div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-semibold">{results.total_volume}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <div className="text-sm text-muted-foreground">Final State</div>
          </CardHeader>
          <CardContent>
            <Badge className={results.final_state === 'open' ? 'bg-success' : ''}>
              {results.final_state}
            </Badge>
          </CardContent>
        </Card>
      </div>

      {/* Market Data */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Market Data</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {symbols.map((symbol) => {
            const market = results.market_data[symbol]
            return (
              <Card key={symbol}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="text-lg font-semibold">{symbol}</div>
                    <Badge>Active</Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <div className="text-muted-foreground">Best Bid</div>
                      <div className="font-medium">${market.best_bid.toFixed(2)}</div>
                    </div>
                    <div>
                      <div className="text-muted-foreground">Best Ask</div>
                      <div className="font-medium">${market.best_ask.toFixed(2)}</div>
                    </div>
                    <div>
                      <div className="text-muted-foreground">Mid Price</div>
                      <div className="font-medium">${market.mid_price.toFixed(2)}</div>
                    </div>
                    <div>
                      <div className="text-muted-foreground">Spread</div>
                      <div className="font-medium">${Math.abs(market.spread).toFixed(4)}</div>
                    </div>
                    <div>
                      <div className="text-muted-foreground">VWAP</div>
                      <div className="font-medium">${market.stats.vwap.toFixed(2)}</div>
                    </div>
                    <div>
                      <div className="text-muted-foreground">Volatility</div>
                      <div className="font-medium">{(market.stats.volatility * 100).toFixed(4)}%</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>
      </div>

      {/* Agent Performance */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Agent Performance</h2>
        <Card>
          <CardContent className="pt-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {results.agents.map((agentId) => {
                const trades = results.agent_trades[agentId] || 0
                return (
                  <div key={agentId} className="flex items-center justify-between p-3 rounded-lg border border-border">
                    <div>
                      <div className="font-medium text-sm">{agentId}</div>
                      <div className="text-xs text-muted-foreground">Trades</div>
                    </div>
                    <div className="text-lg font-semibold">{trades}</div>
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Fact Check Stats */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Fact Check Statistics</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="pb-2">
              <div className="text-sm text-muted-foreground">Total Claims</div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-semibold">{fact_check_stats.total_claims}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <div className="text-sm text-muted-foreground">Verified</div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-semibold text-success">{fact_check_stats.verified_claims}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <div className="text-sm text-muted-foreground">Verification Rate</div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-semibold">{(fact_check_stats.verification_rate * 100).toFixed(1)}%</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <div className="text-sm text-muted-foreground">Hallucination Rate</div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-semibold">{(fact_check_stats.hallucination_rate * 100).toFixed(2)}%</div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Validation Status */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Validation</h2>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between mb-4">
              <div className="font-medium">Status</div>
              <Badge className={validation.success ? 'bg-success' : 'bg-destructive'}>
                {validation.success ? 'Success' : 'Failed'}
              </Badge>
            </div>
            <div className="space-y-2 text-sm">
              <div className="flex items-center justify-between">
                <span className="text-muted-foreground">Agents Trading</span>
                <Badge className={validation.criteria_met.agents_trading ? 'bg-success' : 'bg-muted'}>
                  {validation.criteria_met.agents_trading ? 'Met' : 'Not Met'}
                </Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-muted-foreground">Fact Check</span>
                <Badge className={validation.criteria_met.fact_check ? 'bg-success' : 'bg-muted'}>
                  {validation.criteria_met.fact_check ? 'Passed' : 'Failed'}
                </Badge>
              </div>
              {validation.issues.length > 0 && (
                <div className="mt-4 pt-4 border-t border-border">
                  <div className="text-muted-foreground mb-2">Issues:</div>
                  <ul className="list-disc list-inside space-y-1">
                    {validation.issues.map((issue, i) => (
                      <li key={i} className="text-sm">{issue}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

