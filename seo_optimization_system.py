#!/usr/bin/env python3
"""
SEO Optimization System
Comprehensive SEO analysis and optimization for transformby10x.ai and bizbuilders.ai
"""

import sys
import json
import requests
import time
import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import re
from urllib.parse import urljoin, urlparse
import sqlite3

@dataclass
class SEOAnalysis:
    """Data class for SEO analysis results"""
    url: str
    title: str
    meta_description: str
    h1_tags: List[str]
    h2_tags: List[str]
    images_without_alt: int
    internal_links: int
    external_links: int
    page_load_time: float
    mobile_friendly: bool
    https_enabled: bool
    structured_data: bool
    keywords: List[str]
    content_length: int
    readability_score: float
    seo_score: float
    recommendations: List[str]

class SEOOptimizationSystem:
    def __init__(self, db_path: str = "/home/ubuntu/seo_analysis.db"):
        """Initialize the SEO optimization system"""
        self.db_path = db_path
        self.init_database()
        
        # SEO best practices and guidelines
        self.seo_guidelines = {
            'title_length': {'min': 30, 'max': 60},
            'meta_description_length': {'min': 120, 'max': 160},
            'h1_count': {'min': 1, 'max': 1},
            'content_length': {'min': 300, 'max': 2000},
            'keyword_density': {'min': 0.5, 'max': 3.0},
            'page_load_time': {'max': 3.0},
            'internal_links': {'min': 3, 'max': 100}
        }
        
        # Target keywords for each website
        self.target_keywords = {
            'transformby10x': [
                'AI transformation', 'business automation', '10x growth',
                'AI business tools', 'digital transformation', 'business scaling',
                'automation strategy', 'AI productivity', 'business optimization',
                'exponential growth', 'AI-powered business', 'transformation consulting'
            ],
            'bizbuilders': [
                'business building', 'entrepreneur tools', 'startup automation',
                'business builder', 'entrepreneurship platform', 'business creation',
                'startup tools', 'business automation', 'entrepreneur AI',
                'business development', 'startup growth', 'business empire'
            ]
        }
        
    def init_database(self):
        """Initialize SQLite database for SEO analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS seo_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                title TEXT,
                meta_description TEXT,
                h1_count INTEGER,
                h2_count INTEGER,
                images_without_alt INTEGER,
                internal_links INTEGER,
                external_links INTEGER,
                page_load_time REAL,
                mobile_friendly BOOLEAN,
                https_enabled BOOLEAN,
                structured_data BOOLEAN,
                content_length INTEGER,
                readability_score REAL,
                seo_score REAL,
                timestamp DATETIME,
                recommendations TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keyword_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                keyword TEXT,
                density REAL,
                position INTEGER,
                search_volume INTEGER,
                difficulty REAL,
                timestamp DATETIME
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS technical_seo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                robots_txt BOOLEAN,
                sitemap_xml BOOLEAN,
                canonical_tags BOOLEAN,
                meta_robots BOOLEAN,
                schema_markup BOOLEAN,
                open_graph BOOLEAN,
                twitter_cards BOOLEAN,
                ssl_certificate BOOLEAN,
                timestamp DATETIME
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def analyze_page_content(self, html_content: str, url: str) -> Dict[str, Any]:
        """Analyze HTML content for SEO factors"""
        from bs4 import BeautifulSoup
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
        except:
            # Fallback if BeautifulSoup is not available
            return self.analyze_content_regex(html_content, url)
        
        analysis = {
            'title': '',
            'meta_description': '',
            'h1_tags': [],
            'h2_tags': [],
            'images_without_alt': 0,
            'internal_links': 0,
            'external_links': 0,
            'content_length': 0,
            'structured_data': False,
            'canonical_url': '',
            'meta_robots': '',
            'open_graph': False,
            'twitter_cards': False
        }
        
        # Title analysis
        title_tag = soup.find('title')
        if title_tag:
            analysis['title'] = title_tag.get_text().strip()
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            analysis['meta_description'] = meta_desc.get('content', '').strip()
        
        # Heading tags
        h1_tags = soup.find_all('h1')
        analysis['h1_tags'] = [h1.get_text().strip() for h1 in h1_tags]
        
        h2_tags = soup.find_all('h2')
        analysis['h2_tags'] = [h2.get_text().strip() for h2 in h2_tags]
        
        # Image analysis
        images = soup.find_all('img')
        analysis['images_without_alt'] = len([img for img in images if not img.get('alt')])
        
        # Link analysis
        links = soup.find_all('a', href=True)
        domain = urlparse(url).netloc
        
        for link in links:
            href = link['href']
            if href.startswith('http'):
                if domain in href:
                    analysis['internal_links'] += 1
                else:
                    analysis['external_links'] += 1
            elif href.startswith('/') or not href.startswith('#'):
                analysis['internal_links'] += 1
        
        # Content length
        body = soup.find('body')
        if body:
            text_content = body.get_text()
            analysis['content_length'] = len(text_content.strip())
        
        # Structured data
        json_ld = soup.find('script', type='application/ld+json')
        analysis['structured_data'] = json_ld is not None
        
        # Canonical URL
        canonical = soup.find('link', rel='canonical')
        if canonical:
            analysis['canonical_url'] = canonical.get('href', '')
        
        # Meta robots
        meta_robots = soup.find('meta', attrs={'name': 'robots'})
        if meta_robots:
            analysis['meta_robots'] = meta_robots.get('content', '')
        
        # Open Graph
        og_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))
        analysis['open_graph'] = len(og_tags) > 0
        
        # Twitter Cards
        twitter_tags = soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('twitter:')})
        analysis['twitter_cards'] = len(twitter_tags) > 0
        
        return analysis
    
    def analyze_content_regex(self, html_content: str, url: str) -> Dict[str, Any]:
        """Fallback content analysis using regex"""
        analysis = {
            'title': '',
            'meta_description': '',
            'h1_tags': [],
            'h2_tags': [],
            'images_without_alt': 0,
            'internal_links': 0,
            'external_links': 0,
            'content_length': len(html_content),
            'structured_data': False,
            'canonical_url': '',
            'meta_robots': '',
            'open_graph': False,
            'twitter_cards': False
        }
        
        # Title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
        if title_match:
            analysis['title'] = title_match.group(1).strip()
        
        # Meta description
        meta_desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', html_content, re.IGNORECASE)
        if meta_desc_match:
            analysis['meta_description'] = meta_desc_match.group(1).strip()
        
        # H1 tags
        h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', html_content, re.IGNORECASE | re.DOTALL)
        analysis['h1_tags'] = [re.sub(r'<[^>]+>', '', h1).strip() for h1 in h1_matches]
        
        # H2 tags
        h2_matches = re.findall(r'<h2[^>]*>(.*?)</h2>', html_content, re.IGNORECASE | re.DOTALL)
        analysis['h2_tags'] = [re.sub(r'<[^>]+>', '', h2).strip() for h2 in h2_matches]
        
        # Images without alt
        img_matches = re.findall(r'<img[^>]*>', html_content, re.IGNORECASE)
        analysis['images_without_alt'] = len([img for img in img_matches if 'alt=' not in img.lower()])
        
        # Structured data
        analysis['structured_data'] = 'application/ld+json' in html_content
        
        # Open Graph
        analysis['open_graph'] = 'property="og:' in html_content
        
        # Twitter Cards
        analysis['twitter_cards'] = 'name="twitter:' in html_content
        
        return analysis
    
    def calculate_keyword_density(self, content: str, keywords: List[str]) -> Dict[str, float]:
        """Calculate keyword density for target keywords"""
        content_lower = content.lower()
        word_count = len(content_lower.split())
        
        keyword_densities = {}
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            keyword_count = content_lower.count(keyword_lower)
            density = (keyword_count / max(word_count, 1)) * 100
            keyword_densities[keyword] = density
        
        return keyword_densities
    
    def calculate_readability_score(self, content: str) -> float:
        """Calculate readability score (simplified Flesch Reading Ease)"""
        sentences = len(re.split(r'[.!?]+', content))
        words = len(content.split())
        syllables = self.count_syllables(content)
        
        if sentences == 0 or words == 0:
            return 0.0
        
        # Simplified Flesch Reading Ease formula
        score = 206.835 - (1.015 * (words / sentences)) - (84.6 * (syllables / words))
        return max(0, min(100, score))
    
    def count_syllables(self, text: str) -> int:
        """Count syllables in text (simplified)"""
        vowels = 'aeiouy'
        syllable_count = 0
        words = re.findall(r'\b\w+\b', text.lower())
        
        for word in words:
            word_syllables = 0
            prev_was_vowel = False
            
            for char in word:
                if char in vowels:
                    if not prev_was_vowel:
                        word_syllables += 1
                    prev_was_vowel = True
                else:
                    prev_was_vowel = False
            
            # Handle silent e
            if word.endswith('e') and word_syllables > 1:
                word_syllables -= 1
            
            # Ensure at least one syllable per word
            syllable_count += max(1, word_syllables)
        
        return syllable_count
    
    def calculate_seo_score(self, analysis: Dict[str, Any], keywords: List[str]) -> float:
        """Calculate overall SEO score based on various factors"""
        score = 0
        max_score = 100
        
        # Title optimization (20 points)
        title = analysis.get('title', '')
        if len(title) >= self.seo_guidelines['title_length']['min'] and len(title) <= self.seo_guidelines['title_length']['max']:
            score += 10
        if any(keyword.lower() in title.lower() for keyword in keywords):
            score += 10
        
        # Meta description (15 points)
        meta_desc = analysis.get('meta_description', '')
        if len(meta_desc) >= self.seo_guidelines['meta_description_length']['min'] and len(meta_desc) <= self.seo_guidelines['meta_description_length']['max']:
            score += 8
        if any(keyword.lower() in meta_desc.lower() for keyword in keywords):
            score += 7
        
        # Heading structure (15 points)
        h1_count = len(analysis.get('h1_tags', []))
        if h1_count == 1:
            score += 8
        if h1_count > 0 and any(keyword.lower() in h1.lower() for h1 in analysis.get('h1_tags', []) for keyword in keywords):
            score += 7
        
        # Content quality (20 points)
        content_length = analysis.get('content_length', 0)
        if content_length >= self.seo_guidelines['content_length']['min']:
            score += 10
        
        readability = analysis.get('readability_score', 0)
        if readability >= 60:  # Good readability
            score += 10
        
        # Technical SEO (15 points)
        if analysis.get('structured_data', False):
            score += 5
        if analysis.get('open_graph', False):
            score += 5
        if analysis.get('twitter_cards', False):
            score += 5
        
        # Images and accessibility (10 points)
        images_without_alt = analysis.get('images_without_alt', 0)
        if images_without_alt == 0:
            score += 10
        elif images_without_alt <= 2:
            score += 5
        
        # Internal linking (5 points)
        internal_links = analysis.get('internal_links', 0)
        if internal_links >= self.seo_guidelines['internal_links']['min']:
            score += 5
        
        return min(score, max_score)
    
    def generate_seo_recommendations(self, analysis: Dict[str, Any], keywords: List[str]) -> List[str]:
        """Generate SEO improvement recommendations"""
        recommendations = []
        
        # Title recommendations
        title = analysis.get('title', '')
        if len(title) < self.seo_guidelines['title_length']['min']:
            recommendations.append(f"Expand title to at least {self.seo_guidelines['title_length']['min']} characters")
        elif len(title) > self.seo_guidelines['title_length']['max']:
            recommendations.append(f"Shorten title to under {self.seo_guidelines['title_length']['max']} characters")
        
        if not any(keyword.lower() in title.lower() for keyword in keywords):
            recommendations.append("Include target keywords in the title tag")
        
        # Meta description recommendations
        meta_desc = analysis.get('meta_description', '')
        if len(meta_desc) < self.seo_guidelines['meta_description_length']['min']:
            recommendations.append(f"Expand meta description to at least {self.seo_guidelines['meta_description_length']['min']} characters")
        elif len(meta_desc) > self.seo_guidelines['meta_description_length']['max']:
            recommendations.append(f"Shorten meta description to under {self.seo_guidelines['meta_description_length']['max']} characters")
        
        if not meta_desc:
            recommendations.append("Add a compelling meta description")
        
        # Heading recommendations
        h1_count = len(analysis.get('h1_tags', []))
        if h1_count == 0:
            recommendations.append("Add an H1 tag to the page")
        elif h1_count > 1:
            recommendations.append("Use only one H1 tag per page")
        
        # Content recommendations
        content_length = analysis.get('content_length', 0)
        if content_length < self.seo_guidelines['content_length']['min']:
            recommendations.append(f"Increase content length to at least {self.seo_guidelines['content_length']['min']} words")
        
        # Technical SEO recommendations
        if not analysis.get('structured_data', False):
            recommendations.append("Add structured data (JSON-LD) for better search engine understanding")
        
        if not analysis.get('open_graph', False):
            recommendations.append("Add Open Graph meta tags for better social media sharing")
        
        if not analysis.get('twitter_cards', False):
            recommendations.append("Add Twitter Card meta tags for enhanced Twitter sharing")
        
        # Image recommendations
        images_without_alt = analysis.get('images_without_alt', 0)
        if images_without_alt > 0:
            recommendations.append(f"Add alt text to {images_without_alt} images for better accessibility")
        
        # Internal linking recommendations
        internal_links = analysis.get('internal_links', 0)
        if internal_links < self.seo_guidelines['internal_links']['min']:
            recommendations.append("Add more internal links to improve site navigation and SEO")
        
        return recommendations
    
    def create_seo_enhancements(self, website_name: str) -> Dict[str, str]:
        """Create SEO enhancement files for a website"""
        keywords = self.target_keywords.get(website_name, [])
        
        enhancements = {}
        
        # Robots.txt
        enhancements['robots.txt'] = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /private/
Disallow: /*.json$

Sitemap: https://{website_name}.ai/sitemap.xml
"""
        
        # Sitemap.xml
        enhancements['sitemap.xml'] = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://{website_name}.ai/</loc>
        <lastmod>{datetime.date.today().isoformat()}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://{website_name}.ai/features</loc>
        <lastmod>{datetime.date.today().isoformat()}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://{website_name}.ai/pricing</loc>
        <lastmod>{datetime.date.today().isoformat()}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://{website_name}.ai/about</loc>
        <lastmod>{datetime.date.today().isoformat()}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
    <url>
        <loc>https://{website_name}.ai/contact</loc>
        <lastmod>{datetime.date.today().isoformat()}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
</urlset>
"""
        
        # Meta tags component
        primary_keyword = keywords[0] if keywords else f"{website_name} platform"
        
        enhancements['meta_tags.jsx'] = f"""// SEO Meta Tags Component for {website_name}
import {{ Helmet }} from 'react-helmet-async';

export const SEOMetaTags = ({{ 
  title = "{website_name.title()} - {primary_keyword.title()}",
  description = "Transform your business with {primary_keyword}. Join thousands of successful entrepreneurs.",
  keywords = "{', '.join(keywords[:10])}",
  url = "https://{website_name}.ai",
  image = "https://{website_name}.ai/og-image.jpg"
}}) => {{
  return (
    <Helmet>
      {{/* Basic Meta Tags */}}
      <title>{{title}}</title>
      <meta name="description" content={{description}} />
      <meta name="keywords" content={{keywords}} />
      <meta name="robots" content="index, follow" />
      <meta name="author" content="{website_name.title()}" />
      <link rel="canonical" href={{url}} />
      
      {{/* Open Graph Meta Tags */}}
      <meta property="og:type" content="website" />
      <meta property="og:title" content={{title}} />
      <meta property="og:description" content={{description}} />
      <meta property="og:url" content={{url}} />
      <meta property="og:image" content={{image}} />
      <meta property="og:site_name" content="{website_name.title()}" />
      
      {{/* Twitter Card Meta Tags */}}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={{title}} />
      <meta name="twitter:description" content={{description}} />
      <meta name="twitter:image" content={{image}} />
      
      {{/* Additional SEO Meta Tags */}}
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta httpEquiv="Content-Type" content="text/html; charset=utf-8" />
      <meta name="language" content="English" />
      <meta name="revisit-after" content="7 days" />
    </Helmet>
  );
}};
"""
        
        # Structured data component
        enhancements['structured_data.jsx'] = f"""// Structured Data Component for {website_name}
import {{ Helmet }} from 'react-helmet-async';

export const StructuredData = () => {{
  const organizationSchema = {{
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "{website_name.title()}",
    "url": "https://{website_name}.ai",
    "logo": "https://{website_name}.ai/logo.png",
    "description": "Leading {primary_keyword} platform for entrepreneurs and businesses",
    "sameAs": [
      "https://twitter.com/{website_name}",
      "https://linkedin.com/company/{website_name}",
      "https://facebook.com/{website_name}"
    ],
    "contactPoint": {{
      "@type": "ContactPoint",
      "telephone": "+1-555-0123",
      "contactType": "customer service",
      "availableLanguage": "English"
    }}
  }};
  
  const websiteSchema = {{
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "{website_name.title()}",
    "url": "https://{website_name}.ai",
    "description": "Transform your business with {primary_keyword}",
    "potentialAction": {{
      "@type": "SearchAction",
      "target": "https://{website_name}.ai/search?q={{search_term_string}}",
      "query-input": "required name=search_term_string"
    }}
  }};
  
  const serviceSchema = {{
    "@context": "https://schema.org",
    "@type": "Service",
    "name": "{primary_keyword.title()} Services",
    "description": "Comprehensive {primary_keyword} solutions for businesses",
    "provider": {{
      "@type": "Organization",
      "name": "{website_name.title()}"
    }},
    "serviceType": "{primary_keyword}",
    "areaServed": "Worldwide"
  }};
  
  return (
    <Helmet>
      <script type="application/ld+json">
        {{JSON.stringify(organizationSchema)}}
      </script>
      <script type="application/ld+json">
        {{JSON.stringify(websiteSchema)}}
      </script>
      <script type="application/ld+json">
        {{JSON.stringify(serviceSchema)}}
      </script>
    </Helmet>
  );
}};
"""
        
        return enhancements
    
    def save_seo_analysis(self, analysis: SEOAnalysis):
        """Save SEO analysis to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO seo_analysis 
            (url, title, meta_description, h1_count, h2_count, images_without_alt,
             internal_links, external_links, page_load_time, mobile_friendly,
             https_enabled, structured_data, content_length, readability_score,
             seo_score, timestamp, recommendations)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            analysis.url, analysis.title, analysis.meta_description,
            len(analysis.h1_tags), len(analysis.h2_tags), analysis.images_without_alt,
            analysis.internal_links, analysis.external_links, analysis.page_load_time,
            analysis.mobile_friendly, analysis.https_enabled, analysis.structured_data,
            analysis.content_length, analysis.readability_score, analysis.seo_score,
            datetime.datetime.now(), json.dumps(analysis.recommendations)
        ))
        
        conn.commit()
        conn.close()
    
    def generate_seo_report(self, website_name: str) -> Dict[str, Any]:
        """Generate comprehensive SEO report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get latest analysis
        cursor.execute('''
            SELECT * FROM seo_analysis 
            WHERE url LIKE ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        ''', (f'%{website_name}%',))
        
        latest_analysis = cursor.fetchone()
        
        # Get historical data
        cursor.execute('''
            SELECT seo_score, timestamp FROM seo_analysis 
            WHERE url LIKE ? 
            ORDER BY timestamp DESC 
            LIMIT 10
        ''', (f'%{website_name}%',))
        
        historical_scores = cursor.fetchall()
        
        conn.close()
        
        report = {
            'website': website_name,
            'timestamp': datetime.datetime.now().isoformat(),
            'current_analysis': latest_analysis,
            'historical_scores': historical_scores,
            'target_keywords': self.target_keywords.get(website_name, []),
            'seo_enhancements': self.create_seo_enhancements(website_name)
        }
        
        return report

def main():
    """Main function to run SEO optimization system"""
    print("🔍 SEO Optimization System")
    print("=" * 40)
    
    # Initialize the SEO system
    seo_system = SEOOptimizationSystem()
    
    # Generate SEO enhancements for both websites
    websites = ['transformby10x', 'bizbuilders']
    
    for website in websites:
        print(f"\n📊 Generating SEO enhancements for {website}...")
        
        # Create SEO enhancements
        enhancements = seo_system.create_seo_enhancements(website)
        
        # Save enhancements to files
        website_dir = f"/home/ubuntu/{website}_seo_enhancements"
        import os
        os.makedirs(website_dir, exist_ok=True)
        
        for filename, content in enhancements.items():
            filepath = os.path.join(website_dir, filename)
            with open(filepath, 'w') as f:
                f.write(content)
        
        print(f"✅ SEO enhancements saved to {website_dir}")
        
        # Generate SEO report
        report = seo_system.generate_seo_report(website)
        
        # Save report
        report_path = f"/home/ubuntu/{website}_seo_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"📋 SEO report saved to {report_path}")
    
    print(f"\n✅ SEO optimization complete!")
    print(f"📈 Generated enhancements for {len(websites)} websites")
    print(f"🎯 Target keywords configured for optimal ranking")

if __name__ == "__main__":
    main()

