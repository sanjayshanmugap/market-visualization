"use client"

import LiquidEther from '../../../components/LiquidEther'

// Step 1: Just LiquidEther with minimal container
export default function LiquidEtherDebugPage() {
  return (
    <div className="fixed inset-0 bg-black">
      <LiquidEther className="h-full w-full" />
      <div className="absolute inset-0 flex items-center justify-center z-10 pointer-events-none">
        <div className="text-white text-2xl font-bold bg-black/50 px-4 py-2 rounded">
          LiquidEther Test - If you see this but no animation, check browser console
        </div>
      </div>
    </div>
  )
}

