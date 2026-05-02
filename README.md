# 🛡️ HackerAI Framework (Project Sirra)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Security Status](https://img.shields.io/badge/Security-Audited-brightgreen.svg)]()

**HackerAI Framework** (codenamed **Sirra**) is a lightweight, modular security testing environment designed for ethical hackers and security researchers. It is optimized for cross-platform use, including mobile environments like iOS and Android.

---

## 🚀 Key Features

- **Universal Orchestrator:** Centralized module management for easy expansion.
- **Security Scanner:** Built-in code analysis to identify potentially dangerous modules.
- **Advanced Web Scanner:** High-performance scanning with asynchronous support.
- **Multi-Format Reporting:** Export results in HTML, JSON, CSV, and Markdown.
- **Cross-Platform:** Works seamlessly on Windows, Linux, Android (Termux), and iOS (a-Shell).

---

## 🛠️ Installation Guide

### 📱 Mobile (Android/iOS)
1. **Android (Termux):** `pkg install python git`
2. **iOS (a-Shell):** Install from App Store.
3. **Clone & Run:**
   ```bash
   git clone https://github.com/Quincunx33/EthicalHackingTools.git
   cd EthicalHackingTools
   pip install -r requirements.txt
   python main.py
   ```

### 💻 Desktop (Linux/Windows)
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Quincunx33/EthicalHackingTools.git
   cd EthicalHackingTools
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the tool:**
   ```bash
   python main.py
   ```

---

## 📦 Core Dependencies
The framework is kept minimal to ensure compatibility:
- `requests`: For synchronous HTTP operations.
- `aiohttp`: For high-speed asynchronous scanning.
- `colorama`: For cross-platform terminal coloring.
- `dnspython`: For advanced DNS resolution (optional).

---

## 📜 Disclaimer
> **WARNING:** This tool is for **Ethical Hacking** and **Educational Purposes** only. Unauthorized use against targets without prior consent is illegal.

---
**Maintained by:** [Quincunx33](https://github.com/Quincunx33)
