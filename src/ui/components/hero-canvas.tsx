"use client"

import { useEffect, useRef, useState } from 'react'

export function HeroCanvas() {
  const ref = useRef<HTMLCanvasElement | null>(null)
  const [active, setActive] = useState<number | null>(null)

  useEffect(() => {
    const canvas = ref.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return
    let raf = 0

    const mqlReduced = window.matchMedia('(prefers-reduced-motion: reduce)')
    const DPR = Math.min(2, window.devicePixelRatio || 1)

    function anchors() {
      if (!canvas) return { parent: null, source: null, targets: [] }
      const parent = canvas.parentElement as HTMLElement | null
      const source = parent?.querySelector('[data-hero-source]') as HTMLElement | null
      const targets = Array.from(parent?.querySelectorAll('[data-hero-target]') || []) as HTMLElement[]
      return { parent, source, targets }
    }

    function resize() {
      if (!canvas) return
      const { parent } = anchors()
      if (!parent) return
      canvas.width = parent.clientWidth * DPR
      canvas.height = parent.clientHeight * DPR
      canvas.style.width = parent.clientWidth + 'px'
      canvas.style.height = parent.clientHeight + 'px'
    }
    resize()
    window.addEventListener('resize', resize)

    // hover listeners
    const { targets } = anchors()
    targets.forEach((el, idx) => {
      el.addEventListener('mouseenter', () => setActive(idx))
      el.addEventListener('mouseleave', () => setActive((v) => (v === idx ? null : v)))
    })

    const start = performance.now()
    function render(t: number) {
      if (!ctx || !canvas) return
      const { parent, source, targets } = anchors()
      if (!parent || !source || !targets.length) {
        raf = requestAnimationFrame(render)
        return
      }

      const parentRect = parent.getBoundingClientRect()
      const srcRect = source.getBoundingClientRect()
      const sx = (srcRect.left + srcRect.width * 0.5 - parentRect.left) * DPR
      const sy = (srcRect.top + srcRect.height * 0.25 - parentRect.top) * DPR

      ctx.clearRect(0, 0, canvas.width, canvas.height)
      const elapsed = (t - start) / 1000

      targets.forEach((el, i) => {
        const tr = el.getBoundingClientRect()
        const tx = (tr.left + tr.width * 0.85 - parentRect.left) * DPR
        const ty = (tr.top + tr.height * 0.5 - parentRect.top) * DPR
        const mx = (sx + tx) / 2
        const my = (sy + ty) / 2 - 60 * DPR

        const grad = ctx.createLinearGradient(sx, sy, tx, ty)
        grad.addColorStop(0, '#6366F1')
        grad.addColorStop(1, '#8B5CF6')
        ctx.strokeStyle = grad
        const emph = active === i ? 1.15 : 1
        ctx.lineWidth = 2 * DPR * emph
        ctx.setLineDash([8 * DPR, 10 * DPR])
        ctx.lineDashOffset = (i * 6 - elapsed * 20) * DPR
        ctx.beginPath()
        ctx.moveTo(sx, sy)
        ctx.quadraticCurveTo(mx, my, tx, ty)
        if (!mqlReduced.matches) ctx.stroke()

        // endpoints
        ctx.setLineDash([])
        const r = (2 + (active === i ? 1.2 : Math.sin(elapsed * 3 + i) * 1.0)) * DPR
        ctx.fillStyle = '#6366F1'
        ctx.beginPath(); ctx.arc(sx, sy, r, 0, Math.PI * 2); ctx.fill()
        ctx.fillStyle = '#8B5CF6'
        ctx.beginPath(); ctx.arc(tx, ty, r, 0, Math.PI * 2); ctx.fill()
      })

      raf = requestAnimationFrame(render)
    }
    raf = requestAnimationFrame(render)
    return () => {
      cancelAnimationFrame(raf)
      window.removeEventListener('resize', resize)
    }
  }, [active])

  return <canvas ref={ref} className="pointer-events-none absolute inset-0 hidden lg:block" aria-hidden />
}


