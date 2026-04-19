# 🛡️ HackerAI Framework (Project Sirra)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Security Status](https://img.shields.io/badge/Security-Audited-brightgreen.svg)]()

**HackerAI Framework** (codenamed **Sirra**) is a next-generation, modular security testing environment designed for ethical hackers, security researchers, and automated vulnerability assessment. It provides a robust orchestration layer to manage, scan, and execute security modules within a controlled sandbox environment.

---

## 🚀 Key Features

- **Universal Orchestrator:** A centralized "Brain" (`core/orchestrator.py`) that manages module lifecycles, execution, and security policies.
- **Security Sandbox:** Advanced execution environment with automated security scanning for custom modules.
- **Modular Architecture:** Easily plug-in new scanners, exploit testers, or utility modules.
- **Built-in Security Scanner:** Automatically detects potential syntax errors and security risks in newly added modules.
- **Comprehensive Logging:** Integrated logging system for audit trails and debugging.
- **Reporting Engine:** Generate professional security reports automatically after scans.

---

## 📁 Project Structure

```text
HackerAI_Framework/
├── main.py                # Entry point of the framework
├── requirements.txt       # Python dependencies
├── core/                  # Core orchestration and engine logic
│   ├── orchestrator.py    # The "Brain" of the system
│   └── init.py            # Core initialization
├── modules/               # Pluggable security modules
│   ├── scanner/           # Vulnerability scanning modules
│   └── test/              # Stress testing and exploit modules
├── config/                # Configuration and wordlists
│   ├── settings.json      # Global framework settings
│   └── wordlists/         # Dictionaries for brute-forcing
├── utils/                 # Helper utilities (Logging, Reporting)
└── docs/                  # Technical documentation
```

---

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Quincunx33/EthicalHackingTools.git
   cd EthicalHackingTools
   ```

2. **Install Dependencies:**
   Ensure you have Python 3.8+ installed.
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Usage

### Starting the Framework
Run the main entry point to start the orchestrator:
```bash
python main.py
```

### Adding Custom Modules
You can extend the framework by adding your own Python scripts to the `modules/` directory. The orchestrator will automatically:
1. Detect the new module.
2. Run a security scan on the code.
3. Register it for execution if it passes the safety checks.

---

## 🛡️ Security & Sandbox
The framework includes a **Safe Import System** and a **Global Sandbox Namespace**. This ensures that even if a third-party module is executed, it operates within restricted boundaries unless explicitly granted permissions.

---

## 📦 Legacy Version
The previous collection of tools has been archived. You can access the old version here:
👉 [**v1.0-old-tools Release**](https://github.com/Quincunx33/EthicalHackingTools/releases/tag/v1.0-old-tools)

---

## 🤝 Contributing
Contributions are welcome! Please follow these steps:
1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m "Add some AmazingFeature" `).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📜 Disclaimer
> **WARNING:** This tool is intended for **Ethical Hacking** and **Educational Purposes** only. Unauthorized access to computer systems is illegal. The developers are not responsible for any misuse of this framework.

---
**Maintained by:** [Quincunx33](https://github.com/Quincunx33)
