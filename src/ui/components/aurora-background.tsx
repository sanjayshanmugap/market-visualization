"use client"

import { useEffect, useRef } from 'react'

export function AuroraBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    let animationFrameId: number
    let time = 0

    const resize = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    resize()
    window.addEventListener('resize', resize)

    const draw = () => {
      time += 0.005
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      // Create flowing aurora gradient with more visible colors
      const hue1 = (time * 10) % 360
      const hue2 = (time * 10 + 60) % 360
      const hue3 = (time * 10 + 120) % 360
      
      const gradient1 = ctx.createLinearGradient(0, 0, canvas.width, canvas.height)
      gradient1.addColorStop(0, `hsla(${hue1}, 80%, 60%, 0.25)`)
      gradient1.addColorStop(0.5, `hsla(${hue2}, 80%, 60%, 0.2)`)
      gradient1.addColorStop(1, `hsla(${hue3}, 80%, 60%, 0.25)`)

      const gradient2 = ctx.createLinearGradient(canvas.width, 0, 0, canvas.height)
      const hue4 = (time * 10 + 180) % 360
      const hue5 = (time * 10 + 240) % 360
      const hue6 = (time * 10 + 300) % 360
      gradient2.addColorStop(0, `hsla(${hue4}, 80%, 60%, 0.2)`)
      gradient2.addColorStop(0.5, `hsla(${hue5}, 80%, 60%, 0.25)`)
      gradient2.addColorStop(1, `hsla(${hue6}, 80%, 60%, 0.2)`)

      // Draw flowing waves
      ctx.fillStyle = gradient1
      ctx.beginPath()
      ctx.moveTo(0, canvas.height)
      for (let x = 0; x < canvas.width; x += 5) {
        const y = canvas.height / 2 + Math.sin(x * 0.01 + time) * 100 + Math.cos(x * 0.005 + time * 0.7) * 150
        ctx.lineTo(x, y)
      }
      ctx.lineTo(canvas.width, canvas.height)
      ctx.closePath()
      ctx.fill()

      ctx.fillStyle = gradient2
      ctx.beginPath()
      ctx.moveTo(0, canvas.height)
      for (let x = 0; x < canvas.width; x += 5) {
        const y = canvas.height / 2 + Math.sin(x * 0.008 + time * 1.2) * 120 + Math.cos(x * 0.006 + time * 0.9) * 180
        ctx.lineTo(x, y)
      }
      ctx.lineTo(canvas.width, canvas.height)
      ctx.closePath()
      ctx.fill()

      animationFrameId = requestAnimationFrame(draw)
    }

    draw()

    return () => {
      window.removeEventListener('resize', resize)
      cancelAnimationFrame(animationFrameId)
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 -z-10 pointer-events-none opacity-60 dark:opacity-50"
      style={{ mixBlendMode: 'screen' }}
    />
  )
}

