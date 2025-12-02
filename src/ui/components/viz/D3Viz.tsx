"use client"

import { useEffect, useRef, useState } from 'react'
import * as d3 from 'd3'
import { Card, CardContent } from '../ui/card'

interface D3VizProps {
  vizId: string
  type: 'line' | 'bar' | 'scatter' | 'network'
  data?: any
  className?: string
}

export function D3Viz({ vizId, type, data, className }: D3VizProps) {
  const svgRef = useRef<SVGSVGElement>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!svgRef.current || !data) return

    // Clear previous content
    d3.select(svgRef.current).selectAll('*').remove()

    const svg = d3.select(svgRef.current)
    const width = 800
    const height = 600
    const margin = { top: 20, right: 20, bottom: 40, left: 40 }

    svg.attr('width', width).attr('height', height)

    const g = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`)

    const chartWidth = width - margin.left - margin.right
    const chartHeight = height - margin.top - margin.bottom

    // Example: Simple line chart
    if (type === 'line' && data.points) {
      const xExtent = d3.extent(data.points, (d: any) => d.x)
      const yExtent = d3.extent(data.points, (d: any) => d.y)
      
      const xScale = d3
        .scaleLinear()
        .domain(xExtent[0] !== undefined && xExtent[1] !== undefined ? [xExtent[0], xExtent[1]] : [0, 1])
        .range([0, chartWidth])

      const yScale = d3
        .scaleLinear()
        .domain(yExtent[0] !== undefined && yExtent[1] !== undefined ? [yExtent[0], yExtent[1]] : [0, 1])
        .range([chartHeight, 0])

      const line = d3
        .line<any>()
        .x((d) => xScale(d.x))
        .y((d) => yScale(d.y))
        .curve(d3.curveMonotoneX)

      g.append('path')
        .datum(data.points)
        .attr('fill', 'none')
        .attr('stroke', 'steelblue')
        .attr('stroke-width', 2)
        .attr('d', line)

      // Add axes
      g.append('g')
        .attr('transform', `translate(0,${chartHeight})`)
        .call(d3.axisBottom(xScale))

      g.append('g').call(d3.axisLeft(yScale))
    }

    setLoading(false)
  }, [data, type])

  if (loading && !data) {
    return (
      <Card className={className}>
        <CardContent className="flex items-center justify-center h-64">
          <div className="text-muted-foreground">Loading D3 visualization...</div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className={className}>
      <CardContent className="p-4">
        <svg ref={svgRef} className="w-full" />
      </CardContent>
    </Card>
  )
}

