#!/usr/bin/env python3

import asyncio
import sys
import time
import os
from config import *
from menu import MenuSystem
from utils import get_local_ip, clean

# Update LHOST with local IP at startup
LHOST = get_local_ip()

if __name__ == "__main__":
    # Check dependencies
    try:
        import aiohttp
        import requests
        print(f"{G}[✓] Core dependencies loaded{W}")
    except ImportError as e:
        print(f"{R}[!] Missing dependency: {e}{W}")
        print(f"{Y}[*] Install with: pip install aiohttp requests{W}")
        sys.exit(1)
    
    # Display disclaimer
    clean()
    print(f"""{R}
    ╔══════════════════════════════════════════════╗
    ║           SECURITY DISCLAIMER                ║
    ╠══════════════════════════════════════════════╣
    ║ This tool is for EDUCATIONAL and AUTHORIZED  ║
    ║ security testing only. Use only on systems   ║
    ║ you own or have explicit permission to test. ║
    ║                                              ║
    ║ The developer is NOT responsible for any     ║
    ║ misuse or damage caused by this tool.        ║
    ╚══════════════════════════════════════════════╝{W}""")
    
    input(f"\n{Y}Press Enter to accept and continue...{W}")
    
    # Start main menu
    try:
        menu_system = MenuSystem()
        menu_system.main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Y}[*] Program terminated by user.{W}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{R}[!] Critical error: {e}{W}")
        import traceback
        traceback.print_exc()
        sys.exit(1)