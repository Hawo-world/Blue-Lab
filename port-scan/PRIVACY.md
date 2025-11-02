## 🔒 Privacy Policy — Educational Port Scanner

Last updated: November 2, 2025


---

## 🧭 Overview

This document describes how the Educational Port Scanner project handles user data and network information.
Our goal is to ensure complete transparency and maintain user privacy and safety.


---

## 1. Local-Only Operation

This application runs entirely on the user’s computer.
All scanning, analysis, and report generation occur locally within the user’s system.
No data leaves the user’s machine unless they explicitly choose to share it.


---

## 2. Data Collection

The application does not collect, transmit, or store any of the following information externally:

IP addresses scanned

Scan results or open ports

System information (hostname, OS, etc.)

Any personal or identifying data


All data is processed locally in memory and can be optionally saved by the user as a JSON file on their own computer.


---

## 3. Network Traffic

When scanning 127.0.0.1 (localhost) or a private IP (e.g. 192.168.x.x), all packets remain within the user’s local network.

If the user scans a public IP, any connections made originate from the user’s own network.

No traffic is ever routed through or visible to the project authors.



---

## 4. Optional Updates & Dependencies

The app may request package updates (via pip install), but these requests go directly to official repositories like PyPI.org — not to any developer-controlled servers.

The codebase includes no telemetry, analytics, or external logging by default.



---

## 5. User Control

Users have complete control over:

Which IPs and ports they scan

Whether they save results to disk

Whether they modify or redistribute the code


Users may delete the application and all associated files at any time.


---

## 6. Third-Party Libraries

This project uses Streamlit, which may collect anonymous usage metrics if telemetry is not disabled.
To disable Streamlit telemetry, run:

streamlit config show

Then set:

browser.gatherUsageStats = false

This prevents any anonymous analytics from being sent to Streamlit’s maintainers.


---

## 7. Disclaimer

This is an educational tool, not a commercial service.
It is provided as-is, with no warranties.
The authors assume no responsibility for user actions or misuse of the tool.


---

## 8. Contact

For privacy or security-related concerns about this project, please:

Open an issue on the GitHub repository, or

Contact the maintainer listed in the project’s README file.



---

## ✅ Summary

This project values user privacy.
It runs locally, stores nothing online, and does not collect or share data.


---
