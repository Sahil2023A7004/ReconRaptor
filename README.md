# 🦖 ReconRaptor v1.2

> *"The quieter you become, the more you can hear."*

ReconRaptor is a Python-based network reconnaissance tool for scanning ports on target IPs and domains. It supports SYN scanning and stealth scanning on both single ports and port ranges.

---

## ⚠️ Legal Disclaimer

This tool is intended for **authorized security testing and educational purposes only**. Scanning systems without explicit permission is illegal. The developers assume no liability for misuse of this tool. Always obtain proper authorization before scanning any network or system.

---

## 📋 Requirements

- Linux (Kali, Ubuntu, Debian or any distro)
- Python 3.8+
- Root privileges (required for stealth/SYN scanning via Scapy)

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Sahil2023A7004/ReconRaptor.git
cd reconraptor
```

### 2. Install Python dependencies

```bash
pip install scapy
```

Or if you are on a system-managed Python environment:

```bash
pip install scapy --break-system-packages
```

### 3. Give execute permission

```bash
chmod +x reconraptor.py
```

---

## 🚀 Usage

ReconRaptor must be run as root due to raw packet operations used in stealth scanning.

```bash
sudo python3 reconraptor.py
```

---

## 🗺️ Navigation

### Main Menu

```
Enter 1 for IP      → Scan a target by IPv4 address
Enter 2 for Domain  → Scan a target by domain name (auto-resolves to IP)
```

### Port Input

```
80        → Single port scan
20-80     → Port range scan
```

### Scan Types

```
1 → SYN Scan     — Fast TCP connect scan, less stealthy
2 → Stealth Scan — SYN stealth scan, does not complete handshake
```

---

## 🔍 Scan Types Explained

### SYN Scan
A standard TCP connect scan. Attempts a full connection to the target port. Faster but more likely to be logged by the target system.

- Single port → reports OPEN or CLOSED
- Port range → reports status for each port in range

### Stealth Scan
A SYN stealth scan using raw packets via Scapy. Sends a SYN packet and reads the response without completing the TCP handshake. Less likely to appear in application logs.

- Responds with OPEN, CLOSED, or FILTERED
- Single port and port range both supported
- Requires root privileges

---

## 📁 Project Structure

```
reconraptor/
├── recon_raptor.py    # Main tool
└── README.md          # This file
```

---

## 🛠️ Built With

- [Python 3](https://www.python.org/)
- [Scapy](https://scapy.net/) — packet manipulation library

---

## 👤 Author

Made with 🦖 by Sahil Mushtaq
For educational purposes — scan responsibly.
