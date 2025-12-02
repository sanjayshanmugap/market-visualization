"use client"

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import { StaticViz } from '../../../components/viz/StaticViz'
import { PlotlyViz } from '../../../components/viz/PlotlyViz'
import { MapViz } from '../../../components/viz/MapViz'
import { NetworkViz } from '../../../components/viz/NetworkViz'
import { ThreeViz } from '../../../components/viz/ThreeViz'
import { Card, CardContent, CardHeader, CardTitle } from '../../../components/ui/card'

interface Visualization {
  id: string
  title: string
  description: string
  domain: string
  tool: string
  type: string
}

export default function VizPage() {
  const params = useParams()
  const id = params?.id as string
  const [viz, setViz] = useState<Visualization | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!id) return

    // Fetch from visualization list
    fetch('/api/viz/list')
      .then((res) => res.json())
      .then((vizList) => {
        const found = vizList.find((v: Visualization) => v.id === id)
        setViz(found || null)
        setLoading(false)
      })
      .catch(() => {
        setLoading(false)
      })
  }, [id])

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-16">
        <div className="text-center text-muted-foreground">Loading visualization...</div>
      </div>
    )
  }

  if (!viz) {
    return (
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Visualization not found</h1>
          <p className="text-muted-foreground">The visualization you're looking for doesn't exist.</p>
        </div>
      </div>
    )
  }

  const renderViz = () => {
    switch (viz.type) {
      case 'static':
        return (
          <StaticViz
            src={`/api/viz/${viz.id}/static?format=png`}
            alt={viz.title}
            className="w-full"
          />
        )
      case 'plotly':
        return <PlotlyViz vizId={viz.id} className="w-full" />
      case 'map':
        return <MapViz vizId={viz.id} className="w-full" />
      case 'network':
        return <NetworkViz vizId={viz.id} className="w-full" />
      case '3d':
        return <ThreeViz vizId={viz.id} className="w-full" />
      default:
        return <div>Unsupported visualization type</div>
    }
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-4">{viz.title}</h1>
        <p className="text-lg text-muted-foreground">{viz.description}</p>
      </div>

      <Card className="w-full">
        <CardHeader>
          <CardTitle>Visualization</CardTitle>
        </CardHeader>
        <CardContent>{renderViz()}</CardContent>
      </Card>
    </div>
  )
}

