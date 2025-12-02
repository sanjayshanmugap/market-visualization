"use client"

import Threads from '../../../components/Threads'

export default function ThreadsTestPage() {
  return (
    <div className="relative h-screen w-screen overflow-hidden bg-black">
      <Threads />
      <div className="absolute inset-0 flex items-center justify-center z-10">
        <h1 className="text-5xl font-bold text-white">Threads Background</h1>
      </div>
    </div>
  )
}

