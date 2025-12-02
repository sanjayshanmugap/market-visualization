import Link from 'next/link'
import { Button } from '../components/ui/button'

export default function HomePage() {
  return (
    <div className="relative">
      <section className="relative z-10 mx-auto flex min-h-[85vh] flex-col items-center justify-center px-6 pt-32 text-center sm:px-8">
        <div className="glass-hero max-w-3xl space-y-8 rounded-[32px] border border-slate-200/70 bg-white/80 p-10 text-slate-900 backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/60 dark:text-white">
          <h1 className="text-4xl font-semibold leading-tight text-slate-900 sm:text-5xl md:text-6xl dark:text-white">
            House Prices
            <span className="text-gradient"> Data Analysis</span>
          </h1>
          <p className="text-lg text-slate-600 md:text-xl dark:text-white/70">
            Exploring patterns and relationships in housing data to predict sale prices.
          </p>
          <div className="flex flex-col gap-4 pt-2 sm:flex-row sm:items-center sm:justify-center">
            <Link href="/gallery">
              <Button className="glass-button primary">
                Explore Gallery
              </Button>
            </Link>
            <Link href="/stories">
              <Button variant="outline" className="glass-button subtle">
                Read Stories
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
