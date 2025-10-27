# Network Visibility

*“Know who’s on your network before they know you.”*

## Purpose
This folder gathers lightweight, open‑source utilities and command snippets that help security researchers—and anyone interested in personal privacy—quickly assess what devices, services, and open ports are present on a local network. By providing clear, responsibly‑written examples we aim to raise awareness of how easily an attacker can enumerate a network and to empower defenders to spot and remediate exposure.

## Contents
- **`commands.md`** – Curated one‑liners for tools such as `nmap`, `netdiscover`, `ss`, `arp‑scan`, and others.  
- **`ethics.md`** – Guidelines and a legal disclaimer outlining responsible use and the steps you’ve taken to ensure ethical distribution.  

## Getting Started
```bash
# Clone the repository (or just this folder)
git clone https://github.com/<your‑username>/Blue-lab.git
cd Blue-lab/network\ visibility

# Install prerequisites (Debian/Ubuntu example)
sudo apt update
sudo apt install nmap netdiscover arp-scan iproute2
Copy
⚠️ Important: Many of the commands require elevated privileges (sudo). Use them only on networks you own or have explicit permission to test.

Stay curious, stay safe.
— The Blue‑lab Team

