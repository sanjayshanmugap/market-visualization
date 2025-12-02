import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url)
    const start = searchParams.get('start') || '2019-01-01'
    const end = searchParams.get('end') || '2024-01-01'
    
    // Find the most recent backtest file or the one matching the date range
    const projectRoot = process.cwd().includes('src/ui') 
      ? path.join(process.cwd(), '../..')
      : process.cwd()
    
    const resultsDir = path.join(projectRoot, 'results', 'backtest')
    
    if (!fs.existsSync(resultsDir)) {
      return NextResponse.json({ error: 'No backtest results found' }, { status: 404 })
    }
    
    // Try to find matching file
    const filename = `backtest_${start}_${end}.json`
    const filePath = path.join(resultsDir, filename)
    
    if (!fs.existsSync(filePath)) {
      // Find the most recent backtest file
      const files = fs.readdirSync(resultsDir)
        .filter(f => f.startsWith('backtest_') && f.endsWith('.json'))
        .sort()
        .reverse()
      
      if (files.length === 0) {
        return NextResponse.json({ error: 'No backtest results found' }, { status: 404 })
      }
      
      const mostRecentFile = path.join(resultsDir, files[0])
      const data = JSON.parse(fs.readFileSync(mostRecentFile, 'utf-8'))
      return NextResponse.json(data)
    }
    
    const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'))
    return NextResponse.json(data)
  } catch (error: any) {
    console.error('Error loading backtest results:', error)
    return NextResponse.json(
      { error: `Failed to load backtest results: ${error.message}` },
      { status: 500 }
    )
  }
}

