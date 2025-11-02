# educational_port_scanner_streamlit.py
# Streamlit app: educational local/private IP port scanner with safety checks.
#
# Usage:
# 1. Install streamlit:  pip install streamlit
# 2. Run locally:        streamlit run educational_port_scanner_streamlit.py
#
# IMPORTANT safety: by default this app allows only localhost and private IP ranges.
# If someone wants to scan a public IP, they must explicitly type the consent phrase
# "I HAVE_PERMISSION" into the confirmation box.

import streamlit as st
import socket
import ipaddress
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# ---------------------------
# Helper / Configuration
# ---------------------------
# Curated ports to check by default (common services). Educators can expand this.
DEFAULT_PORTS = [21, 22, 23, 25, 80, 443, 3306, 3389, 445, 5900, 6379]

# Short network timeouts to avoid long blocking waits.
CONNECT_TIMEOUT = 0.5   # seconds for connect attempts
BANNER_TIMEOUT = 0.3    # seconds for banner read

# A short phrase the user must type if they want to scan a public (non-private) IP.
PUBLIC_SCAN_CONSENT = "I HAVE_PERMISSION"

# Mapping port -> (service name, short risk note) for UI explanations
PORT_INFO = {
    21:  ("FTP",  "Plain-text credentials common; anonymous file access possible."),
    22:  ("SSH",  "Remote shell; ensure key auth and strong passwords."),
    23:  ("Telnet", "Plain-text remote login; insecure—use SSH instead."),
    25:  ("SMTP", "Mail server; misconfig can cause open relay issues."),
    80:  ("HTTP", "Web server; applications on it may have vulnerabilities."),
    443: ("HTTPS","Encrypted web; still may host vulnerable apps."),
    445: ("SMB",  "File sharing; high-risk if exposed externally."),
    3306:("MySQL","Database server; can expose data if reachable."),
    3389:("RDP",  "Remote desktop; common target for takeover attempts."),
    5900:("VNC",  "Remote desktop; often weak/no auth in default configs."),
    6379:("Redis","In-memory store; commonly misconfigured with no auth."),
}

# ---------------------------
# Utility functions
# ---------------------------
def is_private_or_local(ip_str):
    """
    Return True if ip_str is loopback (::1 or 127.0.0.1) or a private address
    per RFC1918 (10/8, 172.16/12, 192.168/16).
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_loopback or ip.is_private
    except ValueError:
        return False

def valid_ip(ip_str):
    """Return True if ip_str is a valid IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

def check_port(target, port, connect_timeout=CONNECT_TIMEOUT, banner_timeout=BANNER_TIMEOUT):
    """
    Try to open a TCP connection to (target,port).
    Returns a dict: {'port':port, 'open':bool, 'banner':str}
    - Uses connect_ex to avoid raising exceptions for common socket errors.
    - Short timeouts keep scan polite.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(connect_timeout)
    try:
        # connect_ex returns 0 on success (connected), otherwise an errno code
        res = s.connect_ex((target, port))
        if res == 0:
            # If connected, attempt a tiny non-blocking banner read (safe & polite).
            banner = ""
            try:
                s.settimeout(banner_timeout)
                banner = s.recv(1024).decode(errors="ignore").strip()
            except Exception:
                banner = ""
            finally:
                s.close()
            return {"port": port, "open": True, "banner": banner}
        else:
            s.close()
            return {"port": port, "open": False, "banner": ""}
    except Exception as e:
        # On unexpected errors, close and report closed; keep UX friendly
        try:
            s.close()
        except Exception:
            pass
        return {"port": port, "open": False, "banner": "", "error": str(e)}

def analyze_result(item):
    """
    Add human-readable service name, risk level, and mitigation suggestions.
    This keeps the UI educational: it explains *why* an open port matters.
    """
    port = item["port"]
    open_ = item["open"]
    banner = item.get("banner", "")
    service_name, short_note = PORT_INFO.get(port, (f"port-{port}", "Unknown service; research recommended."))

    if not open_:
        return {
            "port": port,
            "service": service_name,
            "open": False,
            "banner": banner,
            "risk": "Low",
            "explanation": "Port is closed — no direct network exposure on this port.",
            "mitigation": "No action required for this port."
        }
    else:
        high_risk_ports = {23, 445, 3389, 5900, 6379}
        medium_risk_ports = {21, 25, 3306}
        if port in high_risk_ports:
            risk = "High"
        elif port in medium_risk_ports:
            risk = "Medium"
        else:
            risk = "Medium"

        explanation = f"Port {port} is open and commonly runs {service_name}. {short_note}"
        if banner:
            # show first 200 chars of banner to keep UI tidy
            explanation += f" Detected banner (first 200 chars): {banner[:200]!s}"
        mitigation = "Limit external access with a firewall, enforce strong auth, and keep software updated."

        return {
            "port": port,
            "service": service_name,
            "open": True,
            "banner": banner,
            "risk": risk,
            "explanation": explanation,
            "mitigation": mitigation
        }

def run_scan(target, ports, max_workers=50):
    """
    Run a multi-threaded scan using ThreadPoolExecutor.
    - max_workers controls concurrency; we keep it reasonable for local testing.
    - Returns a dict with metadata and per-port results.
    """
    start = datetime.utcnow().isoformat() + "Z"
    results = []

    # Use ThreadPoolExecutor for simple concurrency (easy to understand for beginners).
    with ThreadPoolExecutor(max_workers=min(max_workers, len(ports))) as exe:
        futures = {exe.submit(check_port, target, p): p for p in ports}
        for future in as_completed(futures):
            res = future.result()
            results.append(analyze_result(res))

    # Sort results by port number for consistent UI
    results.sort(key=lambda r: r["port"])
    return {"target": target, "timestamp": start, "results": results}

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Educational Port Scanner", layout="centered")

st.title("Educational Port Scanner — local & private networks only")
st.markdown(
    """
**Safety first.** This tool is for learning and should be used *only* on machines or networks
you own or have explicit permission to test.

By default the app allows scanning **localhost** and **private (RFC1918)** IP ranges:
- 127.0.0.1 / ::1 (loopback)
- 10.0.0.0/8
- 172.16.0.0/12
- 192.168.0.0/16

If you want to scan a public IP, you must type the confirmation phrase `I HAVE_PERMISSION`
to indicate you have the right to scan that address.
"""
)

# Input: target IP
target_ip = st.text_input("Enter the IP address to scan (e.g. 127.0.0.1):", value="127.0.0.1")

# Port selection UI: quick preset or custom comma-separated list
port_choice = st.radio("Ports to scan", ("Default common ports", "Custom list (comma separated)"))
if port_choice.startswith("Default"):
    ports_to_scan = DEFAULT_PORTS
else:
    custom = st.text_input("Enter ports separated by commas (e.g. 22,80,443):", value="22,80,443")
    # parse and sanitize user input
    ports_to_scan = []
    try:
        for piece in custom.split(","):
            p = piece.strip()
            if p:
                pi = int(p)
                if 1 <= pi <= 65535:
                    ports_to_scan.append(pi)
    except Exception:
        st.error("Invalid custom ports input. Please enter numbers 1-65535 separated by commas.")
        st.stop()

st.write(f"Ports to be scanned: {ports_to_scan}")

# Safety confirmation area
st.markdown("### Permission & Safety Check")
if not valid_ip(target_ip):
    st.error("Please enter a valid IPv4 or IPv6 address.")
    st.stop()

if is_private_or_local(target_ip):
    st.success("Target is localhost or a private IP (allowed). Please confirm you own or have permission to test this host.")
    owner_confirm = st.checkbox("I confirm I own or have permission to scan this IP (required).")
    public_consent = False
else:
    st.warning("Target appears to be a public IP. Scanning public IPs without explicit permission may be illegal.")
    st.info(f"To proceed you must type the exact consent phrase: {PUBLIC_SCAN_CONSENT}")
    owner_confirm = False
    public_consent = st.text_input("Type consent phrase to allow public scan:", value="")

# Action button is only enabled when user provided required confirmation
allow_scan = False
if is_private_or_local(target_ip):
    allow_scan = owner_confirm
else:
    allow_scan = (public_consent.strip() == PUBLIC_SCAN_CONSENT)

if not allow_scan:
    st.stop()

# Scan button
if st.button("Start scan"):
    st.info(f"Starting scan of {target_ip} — this runs on your machine only.")
    # Run the scan
    scan_output = run_scan(target_ip, ports_to_scan)

    # Show summary counts
    open_ports = [r for r in scan_output["results"] if r["open"]]
    high = sum(1 for r in open_ports if r["risk"] == "High")
    medium = sum(1 for r in open_ports if r["risk"] == "Medium")
    low = sum(1 for r in open_ports if r["risk"] == "Low")

    st.markdown("### Scan summary")
    st.write(f"Target: **{scan_output['target']}**")
    st.write(f"Scan time (UTC): **{scan_output['timestamp']}**")
    st.write(f"Open ports found: **{len(open_ports)}**")
    st.write(f"Risk breakdown — High: **{high}**, Medium: **{medium}**, Low: **{low}**")

    # Detailed results table
    st.markdown("### Detailed results")
    for r in scan_output["results"]:
        if r["open"]:
            color = "🔴" if r["risk"] == "High" else "🟠" if r["risk"] == "Medium" else "🟢"
            st.markdown(f"**Port {r['port']} — {r['service']}** {color}")
            st.write(f"- Open: **{r['open']}**")
            if r.get("banner"):
                st.write(f"- Banner (first 200 chars): `{r['banner'][:200]}`")
            st.write(f"- Risk: **{r['risk']}**")
            st.write(f"- Explanation: {r['explanation']}")
            st.write(f"- Suggested mitigation: {r['mitigation']}")
            st.write("---")
        else:
            st.markdown(f"**Port {r['port']} — {r['service']}** 🟢 (closed)")

    # Raw JSON download
    raw = json.dumps(scan_output, indent=2)
    st.download_button("Download JSON results", data=raw, file_name="scan_results.json", mime="application/json")
