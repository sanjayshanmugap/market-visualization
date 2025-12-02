# Quick Deployment Guide

## ✅ What's Been Done

1. ✅ Removed all tags (housing, plotly) from UI
2. ✅ Removed filter tools from gallery
3. ✅ Made cards text-only (no images)
4. ✅ Created Next.js API routes (no FastAPI needed!)
5. ✅ Copied data files to `src/ui/public/data/viz/`

## 🚀 Deploy to Vercel

### Step 1: Commit to GitHub

```bash
# Initialize git (if needed)
git init

# Add all files
git add .

# Commit
git commit -m "House prices data visualization - ready for deployment"

# Add remote
git remote add origin https://github.com/sanjayshanmugap/market-visualization.git

# Push
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Vercel

**Option A: Via Vercel Dashboard (Easiest)**
1. Go to https://vercel.com
2. Sign in with GitHub
3. Click "Add New Project"
4. Select `sanjayshanmugap/market-visualization`
5. Vercel will auto-detect Next.js
6. **Important:** Set "Root Directory" to `src/ui`
   - Click "Configure Project" before deploying
   - Under "Root Directory", enter: `src/ui`
   - Or set it later in: Settings → General → Root Directory
7. Click "Deploy"

**Option B: Via CLI**
```bash
npm i -g vercel
cd src/ui
vercel
# Follow prompts, set root directory to current (src/ui)
```

## 🎬 Manim Integration

### Current Status
- Manim metadata files are generated
- Actual video rendering needs to be done locally

### To Add Manim Videos:

1. **Render videos locally:**
   ```bash
   source venv/bin/activate
   # Create scene files based on metadata
   manim -pql your_scene.py SceneName
   ```

2. **Add videos to public folder:**
   ```bash
   mkdir -p src/ui/public/animations
   cp rendered_videos/*.mp4 src/ui/public/animations/
   ```

3. **Update story pages to show videos** (optional - can be done later)

### For Now
- ✅ All Plotly visualizations work perfectly
- ✅ Manim can be added later
- ✅ Focus on deploying the working visualizations first

## 📝 Important Notes

- **Data Location:** `src/ui/public/data/viz/` (already copied)
- **API Routes:** Already created in `src/ui/app/api/`
- **No Backend Needed:** Everything runs on Vercel!
- **File Size:** All JSON files are small, well under Vercel limits

## 🧪 Test Before Deploying

```bash
# 1. Test build
cd src/ui
npm run build

# 2. Test locally (optional)
npm run dev
# Visit http://localhost:3000
```

## ✅ After Deployment

Your site will be live at: `https://your-project.vercel.app`

Check:
- Gallery page loads
- Stories page loads  
- Individual story pages work
- Visualizations display correctly

