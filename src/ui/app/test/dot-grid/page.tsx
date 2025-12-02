"use client"

import DotGrid from '../../../components/DotGrid'

export default function DotGridTestPage() {
  return (
    <div className="relative h-screen w-screen overflow-hidden bg-black">
      <DotGrid />
      <div className="absolute inset-0 flex items-center justify-center z-10">
        <h1 className="text-5xl font-bold text-white">Dot Grid Background</h1>
      </div>
    </div>
  )
}

