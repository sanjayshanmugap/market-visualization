"use client"

import { useEffect, useState } from 'react'
import { Card, CardContent } from '../ui/card'
import dynamic from 'next/dynamic'

// Dynamically import Leaflet to avoid SSR issues
const MapContainer = dynamic(() => import('react-leaflet').then((mod) => mod.MapContainer), { ssr: false })
const TileLayer = dynamic(() => import('react-leaflet').then((mod) => mod.TileLayer), { ssr: false })
const Marker = dynamic(() => import('react-leaflet').then((mod) => mod.Marker), { ssr: false })
const Popup = dynamic(() => import('react-leaflet').then((mod) => mod.Popup), { ssr: false })

interface MapVizProps {
  vizId: string
  data?: Array<{ lat: number; lon: number; label?: string }>
  className?: string
}

export function MapViz({ vizId, data, className }: MapVizProps) {
  const [mapData, setMapData] = useState(data)
  const [loading, setLoading] = useState(!data)

  useEffect(() => {
    if (!data) {
      fetch(`/api/viz/${vizId}/data`)
        .then((res) => res.json())
        .then((jsonData) => {
          setMapData(jsonData.points || jsonData)
          setLoading(false)
        })
        .catch(() => setLoading(false))
    }
  }, [vizId, data])

  if (loading) {
    return (
      <Card className={className}>
        <CardContent className="flex items-center justify-center h-64">
          <div className="text-muted-foreground">Loading map...</div>
        </CardContent>
      </Card>
    )
  }

  if (!mapData || mapData.length === 0) {
    return (
      <Card className={className}>
        <CardContent className="flex items-center justify-center h-64">
          <div className="text-muted-foreground">No map data available</div>
        </CardContent>
      </Card>
    )
  }

  // Calculate center
  const centerLat = mapData.reduce((sum, p) => sum + p.lat, 0) / mapData.length
  const centerLon = mapData.reduce((sum, p) => sum + p.lon, 0) / mapData.length

  return (
    <Card className={className}>
      <CardContent className="p-0">
        <div style={{ height: '600px', width: '100%' }}>
          <MapContainer
            center={[centerLat, centerLon]}
            zoom={5}
            style={{ height: '100%', width: '100%' }}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {mapData.map((point, idx) => (
              <Marker key={idx} position={[point.lat, point.lon]}>
                {point.label && <Popup>{point.label}</Popup>}
              </Marker>
            ))}
          </MapContainer>
        </div>
      </CardContent>
    </Card>
  )
}

