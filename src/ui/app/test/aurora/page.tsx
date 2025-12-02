"use client"

import Aurora from '../../../components/Aurora'

export default function AuroraTestPage() {
  return (
    <div className="relative h-screen w-screen overflow-hidden bg-black">
      <Aurora />
      <div className="absolute inset-0 flex items-center justify-center z-10">
        <h1 className="text-5xl font-bold text-white">Aurora Background</h1>
      </div>
    </div>
  )
}

