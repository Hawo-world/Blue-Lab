## Image hygiene — defensive commands & automation

Purpose: concrete, safe commands and scripts to remove metadata, downsample, redact, verify, and automate safe publishing of images.
Warning: run these only on images you own or are authorized to process. Keep originals backed up and hashed before any mass processing.

---

## Table of contents

---

Quick principles

Tools referenced (install links not included)

Inspecting metadata (verification)

Removing metadata (single file & batch)

Downsampling / reducing detail

Redaction (blur / pixelate / crop)

Windows / PowerShell equivalents

Python (scripted sanitization)

CI / GitHub Action: auto-strip on push

Best practices, logging & safety

---

## 1) Quick principles

Always keep an immutable archive of originals (read-only, hashed).

Work on copies. Never overwrite originals until you’ve verified outputs.

Verify removal with exiftool / identify -verbose.

Automate stripping at the point of publication (CMS, CI) so public images are sanitized by default.

Remove GPS/EXIF and also consider downsampling or cropping to remove contextual detail.

---

## 2) Tools referenced

exiftool — metadata read/remove (recommended).

ImageMagick (convert, mogrify, identify) — image processing, strip, resize, crop, blur.

jpegtran / jpegoptim / mozjpeg — lossless or optimized JPEG recompression.

optipng / pngcrush — PNG re-encode/optimize.

sha256sum / shasum — checksums for provenance.

python + Pillow — programmatic sanitization (example included).

(Install these using your platform package manager if needed — e.g., apt, brew, choco — but do not publish extraction tools or instructions for misuse.)

---

## 3) Inspect metadata (verify what’s present)

Run these read-only checks on files you own to see what metadata exists.

# 1) Basic EXIF summary (exiftool is most informative)
exiftool image.jpg

# 2) Full ImageMagick verbose header
identify -verbose image.jpg

# 3) Quick list of common GPS/Date/Model fields
exiftool -gps:all -DateTimeOriginal -Model -Make image.jpg

Always run these before changes to capture the baseline. Store a checksum of the original:

sha256sum original/image.jpg > original/image.jpg.sha256

---

## 4) Remove metadata (safe defensive commands)
Single file — exiftool (recommended)
# Create a cleaned copy (preserves original)
exiftool -all= -o cleaned/image_stripped.jpg original/image.jpg

# Overwrite the original (use with caution; ensure backup exists)
exiftool -all= -overwrite_original_in_place original/image.jpg

ImageMagick (re-encode + strip)
# Creates a sanitized re-encoded copy and strips metadata
convert original/image.jpg -strip cleaned/image_stripped.jpg

PNG-specific (optimize & strip)
# Convert + strip then optimize (keeps visual content)
convert original/image.png -strip cleaned/image.png
optipng cleaned/image.png

Batch (Linux/macOS) — using exiftool
# Strip metadata from all JPEGs in a folder and write cleaned/ copies
mkdir -p cleaned
for f in originals/*.jpg; do
  fname=$(basename "$f")
  exiftool -all= -o cleaned/"$fname" "$f"
done


Note: exiftool supports -overwrite_original_in_place if you need in-place, but do backups first.

---

## 5) Downsample / reduce resolution (defensive)

Lower resolution and/or recompress to remove fine-grained details that might leak information.

# Downsample to max 1920x1080 (keeps aspect ratio) and strip metadata
convert original/image.jpg -resize 1920x1080\> -strip cleaned/image_downsampled.jpg

# Recompress JPEG with quality target and strip
convert original/image.jpg -quality 85 -strip cleaned/image_q85.jpg


For lossless-ish recompression with better quality control (JPEG):

# Using jpegoptim to recompress and remove ancillary markers (no metadata)
jpegoptim --strip-all --max=85 cleaned/image.jpg

---

## 6) Redaction (blur, pixelate, or crop sensitive areas)

These are defensive techniques to remove visible sensitive content (screens, badges, faces, license plates) before publishing.

Crop out sensitive regions
# Crop: convert input -crop <width>x<height>+<x>+<y> output
convert original/image.jpg -crop 1000x600+50+200 +repage cleaned/image_cropped.jpg

Blur (Gaussian blur)
# Blur a region — use -region to limit effect (ImageMagick)
convert original/image.jpg -region 400x200+50+100 -blur 0x8 cleaned/image_blurred.jpg

Pixelate (scale down & back up to pixelate)
# Pixelate a region by scaling it down then up
convert original/image.jpg \
  \( -clone 0 -crop 200x200+50+100 +repage -resize 10x10 -resize 200x200 \) \
  -compose over -composite cleaned/image_pixelated.jpg


Tip: for repeatable redaction workflows, note the coordinates in your experiment log.

---

## 7) Windows / PowerShell snippets

Assuming exiftool(-k).exe is in PATH or the current folder:

# Create cleaned directory
New-Item -ItemType Directory -Path .\cleaned -Force

# Strip metadata for a single file (exiftool)
.\exiftool.exe -all= -o .\cleaned\image_stripped.jpg .\original\image.jpg

# Batch (PowerShell)
Get-ChildItem .\original\*.jpg | ForEach-Object {
  $out = ".\cleaned\$($_.Name)"
  .\exiftool.exe -all= -o $out $_.FullName
}

---

## 8) Python script for sanitization (Pillow)

A simple, safe script that loads an image and saves a new file without EXIF. This is useful when you want language-level control or to integrate into apps.

# sanitize_image.py
from PIL import Image
import sys
from pathlib import Path

def sanitize(in_path, out_path, resize=None, quality=85):
    img = Image.open(in_path)
    # If resize specified as (w, h), do a thumbnail (keeps aspect)
    if resize:
        img.thumbnail(resize)
    # Save without exif by not passing exif parameter
    img.save(out_path, quality=quality)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python sanitize_image.py input.jpg cleaned/output.jpg [max_width] [max_height]")
        sys.exit(1)
    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    if len(sys.argv) == 5:
        max_w, max_h = int(sys.argv[3]), int(sys.argv[4])
        sanitize(in_path, out_path, resize=(max_w, max_h))
    else:
        sanitize(in_path, out_path)


Use: python sanitize_image.py original/image.jpg cleaned/image.jpg 1920 1080

---

## 9) CI / GitHub Action: auto-strip on push (example)

This example runs in CI to sanitize images in a specific folder before they are published. Design for your org’s workflow — do not run blindly on all files without approvals.

.github/workflows/strip-images.yml

name: Strip image metadata before publish
on:
  push:
    paths:
      - 'public_assets/images/**'

jobs:
  sanitize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install exiftool
        run: sudo apt-get update && sudo apt-get install -y libimage-exiftool-perl

      - name: Sanitize images
        run: |
          mkdir -p sanitized
          for img in public_assets/images/*.{jpg,jpeg,png}; do
            if [ -f "$img" ]; then
              fname=$(basename "$img")
              exiftool -all= -o "sanitized/$fname" "$img"
            fi
          done

      - name: Show summary
        run: ls -l sanitized || true

      # Optionally: commit sanitized files to a sanitized branch or upload to artifact storage


Note: add policy gates and approvals — don’t auto-push sanitized assets without human review in sensitive orgs.

---

## 10) Best practices, logging & safety

Provenance: store SHA-256 of originals and cleaned files; log who performed sanitization and when.

Audit trail: keep an experiments.log text file with: date, operator, files processed, tools & versions, and retention policy.

Automation: integrate sanitization into the content publishing pipeline (CMS, PR templates) so human error is minimized.

Training: brief content teams (marketing, social media) on safe image sharing (turn off geotagging, remove EXIF, avoid high-res originals).

Mobile device hygiene: disable camera geolocation/embedded location in device settings (iOS & Android) and use built-in sharing options that strip metadata when available. Also prefer platform upload flows that automatically remove metadata or choose “remove location” options.

Example “safe_publish” checklist (one-liner)

Before publishing an image publicly:

Confirm image is owned or consented.

Archive original + record SHA-256.

Create sanitized copy (exiftool -all= or convert -strip).

Downsample to required resolution (if possible).

Redact visible sensitive regions.

Verify metadata absence (exiftool sanitized.jpg).

Publish sanitized copy only.

Final notes & legal/ethical reminder

These commands are defensive and intended to protect privacy. They should only be run on images you own or are explicitly authorized to handle. Follow local laws and your organization’s policy when processing images. If you plan to publish research based on experiments, include an ethics/authorization statement and sanitize any published artifacts (remove PII, metadata, and replace images with synthetic examples when possible).
