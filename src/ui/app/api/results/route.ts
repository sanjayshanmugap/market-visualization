import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET() {
  try {
    // Try multiple possible paths for the results file
    const possiblePaths = [
      // From src/ui/ up to project root
      path.resolve(process.cwd(), '../../results/month1/experiment_report.json'),
      // Alternative: absolute from project root
      path.resolve(process.cwd(), '../../../results/month1/experiment_report.json'),
      // If running from project root
      path.join(process.cwd(), 'results', 'month1', 'experiment_report.json'),
    ]
    
    let fileContents: string | null = null
    for (const resultsPath of possiblePaths) {
      if (fs.existsSync(resultsPath)) {
        fileContents = fs.readFileSync(resultsPath, 'utf8')
        break
      }
    }
    
    if (!fileContents) {
      // Return a helpful error with path information for debugging
      return NextResponse.json(
        { 
          error: 'Results file not found',
          searchedPaths: possiblePaths,
          cwd: process.cwd()
        },
        { status: 404 }
      )
    }
    
    const data = JSON.parse(fileContents)
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error reading results:', error)
    return NextResponse.json(
      { error: 'Failed to load simulation results', details: error instanceof Error ? error.message : String(error) },
      { status: 500 }
    )
  }
}

