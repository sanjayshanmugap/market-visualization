# Deployment Guide: Manim Integration & Vercel Deployment

## Part 1: Incorporating Manim Animations

### Current Status
Manim animation metadata has already been generated. The animations are stored as metadata files in `data/viz/static/` with `_metadata.json` extensions.

### Option A: Pre-render Manim Videos (Recommended for Vercel)

Since Vercel doesn't support running Manim during build time, you should pre-render videos locally:

1. **Render Manim animations locally:**
   ```bash
   source venv/bin/activate
   python scripts/generate_housing_manim.py
   ```

2. **Create actual Manim scene files** (you'll need to create these based on the metadata):
   ```python
   # Example: scripts/manim_scenes/correlation_animation.py
   from manim import *
   import json
   
   class CorrelationAnimation(Scene):
       def construct(self):
           # Load metadata
           with open('data/viz/static/housing_correlation_animation_metadata.json') as f:
               data = json.load(f)
           
           # Create animation based on metadata
           # ... (implement animation logic)
   ```

3. **Render videos:**
   ```bash
   manim -pql scripts/manim_scenes/correlation_animation.py CorrelationAnimation
   ```

4. **Move rendered videos to public directory:**
   ```bash
   mkdir -p src/ui/public/animations
   cp media/videos/correlation_animation/720p30/*.mp4 src/ui/public/animations/
   ```

5. **Update frontend to display videos:**
   - Add video player component in story pages
   - Reference videos from `/animations/` path

### Option B: Use External Hosting (Alternative)

1. Upload Manim videos to:
   - YouTube (unlisted)
   - Cloudinary
   - AWS S3
   - Vercel Blob Storage

2. Store video URLs in story metadata
3. Embed videos in story pages

### Option C: Skip Manim for Now (Simplest)

The visualizations work without Manim. You can:
- Keep the metadata files for future use
- Add Manim videos later when needed
- Focus on the Plotly visualizations which are already working

## Part 2: Deploying to Vercel

### Step 1: Prepare for Deployment

1. **Copy data files to public directory:**
   ```bash
   mkdir -p src/ui/public/data
   cp -r data/viz src/ui/public/data/
   ```

2. **Generate visualizations before committing:**
   ```bash
   source venv/bin/activate
   python scripts/generate_housing_stories.py
   ```

3. **Build frontend to check for errors:**
   ```bash
   cd src/ui
   npm run build
   ```

### Step 2: Commit to GitHub

1. **Initialize git (if not already):**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: House prices data visualization"
   ```

2. **Add remote and push:**
   ```bash
   git remote add origin https://github.com/sanjayshanmugap/market-visualization.git
   git branch -M main
   git push -u origin main
   ```

### Step 3: Configure Vercel

#### Option A: Vercel Web UI (Recommended)

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click "Add New Project"
3. Import your GitHub repository: `sanjayshanmugap/market-visualization`
4. Configure project settings:
   - **Framework Preset:** Next.js (auto-detected)
   - **Root Directory:** Set to `src/ui` in project settings (Settings → General → Root Directory)
   - **Build Command:** `npm run build` (or leave default)
   - **Output Directory:** `.next` (or leave default)
   - **Install Command:** `npm install` (or leave default)
   
   **Note:** Root Directory must be set in Vercel dashboard, not in vercel.json

5. **Environment Variables (if needed):**
   - Add any API keys or environment variables in the Vercel dashboard

6. Click **Deploy**

#### Option B: Vercel CLI

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Login:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   cd src/ui
   vercel
   ```

4. **Follow prompts:**
   - Link to existing project or create new
   - Set root directory: `src/ui` (or navigate to it first)

### Step 4: API Routes (Already Set Up!)

✅ **Good news:** I've already created Next.js API routes that replace the FastAPI backend:
- `/api/viz/list` - Lists all visualizations
- `/api/viz/stories` - Lists all stories
- `/api/viz/stories/[slug]` - Gets a specific story
- `/api/viz/[id]/plotly` - Gets Plotly visualization data

These routes read from the `public/data/viz/` directory, which works perfectly with Vercel's static file serving.

### Step 5: Vercel Configuration

✅ **Already created:** `src/ui/vercel.json` with proper configuration.

When setting up in Vercel dashboard:
- **Root Directory:** `src/ui` (set in project settings)
- **Framework:** Next.js (auto-detected)
- Vercel will use the `vercel.json` in the `src/ui` directory

### Step 6: Important Notes

1. **Data Files Location:**
   - Data files are in `src/ui/public/data/viz/`
   - These are served as static files by Vercel
   - API routes read from this location

2. **File Size Limits:**
   - Vercel has a 100MB file size limit per deployment
   - Your JSON files should be well under this limit
   - If you add Manim videos, consider external hosting

3. **Build Process:**
   - Vercel will run `npm install` and `npm run build` in `src/ui/`
   - Make sure all dependencies are in `src/ui/package.json`
   - Python scripts are only needed locally for generating data

### Step 7: Post-Deployment Checklist

- [ ] Verify all visualizations load correctly
- [ ] Test story pages
- [ ] Check gallery page
- [ ] Verify API endpoints work (check Network tab)
- [ ] Test dark mode
- [ ] Check mobile responsiveness
- [ ] Verify all links work

## Quick Start Commands

```bash
# 1. Generate visualizations
source venv/bin/activate
python scripts/generate_housing_stories.py

# 2. Copy data to public directory
mkdir -p src/ui/public/data
cp -r data/viz src/ui/public/data/

# 3. Test build
cd src/ui
npm run build

# 4. Commit to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# 5. Deploy to Vercel (via CLI)
cd src/ui
vercel

# Or deploy via Vercel dashboard
# Go to vercel.com → Import Project → Select GitHub repo
```

## Troubleshooting

### Build Fails
- Check Node.js version (Vercel uses Node 18+)
- Ensure all dependencies are in `package.json`
- Check for TypeScript errors: `cd src/ui && npm run build`

### API Not Working
- Verify data files are in `src/ui/public/data/viz/`
- Check API route files exist in `src/ui/app/api/`
- Check browser console for errors
- Verify file paths in API routes match your structure

### Visualizations Not Loading
- Ensure JSON files are in `src/ui/public/data/viz/data/`
- Check API routes return correct data
- Verify file paths are correct
- Check browser Network tab for failed requests

### Manim Videos Not Showing
- Videos must be pre-rendered and committed to repo
- Or use external hosting (YouTube, Cloudinary, etc.)
- Or skip Manim for initial deployment (recommended)

## Notes

- ✅ Next.js API routes are already set up - no FastAPI needed!
- ✅ Data files should be in `src/ui/public/data/viz/` for Vercel
- ✅ Vercel has a 100MB file size limit per deployment
- ✅ Next.js API routes have execution time limits (10s on Hobby, 60s on Pro)
- ✅ All visualizations are static JSON files - perfect for Vercel!
