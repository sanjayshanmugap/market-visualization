"use client"

import Link from 'next/link'
import { useState } from 'react'
import { ThemeToggle } from './theme-toggle'

export function Header() {
  const [open, setOpen] = useState(false)
  const navItems = [
    { label: 'Home', href: '/' },
    { label: 'Gallery', href: '/gallery' },
    { label: 'Stories', href: '/stories' },
    { label: 'About', href: '/about' },
  ]

  return (
    <header className="sticky top-6 z-50 flex justify-center px-4 md:px-6">
      <div className="glass-nav flex w-full max-w-6xl items-center justify-between rounded-full border border-slate-200/60 bg-white/80 px-4 py-2 text-sm text-slate-900 shadow-lg shadow-primary/10 backdrop-blur-2xl dark:border-white/10 dark:bg-white/5 dark:text-white md:px-6">
        <Link href="/" className="flex items-center gap-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-white shadow-sm dark:bg-white/10">
            <span className="text-lg font-semibold text-slate-900 dark:text-white">Λ</span>
          </div>
          <div className="flex flex-col leading-tight">
            <span className="text-xs uppercase tracking-widest text-slate-500 dark:text-white/70">Data</span>
            <span className="text-base font-semibold text-slate-900 dark:text-white">Visualization Portfolio</span>
          </div>
        </Link>

        <nav className="hidden items-center gap-6 font-medium md:flex">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="transition-colors duration-200 text-slate-600 hover:text-slate-900 dark:text-white/70 dark:hover:text-white"
            >
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-3">
          <ThemeToggle />
          <Link
            href="/gallery"
            className="hidden rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow-sm transition-transform duration-200 hover:-translate-y-0.5 hover:bg-black md:inline-flex dark:bg-white dark:text-slate-900 dark:hover:bg-white/90"
          >
            View Gallery
          </Link>
          <button
            className="inline-flex items-center justify-center rounded-full border border-slate-200/80 bg-white/90 p-2 text-slate-700 transition-colors md:hidden dark:border-white/20 dark:bg-white/10 dark:text-white"
            aria-label="Toggle menu"
            onClick={() => setOpen((v) => !v)}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M4 6h16M4 12h16M4 18h16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
            </svg>
          </button>
        </div>
      </div>

      {open && (
        <div className="absolute inset-x-4 top-[4.5rem] md:hidden">
          <nav className="glass-panel flex flex-col gap-2 rounded-3xl border border-slate-200/70 bg-white/90 p-4 text-slate-900 shadow-lg shadow-primary/10 backdrop-blur-2xl dark:border-white/10 dark:bg-white/10 dark:text-white">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="rounded-2xl px-3 py-2 text-base font-medium text-slate-700 transition-colors hover:bg-white hover:text-slate-900 dark:text-white/80 dark:hover:bg-white/10 dark:hover:text-white"
                onClick={() => setOpen(false)}
              >
                {item.label}
              </Link>
            ))}
            <Link
              href="/gallery"
              className="rounded-2xl bg-slate-900 px-3 py-2 text-center text-sm font-semibold text-white transition hover:bg-black dark:bg-white dark:text-slate-900 dark:hover:bg-white/90"
              onClick={() => setOpen(false)}
            >
              View Gallery
            </Link>
          </nav>
        </div>
      )}
    </header>
  )
}


