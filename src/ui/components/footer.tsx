import Link from 'next/link'

const columns = [
  {
    heading: 'Explore',
    links: [
      { label: 'Stories', href: '/stories' },
      { label: 'Gallery', href: '/gallery' },
      { label: 'About', href: '/about' },
    ],
  },
]

export function Footer() {
  return (
    <footer className="relative z-10 mx-auto w-full max-w-6xl px-6 pb-16 text-slate-700 sm:px-8 dark:text-white/70">
      <div className="glass-section rounded-[32px] border border-slate-200/70 bg-white/85 p-10 backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/50">
        <div className="flex flex-col gap-10 md:flex-row md:justify-between">
          <div className="max-w-sm space-y-4">
            <div className="flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-900 text-white dark:bg-white/10">
                <span className="text-xl font-semibold">🏠</span>
              </div>
              <div>
                <div className="text-lg font-semibold text-slate-900 dark:text-white">House Prices Analysis</div>
              </div>
            </div>
            <p className="text-sm leading-relaxed text-slate-600 dark:text-white/70">
              Exploring patterns and relationships in housing data to predict sale prices.
            </p>
          </div>

          <div className="grid flex-1 gap-8 text-sm text-slate-600 sm:grid-cols-2 md:grid-cols-3 dark:text-white/70">
            {columns.map((column) => (
              <div key={column.heading} className="space-y-3">
                <div className="text-xs uppercase tracking-[0.35em] text-slate-500 dark:text-white/60">{column.heading}</div>
                <ul className="space-y-2">
                  {column.links.map((link) => (
                    <li key={link.label}>
                      <Link
                        href={link.href}
                        className="text-sm text-slate-600 transition hover:text-slate-900 dark:text-white/70 dark:hover:text-white"
                      >
                        {link.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-10 flex flex-col gap-4 border-t border-slate-200/80 pt-6 text-xs text-slate-500 sm:flex-row sm:items-center sm:justify-between dark:border-white/20 dark:text-white/60">
          <span>© {new Date().getFullYear()} House Prices Data Analysis</span>
        </div>
      </div>
    </footer>
  )
}


