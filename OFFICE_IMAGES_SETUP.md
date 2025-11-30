# AB_Office Images Setup

## ✅ What's Been Done

All dark backgrounds have been replaced with **tiled AB_Office images** with transparency overlays for a brighter, cleaner aesthetic!

## 📁 Required File

**Expected location:** `videos/AB_Office.jpg` (or `.png`)

### If you have multiple office images:

If you have multiple office images (e.g., `AB_Office_1.jpg`, `AB_Office_2.jpg`), you can:
- Use one image that tiles well (recommended)
- OR use different images for different sections

## 🎨 Current Implementation

### Sections Using Office Backgrounds:

1. **Body (Overall background)**
   - Tiled pattern: 400px × 400px
   - Dark overlay: 40% opacity

2. **Hero Section**
   - Tiled pattern: 500px × 500px
   - Gradient overlay for depth

3. **Social Proof Section**
   - Tiled pattern: 450px × 450px
   - 60% dark overlay

4. **Testimonials Section**
   - Tiled pattern: 500px × 500px
   - Gradient overlay

5. **FAQ Section**
   - Tiled pattern: 450px × 450px
   - 50% dark overlay

6. **Why Choose Section**
   - Tiled pattern: 450px × 450px
   - 55% dark overlay

## 🔧 Customization

### To adjust brightness:
Edit the overlay opacity in each section's `::before` pseudo-element:
- Lower opacity = brighter (e.g., `rgba(10, 10, 10, 0.3)`)
- Higher opacity = darker (e.g., `rgba(10, 10, 10, 0.7)`)

### To change tile size:
Edit `background-size` property:
- Larger = less repetition (e.g., `800px 800px`)
- Smaller = more repetition (e.g., `200px 200px`)

### To use different images per section:
Change the `url('videos/AB_Office.jpg')` to your specific image name

## 📝 Notes

- Images will **tile/repeat** across the entire section
- Overlays ensure **text remains readable**
- The design maintains a **premium, clean aesthetic**
- Office images add **professional, bright atmosphere**

## ✅ Next Steps

1. Place `AB_Office.jpg` (or `.png`) in the `videos/` folder
2. Test the page to see the brighter layout!
3. Adjust overlay opacity if needed for your specific image

---

**Result:** Bright, clean, professional layout with office imagery! ✨

