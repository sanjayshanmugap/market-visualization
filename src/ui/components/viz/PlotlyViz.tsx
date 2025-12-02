"use client"

import { useEffect, useState } from 'react'
import dynamic from 'next/dynamic'
import { Card, CardContent } from '../ui/card'

// Dynamically import Plotly to avoid SSR issues
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false })

interface PlotlyVizProps {
  vizId: string
  className?: string
}

export function PlotlyViz({ vizId, className }: PlotlyVizProps) {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch(`/api/viz/${vizId}/plotly`)
      .then((res) => {
        if (!res.ok) throw new Error('Failed to load visualization')
        return res.json()
      })
      .then((plotlyData) => {
        setData(plotlyData)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [vizId])

  if (loading) {
    return (
      <Card className={className}>
        <CardContent className="flex items-center justify-center h-64">
          <div className="text-muted-foreground">Loading interactive chart...</div>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Card className={className}>
        <CardContent className="flex items-center justify-center h-64">
          <div className="text-destructive">Error: {error}</div>
        </CardContent>
      </Card>
    )
  }

  if (!data) {
    return (
      <Card className={className}>
        <CardContent className="flex items-center justify-center h-64">
          <div className="text-muted-foreground">No data available</div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className={className}>
      <CardContent className="p-4">
        <Plot
          data={data.data || []}
          layout={data.layout || {}}
          config={{
            displayModeBar: true,
            displaylogo: false,
            responsive: true,
          }}
          style={{ width: '100%', height: '600px' }}
        />
      </CardContent>
    </Card>
  )
}

