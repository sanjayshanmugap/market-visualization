"use client"

import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'

interface VizCardProps {
  id: string
  title: string
  description: string
  domain: string
  tool: string
  vizType: string
  thumbnail?: string
  slug?: string
}

export function VizCard({
  id,
  title,
  description,
  domain,
  tool,
  vizType,
  thumbnail,
  slug,
}: VizCardProps) {
  const href = slug ? `/stories/${slug}` : `/viz/${id}`
  
  return (
    <Link href={href}>
      <Card className="glass-card group h-full transition-all duration-300 hover:scale-105 hover:shadow-lg rounded-[32px] border border-slate-200/70 bg-white/80 backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/60 dark:text-white">
        <CardContent className="p-6">
          <CardTitle className="text-lg line-clamp-2 mb-3 text-slate-900 dark:text-white">{title}</CardTitle>
          <p className="text-sm text-slate-600 dark:text-white/70 line-clamp-3">{description}</p>
        </CardContent>
      </Card>
    </Link>
  )
}

