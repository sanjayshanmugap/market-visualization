"use client"

import LightRays from '../../../components/LightRays'

export default function LightRaysTestPage() {
  return (
    <div className="relative h-screen w-screen overflow-hidden bg-black">
      <LightRays />
      <div className="absolute inset-0 flex items-center justify-center z-10">
        <h1 className="text-5xl font-bold text-white">Light Rays Background</h1>
      </div>
    </div>
  )
}

