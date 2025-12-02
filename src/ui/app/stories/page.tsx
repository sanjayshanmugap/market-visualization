"use client"

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card'

interface Story {
  id: string
  title: string
  description: string
  domain: string
  slug: string
}

export default function StoriesPage() {
  const [stories, setStories] = useState<Story[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/viz/stories')
      .then((res) => res.json())
      .then((data) => {
        setStories(data)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Error fetching stories:', err)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-16">
        <div className="glass-card rounded-[32px] border border-slate-200/70 bg-white/80 p-12 text-center backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/60 dark:text-white">
          <div className="text-slate-600 dark:text-white/70">Loading stories...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="relative z-10">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <div className="mb-8">
          <div className="glass-hero rounded-[32px] border border-slate-200/70 bg-white/80 p-8 text-slate-900 backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/60 dark:text-white">
            <h1 className="text-4xl font-bold mb-2 text-slate-900 dark:text-white">Data Stories</h1>
            <p className="text-lg text-slate-600 dark:text-white/70">
              Explore data-driven narratives across multiple domains
            </p>
          </div>
        </div>

        {stories.length === 0 ? (
          <div className="glass-card rounded-[32px] border border-slate-200/70 bg-white/80 p-12 text-center backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/60 dark:text-white">
            <p className="text-slate-600 dark:text-white/70">No stories available yet.</p>
            <p className="text-sm text-slate-600 dark:text-white/60 mt-2">
              Run the story generation script to create stories.
            </p>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {stories.map((story) => (
              <Link key={story.id} href={`/stories/${story.slug}`}>
                <Card className="glass-card h-full transition-all duration-300 hover:scale-105 hover:shadow-lg rounded-[32px] border border-slate-200/70 bg-white/80 backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/60 dark:text-white">
                  <CardHeader>
                    <CardTitle className="text-xl text-slate-900 dark:text-white">{story.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-slate-600 dark:text-white/70 line-clamp-3">{story.description}</p>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

