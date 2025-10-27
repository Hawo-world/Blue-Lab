---
# Network‑Visibility Commands

Below are vetted one‑liners for quick reconnaissance. All commands assume you have the required tools installed (see the README for a package list).

---

## 1️⃣ Nmap – Fast LAN sweep
```bash
# Ping‑scan the entire /24 subnet and then probe the most common ports (1‑1000)
sudo nmap -sn 192.168.1.0/24 && sudo nmap -p 1-1000 192.168.1.0/24
Copy
-sn = host discovery only.
Second pass enumerates the most frequently used ports.
2️⃣ Netdiscover – Passive ARP sniffing
sudo netdiscover -r 192.168.1.0/24 -i eth0
Copy
Shows MAC addresses, vendors, and IPs without generating active traffic.

3️⃣ ss – List listening sockets
ss -tulnp
Copy
Displays all TCP/UDP listeners together with the owning process ID/name.

4️⃣ arp‑scan – Active ARP enumeration
sudo arp-scan --interface=eth0 --localnet
Copy
Provides a concise table of IP ↔ MAC ↔ Vendor for every device on the LAN.

5️⃣ netscan (Rust) – Parallel port scanner
netscan -c 1000 -p 22,80,443 192.168.1.0/24
Copy
-c sets concurrency (higher = faster).
Great for larger subnets when speed matters.
6️⃣ Combined snapshot (single line)
{
  echo "=== Nmap Live Hosts ==="; sudo nmap -sn 192.168.1.0/24;
  echo "=== ss Listening ==="; ss -tulnp;
  echo "=== netdiscover ==="; sudo netdiscover -r 192.168.1.0/24 -i eth0;
} | tee network-overview-$(date +%F).txt
Copy
Creates a timestamped text file summarizing the current network state.

Safety Tips
Scope: Scan only networks you own or have written permission to test.
Rate‑limit: Use --max-rate (nmap) or -c (netscan) to avoid flooding.
Legal: Unauthorized scanning can breach local laws and organizational policies.
