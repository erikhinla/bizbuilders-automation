#!/bin/bash

# Auto-setup script to find and organize all video/image files

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VIDEOS_DIR="$PROJECT_DIR/videos"

echo "═══════════════════════════════════════════════════"
echo "   🔧 Auto-Setup: Organizing Video & Image Files"
echo "═══════════════════════════════════════════════════"
echo ""

# Create videos folder
mkdir -p "$VIDEOS_DIR"

# Find files in Downloads
DOWNLOADS="$HOME/Downloads"
DESKTOP="$HOME/Desktop"

echo "🔍 Searching for files..."
echo ""

files_found=0

# Function to copy file with logging
copy_file() {
    local src=$1
    local dest=$2
    if [ -f "$src" ]; then
        cp "$src" "$dest"
        echo "✅ Copied: $(basename "$src") → videos/$(basename "$dest")"
        ((files_found++))
        return 0
    fi
    return 1
}

# Look for logo
echo "🖼️  Logo:"
for loc in "$DOWNLOADS" "$DESKTOP" "$VIDEOS_DIR"; do
    for pattern in "*adda*logo*" "*logo*adda*" "*Anaconda*logo*"; do
        file=$(find "$loc" -maxdepth 1 -type f -iname "$pattern" 2>/dev/null | head -1)
        if [ -n "$file" ] && [ -f "$file" ]; then
            ext="${file##*.}"
            copy_file "$file" "$VIDEOS_DIR/adda-brow-logo.$ext" && break 2
        fi
    done
done

# Look for videos
echo ""
echo "📹 Videos:"
echo "  Background 1:"
for loc in "$DOWNLOADS" "$DESKTOP" "$VIDEOS_DIR"; do
    for pattern in "*background-1*" "*background_1*" "*bg1*"; do
        file=$(find "$loc" -maxdepth 1 -type f \( -iname "$pattern" -o -iname "*.mp4" -o -iname "*.mov" \) 2>/dev/null | head -1)
        if [ -n "$file" ] && [ -f "$file" ]; then
            ext="${file##*.}"
            copy_file "$file" "$VIDEOS_DIR/background-1.$ext" && break 2
        fi
    done
done

echo "  Background 2:"
for loc in "$DOWNLOADS" "$DESKTOP" "$VIDEOS_DIR"; do
    for pattern in "*background-2*" "*background_2*" "*bg2*"; do
        file=$(find "$loc" -maxdepth 1 -type f \( -iname "$pattern" -o -iname "*.mp4" -o -iname "*.mov" \) 2>/dev/null | head -1)
        if [ -n "$file" ] && [ -f "$file" ]; then
            ext="${file##*.}"
            copy_file "$file" "$VIDEOS_DIR/background-2.$ext" && break 2
        fi
    done
done

# Look for office images/videos
echo ""
echo "🏢 Office Images:"
office_file=$(find "$DOWNLOADS" "$DESKTOP" -maxdepth 1 -type f -iname "*office*" 2>/dev/null | head -1)
if [ -n "$office_file" ] && [ -f "$office_file" ]; then
    ext="${office_file##*.}"
    echo "✅ Found office file: $(basename "$office_file")"
    # Copy to all 6 office slots (they can use same image or we'll handle multiple later)
    for i in {1..6}; do
        cp "$office_file" "$VIDEOS_DIR/AB_Office_$i.$ext"
        echo "   → Created: AB_Office_$i.$ext"
        ((files_found++))
    done
else
    echo "⚠️  No office images found - will use fallback backgrounds"
fi

# Summary
echo ""
echo "═══════════════════════════════════════════════════"
echo "   📋 Files in videos/ folder:"
echo "═══════════════════════════════════════════════════"
ls -lh "$VIDEOS_DIR/" 2>/dev/null | tail -n +2 | awk '{print "   " $9 " (" $5 ")"}' || echo "   (no files yet)"
echo ""
echo "✅ Found and organized $files_found file(s)!"
echo ""
echo "🌐 View your page: http://localhost:8080/brows-quiz.html"

