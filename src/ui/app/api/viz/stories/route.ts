import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET() {
  try {
    // Try multiple possible paths
    const possibleDirs = [
      path.join(process.cwd(), 'public', 'data', 'viz', 'stories'),
      path.join(process.cwd(), '..', '..', '..', 'data', 'viz', 'stories'),
      path.join(process.cwd(), 'data', 'viz', 'stories'),
    ]
    
    const storiesDir = possibleDirs.find(dir => fs.existsSync(dir))
    
    if (!storiesDir) {
      return NextResponse.json({ error: 'Stories directory not found' }, { status: 404 })
    }
    
    const files = fs.readdirSync(storiesDir).filter(f => f.endsWith('.json'))
    
    const stories = files.map(file => {
      const filePath = path.join(storiesDir, file)
      const content = fs.readFileSync(filePath, 'utf8')
      const story = JSON.parse(content)
      return {
        id: story.id,
        title: story.title,
        description: story.description,
        domain: story.domain,
        slug: story.slug,
      }
    })
    
    return NextResponse.json(stories)
  } catch (error) {
    console.error('Error loading stories:', error)
    return NextResponse.json({ error: 'Failed to load stories' }, { status: 500 })
  }
}

