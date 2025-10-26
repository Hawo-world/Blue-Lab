# Image Privacy Research — Defensive Image Hygiene

This repository contains **safe, defensive examples** for protecting privacy and sensitive information in digital images.  
It is designed for **researchers, educators, and security professionals** studying data leakage prevention and privacy by design.

---

## 🧩 Purpose

Images can unintentionally reveal private details:
- GPS coordinates
- Device information
- Timestamps
- Text or visual content in reflections or screens

This repository teaches **how to remove**, **verify**, and **audit** that data safely and ethically.

---

## 🛡️ Defensive capabilities

| Goal | Tool | Description |
|------|------|--------------|
| Verify metadata | `exiftool`, `identify` | Inspect metadata (EXIF/IPTC/XMP) in owned files |
| Strip metadata | `exiftool`, `convert -strip` | Remove all non-visual metadata |
| Downsample | `convert` | Reduce resolution to prevent fine-detail leaks |
| Redact | `convert` regions | Blur or pixelate sensitive areas |
| Verify hash | `sha256sum` / `Get-FileHash` | Create integrity fingerprints of sanitized files |

See [`safe-examples.sh`](safe-examples.sh) for cross-platform commands.

---

## ⚙️ GitHub Actions

The included workflow (`.github/workflows/sanity-check.yml`) scans for metadata and **warns** contributors if unsanitized images are detected.

---

## 🧾 Authorization & Ethics

Before performing tests or publishing results:
- Obtain written consent using [`AUTHORIZATION.md`](AUTHORIZATION.md).
- Read and comply with [`ETHICS.md`](ETHICS.md).

---

## ✅ Quick Start

```bash
# Linux / macOS
bash safe-examples.sh

# Windows PowerShell
.\exiftool.exe image.jpg
.\magick.exe convert image.jpg -strip image_cleaned.jpg
