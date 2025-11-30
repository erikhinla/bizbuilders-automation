# Video Backgrounds

Place your video background files here.

## Recommended Video Specs

- **Format**: MP4 (H.264 codec)
- **Resolution**: 1920x1080 or 4K
- **Duration**: 10-30 seconds (will loop)
- **File Size**: Keep under 5MB for web performance
- **Transparency**: Not required (opacity handled in CSS)
- **Content**: Abstract patterns, particles, or subtle motion

## File Naming

- `background.mp4` - Main background video (used by default)
- `dashboard-bg.mp4` - Dashboard background
- `hero-bg.mp4` - Hero section background

## Free Video Resources

- **Pexels Videos**: https://www.pexels.com/videos/
- **Pixabay Videos**: https://pixabay.com/videos/
- **Coverr**: https://coverr.co/
- **Videvo**: https://www.videvo.net/

## Usage

The VideoBackground component will automatically:
- Loop the video
- Apply transparency (opacity)
- Fall back to animated gradient if video fails to load
- Optimize for performance

## Example

```jsx
<VideoBackground 
  src="/videos/background.mp4" 
  opacity={0.25}
/>
```

