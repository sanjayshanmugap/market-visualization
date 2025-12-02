"use client"

import Image from 'next/image'
import { useState } from 'react'

interface StaticVizProps {
  src: string
  alt: string
  width?: number
  height?: number
  className?: string
}

export function StaticViz({ src, alt, width = 1200, height = 800, className }: StaticVizProps) {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  return (
    <div className={`relative ${className}`}>
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center bg-muted animate-pulse">
          <div className="text-muted-foreground">Loading visualization...</div>
        </div>
      )}
      {error ? (
        <div className="flex items-center justify-center h-64 bg-muted rounded-lg">
          <div className="text-destructive">Failed to load image</div>
        </div>
      ) : (
        <Image
          src={src}
          alt={alt}
          width={width}
          height={height}
          className="w-full h-auto rounded-lg"
          onLoad={() => setLoading(false)}
          onError={() => {
            setLoading(false)
            setError(true)
          }}
        />
      )}
    </div>
  )
}

