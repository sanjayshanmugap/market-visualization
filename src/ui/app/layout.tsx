import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { ThemeProvider } from '../components/theme-provider'
import { Header } from '../components/header'
import { Footer } from '../components/footer'
import LiquidEtherWrapper from '../components/liquid-ether-wrapper'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Data Visualization Portfolio',
  description: 'A comprehensive portfolio showcasing Python visualization skills across multiple libraries, domains, and formats.',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider>
          <div className="relative min-h-screen">
            <div className="fixed inset-0 -z-10">
              <div className="h-full w-full bg-transparent dark:bg-slate-950">
                <LiquidEtherWrapper className="h-full w-full" />
              </div>
            </div>
            <div className="relative z-10 flex min-h-screen flex-col">
              <Header />
              <main className="flex-1">{children}</main>
              <Footer />
            </div>
          </div>
        </ThemeProvider>
      </body>
    </html>
  )
}
