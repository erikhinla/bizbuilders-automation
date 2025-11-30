// SEO Meta Tags Component for transformby10x
import { Helmet } from 'react-helmet-async';

export const SEOMetaTags = ({ 
  title = "Transformby10X - Ai Transformation",
  description = "Transform your business with AI transformation. Join thousands of successful entrepreneurs.",
  keywords = "AI transformation, business automation, 10x growth, AI business tools, digital transformation, business scaling, automation strategy, AI productivity, business optimization, exponential growth",
  url = "https://transformby10x.ai",
  image = "https://transformby10x.ai/og-image.jpg"
}) => {
  return (
    <Helmet>
      {/* Basic Meta Tags */}
      <title>{title}</title>
      <meta name="description" content={description} />
      <meta name="keywords" content={keywords} />
      <meta name="robots" content="index, follow" />
      <meta name="author" content="Transformby10X" />
      <link rel="canonical" href={url} />
      
      {/* Open Graph / Facebook */}
      <meta property="og:type" content="website" />
      <meta property="og:url" content={url} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={image} />
      
      {/* Twitter */}
      <meta property="twitter:card" content="summary_large_image" />
      <meta property="twitter:url" content={url} />
      <meta property="twitter:title" content={title} />
      <meta property="twitter:description" content={description} />
      <meta property="twitter:image" content={image} />
    </Helmet>
  );
};
