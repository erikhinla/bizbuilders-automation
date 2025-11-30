# 📹 Video Integration Instructions

## ✅ What's Done

All video/image paths in `brows-quiz.html` have been updated to use local files:
- ✅ Logo: `videos/adda-brow-logo.png`
- ✅ Hero video: `videos/background-1.MP4`
- ✅ Parallax video: `videos/background-2.mp4`

## 📥 Download from Google Drive

**Google Drive Folder:** https://drive.google.com/drive/folders/1HVv67H_k4qP0tdgN80ZMUwu96UOin8Zc

### Files to Download:

1. **AB_book-now-video.mp4** (8.4 MB)
2. **adda-brow-logo.png** (2 MB) - **REQUIRED**
3. **background-1.MP4** (2.3 MB) - **REQUIRED**
4. **background-2.mp4** (2.3 MB) - **REQUIRED**
5. **hero-intro.MP4** (3.5 MB) - Optional (if you want to use it)

### Steps:

1. **Open Google Drive folder** in your browser
2. **Select all files** (or download individually)
3. **Download** to your computer
4. **Move files** to: `videos/` folder in your project root
5. **Verify** all files are in place

### Quick Command:

After downloading to your Downloads folder:

```bash
# Move files to videos folder
mv ~/Downloads/AB_book-now-video.mp4 videos/
mv ~/Downloads/adda-brow-logo.png videos/
mv ~/Downloads/background-1.MP4 videos/
mv ~/Downloads/background-2.mp4 videos/
mv ~/Downloads/hero-intro.MP4 videos/  # optional

# Verify files are there
ls -lh videos/
```

You should see:
```
AB_book-now-video.mp4
adda-brow-logo.png
background-1.MP4
background-2.mp4
hero-intro.MP4 (optional)
```

---

## 🚀 After Downloading

Once files are in the `videos/` folder:

1. **Test locally:**
   ```bash
   # If you have a local server running
   open http://localhost:8080/brows-quiz.html
   ```

2. **Files will work automatically** - no code changes needed!

3. **For deployment** (Vercel):
   - Files in `videos/` folder will be deployed automatically
   - Paths will resolve to `/videos/...` on live site

---

## ✅ Verification Checklist

- [ ] All 5 files downloaded from Google Drive
- [ ] Files placed in `videos/` folder
- [ ] File names match exactly (case-sensitive!)
- [ ] Test page loads with videos/images
- [ ] Hero video plays in background
- [ ] Logo displays in header
- [ ] Parallax video plays behind quiz

---

## 🔧 Troubleshooting

**Problem: Videos/images not showing**
- ✅ Check file names match exactly (case-sensitive)
- ✅ Verify files are in `videos/` folder (not `public/videos/`)
- ✅ Check browser console for 404 errors
- ✅ Ensure file paths don't have extra spaces

**Problem: Video won't play**
- ✅ Check file format is MP4 (H.264 codec)
- ✅ Try different browser
- ✅ Check file size (should be under 10MB each)

---

## 📝 Notes

- **Case-sensitive filenames:** `background-1.MP4` (uppercase) vs `background-1.mp4` (lowercase) matters!
- **File locations:** Videos folder is at project root, not in `public/` for this HTML file
- **Deployment:** Vercel will serve files from `videos/` folder automatically

---

**Ready to integrate!** Just download the files and place them in `videos/` folder. 🎉

