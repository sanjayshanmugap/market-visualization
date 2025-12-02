"use client"

import { useEffect, useState } from 'react'
import { VizCard } from '../../components/viz/VizCard'

interface Visualization {
  id: string
  title: string
  description: string
  domain: string
  tool: string
  type: string
  thumbnail?: string
  slug?: string
}

export default function GalleryPage() {
  const [visualizations, setVisualizations] = useState<Visualization[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/viz/list')
      .then((res) => res.json())
      .then((data) => {
        setVisualizations(data)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Error fetching visualizations:', err)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-16">
        <div className="glass-card rounded-[32px] border border-slate-200/70 bg-white/80 p-12 text-center backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/60 dark:text-white">
          <div className="text-slate-600 dark:text-white/70">Loading gallery...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="relative z-10">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="mb-8">
          <div className="glass-hero rounded-[32px] border border-slate-200/70 bg-white/80 p-8 text-slate-900 backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/60 dark:text-white">
            <h1 className="text-4xl font-bold mb-2 text-slate-900 dark:text-white">Visualization Gallery</h1>
            <p className="text-lg text-slate-600 dark:text-white/70">
              Explore {visualizations.length} visualizations from the house prices analysis
            </p>
          </div>
        </div>

        {visualizations.length === 0 ? (
          <div className="glass-card rounded-[32px] border border-slate-200/70 bg-white/80 p-12 text-center backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/60 dark:text-white">
            <p className="text-slate-600 dark:text-white/70">No visualizations available.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {visualizations.map((viz) => (
              <VizCard
                key={viz.id}
                id={viz.id}
                title={viz.title}
                description={viz.description}
                domain={viz.domain}
                tool={viz.tool}
                vizType={viz.type}
                thumbnail={viz.thumbnail}
                slug={viz.slug}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

