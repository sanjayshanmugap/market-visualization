"use client"

import Particles from '../../../components/Particles'

export default function ParticlesTestPage() {
  return (
    <div className="relative h-screen w-screen overflow-hidden bg-black">
      <Particles />
      <div className="absolute inset-0 flex items-center justify-center z-10">
        <h1 className="text-5xl font-bold text-white">Particles Background</h1>
      </div>
    </div>
  )
}

