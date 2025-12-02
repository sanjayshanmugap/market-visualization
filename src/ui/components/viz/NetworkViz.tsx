"use client"

import { useEffect, useState } from 'react'
import { PlotlyViz } from './PlotlyViz'
import { Card, CardContent } from '../ui/card'

interface NetworkVizProps {
  vizId: string
  className?: string
}

export function NetworkViz({ vizId, className }: NetworkVizProps) {
  // For now, network visualizations can use Plotly
  // In the future, could use specialized network libraries like vis.js or cytoscape.js
  return <PlotlyViz vizId={vizId} className={className} />
}

