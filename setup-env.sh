#!/bin/bash

echo "🔐 Vercel Environment Variable Setup"
echo "===================================="
echo ""
echo "We need your Supabase Project ID to set up the Voice Agent widget."
echo ""
echo "📋 How to get your Supabase Project ID:"
echo "   1. Go to: https://supabase.com/dashboard"
echo "   2. Select your project (or create one)"
echo "   3. Go to Settings → General"
echo "   4. Find 'Reference ID' - that's your Project ID"
echo "   OR"
echo "   Look at your Supabase URL: https://YOUR_PROJECT_ID.supabase.co"
echo ""
echo "===================================="
echo ""

read -p "Enter your Supabase Project ID: " SUPABASE_PROJECT_ID

if [ -z "$SUPABASE_PROJECT_ID" ]; then
    echo "❌ Error: Project ID cannot be empty!"
    exit 1
fi

echo ""
echo "Setting environment variable for all environments..."
echo ""

# Set for all environments
npx vercel env add VITE_SUPABASE_PROJECT_ID production preview development <<EOF
$SUPABASE_PROJECT_ID
EOF

echo ""
echo "✅ Environment variable set!"
echo ""
echo "Next step: Redeploy your site..."
echo ""
read -p "Redeploy to production now? (y/n): " REDEPLOY

if [ "$REDEPLOY" = "y" ] || [ "$REDEPLOY" = "Y" ]; then
    echo "Redeploying to production..."
    npx vercel --prod --yes
    echo ""
    echo "✅ Deployment complete!"
    echo ""
    echo "🎉 Your Voice Agent widget should now work!"
    echo "Visit: https://bizbuilders-automation-s4kxnfv9w-erik-bizbuilders-projects.vercel.app"
else
    echo ""
    echo "To redeploy later, run:"
    echo "  npx vercel --prod"
fi

