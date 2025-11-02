## 🛡️ Educational Port Scanner

An educational tool that helps learners understand open ports, network exposure, and cybersecurity fundamentals — safely and ethically.

This scanner runs locally on your computer, checks which ports are open on your own device or private network, and explains:

what each port/service is used for

what the risks are if it’s open

and how to mitigate those risks

Built with Python and Streamlit for a simple, beginner-friendly web interface.

---

## 🚀 Features

🧠 Educational explanations for each detected service

🔍 Local & private-network scanning (safe by default)

⚡ Fast multi-threaded scan of common ports

🔒 Safety enforcement — only localhost/private IPs by default

🗂️ Downloadable JSON results

🌈 Clean, interactive UI powered by Streamlit

---

## ⚙️ Installation

Clone or download this repository:

git clone https://github.com/yourusername/educational-port-scanner.git
cd educational-port-scanner


Create a virtual environment (recommended):

python3 -m venv venv
source venv/bin/activate      # On macOS/Linux
venv\Scripts\activate         # On Windows


Install dependencies:

pip install -r requirements.txt


If you don’t have a requirements.txt yet, you can install Streamlit directly:

pip install streamlit

---

## ▶️ How to Run

Launch the app with:

streamlit run educational_port_scanner_streamlit.py


Then open the local web interface (usually at http://localhost:8501).

Enter your IP (e.g. 127.0.0.1 or 192.168.x.x), choose ports, confirm you have permission, and click Start Scan.

---

## 🧩 Example Output

Open ports are listed with:

Port number and service name

Risk level (Low / Medium / High)

Explanations of what the service does and why it matters

Mitigation tips

Results can be downloaded as scan_results.json.

---

## 🧱 Architecture Overview

Language: Python 3

Frontend / UI: Streamlit

Concurrency: ThreadPoolExecutor for faster scans

Output format: JSON + on-screen summary

Default scan set: common service ports (21, 22, 23, 25, 80, 443, 3306, 3389, 445, 5900, 6379)

---

## 🔐 Privacy & Data Policy

This app runs entirely on your local machine.

It does not send any scan data, IP addresses, or results to any external server.

When you scan 127.0.0.1 or a private IP (e.g. 192.168.x.x), the scan happens only within your own network.

If you scan a public IP, the remote server will see your public IP, not the developer’s.

---

## ⚠️ Legal & Ethical Disclaimer

This project is for educational use only.
You must only scan systems you own or have explicit permission to test. Unauthorized scanning of external networks may be illegal in your jurisdiction. The authors assume no responsibility for misuse or damage caused by this tool.

---

📜 License

MIT License — free for learning and sharing.
See LICENSE file for details.
