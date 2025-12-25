# 🛡️ HackerAI - Advanced Security Assessment Toolkit v3.0

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-Educational%20Use%20Only-red)
![Version](https://img.shields.io/badge/Version-3.0%20ADVANCED-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20MacOS-lightgrey)

## 📖 Table of Contents
- [Overview](#-overview)
- [⚠️ Disclaimer](#%EF%B8%8F-disclaimer)
- [✨ Features](#-features)
- [🚀 Installation](#-installation)
- [🛠️ Modules Overview](#%EF%B8%8F-modules-overview)
- [📊 Usage Guide](#-usage-guide)
- [🔧 Configuration](#-configuration)
- [📁 Project Structure](#-project-structure)
- [🔐 Security Guidelines](#-security-guidelines)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## 🎯 Overview

**HackerAI** is an advanced, modular security assessment and ethical hacking toolkit designed for cybersecurity professionals, penetration testers, and security researchers. Built with Python 3.8+, it features an asynchronous engine for high-performance operations and includes comprehensive modules for reconnaissance, vulnerability assessment, exploitation, and post-exploitation.

### Key Highlights:
- **Asynchronous Engine**: High-performance async/await architecture
- **Modular Design**: Independent, reusable components
- **Advanced Evasion**: WAF bypass, proxy rotation, Tor support
- **Comprehensive Toolset**: From reconnaissance to post-exploitation
- **Professional Reporting**: JSON-based reporting with export options

## ⚠️ DISCLAIMER

                            SECURITY DISCLAIMER     

 This tool is for EDUCATIONAL PURPOSES and AUTHORIZED security testing ONLY.  
                                                                              
 LEGAL USE ONLY:                                                              
 • Use only on systems you OWN                                                
 • Use only with EXPLICIT WRITTEN PERMISSION                                  
 • Comply with all applicable LAWS and REGULATIONS                            
                                                                              
 The developers are NOT RESPONSIBLE for any:                                  
 • Misuse or illegal use of this tool                                         
 • Damage caused by unauthorized testing                                      
 • Legal consequences of improper usage                                       

 By using this tool, you ACCEPT FULL RESPONSIBILITY for your actions.         

```

## ✨ Features

### 🔍 **Reconnaissance & Intelligence**
- **Advanced Port Scanning**: Fast socket-based scanning with service fingerprinting
- **WAF Detection**: Cloudflare, Akamai, Imperva, AWS WAF, Sucuri detection
- **Subdomain Enumeration**: Async subdomain discovery
- **Network Scanning**: CIDR-based host discovery
- **Technology Detection**: CMS, frameworks, server technologies

### 🎯 **Vulnerability Assessment**
- **Web Vulnerability Scanner**: SQLi, XSS, LFI, RCE, Command Injection
- **Security Header Analysis**: Missing security headers detection
- **Directory Bruteforce**: Intelligent wordlist selection
- **Auto-Exploitation**: SQLi, LFI, XSS, Command Injection, RCE

### ⚡ **Attack Tools**
- **Advanced Stress Tester**: HTTP floods, Slowloris, SYN floods, UDP floods
- **Reverse Shell Generator**: 20+ shell types with evasion techniques
- **Payload Obfuscation**: Multiple encoding/encryption methods
- **Post-Exploitation**: System info gathering, privilege escalation checks

### 🛡️ **Evasion & Anonymity**
- **Proxy Manager**: Rotating proxies with verification
- **Tor Integration**: Full Tor network support
- **User-Agent Rotation**: 50+ realistic user agents
- **Stealth Mode**: Advanced header manipulation
- **Packet Fragmentation**: Firewall evasion techniques

### 📊 **Reporting & Management**
- **JSON Reporting**: Structured finding storage
- **Export Options**: TXT, JSON export formats
- **Session Management**: Persistent session handling
- **Real-time Statistics**: Attack performance metrics
```
## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/hackerai.git
cd hackerai

Step 1:cd 

```bash
cd pythonattack
```

Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install aiohttp requests fake_useragent urllib3 colorama beautifulsoup4

```

For A shell(manually)

```bash
pip install aiohttp 
```
```bash
pip install requests
```
```bash
pip install colorama
```
```bash
pip install beautifulsoup4
```
```bash
pip install urllib3 
```
```bash
pip install fake_useragent 
```


Step 3: Run it

```bash
python3 main.py
```
### Use vpn on ios 
### Use tor on android
Optional: Tor Setup (For Enhanced Anonymity)

```bash
# Ubuntu/Debian
sudo apt install tor
sudo systemctl start tor

# macOS
brew install tor
brew services start tor

# Windows
# Download from: https://www.torproject.org/download/
```

### 🛠️ Modules Overview
```
main.py - Entry Point

· Tool initialization
· Dependency checking
· Disclaimer display
· Main menu launcher

scanner.py - Advanced Scanner Module

· Intelligent fingerprinting
· WAF detection
· Fast port scanning
· Technology stack analysis
· Vulnerability hint generation

reverse_shell.py - Reverse Shell Generator

· 20+ shell types (bash, python, powershell, PHP, etc.)
· Encryption/obfuscation (XOR, AES, RC4, Base64)
· Windows evasion (AMSI bypass, registry persistence)
· Linux evasion (fileless execution, cron persistence)
· Interactive handler with multi-session support

auto_exploit.py - Auto Exploitation Engine

· Payload obfuscation (10+ methods)
· Post-exploitation module
· Web shell deployment
· Advanced SQLi/LFI/XSS/RCE exploitation
· Evasion techniques integration

stress_tester.py - Advanced Stress Tester

· Async HTTP floods
· Slowloris attacks
· SYN/UDP floods
· Packet fragmentation
· Distributed attack simulation
· Custom HTTP methods support

proxy_manager.py - Proxy & Anonymity Manager

· Proxy rotation with verification
· Tor network integration
· User-agent database (50+ agents)
· Stealth mode headers
· Session management

menu.py - Interactive Menu System

· Color-coded interface
· Status display
· Settings management
· Report viewer with export options

config.py - Configuration

· Color schemes
· Global variables
· Default settings
· User agents list

utils.py - Utilities (Assumed)

· Common functions
· File operations
· Network utilities
· Reporting helper
```

### 📊 Usage Guide

Starting the Tool

```bash
python main.py
```

Main Menu Navigation

```
━━━━━━━━━━━━━━━[ SCANNING TOOLS ]━━━━━━━━━━━━━━━
  [1] Advanced Reconnaissance
  [2] Web Vulnerability Auditor
  [3] Directory Bruteforce
  [4] Subdomain Enumeration
  [5] Network Scanner

━━━━━━━━━━━━━━━[ ATTACK TOOLS ]━━━━━━━━━━━━━━━━
  [6] Advanced Stress Tester (Async)
  [7] Reverse Shell Generator
  [8] Auto-Exploit Module

━━━━━━━━━━━━━━━[ UTILITIES ]━━━━━━━━━━━━━━━━━━━
  [S] Settings & Configuration
  [R] View & Export Reports
  [H] Help
  [A] About HackerAI
  [0] Exit Tool
```

Example Workflows

1. Complete Security Assessment

```bash
1. Advanced Reconnaissance → Gather target information
2. Web Vulnerability Auditor → Scan for vulnerabilities
3. Auto-Exploit Module → Test exploitation
4. View Reports → Analyze findings
```

2. Reverse Shell Generation

```bash
1. Navigate to Reverse Shell Generator
2. Configure LHOST/LPORT
3. Select shell type
4. Copy generated payload
5. Start listener
```

3. Stress Testing (Authorized Only)

```bash
1. Navigate to Advanced Stress Tester
2. Enter target URL
3. Select attack type
4. Configure duration/concurrency
5. Start attack
```

### 🔧 Configuration

Edit config.py for Custom Settings:

```python
# Network Settings
THREADS = 50              # Concurrent threads
TIMEOUT = 10              # Request timeout (seconds)
LHOST = "192.168.1.100"   # Default listener IP
LPORT = 4444              # Default listener port

# Reporting
REPORT_FILE = "hackerai_scan_report.json"

# Colors (Customize UI)
R = "\033[31m"   # Red
G = "\033[32m"   # Green
Y = "\033[33m"   # Yellow
B = "\033[34m"   # Blue
C = "\033[36m"   # Cyan
W = "\033[0m"    # White
```

Proxy Configuration

Enable in Settings Menu:

1. Proxy Rotation: ON
2. Tor Network: ON/OFF
3. Stealth Mode: ON
4. Auto-refresh: ON

Custom Wordlists

Add custom wordlists to:

· wordlists/directory.txt - Directory bruteforce
· wordlists/subdomains.txt - Subdomain enumeration
· user_agents.txt - Additional user agents

### 📁 Project Structure

```
hackerai/
├── main.py                 # Entry point
├── config.py              # Configuration & colors
├── menu.py                # Interactive menu system
├── scanner.py             # Advanced scanner module
├── reverse_shell.py       # Reverse shell generator
├── auto_exploit.py        # Auto exploitation engine
├── stress_tester.py       # Advanced stress tester
├── proxy_manager.py       # Proxy & anonymity manager
├── utils.py              # Utility functions
├── requirements.txt       # Dependencies
├── README.md             # This file
├── reports/              # Generated reports
├── sessions/             # Session data
└── wordlists/            # Custom wordlists
```

### 🔐 Security Guidelines

✅ Authorized Testing Checklist

· Written permission obtained
· Scope clearly defined
· Legal compliance verified
· Data backup completed
· Emergency contacts listed
· Testing window scheduled

⛔ Prohibited Activities

· Testing without explicit authorization
· Targeting critical infrastructure
· Data theft or destruction
· Denial of Service on production systems
· Privacy violation or harassment

🔒 Safe Testing Practices

1. Use Lab Environments: Test in isolated networks
2. Limit Impact: Use controlled, non-destructive techniques
3. Document Everything: Keep detailed logs of all activities
4. Respect Privacy: Avoid accessing personal data
5. Follow Scope: Stay within authorized boundaries

🤝 Contributing

We welcome contributions! Please follow these guidelines:

Reporting Issues

1. Check existing issues
2. Use the issue template
3. Include steps to reproduce
4. Provide error messages/logs

Code Contributions

1. Fork the repository
2. Create a feature branch
3. Follow PEP 8 style guide
4. Add tests if applicable
5. Submit a pull request

Feature Requests

1. Describe the use case
2. Explain the benefit
3. Suggest implementation approach
4. Consider security implications

### 📄 License

Educational Use Only License

This software is provided for educational purposes only. By using this software, you agree to:

1. Use only for legitimate security testing on systems you own or have explicit permission to test
2. Not use for any illegal or unauthorized activities
3. Accept full responsibility for your actions
4. Comply with all applicable laws and regulations

No Warranty

THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. The developers shall not be liable for any damages arising from the use of this software.

Copyright Notice

© 2024 HackerAI Development Team. All rights reserved for authorized educational use.

---

🚨 Emergency Contact & Responsible Disclosure

If you discover vulnerabilities using this tool:

1. Do not exploit without authorization
2. Document the finding responsibly
3. Contact the system owner/administrator
4. Follow responsible disclosure practices

📞 Support & Resources

· Documentation: GitHub Wiki
· Community: Security Forums
· Training: Cybersecurity Courses
· Legal: Consult with legal counsel before testing

---

<div align="center">
  <p><strong>Remember: With great power comes great responsibility.</strong></p>
  <p>Stay ethical. Stay legal. Stay secure.</p><sub>Made with ❤️ by security professionals for security professionals</sub>

</div>

```
# HackerAI - Advanced Security Assessment Toolkit v3.0

An advanced, modular security assessment and ethical hacking toolkit featuring asynchronous operations, comprehensive vulnerability scanning, reverse shell generation, stress testing, and advanced evasion techniques. For authorized educational use and security testing only.

🔹 Features: Async engine, WAF detection, proxy rotation, Tor support, 20+ reverse shells, auto-exploitation, intelligent scanning
🔹 Requirements: Python 3.8+, aiohttp, requests
🔹 License: Educational Use Only
🔹 Disclaimer: For authorized testing only. Use responsibly.
```

For requirements.txt:

```txt

aiohttp>=3.8.0
requests>=2.28.0
fake-useragent>=1.1.0
urllib3>=1.26.0
colorama>=0.4.6
beautifulsoup4>=4.12.0

```

Quick Start Command:

```bash
https://github.com/nafis548/EthicalHackingTools.git && cd pythonattack && pip install -r requirements.txt && python3 main.py
```
