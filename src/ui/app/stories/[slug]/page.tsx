"use client"

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import { StaticViz } from '../../../components/viz/StaticViz'
import { PlotlyViz } from '../../../components/viz/PlotlyViz'
import { MapViz } from '../../../components/viz/MapViz'
import { NetworkViz } from '../../../components/viz/NetworkViz'
import { ThreeViz } from '../../../components/viz/ThreeViz'
import { Card, CardContent, CardHeader, CardTitle } from '../../../components/ui/card'
import { Badge } from '../../../components/ui/badge'

interface Story {
  id: string
  title: string
  description: string
  domain: string
  narrative: string
  visualizations: Array<{
    id: string
    title: string
    type: 'static' | 'plotly' | 'map' | 'network' | '3d'
    description?: string
  }>
}

export default function StoryPage() {
  const params = useParams()
  const slug = params?.slug as string
  const [story, setStory] = useState<Story | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!slug) return

    fetch(`/api/viz/stories/${slug}`)
      .then((res) => {
        if (!res.ok) throw new Error('Story not found')
        return res.json()
      })
      .then((data) => {
        setStory(data)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Error loading story:', err)
        setLoading(false)
      })
  }, [slug])

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-16">
        <div className="glass-card rounded-[32px] border border-slate-200/70 bg-white/80 p-12 text-center backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/60 dark:text-white">
          <div className="text-slate-600 dark:text-white/70">Loading story...</div>
        </div>
      </div>
    )
  }

  if (!story) {
    return (
      <div className="container mx-auto px-4 py-16">
        <div className="glass-card rounded-[32px] border border-slate-200/70 bg-white/80 p-12 text-center backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/60 dark:text-white">
          <h1 className="text-2xl font-bold mb-4 text-slate-900 dark:text-white">Story not found</h1>
          <p className="text-slate-600 dark:text-white/70">The story you're looking for doesn't exist.</p>
        </div>
      </div>
    )
  }

  const renderViz = (viz: Story['visualizations'][0]) => {
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
    <div className="relative z-10">
      <div className="container mx-auto px-4 py-8 max-w-5xl">
        <div className="mb-8">
          <div className="glass-hero rounded-[32px] border border-slate-200/70 bg-white/80 p-8 text-slate-900 backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/60 dark:text-white">
            <h1 className="text-4xl font-bold mb-4 text-slate-900 dark:text-white">{story.title}</h1>
            <p className="text-lg text-slate-600 dark:text-white/70 mb-6">{story.description}</p>
          </div>
        </div>

        <div className="glass-card rounded-[32px] border border-slate-200/70 bg-white/80 p-8 text-slate-900 backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/60 dark:text-white mb-8">
          <div className="prose prose-slate dark:prose-invert max-w-none">
            <div className="whitespace-pre-line text-slate-700 dark:text-white/80">{story.narrative}</div>
          </div>
        </div>

        <div className="space-y-8">
          {story.visualizations.map((viz) => (
            <Card key={viz.id} className="glass-card w-full rounded-[32px] border border-slate-200/70 bg-white/80 backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/60 dark:text-white">
              <CardHeader>
                <CardTitle className="text-slate-900 dark:text-white">{viz.title}</CardTitle>
                {viz.description && <p className="text-sm text-slate-600 dark:text-white/70 mt-2">{viz.description}</p>}
              </CardHeader>
              <CardContent>{renderViz(viz)}</CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}

