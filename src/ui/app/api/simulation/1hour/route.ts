import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET() {
  try {
    const cwd = process.cwd()
    
    // Try to find project root
    let projectRoot = cwd
    const dirsToCheck = [cwd, path.resolve(cwd, '..'), path.resolve(cwd, '../..'), path.resolve(cwd, '../../..')]
    
    for (const dir of dirsToCheck) {
      const resultsDir = path.join(dir, 'results', '1hour')
      if (fs.existsSync(resultsDir)) {
        projectRoot = dir
        break
      }
    }
    
    // Build possible paths
    const possiblePaths = [
      path.join(projectRoot, 'results', '1hour', 'experiment_report.json'),
      path.resolve(cwd, '../../results/1hour/experiment_report.json'),
      path.resolve(cwd, '../../../results/1hour/experiment_report.json'),
      path.join(cwd, 'results', '1hour', 'experiment_report.json'),
    ]
    
    let fileContents: string | null = null
    
    for (const resultsPath of possiblePaths) {
      try {
        if (fs.existsSync(resultsPath)) {
          fileContents = fs.readFileSync(resultsPath, 'utf8')
          break
        }
      } catch (err) {
        continue
      }
    }
    
    if (!fileContents) {
      return NextResponse.json(
        { 
          error: '1-hour simulation results not found',
          hint: 'Make sure you have run: python scripts/run_1hour_simulation.py'
        },
        { status: 404 }
      )
    }
    
    const data = JSON.parse(fileContents)
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error reading 1hour results:', error)
    return NextResponse.json(
      { error: 'Failed to load simulation results', details: error instanceof Error ? error.message : String(error) },
      { status: 500 }
    )
  }
}

