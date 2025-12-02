import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET() {
  try {
    const cwd = process.cwd()
    
    // Try to find project root by looking for package.json or other markers
    // Start from current directory and walk up
    let projectRoot = cwd
    let foundRoot = false
    
    // Look for project root by checking for results directory or package.json at project root
    const dirsToCheck = [cwd, path.resolve(cwd, '..'), path.resolve(cwd, '../..'), path.resolve(cwd, '../../..')]
    
    for (const dir of dirsToCheck) {
      const resultsDir = path.join(dir, 'results', '30min')
      if (fs.existsSync(resultsDir)) {
        projectRoot = dir
        foundRoot = true
        break
      }
    }
    
    // Build possible paths (all relative, no hardcoded absolute paths)
    const possiblePaths = [
      // From detected project root
      path.join(projectRoot, 'results', '30min', 'experiment_report.json'),
      // From src/ui/ up 2 levels (most common case)
      path.resolve(cwd, '../../results/30min/experiment_report.json'),
      // Other fallbacks
      path.resolve(cwd, '../../../results/30min/experiment_report.json'),
      path.join(cwd, 'results', '30min', 'experiment_report.json'),
    ]
    
    let fileContents: string | null = null
    let foundPath: string | null = null
    
    for (const resultsPath of possiblePaths) {
      try {
        if (fs.existsSync(resultsPath)) {
          fileContents = fs.readFileSync(resultsPath, 'utf8')
          foundPath = resultsPath
          break
        }
      } catch (err) {
        // Continue to next path
        continue
      }
    }
    
    if (!fileContents) {
      // Return error with helpful debugging info (sanitize paths to avoid exposing system structure)
      const sanitizedPaths = possiblePaths.map(p => {
        // Replace user home directory with ~ for privacy
        const homeDir = process.env.HOME || process.env.USERPROFILE || ''
        if (homeDir && p.startsWith(homeDir)) {
          return p.replace(homeDir, '~')
        }
        return p
      })
      
      return NextResponse.json(
        { 
          error: '30-minute simulation results not found',
          debug: {
            cwd: cwd.replace(process.env.HOME || process.env.USERPROFILE || '', '~'),
            projectRoot: foundRoot ? projectRoot.replace(process.env.HOME || process.env.USERPROFILE || '', '~') : 'not found',
            searchedPaths: sanitizedPaths,
            firstPathExists: fs.existsSync(possiblePaths[0]),
          },
          hint: 'Make sure you have run: python scripts/run_30min_simulation.py'
        },
        { status: 404 }
      )
    }
    
    const data = JSON.parse(fileContents)
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error reading 30min results:', error)
    return NextResponse.json(
      { error: 'Failed to load simulation results', details: error instanceof Error ? error.message : String(error) },
      { status: 500 }
    )
  }
}

