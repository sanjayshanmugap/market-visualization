"use client"

import Orb from '../../../components/Orb'

export default function OrbTestPage() {
  return (
    <div className="relative h-screen w-screen overflow-hidden bg-black">
      <Orb />
      <div className="absolute inset-0 flex items-center justify-center z-10">
        <h1 className="text-5xl font-bold text-white">Orb Background</h1>
      </div>
    </div>
  )
}

