import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const vizId = params.id
    
    // Try multiple possible data directories
    const possibleDirs = [
      path.join(process.cwd(), 'public', 'data', 'viz', 'data'),
      path.join(process.cwd(), '..', '..', '..', 'data', 'viz', 'data'),
      path.join(process.cwd(), 'data', 'viz', 'data'),
    ]
    
    const dataDir = possibleDirs.find(dir => fs.existsSync(dir))
    
    if (!dataDir) {
      return NextResponse.json({ error: 'Data directory not found' }, { status: 404 })
    }
    
    // Try exact viz_id first
    let filePath = path.join(dataDir, `${vizId}.json`)
    
    // If not found, try with _plotly suffix
    if (!fs.existsSync(filePath)) {
      filePath = path.join(dataDir, `${vizId}_plotly.json`)
    }
    
    if (!fs.existsSync(filePath)) {
      return NextResponse.json({ error: 'Visualization not found' }, { status: 404 })
    }
    
    const content = fs.readFileSync(filePath, 'utf8')
    const data = JSON.parse(content)
    
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error loading visualization:', error)
    return NextResponse.json({ error: 'Failed to load visualization' }, { status: 500 })
  }
}

