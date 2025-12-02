"use client"

import LiquidEther from '../../../components/LiquidEther'
import { useState } from 'react'

// Progressive test: Add elements one by one
export default function LiquidEtherProgressivePage() {
  const [step, setStep] = useState(1)

  const steps = [
    {
      id: 1,
      name: "Step 1: Just LiquidEther",
      content: (
        <div className="fixed inset-0">
          <LiquidEther className="h-full w-full" />
        </div>
      )
    },
    {
      id: 2,
      name: "Step 2: Add z-index container",
      content: (
        <div className="relative min-h-screen">
          <div className="fixed inset-0 -z-10">
            <LiquidEther className="h-full w-full" />
          </div>
        </div>
      )
    },
    {
      id: 3,
      name: "Step 3: Add content layer (z-10)",
      content: (
        <div className="relative min-h-screen">
          <div className="fixed inset-0 -z-10">
            <LiquidEther className="h-full w-full" />
          </div>
          <div className="relative z-10 flex min-h-screen flex-col">
            <div className="p-8">
              <h1 className="text-white text-4xl">Content Layer</h1>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 4,
      name: "Step 4: Add glassmorphic card",
      content: (
        <div className="relative min-h-screen">
          <div className="fixed inset-0 -z-10">
            <LiquidEther className="h-full w-full" />
          </div>
          <div className="relative z-10 flex min-h-screen flex-col items-center justify-center p-8">
            <div className="glass-hero max-w-3xl rounded-[32px] border border-slate-200/70 bg-white/80 p-10 text-slate-900 backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/60 dark:text-white">
              <h1 className="text-4xl font-semibold">Glassmorphic Card</h1>
              <p className="mt-4 text-lg">This card has backdrop-blur and transparency</p>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 5,
      name: "Step 5: Add Header (like layout)",
      content: (
        <div className="relative min-h-screen">
          <div className="fixed inset-0 -z-10">
            <LiquidEther className="h-full w-full" />
          </div>
          <div className="relative z-10 flex min-h-screen flex-col">
            <header className="p-6 bg-black/20 backdrop-blur-sm">
              <div className="text-white">Header</div>
            </header>
            <main className="flex-1 flex items-center justify-center p-8">
              <div className="glass-hero max-w-3xl rounded-[32px] border border-slate-200/70 bg-white/80 p-10 text-slate-900 backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/60 dark:text-white">
                <h1 className="text-4xl font-semibold">With Header</h1>
              </div>
            </main>
          </div>
        </div>
      )
    },
    {
      id: 6,
      name: "Step 6: Full home page structure",
      content: (
        <div className="relative min-h-screen">
          <div className="fixed inset-0 -z-10">
            <LiquidEther className="h-full w-full" />
          </div>
          <div className="relative z-10 flex min-h-screen flex-col">
            <header className="p-6 bg-black/20 backdrop-blur-sm">
              <div className="text-white">Header</div>
            </header>
            <main className="flex-1">
              <section className="relative z-10 mx-auto flex min-h-[85vh] flex-col items-center justify-center px-6 pt-32 text-center sm:px-8">
                <div className="glass-hero max-w-3xl space-y-8 rounded-[32px] border border-slate-200/70 bg-white/80 p-10 text-slate-900 backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/60 dark:text-white">
                  <h1 className="text-4xl font-semibold leading-tight text-slate-900 sm:text-5xl md:text-6xl dark:text-white">
                    The agentic trading lab
                  </h1>
                  <p className="text-lg text-slate-600 md:text-xl dark:text-white/70">
                    Architect your market simulator
                  </p>
                </div>
              </section>
            </main>
          </div>
        </div>
      )
    }
  ]

  const currentStep = steps.find(s => s.id === step) || steps[0]

  return (
    <div className="relative min-h-screen">
      {/* Step Controls */}
      <div className="fixed top-4 right-4 z-50 bg-black/80 backdrop-blur-sm rounded-lg p-4 text-white">
        <div className="mb-2">
          <label className="text-sm font-semibold">Current Step: {step}</label>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setStep(Math.max(1, step - 1))}
            className="px-3 py-1 bg-blue-600 rounded hover:bg-blue-700"
            disabled={step === 1}
          >
            Previous
          </button>
          <button
            onClick={() => setStep(Math.min(steps.length, step + 1))}
            className="px-3 py-1 bg-blue-600 rounded hover:bg-blue-700"
            disabled={step === steps.length}
          >
            Next
          </button>
        </div>
        <div className="mt-2 text-xs text-gray-400">{currentStep.name}</div>
      </div>

      {/* Render current step */}
      {currentStep.content}
    </div>
  )
}

