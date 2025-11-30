# How to View Your Quiz Page

## ✅ Quick Access (Server Already Running!)

**Local URL:**
```
http://localhost:8080/brows-quiz.html
```

Just copy this URL and paste it into your browser!

---

## 📱 Alternative Methods

### Option 1: Double-Click (Simplest)
1. Open Finder
2. Navigate to your project folder
3. Double-click `brows-quiz.html`
4. It will open in your default browser

### Option 2: Drag & Drop
1. Open your browser
2. Drag `brows-quiz.html` into the browser window

### Option 3: Right-Click → Open With
1. Right-click `brows-quiz.html`
2. Select "Open With" → Your preferred browser

---

## 🚀 Start Server (If Not Running)

If the server isn't running, start it with:

```bash
cd /Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
python3 -m http.server 8080
```

Then open: `http://localhost:8080/brows-quiz.html`

---

## 📝 Important Notes

### Files Needed for Full Experience:

The page will work, but some elements need files in the `videos/` folder:

**Videos:**
- `background-1.MP4` (hero video)
- `background-2.mp4` (parallax video)

**Images:**
- `adda-brow-logo.png` (logo)
- `AB_Office_1.jpg` through `AB_Office_6.jpg` (office backgrounds)

**Without these files:**
- Videos won't play (will show black backgrounds)
- Logo won't display (will show broken image icon)
- Office backgrounds won't show (will use fallback dark colors)

---

## 🔧 Troubleshooting

**Problem: Page looks broken**
- ✅ Make sure you're viewing via `localhost:8080` (not file://)
- ✅ Check browser console for errors (F12 → Console)
- ✅ Verify files exist in `videos/` folder

**Problem: Images/videos not showing**
- ✅ Check file names match exactly (case-sensitive!)
- ✅ Verify files are in `videos/` folder (not `public/videos/`)
- ✅ Check browser console for 404 errors

**Problem: Can't access localhost:8080**
- ✅ Server might not be running - start it with command above
- ✅ Try a different port: `python3 -m http.server 3000`
- ✅ Then access: `http://localhost:3000/brows-quiz.html`

---

## ✅ Quick Checklist

- [ ] Server running? Check: `http://localhost:8080`
- [ ] Opened `brows-quiz.html` in browser?
- [ ] All files in `videos/` folder?
- [ ] No console errors? (Press F12 to check)

---

**Enjoy viewing your premium quiz page!** 🎉

