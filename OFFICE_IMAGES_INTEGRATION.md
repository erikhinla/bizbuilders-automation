# Office Images Integration Plan

## Current Dark Backgrounds to Replace

1. **Body background:** `#0a0a0a` (solid black)
2. **Hero section:** Dark gradient `linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0f0f0f 100%)`
3. **Social Proof section:** `#111111` (dark gray)
4. **Testimonials section:** Dark gradient
5. **Quiz container:** `rgba(10, 10, 10, 0.95)` (near black)
6. **FAQ section:** `#111111`

## Strategy: Tiled Background Images with Transparency

### Approach:
- Use AB_Office images as **subtle, repeating backgrounds**
- Apply **dark overlay** (30-40% opacity) to maintain text readability
- Create **clean, bright aesthetic** while keeping premium feel
- Use **glass morphism** on cards/elements for depth

### Implementation:

1. **Body background:**
   - Tiled AB_Office image (repeat)
   - Dark overlay: `rgba(10, 10, 10, 0.5)`

2. **Section backgrounds:**
   - Alternating office images or same image
   - Lighter overlay for brightness
   - Maintain text contrast

3. **Cards/Elements:**
   - Glass morphism with backdrop blur
   - Slight transparency to show background

## Files Needed

- AB_Office images (JPG/PNG format)
- Place in: `videos/` or `images/` folder

## CSS Pattern:

```css
background-image: 
    url('videos/AB_Office.jpg'),
    linear-gradient(rgba(10, 10, 10, 0.5), rgba(10, 10, 10, 0.5));
background-size: cover;
background-position: center;
background-repeat: repeat; /* or no-repeat for full coverage */
background-blend-mode: overlay;
```

