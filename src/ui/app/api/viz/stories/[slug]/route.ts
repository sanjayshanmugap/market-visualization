import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET(
  request: Request,
  { params }: { params: { slug: string } }
) {
  try {
    const slug = params.slug
    
    // Try multiple possible paths
    const possiblePaths = [
      path.join(process.cwd(), 'public', 'data', 'viz', 'stories', `${slug}.json`),
      path.join(process.cwd(), '..', '..', '..', 'data', 'viz', 'stories', `${slug}.json`),
      path.join(process.cwd(), 'data', 'viz', 'stories', `${slug}.json`),
    ]
    
    const storyPath = possiblePaths.find(p => fs.existsSync(p))
    
    if (!storyPath) {
      return NextResponse.json({ error: 'Story not found' }, { status: 404 })
    }
    
    const content = fs.readFileSync(storyPath, 'utf8')
    const story = JSON.parse(content)
    
    return NextResponse.json(story)
  } catch (error) {
    console.error('Error loading story:', error)
    return NextResponse.json({ error: 'Failed to load story' }, { status: 500 })
  }
}

