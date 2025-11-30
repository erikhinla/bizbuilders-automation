import { Helmet } from 'react-helmet-async';

export const StructuredData = () => {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "TransformBy10X",
    "url": "https://transformby10x.ai",
    "logo": "https://transformby10x.ai/logo.png",
    "description": "Scale your business 10X faster with AI-powered automation and proven transformation strategies",
    "sameAs": [
      "https://twitter.com/transformby10x",
      "https://linkedin.com/company/transformby10x"
    ],
    "contactPoint": {
      "@type": "ContactPoint",
      "contactType": "Customer Service",
      "email": "contact@transformby10x.ai"
    }
  };

  return (
    <Helmet>
      <script type="application/ld+json">
        {JSON.stringify(structuredData)}
      </script>
    </Helmet>
  );
};

