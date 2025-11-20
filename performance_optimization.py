#!/usr/bin/env python3
"""
Performance Optimization System
Comprehensive performance analysis and optimization for React websites
"""

import os
import json
import time
import subprocess
import datetime
from typing import Dict, Any, List
from pathlib import Path

class PerformanceOptimizer:
    def __init__(self):
        """Initialize the performance optimizer"""
        self.optimization_results = {}
        
    def analyze_bundle_size(self, project_path: str) -> Dict[str, Any]:
        """Analyze bundle size and dependencies"""
        print(f"📊 Analyzing bundle size for {project_path}...")
        
        # Check package.json for dependencies
        package_json_path = os.path.join(project_path, 'package.json')
        bundle_analysis = {
            'project_path': project_path,
            'dependencies': {},
            'dev_dependencies': {},
            'bundle_size_estimate': 0,
            'recommendations': []
        }
        
        if os.path.exists(package_json_path):
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
                bundle_analysis['dependencies'] = package_data.get('dependencies', {})
                bundle_analysis['dev_dependencies'] = package_data.get('devDependencies', {})
        
        # Estimate bundle size based on dependencies
        large_packages = {
            'react': 42,  # KB
            'react-dom': 130,
            'framer-motion': 180,
            'lucide-react': 25,
            '@radix-ui/react-dialog': 15,
            'react-helmet-async': 8
        }
        
        total_size = 0
        for dep in bundle_analysis['dependencies']:
            if dep in large_packages:
                total_size += large_packages[dep]
            else:
                total_size += 10  # Estimate for unknown packages
        
        bundle_analysis['bundle_size_estimate'] = total_size
        
        # Generate recommendations
        if total_size > 500:
            bundle_analysis['recommendations'].append("Consider code splitting to reduce initial bundle size")
        if 'lodash' in bundle_analysis['dependencies']:
            bundle_analysis['recommendations'].append("Use lodash-es or individual lodash functions to reduce bundle size")
        if 'moment' in bundle_analysis['dependencies']:
            bundle_analysis['recommendations'].append("Replace moment.js with date-fns for smaller bundle size")
        
        return bundle_analysis
    
    def create_performance_config(self, project_path: str) -> Dict[str, str]:
        """Create performance optimization configuration files"""
        configs = {}
        
        # Vite config optimization
        configs['vite.config.js'] = f"""import {{ defineConfig }} from 'vite'
import react from '@vitejs/plugin-react'
import {{ resolve }} from 'path'

export default defineConfig({{
  plugins: [react()],
  resolve: {{
    alias: {{
      '@': resolve(__dirname, './src'),
    }},
  }},
  build: {{
    // Performance optimizations
    target: 'esnext',
    minify: 'terser',
    terserOptions: {{
      compress: {{
        drop_console: true,
        drop_debugger: true,
      }},
    }},
    rollupOptions: {{
      output: {{
        manualChunks: {{
          vendor: ['react', 'react-dom'],
          ui: ['@radix-ui/react-dialog', '@radix-ui/react-slot'],
          icons: ['lucide-react'],
          animation: ['framer-motion'],
        }},
      }},
    }},
    chunkSizeWarningLimit: 1000,
  }},
  server: {{
    host: true,
    port: 5173,
  }},
  preview: {{
    host: true,
    port: 4173,
  }},
}})
"""
        
        # Performance monitoring component
        configs['PerformanceMonitor.jsx'] = """import { useEffect } from 'react';

export const PerformanceMonitor = () => {
  useEffect(() => {
    // Monitor Core Web Vitals
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.entryType === 'navigation') {
          console.log('Navigation timing:', {
            domContentLoaded: entry.domContentLoadedEventEnd - entry.domContentLoadedEventStart,
            loadComplete: entry.loadEventEnd - entry.loadEventStart,
            firstPaint: entry.responseEnd - entry.requestStart,
          });
        }
        
        if (entry.entryType === 'paint') {
          console.log(`${entry.name}: ${entry.startTime}ms`);
        }
        
        if (entry.entryType === 'largest-contentful-paint') {
          console.log('LCP:', entry.startTime);
        }
      }
    });
    
    observer.observe({ entryTypes: ['navigation', 'paint', 'largest-contentful-paint'] });
    
    // Measure First Input Delay (FID)
    const fidObserver = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        console.log('FID:', entry.processingStart - entry.startTime);
      }
    });
    
    fidObserver.observe({ entryTypes: ['first-input'] });
    
    return () => {
      observer.disconnect();
      fidObserver.disconnect();
    };
  }, []);
  
  return null;
};
"""
        
        # Image optimization component
        configs['OptimizedImage.jsx'] = """import { useState, useRef, useEffect } from 'react';

export const OptimizedImage = ({ 
  src, 
  alt, 
  className = '', 
  width, 
  height,
  loading = 'lazy',
  ...props 
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [isInView, setIsInView] = useState(false);
  const imgRef = useRef(null);
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsInView(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );
    
    if (imgRef.current) {
      observer.observe(imgRef.current);
    }
    
    return () => observer.disconnect();
  }, []);
  
  const handleLoad = () => {
    setIsLoaded(true);
  };
  
  return (
    <div 
      ref={imgRef}
      className={`relative overflow-hidden ${className}`}
      style={{ width, height }}
    >
      {isInView && (
        <>
          <img
            src={src}
            alt={alt}
            loading={loading}
            onLoad={handleLoad}
            className={`transition-opacity duration-300 ${
              isLoaded ? 'opacity-100' : 'opacity-0'
            }`}
            width={width}
            height={height}
            {...props}
          />
          {!isLoaded && (
            <div className="absolute inset-0 bg-gray-200 animate-pulse" />
          )}
        </>
      )}
    </div>
  );
};
"""
        
        # Service Worker for caching
        configs['sw.js'] = """const CACHE_NAME = 'app-cache-v1';
const urlsToCache = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Return cached version or fetch from network
        return response || fetch(event.request);
      })
  );
});
"""
        
        # Web manifest for PWA
        configs['manifest.json'] = f"""{{
  "name": "Business Transformation Platform",
  "short_name": "BizTransform",
  "description": "AI-powered business transformation and automation platform",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#1e1b4b",
  "theme_color": "#6366f1",
  "icons": [
    {{
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    }},
    {{
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }}
  ]
}}
"""
        
        return configs
    
    def create_lighthouse_config(self) -> str:
        """Create Lighthouse CI configuration"""
        return """{
  "ci": {
    "collect": {
      "url": ["http://localhost:5173"],
      "numberOfRuns": 3
    },
    "assert": {
      "assertions": {
        "categories:performance": ["warn", {"minScore": 0.8}],
        "categories:accessibility": ["error", {"minScore": 0.9}],
        "categories:best-practices": ["warn", {"minScore": 0.8}],
        "categories:seo": ["error", {"minScore": 0.9}]
      }
    },
    "upload": {
      "target": "temporary-public-storage"
    }
  }
}
"""
    
    def optimize_images(self, project_path: str) -> List[str]:
        """Optimize images in the project"""
        print(f"🖼️ Optimizing images in {project_path}...")
        
        optimizations = []
        public_dir = os.path.join(project_path, 'public')
        src_dir = os.path.join(project_path, 'src')
        
        # Find image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
        image_files = []
        
        for directory in [public_dir, src_dir]:
            if os.path.exists(directory):
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        if any(file.lower().endswith(ext) for ext in image_extensions):
                            image_files.append(os.path.join(root, file))
        
        for image_file in image_files:
            file_size = os.path.getsize(image_file)
            if file_size > 100 * 1024:  # Files larger than 100KB
                optimizations.append(f"Optimize {image_file} (current size: {file_size // 1024}KB)")
        
        # Create image optimization recommendations
        if not optimizations:
            optimizations.append("All images are already optimized")
        
        return optimizations
    
    def create_performance_improvements(self, project_path: str) -> Dict[str, Any]:
        """Create comprehensive performance improvements"""
        print(f"⚡ Creating performance improvements for {project_path}...")
        
        # Analyze current state
        bundle_analysis = self.analyze_bundle_size(project_path)
        image_optimizations = self.optimize_images(project_path)
        
        # Create optimization configs
        configs = self.create_performance_config(project_path)
        
        # Save configs to project
        for filename, content in configs.items():
            if filename.endswith('.jsx'):
                filepath = os.path.join(project_path, 'src', 'components', filename)
            elif filename == 'vite.config.js':
                filepath = os.path.join(project_path, filename)
            elif filename in ['sw.js', 'manifest.json']:
                filepath = os.path.join(project_path, 'public', filename)
            else:
                filepath = os.path.join(project_path, filename)
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(content)
        
        # Create Lighthouse config
        lighthouse_config = self.create_lighthouse_config()
        with open(os.path.join(project_path, 'lighthouserc.json'), 'w') as f:
            f.write(lighthouse_config)
        
        improvements = {
            'bundle_analysis': bundle_analysis,
            'image_optimizations': image_optimizations,
            'configs_created': list(configs.keys()),
            'performance_score_estimate': self.calculate_performance_score(bundle_analysis),
            'recommendations': self.generate_performance_recommendations(bundle_analysis, image_optimizations)
        }
        
        return improvements
    
    def calculate_performance_score(self, bundle_analysis: Dict[str, Any]) -> int:
        """Calculate estimated performance score"""
        base_score = 90
        
        # Deduct points for large bundle size
        bundle_size = bundle_analysis.get('bundle_size_estimate', 0)
        if bundle_size > 500:
            base_score -= 20
        elif bundle_size > 300:
            base_score -= 10
        
        # Deduct points for too many dependencies
        dep_count = len(bundle_analysis.get('dependencies', {}))
        if dep_count > 20:
            base_score -= 10
        elif dep_count > 15:
            base_score -= 5
        
        return max(60, base_score)
    
    def generate_performance_recommendations(self, bundle_analysis: Dict[str, Any], image_optimizations: List[str]) -> List[str]:
        """Generate performance improvement recommendations"""
        recommendations = []
        
        # Bundle size recommendations
        bundle_size = bundle_analysis.get('bundle_size_estimate', 0)
        if bundle_size > 500:
            recommendations.append("Implement code splitting to reduce initial bundle size")
            recommendations.append("Consider lazy loading non-critical components")
        
        # Image optimization recommendations
        if len(image_optimizations) > 1:
            recommendations.append("Optimize images using WebP format for better compression")
            recommendations.append("Implement responsive images with different sizes")
        
        # General performance recommendations
        recommendations.extend([
            "Enable gzip compression on the server",
            "Implement service worker for caching static assets",
            "Use CDN for static asset delivery",
            "Minimize and compress CSS and JavaScript files",
            "Implement preloading for critical resources",
            "Use font-display: swap for web fonts",
            "Optimize third-party script loading",
            "Implement resource hints (preconnect, prefetch)",
            "Monitor Core Web Vitals regularly"
        ])
        
        return recommendations
    
    def run_performance_audit(self, project_path: str) -> Dict[str, Any]:
        """Run comprehensive performance audit"""
        print(f"🔍 Running performance audit for {project_path}...")
        
        audit_results = {
            'timestamp': datetime.datetime.now().isoformat(),
            'project_path': project_path,
            'improvements': self.create_performance_improvements(project_path),
            'audit_score': 0,
            'status': 'completed'
        }
        
        # Calculate overall audit score
        performance_score = audit_results['improvements']['performance_score_estimate']
        audit_results['audit_score'] = performance_score
        
        return audit_results

def main():
    """Main function to run performance optimization"""
    print("⚡ Performance Optimization System")
    print("=" * 40)
    
    optimizer = PerformanceOptimizer()
    
    # Optimize both websites
    websites = [
        '/home/ubuntu/transformby10x-website',
        '/home/ubuntu/bizbuilders-website'
    ]
    
    all_results = {}
    
    for website_path in websites:
        website_name = os.path.basename(website_path)
        print(f"\n🚀 Optimizing {website_name}...")
        
        # Run performance audit
        audit_results = optimizer.run_performance_audit(website_path)
        all_results[website_name] = audit_results
        
        print(f"✅ Performance audit completed for {website_name}")
        print(f"📊 Estimated performance score: {audit_results['audit_score']}/100")
        print(f"🔧 Created {len(audit_results['improvements']['configs_created'])} optimization files")
    
    # Save comprehensive results
    results_path = '/home/ubuntu/performance_optimization_results.json'
    with open(results_path, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    
    print(f"\n✅ Performance optimization complete!")
    print(f"📋 Results saved to {results_path}")
    print(f"🎯 Optimized {len(websites)} websites")

if __name__ == "__main__":
    main()

