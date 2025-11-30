# Download Videos from Google Drive

## Quick Setup Instructions

1. **Download all files from Google Drive:**
   - Go to: https://drive.google.com/drive/folders/1HVv67H_k4qP0tdgN80ZMUwu96UOin8Zc?usp=sharing
   - Download these 5 files:
     - `AB_book-now-video.mp4`
     - `adda-brow-logo.png`
     - `background-1.MP4`
     - `background-2.mp4`
     - `hero-intro.MP4`

2. **Place them in the correct folder:**
   - Copy all files to: `/public/videos/` folder
   - Make sure filenames match exactly (case-sensitive)

3. **Verify files are in place:**
   ```bash
   ls -la public/videos/
   ```
   You should see all 5 files listed.

---

## After Downloading

Once files are downloaded, the site will automatically use them. The paths will be updated to:
- `/videos/adda-brow-logo.png` (logo)
- `/videos/background-1.MP4` (hero video)
- `/videos/background-2.mp4` (parallax video)
- `/videos/hero-intro.MP4` (if needed)
- `/videos/AB_book-now-video.mp4` (if needed)

---

## Alternative: Direct Download Links

If you prefer, you can:
1. Right-click each file in Google Drive
2. Select "Get link" → "Anyone with the link"
3. Use the file IDs to create direct download links

Then I can create a download script for you!

