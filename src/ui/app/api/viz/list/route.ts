import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET() {
  try {
    // Try multiple possible paths for flexibility
    const possiblePaths = [
      path.join(process.cwd(), 'public', 'data', 'viz', 'data', 'viz_index.json'),
      path.join(process.cwd(), '..', '..', '..', 'data', 'viz', 'data', 'viz_index.json'),
      path.join(process.cwd(), 'data', 'viz', 'data', 'viz_index.json'),
    ]
    
    let filePath = possiblePaths.find(p => fs.existsSync(p))
    
    if (!filePath) {
      return NextResponse.json({ error: 'Visualization index not found' }, { status: 404 })
    }
    
    const fileContents = fs.readFileSync(filePath, 'utf8')
    const data = JSON.parse(fileContents)
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error loading visualizations:', error)
    return NextResponse.json({ error: 'Failed to load visualizations' }, { status: 500 })
  }
}

