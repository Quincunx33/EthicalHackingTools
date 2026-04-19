# 🛡️ HackerAI Framework (Project Sirra)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Security Status](https://img.shields.io/badge/Security-Audited-brightgreen.svg)]()

**HackerAI Framework** (codenamed **Sirra**) is a next-generation, modular security testing environment designed for ethical hackers, security researchers, and automated vulnerability assessment.

---

## 🚀 Key Features

- **Universal Orchestrator:** Centralized module lifecycle management.
- **Security Sandbox:** Restricted execution environment for custom modules.
- **Modular Architecture:** Plug-and-play scanners and exploit testers.
- **Reporting Engine:** Automated security report generation.

---

## 🛠️ Multi-Platform Installation Guide

### 📱 Termux (Android)
1. Update and upgrade packages:
   ```bash
   pkg update && pkg upgrade
   ```
2. Install Python and Git:
   ```bash
   pkg install python git
   ```
3. Clone the repository:
   ```bash
   git clone https://github.com/Quincunx33/EthicalHackingTools.git
   cd EthicalHackingTools
   ```
4. Install required libraries (Choose one):
   - **Option A (Recommended):**
     ```bash
     pip install -r requirements.txt
     ```
   - **Option B (Manual):**
     ```bash
     pip install requests aiohttp colorama pyyaml python-dotenv beautifulsoup4 lxml asyncio aiofiles pytest black flake8
     ```
5. Run the tool:
   ```bash
   python main.py
   ```

### 🍎 iOS (a-Shell)
1. Install **a-Shell** from the App Store.
2. Clone the repository:
   ```bash
   git clone https://github.com/Quincunx33/EthicalHackingTools.git
   cd EthicalHackingTools
   ```
3. Install dependencies:
   - **Option A:**
     ```bash
     pip install -r requirements.txt
     ```
   - **Option B:**
     ```bash
     pip install requests aiohttp colorama pyyaml python-dotenv beautifulsoup4 lxml asyncio aiofiles
     ```

### 🐧 Linux (Ubuntu/Kali/Debian)
1. Update system and install base tools:
   ```bash
   sudo apt update && sudo apt install python3 python3-pip git -y
   ```
2. Clone the repository:
   ```bash
   git clone https://github.com/Quincunx33/EthicalHackingTools.git
   cd EthicalHackingTools
   ```
3. Install requirements:
   - **Option A:**
     ```bash
     pip3 install -r requirements.txt
     ```
   - **Option B:**
     ```bash
     pip3 install requests aiohttp colorama pyyaml python-dotenv beautifulsoup4 lxml asyncio aiofiles pytest black flake8
     ```
4. Run the tool:
   ```bash
   python3 main.py
   ```

### 🪟 Windows
1. Install [Python 3.10+](https://www.python.org/downloads/) (Ensure "Add Python to PATH" is checked).
2. Open PowerShell or CMD:
   ```powershell
   git clone https://github.com/Quincunx33/EthicalHackingTools.git
   cd EthicalHackingTools
   ```
3. Install libraries:
   - **Option A:**
     ```powershell
     pip install -r requirements.txt
     ```
   - **Option B:**
     ```powershell
     pip install requests aiohttp colorama pyyaml python-dotenv beautifulsoup4 lxml asyncio aiofiles pytest black flake8
     ```
4. Run the tool:
   ```powershell
   python main.py
   ```

---

## 📦 Required Tools & Libraries
The framework relies on the following Python packages:
- **Networking:** `requests`, `aiohttp`
- **UI/UX:** `colorama`
- **Configuration:** `pyyaml`, `python-dotenv`
- **Parsing:** `beautifulsoup4`, `lxml`
- **Async Operations:** `asyncio`, `aiofiles`
- **Development:** `pytest`, `black`, `flake8`

---

## 📦 Legacy Version
The previous tools have been archived:
👉 [**v1.0-old-tools Release**](https://github.com/Quincunx33/EthicalHackingTools/releases/tag/v1.0-old-tools)

---

## 📜 Disclaimer
> **WARNING:** This tool is for **Ethical Hacking** and **Educational Purposes** only. Unauthorized use is illegal.

---
**Maintained by:** [Quincunx33](https://github.com/Quincunx33)
