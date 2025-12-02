"use client"

import LiquidEther from '../../../components/LiquidEther'

export default function LiquidEtherTestPage() {
  return (
    <div className="relative h-screen w-screen overflow-hidden bg-black">
      <LiquidEther />
      <div className="absolute inset-0 flex items-center justify-center z-10">
        <h1 className="text-5xl font-bold text-white">Liquid Ether Background</h1>
      </div>
    </div>
  )
}

