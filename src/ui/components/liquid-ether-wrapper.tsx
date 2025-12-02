"use client"

import { useEffect, useState } from 'react'
import LiquidEther from './LiquidEther'

export default function LiquidEtherWrapper({ className = "" }: { className?: string }) {
  const [isDark, setIsDark] = useState(false)
  
  useEffect(() => {
    // Check initial theme
    const checkTheme = () => {
      const html = document.documentElement
      setIsDark(html.classList.contains('dark'))
    }
    
    checkTheme()
    
    // Watch for theme changes
    const observer = new MutationObserver(checkTheme)
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class']
    })
    
    return () => observer.disconnect()
  }, [])
  
  // Use darker, more vibrant colors for dark mode
  const darkModeColors = ['#7C3AED', '#A855F7', '#C084FC'] // Purple gradient for dark mode
  const lightModeColors = ['#5227FF', '#FF9FFC', '#B19EEF'] // Original colors for light mode
  
  return (
    <div className={className}>
      <LiquidEther 
        className="h-full w-full" 
        colors={isDark ? darkModeColors : lightModeColors}
      />
    </div>
  )
}

