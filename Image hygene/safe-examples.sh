#!/usr/bin/env bash
# ================================================================
# Safe Examples Script — Defensive image hygiene commands
# Author: [Your Name]
# Repository: [Your Repo Name]
# Description:
#   Defensive commands to protect against metadata leaks.
#   Use ONLY on images you own or are authorized to process.
# ================================================================

# --- SETUP ------------------------------------------------------
mkdir -p cleaned
mkdir -p originals

# --- 1. VERIFY METADATA ----------------------------------------
# Check metadata safely (read-only)
echo "Checking metadata for image.jpg ..."
exiftool image.jpg

# For PowerShell (Windows) equivalent:
# PS> .\exiftool.exe image.jpg

# --- 2. STRIP METADATA -----------------------------------------
# Create a cleaned copy (recommended)
echo "Creating sanitized copy..."
exiftool -all= -o cleaned/image_stripped.jpg originals/image.jpg

# Overwrite in place (use with backup)
# exiftool -all= -overwrite_original_in_place originals/image.jpg

# PowerShell equivalent:
# PS> .\exiftool.exe -all= -o .\cleaned\image_stripped.jpg .\originals\image.jpg

# --- 3. STRIP USING IMAGEMAGICK --------------------------------
echo "Stripping metadata and re-encoding..."
convert originals/image.jpg -strip cleaned/image_stripped_magick.jpg

# Windows equivalent (if ImageMagick installed):
# PS> magick convert originals\image.jpg -strip cleaned\image_stripped_magick.jpg

# --- 4. DOWNSAMPLE / RECOMPRESS --------------------------------
echo "Downsampling to 1920x1080 ..."
convert originals/image.jpg -resize 1920x1080\> -strip cleaned/image_downsampled.jpg

# PowerShell:
# PS> magick convert originals\image.jpg -resize 1920x1080 -strip cleaned\image_downsampled.jpg

# --- 5. VERIFY STRIPPED FILE -----------------------------------
echo "Verifying sanitized file..."
exiftool cleaned/image_stripped.jpg

# --- 6. HASHING -------------------------------------------------
sha256sum cleaned/image_stripped.jpg > cleaned/image_stripped.sha256

# PowerShell equivalent:
# PS> Get-FileHash .\cleaned\image_stripped.jpg -Algorithm SHA256 | Out-File .\cleaned\image_stripped.sha256

echo "✅ Sanitization complete."
