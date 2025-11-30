import { useRef, useEffect } from 'react'

export function VideoBackground({ 
  src, 
  opacity = 0.3, 
  className = '',
  loop = true,
  muted = true,
  autoPlay = true
}) {
  const videoRef = useRef(null)

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.play().catch(err => {
        console.log('Video autoplay prevented:', err)
      })
    }
  }, [])

  return (
    <div className={`absolute inset-0 w-full h-full overflow-hidden ${className}`}>
      <video
        ref={videoRef}
        className="absolute inset-0 w-full h-full object-cover"
        style={{ opacity }}
        loop={loop}
        muted={muted}
        autoPlay={autoPlay}
        playsInline
      >
        <source src={src} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      {/* Overlay for better text readability */}
      <div className="absolute inset-0 bg-gradient-to-br from-black/40 via-transparent to-black/40" />
    </div>
  )
}

// Animated gradient background as fallback
export function AnimatedGradientBackground({ className = '' }) {
  return (
    <div className={`absolute inset-0 w-full h-full overflow-hidden ${className}`}>
      <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(120,119,198,0.3),transparent_50%)] animate-pulse" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_80%_20%,rgba(168,85,247,0.2),transparent_50%)] animate-pulse" style={{ animationDelay: '1s' }} />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_80%,rgba(236,72,153,0.2),transparent_50%)] animate-pulse" style={{ animationDelay: '2s' }} />
      </div>
    </div>
  )
}

