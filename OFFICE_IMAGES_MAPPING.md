# Office Images Mapping

## ✅ Different Office Image Per Section

Each section now uses a **unique office image** for visual variety and interest!

## 📁 Required Files

Place these images in the `videos/` folder:

1. **AB_Office_1.jpg** (or .png) - Body background
2. **AB_Office_2.jpg** (or .png) - Hero section
3. **AB_Office_3.jpg** (or .png) - Social Proof section
4. **AB_Office_4.jpg** (or .png) - Testimonials section
5. **AB_Office_5.jpg** (or .png) - Why Choose section
6. **AB_Office_6.jpg** (or .png) - FAQ section

## 🎨 Section Mapping

| Section | Image File | Tile Size | Overlay |
|---------|-----------|-----------|---------|
| **Body (Overall)** | `AB_Office_1.jpg` | 400px × 400px | 40% dark |
| **Hero** | `AB_Office_2.jpg` | 500px × 500px | Gradient |
| **Social Proof** | `AB_Office_3.jpg` | 450px × 450px | 60% dark |
| **Testimonials** | `AB_Office_4.jpg` | 500px × 500px | Gradient |
| **Why Choose** | `AB_Office_5.jpg` | 450px × 450px | 55% dark |
| **FAQ** | `AB_Office_6.jpg` | 450px × 450px | 50% dark |

## 🔧 Customization

### If you have different filenames:

Simply update the `url('videos/AB_Office_X.jpg')` in each section's CSS to match your file names.

### Example:
If your files are named:
- `office-main.jpg`
- `office-hero.jpg`
- `office-stats.jpg`
- etc.

Update the CSS like:
```css
background: url('videos/office-main.jpg') repeat;
```

### If you have fewer than 6 images:

You can reuse images for similar sections:
- Use same image for Social Proof and Testimonials
- Use same image for Why Choose and FAQ

## 📝 Notes

- Images will **tile/repeat** across each section
- Each section has its own unique visual identity
- Overlays maintain **text readability**
- Creates visual variety throughout the page
- Maintains **premium, clean aesthetic**

## ✅ Next Steps

1. Rename your office images to match the pattern:
   - `AB_Office_1.jpg`
   - `AB_Office_2.jpg`
   - `AB_Office_3.jpg`
   - `AB_Office_4.jpg`
   - `AB_Office_5.jpg`
   - `AB_Office_6.jpg`

2. Place all 6 images in the `videos/` folder

3. Test the page to see the variety!

---

**Result:** Each section has its own unique office background! ✨

