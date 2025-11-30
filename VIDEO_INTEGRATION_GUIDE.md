# Video Integration Guide

## Current Video Setup

The site expects these video files:

1. **Hero Background Video**
   - Currently: GitHub URL
   - Location in code: Line ~893
   - Purpose: Background video in hero section

2. **Parallax Background Videos**
   - Currently: GitHub URLs
   - Location: Quiz section background

3. **Logo Image**
   - Currently: GitHub URL
   - Location: Header and hero section

## Where to Place Videos

### Option 1: Local Files (Recommended for Production)
Create a `/videos/` folder in the project root:

```
/videos/
  hero-intro.mp4 (if needed)
  background-1.mp4
  background-2.mp4
  AB_book-now-video.mp4 (if needed)
  adda-brow-logo.png
```

### Option 2: Keep GitHub URLs (Current)
If videos are hosted on GitHub and working well, we can keep them as-is.

### Option 3: CDN/Hosting Service
Upload to Vercel's public folder or use a CDN like Cloudinary, AWS S3, etc.

---

## Video Requirements

- **Format**: MP4 (H.264 codec recommended)
- **Resolution**: 1920x1080 or higher
- **File Size**: Keep optimized for web (under 10MB per video if possible)
- **Duration**: 10-30 seconds (will loop)

---

## Next Steps

**Please provide:**
1. Where are your videos located? (file paths, URLs, or upload location)
2. What format are they in?
3. Do you want them local or hosted externally?

Once I know where they are, I'll integrate them immediately!

