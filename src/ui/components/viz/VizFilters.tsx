"use client"

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Badge } from '../ui/badge'

interface VizFiltersProps {
  domains: string[]
  tools: string[]
  types: string[]
  selectedDomain?: string
  selectedTool?: string
  selectedType?: string
  onDomainChange: (domain: string | undefined) => void
  onToolChange: (tool: string | undefined) => void
  onTypeChange: (type: string | undefined) => void
}

export function VizFilters({
  domains,
  tools,
  types,
  selectedDomain,
  selectedTool,
  selectedType,
  onDomainChange,
  onToolChange,
  onTypeChange,
}: VizFiltersProps) {
  return (
    <Card className="glass-card sticky top-24 rounded-[32px] border border-slate-200/70 bg-white/80 backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/60 dark:text-white">
      <CardHeader>
        <CardTitle className="text-lg text-slate-900 dark:text-white">Filters</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <h3 className="text-sm font-semibold mb-2 text-slate-900 dark:text-white">Domain</h3>
          <div className="flex flex-wrap gap-2">
            <Badge
              variant={!selectedDomain ? "default" : "outline"}
              className="cursor-pointer"
              onClick={() => onDomainChange(undefined)}
            >
              All
            </Badge>
            {domains.map((domain) => (
              <Badge
                key={domain}
                variant={selectedDomain === domain ? "default" : "outline"}
                className="cursor-pointer"
                onClick={() => onDomainChange(selectedDomain === domain ? undefined : domain)}
              >
                {domain}
              </Badge>
            ))}
          </div>
        </div>
        
        <div>
          <h3 className="text-sm font-semibold mb-2 text-slate-900 dark:text-white">Tool</h3>
          <div className="flex flex-wrap gap-2">
            <Badge
              variant={!selectedTool ? "default" : "outline"}
              className="cursor-pointer"
              onClick={() => onToolChange(undefined)}
            >
              All
            </Badge>
            {tools.map((tool) => (
              <Badge
                key={tool}
                variant={selectedTool === tool ? "default" : "outline"}
                className="cursor-pointer"
                onClick={() => onToolChange(selectedTool === tool ? undefined : tool)}
              >
                {tool}
              </Badge>
            ))}
          </div>
        </div>
        
        <div>
          <h3 className="text-sm font-semibold mb-2 text-slate-900 dark:text-white">Type</h3>
          <div className="flex flex-wrap gap-2">
            <Badge
              variant={!selectedType ? "default" : "outline"}
              className="cursor-pointer"
              onClick={() => onTypeChange(undefined)}
            >
              All
            </Badge>
            {types.map((type) => (
              <Badge
                key={type}
                variant={selectedType === type ? "default" : "outline"}
                className="cursor-pointer"
                onClick={() => onTypeChange(selectedType === type ? undefined : type)}
              >
                {type}
              </Badge>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

