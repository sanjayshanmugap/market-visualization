"use client"

import Galaxy from '../../../components/Galaxy'

export default function GalaxyTestPage() {
  return (
    <div className="relative h-screen w-screen overflow-hidden bg-black">
      <Galaxy />
      <div className="absolute inset-0 flex items-center justify-center z-10">
        <h1 className="text-5xl font-bold text-white">Galaxy Background</h1>
      </div>
    </div>
  )
}

