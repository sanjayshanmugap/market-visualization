"use client"

import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card'

export default function BackgroundTestIndex() {
  const backgrounds = [
    { name: 'Aurora', path: '/test/aurora' },
    { name: 'Liquid Ether', path: '/test/liquid-ether' },
    { name: 'Light Rays', path: '/test/light-rays' },
    { name: 'Plasma', path: '/test/plasma' },
    { name: 'Particles', path: '/test/particles' },
    { name: 'Galaxy', path: '/test/galaxy' },
    { name: 'Dot Grid', path: '/test/dot-grid' },
    { name: 'Threads', path: '/test/threads' },
    { name: 'Orb', path: '/test/orb' },
  ]

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="container mx-auto">
        <h1 className="text-4xl font-bold mb-8">Background Test Pages</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {backgrounds.map((bg) => (
            <Link key={bg.path} href={bg.path}>
              <Card className="hover-lift click-scale">
                <CardHeader>
                  <CardTitle>{bg.name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">Click to view</p>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}

