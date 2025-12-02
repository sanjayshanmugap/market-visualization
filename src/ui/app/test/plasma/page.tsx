"use client"

import Plasma from '../../../components/Plasma'

export default function PlasmaTestPage() {
  return (
    <div className="relative h-screen w-screen overflow-hidden bg-black">
      <Plasma />
      <div className="absolute inset-0 flex items-center justify-center z-10">
        <h1 className="text-5xl font-bold text-white">Plasma Background</h1>
      </div>
    </div>
  )
}

