#!/bin/bash

# Setup script to organize video and image files for Anaconda Brows quiz page

echo "═══════════════════════════════════════════════════"
echo "   📹 Anaconda Brows - Video & Image Setup"
echo "═══════════════════════════════════════════════════"
echo ""

# Create videos folder if it doesn't exist
mkdir -p videos

# Find files in Downloads folder
DOWNLOADS="$HOME/Downloads"

echo "🔍 Looking for files in Downloads folder..."
echo ""

# Function to find and copy files
find_and_copy() {
    local pattern=$1
    local dest_name=$2
    local found=$(find "$DOWNLOADS" -maxdepth 1 -type f -iname "$pattern" 2>/dev/null | head -1)
    
    if [ -n "$found" ]; then
        echo "✅ Found: $(basename "$found")"
        cp "$found" "videos/$dest_name"
        echo "   → Copied to: videos/$dest_name"
        return 0
    else
        echo "❌ Not found: $pattern"
        return 1
    fi
}

# Look for video files
echo "📹 Video Files:"
find_and_copy "*background-1*" "background-1.MP4"
find_and_copy "*background-2*" "background-2.mp4"
find_and_copy "*hero-intro*" "hero-intro.MP4"
find_and_copy "*AB_book*" "AB_book-now-video.mp4"
echo ""

# Look for logo
echo "🖼️  Logo File:"
find_and_copy "*adda*logo*" "adda-brow-logo.png"
find_and_copy "*logo*" "adda-brow-logo.png"
echo ""

# Look for office images
echo "🏢 Office Images:"
for i in {1..6}; do
    # Try various patterns
    found=""
    for pattern in "*office*$i*" "*Office*$i*" "*AB_Office*$i*" "*AB*Office*$i*"; do
        result=$(find "$DOWNLOADS" -maxdepth 1 -type f -iname "$pattern" 2>/dev/null | head -1)
        if [ -n "$result" ]; then
            found="$result"
            break
        fi
    done
    
    if [ -n "$found" ]; then
        ext="${found##*.}"
        echo "✅ Found: $(basename "$found")"
        cp "$found" "videos/AB_Office_$i.$ext"
        echo "   → Copied to: videos/AB_Office_$i.$ext"
    else
        echo "❌ Not found: AB_Office_$i (pattern)"
    fi
done
echo ""

# Summary
echo "═══════════════════════════════════════════════════"
echo "   📋 Files in videos/ folder:"
echo "═══════════════════════════════════════════════════"
ls -lh videos/ 2>/dev/null || echo "   (videos folder is empty)"
echo ""

echo "✅ Setup complete!"
echo ""
echo "🌐 View your page: http://localhost:8080/brows-quiz.html"

