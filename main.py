#!/usr/bin/env python3
"""
Sirra Framework v4.5 - Professional Security Tool
Enhanced with Security Features and Liability Disclaimer
Author: Security Team
Version: 4.5.0

Disclaimer: We are not responsible for any malicious modules added by the user. Use at your own risk.
"""

import os
import sys
import json
import time
import signal
import textwrap
import random
import threading
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Fix encoding for all platforms
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# First, try to import colorama before dependency check
try:
    from colorama import init, Fore, Back, Style
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

# Simple color class if colorama not available
class SimpleColors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_WHITE = '\033[97m'

# Dependency check
def check_dependencies():
    """Check and install missing dependencies"""
    required_packages = ['requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("\n" + "="*60)
        print(" MISSING DEPENDENCIES ".center(60, "!"))
        print("="*60)
        print("\nThe following packages are required but not installed:")
        for pkg in missing_packages:
            print(f"  - {pkg}")
        
        print("\n" + "-"*60)
        print("To install missing packages, run:")
        print(f"  pip install {' '.join(missing_packages)}")
        
        print("\n" + "="*60)
        
        # Auto-fix suggestion
        try:
            confirm = input("\nDo you want to install missing packages now? (y/N): ").strip().lower()
            if confirm == 'y':
                subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
                print("\n[✓] Dependencies installed successfully!")
                print("[*] Please restart the application.")
                return True
        except:
            print("\n[!] Automatic installation failed.")
            print("[*] Please install packages manually.")
        
        return False
    
    return True

# Check dependencies before proceeding
if not check_dependencies():
    print("\n[!] Exiting due to missing dependencies.")
    sys.exit(1)

# Now import dependencies
import requests

# Initialize colorama if available
if COLORAMA_AVAILABLE:
    init(autoreset=True)

# Import local modules
try:
    from core.orchestrator import get_brain
    # Create utils/common if it doesn't exist
    try:
        from utils.common import Colors, clean_screen
    except ImportError:
        # Define Colors class locally
        class Colors:
            CYAN = SimpleColors.CYAN
            GREEN = SimpleColors.GREEN
            YELLOW = SimpleColors.YELLOW
            RED = SimpleColors.RED
            BLUE = SimpleColors.BLUE
            MAGENTA = SimpleColors.MAGENTA
            WHITE = SimpleColors.WHITE
            RESET = SimpleColors.RESET
            BRIGHT_CYAN = SimpleColors.BRIGHT_CYAN
            BRIGHT_GREEN = SimpleColors.BRIGHT_GREEN
            BRIGHT_YELLOW = SimpleColors.BRIGHT_YELLOW
            BRIGHT_BLUE = SimpleColors.BRIGHT_BLUE
            BRIGHT_MAGENTA = SimpleColors.BRIGHT_MAGENTA
            BRIGHT_WHITE = SimpleColors.BRIGHT_WHITE
        
        # Define clean_screen function
        def clean_screen():
            os.system('cls' if os.name == 'nt' else 'clear')
        
        print("[*] Using built-in utilities")
except ImportError as e:
    print(f"\n[!] Error importing local modules: {e}")
    print("[*] Creating directory structure...")
    
    # Create directory structure
    BASE_DIR = Path(__file__).resolve().parent
    for dir_name in ["core", "utils", "modules", "config", "output", "logs"]:
        (BASE_DIR / dir_name).mkdir(exist_ok=True)
    
    # Create __init__.py files
    for init_file in ["core/__init__.py", "utils/__init__.py"]:
        (BASE_DIR / init_file).touch()
    
    print("[✓] Directory structure created")
    print("[*] Please restart the application.")
    sys.exit(1)

# Dynamic path management
BASE_DIR = Path(__file__).resolve().parent

# Color setup using our Colors class
C, G, Y, R, B, M, W, RS = Colors.CYAN, Colors.GREEN, Colors.YELLOW, Colors.RED, Colors.BLUE, Colors.MAGENTA, Colors.WHITE, Colors.RESET
BC, BG, BY, BB, BM, BW = Colors.BRIGHT_CYAN, Colors.BRIGHT_GREEN, Colors.BRIGHT_YELLOW, Colors.BRIGHT_BLUE, Colors.BRIGHT_MAGENTA, Colors.BRIGHT_WHITE


class ProxyManager:
    """Professional proxy management with rotation"""
    
    def __init__(self, proxy_list: List[str] = None):
        self.proxies = proxy_list or []
        self.current_index = 0
        self.rotation_lock = threading.Lock()
        self.rotation_count = 0
        self.failed_proxies = set()
        
    def add_proxy(self, proxy: str) -> bool:
        """Add a proxy to the list"""
        if self.validate_proxy_format(proxy) and proxy not in self.proxies:
            self.proxies.append(proxy)
            return True
        return False
    
    def validate_proxy_format(self, proxy: str) -> bool:
        """Validate proxy format (IP:Port or protocol://IP:Port)"""
        proxy = proxy.strip()
        
        # Check if it has protocol prefix
        if '://' in proxy:
            protocol, address = proxy.split('://', 1)
            if protocol not in ['http', 'https', 'socks4', 'socks5']:
                return False
        else:
            address = proxy
        
        # Validate IP:Port format
        if ':' not in address:
            return False
        
        ip, port = address.split(':', 1)
        
        # Validate IP
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        
        for part in parts:
            if not part.isdigit():
                return False
            num = int(part)
            if num < 0 or num > 255:
                return False
        
        # Validate port
        if not port.isdigit():
            return False
        
        port_num = int(port)
        if port_num < 1 or port_num > 65535:
            return False
        
        return True
    
    def rotate_proxy(self) -> Optional[Dict[str, str]]:
        """Get next proxy with rotation"""
        if not self.proxies:
            return None
        
        with self.rotation_lock:
            # Filter out failed proxies
            available_proxies = [p for p in self.proxies if p not in self.failed_proxies]
            
            if not available_proxies:
                # Reset if all proxies failed
                self.failed_proxies.clear()
                available_proxies = self.proxies
            
            # Select proxy based on mode (simple round-robin)
            if self.current_index >= len(available_proxies):
                self.current_index = 0
            
            selected_proxy = available_proxies[self.current_index]
            self.current_index = (self.current_index + 1) % len(available_proxies)
            self.rotation_count += 1
            
            # Format proxy dict for requests
            if '://' in selected_proxy:
                return {'http': selected_proxy, 'https': selected_proxy}
            else:
                return {'http': f'http://{selected_proxy}', 'https': f'http://{selected_proxy}'}
    
    def mark_failed(self, proxy: str):
        """Mark a proxy as failed"""
        self.failed_proxies.add(proxy)
    
    def clear_failed(self):
        """Clear failed proxies list"""
        self.failed_proxies.clear()
    
    def get_random_proxy(self) -> Optional[Dict[str, str]]:
        """Get a random proxy"""
        if not self.proxies:
            return None
        
        available_proxies = [p for p in self.proxies if p not in self.failed_proxies]
        
        if not available_proxies:
            self.failed_proxies.clear()
            available_proxies = self.proxies
        
        selected = random.choice(available_proxies)
        
        if '://' in selected:
            return {'http': selected, 'https': selected}
        else:
            return {'http': f'http://{selected}', 'https': f'http://{selected}'}
    
    def get_count(self) -> int:
        """Get total proxy count"""
        return len(self.proxies)
    
    def get_active_count(self) -> int:
        """Get active (non-failed) proxy count"""
        return len([p for p in self.proxies if p not in self.failed_proxies])


class SirraFramework:
    def __init__(self):
        """Initialize the framework"""
        try:
            self.brain = get_brain()
            self.config_dir = BASE_DIR / "config"
            self.config_file = self.config_dir / "settings.json"
            self.running = True
            self._exit_flag = False
            
            # Initialize proxy manager
            self.proxy_manager = None
            
            # Default settings - COMPLETE DEFAULTS
            self.default_settings = {
                "proxy_mode": "Rotate",
                "proxy_list": [], 
                "custom_names": {},
                "auto_refresh_proxies": True,
                "request_timeout": 10,
                "max_threads": 5,
                "log_level": "INFO",
                "output_format": "text",
                "save_logs": True,
                "enable_security_scan": True,
                "disable_security": False,
                "show_disclaimer": True,
                "proxy_test_enabled": True,
                "auto_remove_failed_proxies": True,
                "max_retry_attempts": 3,
                "theme": "dark",
                "compact_mode": False,
                "font_size": "normal"
            }
            
            # Initialize with defaults
            self.settings = self.default_settings.copy()
            
            self.stats = {
                "rotations": 0, 
                "current_ip": "Direct Connection",
                "total_scans": 0,
                "successful_scans": 0,
                "failed_scans": 0,
                "security_blocks": 0,
                "proxy_failures": 0,
                "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_execution_time": 0
            }
            
            self.load_settings()
            
            # Initialize proxy manager with loaded proxies
            self.proxy_manager = ProxyManager(self.settings['proxy_list'])
            
            # Setup signal handler
            self._setup_signal_handler()
            
            print(f"{G}[✓] Sirra Framework initialized successfully{RS}")
            print(f"{G}[✓] Security Scanner: {'ENABLED' if not self.settings['disable_security'] else 'DISABLED'}{RS}")
            
        except Exception as e:
            self.handle_error(f"Failed to initialize framework: {e}", critical=True)

    def _setup_signal_handler(self):
        """Setup signal handler for graceful shutdown"""
        def signal_handler(signum, frame):
            """Handle Ctrl+C (SIGINT) gracefully"""
            if self._exit_flag:
                # Second Ctrl+C - force exit
                print(f"\n{R}[!] Force exiting...{RS}")
                sys.exit(1)
            
            self._exit_flag = True
            print(f"\n{Y}[!] Interrupt detected. Press Ctrl+C again to force exit.{RS}")
        
        signal.signal(signal.SIGINT, signal_handler)

    def get_terminal_width(self):
        """Get dynamic terminal width with proper fallback"""
        try:
            width = os.get_terminal_size().columns
            
            # Apply compact mode adjustment
            if self.settings.get('compact_mode', False):
                width = min(width, 70)
            
            # Apply font size adjustment
            font_size = self.settings.get('font_size', 'normal')
            if font_size == 'large':
                width = max(width, 80)  # Ensure minimum width for large font
            elif font_size == 'small':
                width = min(width, 100)  # Limit max width for small font
            
            # Ensure reasonable bounds
            width = max(60, min(width, 120))
            
            return width
        except:
            # Fallback based on settings
            if self.settings.get('compact_mode', False):
                return 65
            return 80

    def handle_error(self, message, critical=False):
        """Handle errors with proper logging"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_msg = f"[{timestamp}] ERROR: {message}"
        
        # Print to console
        print(f"\n{R}[!] {message}{RS}")
        
        # Log to file if enabled
        if self.settings.get('save_logs', True):
            log_file = BASE_DIR / "logs" / "error.log"
            try:
                log_file.parent.mkdir(exist_ok=True)
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(error_msg + "\n")
            except:
                pass
        
        if critical:
            print(f"\n{R}[!] Critical error. Exiting...{RS}")
            sys.exit(1)
        
        time.sleep(2)

    def load_settings(self):
        """Load settings from JSON file with recovery - FIXED VERSION"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                
                if not isinstance(loaded_data, dict):
                    print(f"{Y}[*] Settings file corrupted. Creating backup...{RS}")
                    self._backup_settings_file()
                    raise ValueError("Settings file must contain a JSON object")
                
                # Merge loaded data with defaults (ensuring all keys exist)
                for key in self.default_settings:
                    if key in loaded_data:
                        # Type validation and assignment
                        value = loaded_data[key]
                        
                        if key in ['request_timeout', 'max_threads', 'max_retry_attempts']:
                            if isinstance(value, (int, float)) and value > 0:
                                self.settings[key] = int(value)
                        elif key in ['auto_refresh_proxies', 'save_logs', 'enable_security_scan', 
                                   'disable_security', 'show_disclaimer', 'proxy_test_enabled',
                                   'auto_remove_failed_proxies', 'compact_mode']:
                            if isinstance(value, bool):
                                self.settings[key] = value
                        elif key == 'proxy_mode':
                            if value in ['Direct', 'Rotate', 'Random']:
                                self.settings[key] = value
                        elif key == 'log_level':
                            if value in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
                                self.settings[key] = value
                        elif key == 'output_format':
                            if value in ['text', 'json', 'csv', 'html']:
                                self.settings[key] = value
                        elif key == 'proxy_list':
                            if isinstance(value, list):
                                self.settings[key] = value
                        elif key == 'theme':
                            if value in ['dark', 'light', 'auto']:
                                self.settings[key] = value
                        elif key == 'font_size':
                            if value in ['small', 'normal', 'large']:
                                self.settings[key] = value
                        elif key == 'custom_names':
                            if isinstance(value, dict):
                                self.settings[key] = value
                    else:
                        # Key not in loaded data, use default
                        self.settings[key] = self.default_settings[key]
                
                print(f"{G}[✓] Settings loaded successfully{RS}")
                
            except json.JSONDecodeError as e:
                self.handle_error(f"JSON syntax error in settings file: {e}")
                print(f"{Y}[*] Creating new settings file with defaults...{RS}")
                self._backup_settings_file()
                self.save_settings()
            except Exception as e:
                self.handle_error(f"Error loading settings: {e}")
                print(f"{Y}[*] Using default settings...{RS}")
                self.settings = self.default_settings.copy()
                self.save_settings()
        else:
            print(f"{Y}[*] Settings file not found. Creating default...{RS}")
            self.save_settings()

    def _backup_settings_file(self):
        """Backup corrupted settings file"""
        if self.config_file.exists():
            backup_file = self.config_file.with_suffix('.json.bak')
            try:
                import shutil
                shutil.copy2(self.config_file, backup_file)
                print(f"{G}[✓] Settings backed up to: {backup_file}{RS}")
            except:
                print(f"{R}[!] Failed to backup settings{RS}")

    def save_settings(self):
        """Save settings to JSON file"""
        try:
            self.config_dir.mkdir(exist_ok=True)
            
            # Update proxy list from manager if exists
            if self.proxy_manager:
                self.settings['proxy_list'] = self.proxy_manager.proxies
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False, sort_keys=True)
            
            print(f"{G}[✓] Settings saved{RS}")
            return True
            
        except Exception as e:
            self.handle_error(f"Failed to save settings: {e}")
            return False

    def banner(self):
        """Display application banner with disclaimer"""
        clean_screen()
        
        # Get dynamic width
        width = self.get_terminal_width()
        
        # Liability Disclaimer
        if self.settings.get('show_disclaimer', True):
            disclaimer = "⚠️ DISCLAIMER: We are not responsible for any malicious modules added by the user. Use at your own risk."
            disclaimer_lines = textwrap.wrap(disclaimer, width=width-4)
            
            print(f"{R}┌{'─' * (width - 2)}┐{RS}")
            for line in disclaimer_lines:
                print(f"{R}│ {line.center(width - 4)} │{RS}")
            print(f"{R}└{'─' * (width - 2)}┘{RS}")
            print()
        
        # Main Banner
        print(f"{BC}┌{'─' * (width - 2)}┐{RS}")
        
        # ASCII Art - Responsive
        if width >= 80:
            ascii_art = [
                "███████╗██╗██████╗ ██████╗  █████╗ ",
                "██╔════╝██║██╔══██╗██╔══██╗██╔══██╗",
                "███████╗██║██████╔╝██████╔╝███████║",
                "╚════██║██║██╔══██╗██╔══██╗██╔══██║",
                "███████║██║██║  ██║██║  ██║██║  ██║",
                "╚══════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝"
            ]
        elif width >= 70:
            ascii_art = [
                "███████╗██╗██████╗ ██████╗  █████╗",
                "██╔════╝██║██╔══██╗██╔══██╗██╔══██╗",
                "███████╗██║██████╔╝██████╔╝███████║",
                "╚════██║██║██╔══██╗██╔══██╗██╔══██║",
                "███████║██║██║  ██║██║  ██║██║  ██║",
                "╚══════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝"
            ]
        else:  # Compact mode
            ascii_art = [
                "SIRRA FRAMEWORK",
                "v4.5 - Professional Edition"
            ]
        
        for line in ascii_art:
            print(f"{BC}│{BW}{line.center(width - 2)}{BC}│{RS}")
        
        if width >= 70:
            print(f"{BC}│{BW}{'v4.5 - Professional Edition'.center(width - 2)}{BC}│{RS}")
            print(f"{BC}│{BW}{'With Enhanced Security Scanner'.center(width - 2)}{BC}│{RS}")
        
        print(f"{BC}└{'─' * (width - 2)}┘{RS}")
        
        # Status line
        proxy_status = ""
        if self.proxy_manager:
            if self.settings['proxy_mode'] == 'Direct':
                proxy_status = "Direct Connection"
            else:
                active = self.proxy_manager.get_active_count()
                total = self.proxy_manager.get_count()
                proxy_status = f"{self.settings['proxy_mode']} ({active}/{total})"
        
        status = f"{BC}┣{RS} MODE: {BY}{proxy_status}{RS} | SCANS: {BY}{self.stats['total_scans']}{RS} {BC}┫{RS}"
        print(status.center(width + 10))
        
        # Stats
        success_rate = 0
        if self.stats['total_scans'] > 0:
            success_rate = (self.stats['successful_scans'] / self.stats['total_scans']) * 100
        
        stats_line = f"{BC}📊 Success: {G}{self.stats['successful_scans']}{RS} | Failed: {R}{self.stats['failed_scans']}{RS} | Rate: {BY}{success_rate:.1f}%{RS}"
        print(stats_line.center(width + 10))
        
        # Security stats
        security_status = f"{R}🛡️ Security: DISABLED{RS}" if self.settings['disable_security'] else f"{G}🛡️ Security: ENABLED{RS}"
        print(security_status.center(width + 10))
        
        if self.stats.get('security_blocks', 0) > 0:
            security_line = f"{R}🚫 Security Blocks: {self.stats['security_blocks']}{RS}"
            print(security_line.center(width + 10))
        
        print()

    def fetch_proxies(self, test_proxies=True):
        """Fetch fresh proxy list and test them"""
        print(f"\n{Y}[*] Fetching fresh proxy list...{RS}")
        
        try:
            sources = [
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
                "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt",
                "https://www.proxy-list.download/api/v1/get?type=http"
            ]
            
            all_proxies = []
            timeout = self.settings.get('request_timeout', 10)
            
            for url in sources:
                try:
                    headers = {'User-Agent': 'Mozilla/5.0'}
                    response = requests.get(url, headers=headers, timeout=timeout)
                    response.raise_for_status()
                    
                    raw_proxies = response.text.splitlines()
                    
                    for proxy in raw_proxies:
                        proxy = proxy.strip()
                        if not proxy:
                            continue
                            
                        # Clean and format proxy
                        if '://' in proxy:
                            parts = proxy.split('://')
                            if len(parts) == 2:
                                proxy = parts[1]
                        
                        if ':' in proxy:
                            ip, port = proxy.split(':', 1)
                            if port.isdigit() and 1 <= int(port) <= 65535:
                                if self.validate_ip(ip):
                                    formatted_proxy = f"{ip}:{port}"
                                    if formatted_proxy not in all_proxies:
                                        all_proxies.append(formatted_proxy)
                    
                    print(f"{G}[+] Found {len(raw_proxies)} proxies from source{RS}")
                    
                except Exception as e:
                    print(f"{R}[!] Failed to fetch from {url}: {e}{RS}")
            
            if all_proxies:
                # Test proxies if enabled
                if test_proxies and self.settings.get('proxy_test_enabled', True):
                    print(f"{Y}[*] Testing {len(all_proxies)} proxies...{RS}")
                    working_proxies = self.test_proxies(all_proxies)
                    
                    if working_proxies:
                        self.settings['proxy_list'] = working_proxies
                        if self.proxy_manager:
                            self.proxy_manager.proxies = working_proxies
                            self.proxy_manager.clear_failed()
                        self.save_settings()
                        
                        print(f"{G}[✓] {len(working_proxies)} working proxies loaded{RS}")
                        if len(all_proxies) - len(working_proxies) > 0:
                            print(f"{Y}[*] {len(all_proxies) - len(working_proxies)} proxies failed test{RS}")
                        return True
                    else:
                        print(f"{R}[!] No working proxies found{RS}")
                        return False
                else:
                    # Skip testing, add all proxies
                    self.settings['proxy_list'] = all_proxies
                    if self.proxy_manager:
                        self.proxy_manager.proxies = all_proxies
                    self.save_settings()
                    print(f"{G}[✓] {len(all_proxies)} proxies loaded (untested){RS}")
                    return True
            else:
                print(f"{R}[!] No valid proxies found{RS}")
                
        except Exception as e:
            print(f"{R}[!] Error: {e}{RS}")
        
        return False

    def test_proxies(self, proxies, max_workers=10):
        """Test a list of proxies"""
        import concurrent.futures
        
        test_url = "http://httpbin.org/ip"
        timeout = self.settings.get('request_timeout', 5)
        working_proxies = []
        
        def test_proxy(proxy):
            try:
                proxy_dict = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
                response = requests.get(test_url, proxies=proxy_dict, timeout=timeout)
                if response.status_code == 200:
                    return proxy
            except:
                pass
            return None
        
        print(f"{Y}[*] Testing proxies (max {max_workers} concurrent)...{RS}")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_proxy = {executor.submit(test_proxy, proxy): proxy for proxy in proxies[:100]}  # Test first 100
            
            for future in concurrent.futures.as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                try:
                    result = future.result(timeout=timeout + 2)
                    if result:
                        working_proxies.append(result)
                        print(f"{G}[+] Working: {result}{RS}", end='\r')
                except:
                    pass
        
        print()  # New line after progress
        return working_proxies

    def validate_ip(self, ip):
        """Basic IP validation"""
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        
        for part in parts:
            if not part.isdigit():
                return False
            num = int(part)
            if num < 0 or num > 255:
                return False
        
        return True

    def get_proxy_for_request(self):
        """Get proxy based on current mode"""
        if self.settings['proxy_mode'] == 'Direct' or not self.proxy_manager:
            return None
        
        if self.settings['proxy_mode'] == 'Rotate':
            return self.proxy_manager.rotate_proxy()
        elif self.settings['proxy_mode'] == 'Random':
            return self.proxy_manager.get_random_proxy()
        
        return None

    def get_user_inputs(self, input_config):
        """Get user inputs based on module configuration"""
        inputs = {}
        
        if not input_config:
            # Default input if no config provided
            target = input(f"\n{BC}│{RS}  {Y}🎯 Target URL/IP: {RS}").strip()
            return {'target': target}
        
        width = self.get_terminal_width()
        
        print(f"\n{BC}┌{'─' * (width - 2)}┐{RS}")
        print(f"{BC}│{BW}  📝 MODULE INPUTS {BW}{' ' * (width - 22)}{BC}│{RS}")
        print(f"{BC}├{'─' * (width - 2)}┤{RS}")
        
        for input_field in input_config:
            name = input_field.get('name', 'input')
            field_type = input_field.get('type', 'text')
            prompt = input_field.get('prompt', f'Enter {name}')
            required = input_field.get('required', True)
            default = input_field.get('default', '')
            choices = input_field.get('choices', [])
            
            while True:
                if field_type == 'select' and choices:
                    # Display choices
                    print(f"{BC}│{RS}  {G}◈ {prompt}{RS}")
                    for idx, choice in enumerate(choices, 1):
                        choice_display = str(choice)
                        if len(choice_display) > width - 15:
                            choice_display = choice_display[:width - 18] + "..."
                        print(f"{BC}│{RS}    {C}{idx}.{RS} {choice_display}")
                    
                    choice_input = input(f"{BC}│{RS}  {Y}Select option (1-{len(choices)}): {RS}").strip()
                    
                    if choice_input.isdigit():
                        idx = int(choice_input)
                        if 1 <= idx <= len(choices):
                            inputs[name] = choices[idx-1]
                            break
                    elif choice_input == '' and not required:
                        inputs[name] = default
                        break
                    
                    print(f"{BC}│{RS}  {R}[!] Invalid selection{RS}")
                
                elif field_type == 'boolean':
                    yn_input = input(f"{BC}│{RS}  {Y}{prompt} (y/N): {RS}").strip().lower()
                    if yn_input in ['y', 'yes']:
                        inputs[name] = True
                    elif yn_input in ['n', 'no', '']:
                        inputs[name] = False
                    break
                
                else:  # text, number, etc.
                    value_input = input(f"{BC}│{RS}  {Y}{prompt}: {RS}").strip()
                    
                    if not value_input and required:
                        if default:
                            inputs[name] = default
                            print(f"{BC}│{RS}  {G}[*] Using default: {default}{RS}")
                            break
                        else:
                            print(f"{BC}│{RS}  {R}[!] This field is required{RS}")
                            continue
                    elif not value_input and not required:
                        inputs[name] = default
                        break
                    else:
                        # Validate based on type
                        if field_type == 'number' and not value_input.replace('.', '', 1).isdigit():
                            print(f"{BC}│{RS}  {R}[!] Please enter a valid number{RS}")
                            continue
                        elif field_type == 'url' and not (value_input.startswith('http://') or value_input.startswith('https://')):
                            print(f"{BC}│{RS}  {Y}[!] URL should start with http:// or https://{RS}")
                            continue
                        elif field_type == 'ip' and not self.validate_ip(value_input):
                            print(f"{BC}│{RS}  {R}[!] Invalid IP address format{RS}")
                            continue
                        
                        inputs[name] = value_input
                        break
        
        print(f"{BC}└{'─' * (width - 2)}┘{RS}")
        return inputs

    def execute_tool(self, tool):
        """Execute selected tool with dynamic inputs and security checks"""
        self.banner()
        
        # Security warning for modules if security is enabled
        if (not self.settings['disable_security'] and 
            tool.get('security_status') != 'SAFE' and 
            self.settings.get('enable_security_scan', True)):
            
            print(f"{R}[!] WARNING: This module has not passed full security scan{RS}")
            print(f"{R}[!] Security Status: {tool.get('security_status', 'UNKNOWN')}{RS}")
            
            confirm = input(f"{Y}Continue anyway? (y/N): {RS}").strip().lower()
            if confirm != 'y':
                print(f"{Y}[*] Execution cancelled{RS}")
                time.sleep(1)
                return
        
        # Module info display
        width = self.get_terminal_width()
        box_width = width - 2

        print(f"{BC}┌{'─' * box_width}┐{RS}")
        print(f"{BC}│{BW}  🚀 MODULE LAUNCHER {BW}{' ' * (box_width - 22)}{BC}│{RS}")
        print(f"{BC}├{'─' * box_width}┤{RS}")
        
        # Module name
        name_display = f"{BG}📦 {tool['display_name']}{RS}"
        print(f"{BC}│ {name_display:<{box_width-3}} {BC}│{RS}")
        
        print(f"{BC}├{'─' * box_width}┤{RS}")
        
        # Module info
        security_status = "DISABLED" if self.settings['disable_security'] else tool.get('security_status', 'UNKNOWN')
        security_color = G if security_status == 'SAFE' or self.settings['disable_security'] else R
        
        info_items = [
            (f"{BC}⚙ {RS}Version", f"{G}{tool.get('version', '1.0.0')}{RS}"),
            (f"{BC}👤 {RS}Author", f"{C}{tool.get('author', 'Unknown')}{RS}"),
            (f"{BC}📁 {RS}Category", f"{Y}{tool.get('category', 'General')}{RS}"),
            (f"{BC}🛡️ {RS}Security", f"{security_color}{security_status}{RS}")
        ]
        
        for label, value in info_items:
            line = f"  {label}: {value}"
            print(f"{BC}│ {line:<{box_width-3}} {BC}│{RS}")
        
        print(f"{BC}├{'─' * box_width}┤{RS}")
        
        # Description
        desc = tool.get('description', 'No description provided')
        print(f"{BC}│{BW}  📄 Description:{RS}{' ' * (box_width - 18)}{BC}│{RS}")
        print(f"{BC}├{'─' * box_width}┤{RS}")
        
        desc_lines = textwrap.wrap(desc, width=box_width-6)
        for line in desc_lines:
            print(f"{BC}│  {W}{line:<{box_width-6}}{BC}  │{RS}")
        
        # Show input configuration if exists
        if 'inputs' in tool and tool['inputs']:
            print(f"{BC}├{'─' * box_width}┤{RS}")
            print(f"{BC}│{BW}  📋 Required Inputs:{RS}{' ' * (box_width - 22)}{BC}│{RS}")
            print(f"{BC}├{'─' * box_width}┤{RS}")
            
            for input_field in tool['inputs']:
                name = input_field.get('name', 'input')
                field_type = input_field.get('type', 'text')
                required = "🔴 Required" if input_field.get('required', True) else "🟢 Optional"
                
                line = f"  • {C}{name}{RS} ({Y}{field_type}{RS}) - {required}"
                print(f"{BC}│ {line:<{box_width-3}} {BC}│{RS}")
        
        print(f"{BC}└{'─' * box_width}┘{RS}")
        
        # Get dynamic inputs based on module configuration
        input_config = tool.get('inputs', [])
        module_inputs = self.get_user_inputs(input_config)
        
        if not module_inputs:
            print(f"\n{R}[!] No inputs provided{RS}")
            time.sleep(1)
            return
        
        # Prepare options
        options = {
            "proxy_mode": self.settings['proxy_mode'],
            "proxy_list": self.settings['proxy_list'],
            "get_proxy": self.get_proxy_for_request,
            "callback": self.update_stats,
            "timeout": self.settings.get('request_timeout', 10),
            "max_threads": self.settings.get('max_threads', 5),
            "security_mode": not self.settings['disable_security'],
            "disable_security": self.settings['disable_security']
        }
        
        print(f"\n{Y}[*] Starting execution...{RS}")
        print(f"{Y}[*] Security Scanner: {'ENABLED' if not self.settings['disable_security'] else 'DISABLED'}{RS}")
        time.sleep(0.5)
        
        start_time = time.time()
        
        try:
            # Execute module with dynamic inputs
            result = self.brain.run_module(
                tool['path'], 
                module_inputs, 
                options,
                disable_security=self.settings['disable_security']
            )
            
            execution_time = time.time() - start_time
            self.stats['total_execution_time'] += execution_time
            
            if result is not None:
                self.stats['total_scans'] += 1
                
                # Check result for success/failure
                if isinstance(result, dict):
                    if result.get('success', True):
                        self.stats['successful_scans'] += 1
                        print(f"\n{G}[✓] Execution successful ({execution_time:.2f}s){RS}")
                    else:
                        self.stats['failed_scans'] += 1
                        error_msg = result.get('error', 'Unknown error')
                        print(f"\n{R}[✗] Execution failed: {error_msg} ({execution_time:.2f}s){RS}")
                else:
                    # Non-dict result assumed successful
                    self.stats['successful_scans'] += 1
                    print(f"\n{G}[✓] Execution completed ({execution_time:.2f}s){RS}")
                
                # Show result if available
                if isinstance(result, dict) and 'result' in result:
                    self.display_result(result['result'])
                    
            else:
                self.stats['total_scans'] += 1
                self.stats['failed_scans'] += 1
                
                if not self.settings['disable_security']:
                    self.stats['security_blocks'] = self.stats.get('security_blocks', 0) + 1
                    print(f"\n{R}[✗] Execution blocked due to security issues{RS}")
                else:
                    print(f"\n{R}[✗] Execution failed{RS}")
                
        except Exception as e:
            self.stats['total_scans'] += 1
            self.stats['failed_scans'] += 1
            self.handle_error(f"Execution failed: {e}")
        
        input(f"\n{G}Press Enter to continue...{RS}")

    def display_result(self, result):
        """Display execution result in appropriate format"""
        width = self.get_terminal_width()
        
        title = " EXECUTION RESULT "
        title_length = len(title)
        
        print(f"\n{BC}┌{'─' * ((width - title_length) // 2 - 1)}{title}{'─' * (width - (width - title_length) // 2 - title_length - 2)}┐{RS}")
        
        if isinstance(result, dict):
            for key, value in result.items():
                if isinstance(value, (dict, list)):
                    value_str = json.dumps(value, indent=2)
                else:
                    value_str = str(value)
                
                # Truncate long values
                if len(value_str) > width - 15:
                    value_str = value_str[:width - 18] + "..."
                
                print(f"{BC}│{RS}  {G}{key}:{RS} {W}{value_str}{RS}")
        
        elif isinstance(result, list):
            max_items = 8 if self.settings.get('compact_mode', False) else 10
            for i, item in enumerate(result[:max_items], 1):
                item_str = str(item)
                if len(item_str) > width - 10:
                    item_str = item_str[:width - 13] + "..."
                print(f"{BC}│{RS}  {G}{i}.{RS} {W}{item_str}{RS}")
            
            if len(result) > max_items:
                print(f"{BC}│{RS}  {Y}... and {len(result) - max_items} more items{RS}")
        
        else:
            result_str = str(result)
            lines = textwrap.wrap(result_str, width=width-6)
            for line in lines:
                print(f"{BC}│{RS}  {W}{line}{RS}")
        
        print(f"{BC}└{'─' * width}┘{RS}")

    def update_stats(self, data):
        """Update statistics with comprehensive data"""
        if isinstance(data, dict):
            for key, value in data.items():
                if key in self.stats:
                    if key == 'rotations':
                        self.stats[key] += value
                    elif key == 'current_ip':
                        self.stats[key] = value
                    elif key == 'proxy_failures':
                        self.stats[key] += 1
                        if self.proxy_manager and 'proxy' in data:
                            self.proxy_manager.mark_failed(data['proxy'])
        else:
            # Simple string IP
            self.stats['current_ip'] = data
            self.stats['rotations'] += 1

    def get_module_icon(self, category):
        """Get icon based on module category"""
        icons = {
            'scanner': '🔍',
            'exploit': '💣',
            'recon': '🕵️',
            'cracker': '🔑',
            'analyzer': '📊',
            'network': '🌐',
            'web': '🕸️',
            'sql': '🗄️',
            'xss': '⚡',
            'default': '⚙️'
        }
        
        if not category:
            return icons['default']
        
        category_lower = category.lower()
        for key, icon in icons.items():
            if key in category_lower:
                return icon
        
        return icons['default']

    def settings_menu(self):
        """Complete settings menu"""
        while True:
            self.banner()
            
            width = self.get_terminal_width()
            
            title = " SETTINGS MENU "
            title_length = len(title)
            
            print(f"{BC}┌{'─' * ((width - title_length) // 2 - 1)}{title}{'─' * (width - (width - title_length) // 2 - title_length - 2)}┐{RS}")
            
            # Create settings display with dynamic spacing
            settings_display = [
                (f"{G}1.{RS}", "Proxy Mode", f"{BY}{self.settings['proxy_mode']}{RS}"),
                (f"{G}2.{RS}", "Disable Security", f"{R if self.settings['disable_security'] else G}{self.settings['disable_security']}{RS}"),
                (f"{G}3.{RS}", "Auto-refresh Proxies", f"{BY}{self.settings.get('auto_refresh_proxies', True)}{RS}"),
                (f"{G}4.{RS}", "Request Timeout", f"{BY}{self.settings.get('request_timeout', 10)}s{RS}"),
                (f"{G}5.{RS}", "Max Threads", f"{BY}{self.settings.get('max_threads', 5)}{RS}"),
                (f"{G}6.{RS}", "Output Format", f"{BY}{self.settings.get('output_format', 'text')}{RS}"),
                (f"{G}7.{RS}", "Log Level", f"{BY}{self.settings.get('log_level', 'INFO')}{RS}"),
                (f"{G}8.{RS}", "Save Logs", f"{BY}{self.settings.get('save_logs', True)}{RS}"),
                (f"{G}9.{RS}", "Security Scanner", f"{BY}{self.settings.get('enable_security_scan', True)}{RS}"),
                (f"{G}10.{RS}", "Show Disclaimer", f"{BY}{self.settings.get('show_disclaimer', True)}{RS}"),
                (f"{G}11.{RS}", "Proxy Test Enabled", f"{BY}{self.settings.get('proxy_test_enabled', True)}{RS}"),
                (f"{G}12.{RS}", "Auto Remove Failed Proxies", f"{BY}{self.settings.get('auto_remove_failed_proxies', True)}{RS}"),
                (f"{G}13.{RS}", "Max Retry Attempts", f"{BY}{self.settings.get('max_retry_attempts', 3)}{RS}"),
                (f"{G}14.{RS}", "Theme", f"{BY}{self.settings.get('theme', 'dark')}{RS}"),
                (f"{G}15.{RS}", "Compact Mode", f"{BY}{self.settings.get('compact_mode', False)}{RS}"),
                (f"{G}16.{RS}", "Font Size", f"{BY}{self.settings.get('font_size', 'normal')}{RS}"),
                (f"{G}17.{RS}", "View/Refresh Proxies"),
                (f"{G}18.{RS}", "Reset to Defaults"),
                (f"{G}19.{RS}", "Save Settings"),
                (f"{R}0.{RS}", "Back to Main Menu")
            ]
            
            for item in settings_display:
                if len(item) == 3:
                    # Format: number, label, value
                    label_width = 30 if width >= 70 else 25
                    value_width = width - label_width - 10
                    
                    label = item[1]
                    if len(label) > label_width - 5:
                        label = label[:label_width - 8] + "..."
                    
                    value = item[2]
                    if len(value) > value_width:
                        value = value[:value_width - 3] + "..."
                    
                    line = f"{item[0]:<4} {label:<{label_width}} {value}"
                    print(f"{BC}│{RS}  {line}")
                else:
                    # Format: number, action
                    print(f"{BC}│{RS}  {item[0]:<4} {item[1]}")
            
            print(f"{BC}└{'─' * width}┘{RS}")
            
            choice = input(f"\n{BC}⚙️  Settings » {RS}").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.change_proxy_mode()
            elif choice == '2':
                self.toggle_setting('disable_security')
            elif choice == '3':
                self.toggle_setting('auto_refresh_proxies')
            elif choice == '4':
                self.change_timeout()
            elif choice == '5':
                self.change_threads()
            elif choice == '6':
                self.change_output_format()
            elif choice == '7':
                self.change_log_level()
            elif choice == '8':
                self.toggle_setting('save_logs')
            elif choice == '9':
                self.toggle_setting('enable_security_scan')
            elif choice == '10':
                self.toggle_setting('show_disclaimer')
            elif choice == '11':
                self.toggle_setting('proxy_test_enabled')
            elif choice == '12':
                self.toggle_setting('auto_remove_failed_proxies')
            elif choice == '13':
                self.change_max_retries()
            elif choice == '14':
                self.change_theme()
            elif choice == '15':
                self.toggle_setting('compact_mode')
                print(f"{G}[✓] Compact mode {'enabled' if self.settings['compact_mode'] else 'disabled'}{RS}")
                time.sleep(1)
                # Force UI refresh by re-banner
                return  # Exit and let main loop refresh
            elif choice == '16':
                self.change_font_size()
                # Force UI refresh
                return
            elif choice == '17':
                self.manage_proxies()
            elif choice == '18':
                self.reset_settings()
                # Force UI refresh
                return
            elif choice == '19':
                self.save_settings()
                time.sleep(1)
            else:
                print(f"{R}[!] Invalid choice{RS}")
                time.sleep(1)

    def change_theme(self):
        """Change application theme"""
        themes = ["dark", "light", "auto"]
        
        width = self.get_terminal_width()
        box_width = min(width, 60)
        
        print(f"\n{BC}┌{'─' * box_width}┐{RS}")
        print(f"{BC}│{BW}  THEME SELECTION {BW}{' ' * (box_width - 20)}{BC}│{RS}")
        print(f"{BC}├{'─' * box_width}┤{RS}")
        
        for i, theme in enumerate(themes, 1):
            icon = "✅" if theme == self.settings.get('theme', 'dark') else "⚪"
            print(f"{BC}│{RS}  {G}{i}.{RS} {icon} {theme:<10}")
        
        print(f"{BC}└{'─' * box_width}┘{RS}")
        
        while True:
            choice = input(f"\n{Y}Select theme (1-{len(themes)}): {RS}").strip()
            
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(themes):
                    self.settings['theme'] = themes[idx-1]
                    print(f"{G}[✓] Theme changed to {themes[idx-1]}{RS}")
                    # Force UI refresh
                    return
            
            print(f"{R}[!] Invalid selection{RS}")

    def change_font_size(self):
        """Change font size"""
        sizes = ["small", "normal", "large"]
        
        width = self.get_terminal_width()
        box_width = min(width, 60)
        
        print(f"\n{BC}┌{'─' * box_width}┐{RS}")
        print(f"{BC}│{BW}  FONT SIZE {BW}{' ' * (box_width - 13)}{BC}│{RS}")
        print(f"{BC}├{'─' * box_width}┤{RS}")
        
        for i, size in enumerate(sizes, 1):
            icon = "✅" if size == self.settings.get('font_size', 'normal') else "⚪"
            print(f"{BC}│{RS}  {G}{i}.{RS} {icon} {size:<10}")
        
        print(f"{BC}└{'─' * box_width}┘{RS}")
        
        while True:
            choice = input(f"\n{Y}Select font size (1-{len(sizes)}): {RS}").strip()
            
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(sizes):
                    self.settings['font_size'] = sizes[idx-1]
                    print(f"{G}[✓] Font size changed to {sizes[idx-1]}{RS}")
                    # Force UI refresh
                    return
            
            print(f"{R}[!] Invalid selection{RS}")

    def change_max_retries(self):
        """Change max retry attempts"""
        width = self.get_terminal_width()
        box_width = min(width, 60)
        
        print(f"\n{BC}┌{'─' * box_width}┐{RS}")
        print(f"{BC}│{BW}  MAX RETRY ATTEMPTS {BW}{' ' * (box_width - 24)}{BC}│{RS}")
        print(f"{BC}├{'─' * box_width}┤{RS}")
        print(f"{BC}│{RS}  Current: {BY}{self.settings.get('max_retry_attempts', 3)} attempts{RS}")
        print(f"{BC}└{'─' * box_width}┘{RS}")
        
        while True:
            try:
                retries = input(f"\n{Y}Enter retry attempts (0-10): {RS}").strip()
                if retries.isdigit():
                    retries_int = int(retries)
                    if 0 <= retries_int <= 10:
                        self.settings['max_retry_attempts'] = retries_int
                        print(f"{G}[✓] Max retries updated{RS}")
                        return
                
                print(f"{R}[!] Must be between 0-10{RS}")
            except ValueError:
                print(f"{R}[!] Invalid number{RS}")

    def change_proxy_mode(self):
        """Change proxy mode"""
        modes = ["Direct", "Rotate", "Random"]
        
        width = self.get_terminal_width()
        box_width = min(width, 60)
        
        print(f"\n{BC}┌{'─' * box_width}┐{RS}")
        print(f"{BC}│{BW}  PROXY MODE {BW}{' ' * (box_width - 14)}{BC}│{RS}")
        print(f"{BC}├{'─' * box_width}┤{RS}")
        
        for i, mode in enumerate(modes, 1):
            icon = "✅" if mode == self.settings['proxy_mode'] else "⚪"
            current = "(Current)" if mode == self.settings['proxy_mode'] else ""
            print(f"{BC}│{RS}  {G}{i}.{RS} {icon} {mode:<10} {current}")
        
        print(f"{BC}└{'─' * box_width}┘{RS}")
        
        while True:
            choice = input(f"\n{Y}Select mode (1-{len(modes)}): {RS}").strip()
            
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(modes):
                    self.settings['proxy_mode'] = modes[idx-1]
                    print(f"{G}[✓] Proxy mode changed to {modes[idx-1]}{RS}")
                    
                    # Update proxy manager if needed
                    if self.proxy_manager and modes[idx-1] != 'Direct':
                        if not self.proxy_manager.proxies:
                            print(f"{Y}[*] No proxies available. Fetching...{RS}")
                            self.fetch_proxies(test_proxies=False)
                    
                    return
            
            print(f"{R}[!] Invalid selection{RS}")

    def toggle_setting(self, setting_name):
        """Toggle a boolean setting"""
        current = self.settings.get(setting_name, False)
        self.settings[setting_name] = not current
        
        # Special handling for certain settings
        if setting_name == 'disable_security':
            status = "DISABLED" if self.settings[setting_name] else "ENABLED"
            status_color = R if self.settings[setting_name] else G
        elif setting_name == 'compact_mode':
            status = "ENABLED" if self.settings[setting_name] else "DISABLED"
            status_color = G if self.settings[setting_name] else R
        else:
            status = "enabled" if self.settings[setting_name] else "disabled"
            status_color = G if self.settings[setting_name] else R
        
        setting_display = setting_name.replace('_', ' ').title()
        print(f"{status_color}[✓] {setting_display} {status}{RS}")
        time.sleep(1)

    def change_timeout(self):
        """Change request timeout"""
        width = self.get_terminal_width()
        box_width = min(width, 60)
        
        print(f"\n{BC}┌{'─' * box_width}┐{RS}")
        print(f"{BC}│{BW}  REQUEST TIMEOUT {BW}{' ' * (box_width - 20)}{BC}│{RS}")
        print(f"{BC}├{'─' * box_width}┤{RS}")
        print(f"{BC}│{RS}  Current: {BY}{self.settings.get('request_timeout', 10)} seconds{RS}")
        print(f"{BC}└{'─' * box_width}┘{RS}")
        
        while True:
            try:
                timeout = input(f"\n{Y}Enter timeout (1-60 seconds): {RS}").strip()
                if timeout.isdigit():
                    timeout_int = int(timeout)
                    if 1 <= timeout_int <= 60:
                        self.settings['request_timeout'] = timeout_int
                        print(f"{G}[✓] Timeout updated to {timeout_int}s{RS}")
                        return
                
                print(f"{R}[!] Must be between 1-60{RS}")
            except ValueError:
                print(f"{R}[!] Invalid number{RS}")

    def change_threads(self):
        """Change max threads"""
        width = self.get_terminal_width()
        box_width = min(width, 60)
        
        print(f"\n{BC}┌{'─' * box_width}┐{RS}")
        print(f"{BC}│{BW}  MAX THREADS {BW}{' ' * (box_width - 15)}{BC}│{RS}")
        print(f"{BC}├{'─' * box_width}┤{RS}")
        print(f"{BC}│{RS}  Current: {BY}{self.settings.get('max_threads', 5)} threads{RS}")
        print(f"{BC}│{RS}  {Y}Note: Higher threads = faster but more resource usage{RS}")
        print(f"{BC}└{'─' * box_width}┘{RS}")
        
        while True:
            try:
                threads = input(f"\n{Y}Enter threads (1-50): {RS}").strip()
                if threads.isdigit():
                    threads_int = int(threads)
                    if 1 <= threads_int <= 50:
                        self.settings['max_threads'] = threads_int
                        print(f"{G}[✓] Thread limit updated to {threads_int}{RS}")
                        return
                
                print(f"{R}[!] Must be between 1-50{RS}")
            except ValueError:
                print(f"{R}[!] Invalid number{RS}")

    def change_output_format(self):
        """Change output format"""
        formats = ["text", "json", "csv", "html"]
        
        width = self.get_terminal_width()
        box_width = min(width, 60)
        
        print(f"\n{BC}┌{'─' * box_width}┐{RS}")
        print(f"{BC}│{BW}  OUTPUT FORMAT {BW}{' ' * (box_width - 18)}{BC}│{RS}")
        print(f"{BC}├{'─' * box_width}┤{RS}")
        
        for i, fmt in enumerate(formats, 1):
            icon = "✅" if fmt == self.settings.get('output_format', 'text') else "⚪"
            print(f"{BC}│{RS}  {G}{i}.{RS} {icon} {fmt:<10}")
        
        print(f"{BC}└{'─' * box_width}┘{RS}")
        
        while True:
            choice = input(f"\n{Y}Select format (1-{len(formats)}): {RS}").strip()
            
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(formats):
                    self.settings['output_format'] = formats[idx-1]
                    print(f"{G}[✓] Output format changed to {formats[idx-1]}{RS}")
                    return
            
            print(f"{R}[!] Invalid selection{RS}")

    def change_log_level(self):
        """Change log level"""
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        
        width = self.get_terminal_width()
        box_width = min(width, 60)
        
        print(f"\n{BC}┌{'─' * box_width}┐{RS}")
        print(f"{BC}│{BW}  LOG LEVEL {BW}{' ' * (box_width - 13)}{BC}│{RS}")
        print(f"{BC}├{'─' * box_width}┤{RS}")
        
        for i, level in enumerate(levels, 1):
            icon = "✅" if level == self.settings.get('log_level', 'INFO') else "⚪"
            print(f"{BC}│{RS}  {G}{i}.{RS} {icon} {level:<10}")
        
        print(f"{BC}└{'─' * box_width}┘{RS}")
        
        while True:
            choice = input(f"\n{Y}Select level (1-{len(levels)}): {RS}").strip()
            
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(levels):
                    self.settings['log_level'] = levels[idx-1]
                    print(f"{G}[✓] Log level changed to {levels[idx-1]}{RS}")
                    return
            
            print(f"{R}[!] Invalid selection{RS}")

    def manage_proxies(self):
        """Manage proxy list"""
        while True:
            self.banner()
            
            proxy_count = self.proxy_manager.get_count() if self.proxy_manager else 0
            active_count = self.proxy_manager.get_active_count() if self.proxy_manager else 0
            
            width = self.get_terminal_width()
            
            title = " PROXY MANAGEMENT "
            title_length = len(title)
            
            print(f"{BC}┌{'─' * ((width - title_length) // 2 - 1)}{title}{'─' * (width - (width - title_length) // 2 - title_length - 2)}┐{RS}")
            print(f"{BC}│{RS}  {G}1.{RS} View Current Proxies ({active_count}/{proxy_count} active)")
            print(f"{BC}│{RS}  {G}2.{RS} Refresh Proxy List")
            print(f"{BC}│{RS}  {G}3.{RS} Add Custom Proxy")
            print(f"{BC}│{RS}  {G}4.{RS} Clear All Proxies")
            print(f"{BC}│{RS}  {G}5.{RS} Test All Proxies")
            print(f"{BC}│{RS}  {G}6.{RS} Clear Failed Proxies")
            print(f"{BC}│{RS}  {R}0.{RS} Back to Settings")
            print(f"{BC}└{'─' * width}┘{RS}")
            
            choice = input(f"\n{BC}📡 Proxy Manager » {RS}").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.view_proxies()
            elif choice == '2':
                self.fetch_proxies(test_proxies=self.settings['proxy_test_enabled'])
                input(f"\n{G}Press Enter to continue...{RS}")
            elif choice == '3':
                self.add_custom_proxy()
            elif choice == '4':
                self.clear_proxies()
            elif choice == '5':
                self.test_current_proxies()
            elif choice == '6':
                self.clear_failed_proxies()

    def test_current_proxies(self):
        """Test current proxy list"""
        if not self.proxy_manager or not self.proxy_manager.proxies:
            print(f"\n{Y}[*] No proxies to test{RS}")
            time.sleep(1)
            return
        
        print(f"\n{Y}[*] Testing {len(self.proxy_manager.proxies)} proxies...{RS}")
        working = self.test_proxies(self.proxy_manager.proxies)
        
        if working:
            self.proxy_manager.proxies = working
            self.proxy_manager.clear_failed()
            self.settings['proxy_list'] = working
            self.save_settings()
            print(f"{G}[✓] {len(working)} working proxies saved{RS}")
        else:
            print(f"{R}[!] No working proxies found{RS}")
        
        time.sleep(2)

    def clear_failed_proxies(self):
        """Clear failed proxies list"""
        if self.proxy_manager:
            self.proxy_manager.clear_failed()
            print(f"{G}[✓] Failed proxies cleared{RS}")
        time.sleep(1)

    def view_proxies(self):
        """View current proxy list with status"""
        if not self.proxy_manager or not self.proxy_manager.proxies:
            print(f"\n{Y}[*] No proxies configured{RS}")
            input(f"\n{G}Press Enter to continue...{RS}")
            return
        
        proxies = self.proxy_manager.proxies
        failed_proxies = self.proxy_manager.failed_proxies
        
        width = self.get_terminal_width()
        
        title = f" CURRENT PROXIES ({len(proxies)}) "
        title_length = len(title)
        
        print(f"\n{BC}┌{'─' * ((width - title_length) // 2 - 1)}{title}{'─' * (width - (width - title_length) // 2 - title_length - 2)}┐{RS}")
        
        active = len([p for p in proxies if p not in failed_proxies])
        status_line = f"  Active: {active} | Failed: {len(failed_proxies)}"
        print(f"{BC}│{BW}{status_line}{RS}{' ' * (width - len(status_line) - 2)}{BC}│{RS}")
        print(f"{BC}├{'─' * width}┤{RS}")
        
        max_display = 12 if self.settings.get('compact_mode', False) else 15
        if width < 70:
            max_display = 8
        
        for i, proxy in enumerate(proxies[:max_display], 1):
            status = f"{R}[FAILED]{RS}" if proxy in failed_proxies else f"{G}[ACTIVE]{RS}"
            proxy_display = proxy
            
            # Calculate available space
            max_proxy_len = width - 15  # Account for number, status and padding
            if len(proxy_display) > max_proxy_len:
                proxy_display = proxy_display[:max_proxy_len - 3] + "..."
            
            print(f"{BC}│{RS}  {G}{i:2}.{RS} {W}{proxy_display}{RS} {status}")
        
        if len(proxies) > max_display:
            print(f"{BC}│{RS}  {Y}... and {len(proxies) - max_display} more{RS}")
        
        print(f"{BC}└{'─' * width}┘{RS}")
        
        input(f"\n{G}Press Enter to continue...{RS}")

    def add_custom_proxy(self):
        """Add custom proxy"""
        width = self.get_terminal_width()
        box_width = min(width, 60)
        
        print(f"\n{BC}┌{'─' * box_width}┐{RS}")
        print(f"{BC}│{BW}  ADD CUSTOM PROXY {BW}{' ' * (box_width - 21)}{BC}│{RS}")
        print(f"{BC}├{'─' * box_width}┤{RS}")
        
        proxy = input(f"{BC}│{RS}  {Y}Enter proxy (IP:Port or protocol://IP:Port): {RS}").strip()
        
        if not proxy:
            print(f"{BC}│{RS}  {R}[!] No proxy entered{RS}")
            print(f"{BC}└{'─' * box_width}┘{RS}")
            time.sleep(1)
            return
        
        # Validate and add proxy
        if self.proxy_manager.add_proxy(proxy):
            self.settings['proxy_list'] = self.proxy_manager.proxies
            self.save_settings()
            print(f"{BC}│{RS}  {G}[✓] Proxy added successfully{RS}")
        else:
            print(f"{BC}│{RS}  {R}[!] Invalid proxy format{RS}")
        
        print(f"{BC}└{'─' * box_width}┘{RS}")
        time.sleep(1)

    def clear_proxies(self):
        """Clear all proxies"""
        confirm = input(f"\n{R}[!] Clear all proxies? (y/N): {RS}").strip().lower()
        if confirm == 'y':
            self.settings['proxy_list'] = []
            if self.proxy_manager:
                self.proxy_manager.proxies = []
                self.proxy_manager.clear_failed()
            self.save_settings()
            print(f"{G}[✓] All proxies cleared{RS}")
        
        time.sleep(1)

    def reset_settings(self):
        """Reset all settings to defaults"""
        width = self.get_terminal_width()
        box_width = min(width, 60)
        
        print(f"\n{BC}┌{'─' * box_width}┐{RS}")
        print(f"{BC}│{BW}  ⚠️  RESET SETTINGS {BW}{' ' * (box_width - 21)}{BC}│{RS}")
        print(f"{BC}├{'─' * box_width}┤{RS}")
        print(f"{BC}│{R}  WARNING: All custom settings will be lost!{RS}{BC}│{RS}")
        print(f"{BC}└{'─' * box_width}┘{RS}")
        
        confirm = input(f"\n{R}Type 'RESET' to confirm: {RS}").strip()
        if confirm == 'RESET':
            self.settings = self.default_settings.copy()
            
            # Reset proxy manager
            self.proxy_manager = ProxyManager()
            
            # Reset stats
            self.stats = {
                "rotations": 0, 
                "current_ip": "Direct Connection",
                "total_scans": 0,
                "successful_scans": 0,
                "failed_scans": 0,
                "security_blocks": 0,
                "proxy_failures": 0,
                "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_execution_time": 0
            }
            
            self.save_settings()
            print(f"{G}[✓] Settings reset to defaults{RS}")
        else:
            print(f"{Y}[*] Reset cancelled{RS}")
        
        time.sleep(1)

    def show_help(self):
        """Show detailed help information"""
        self.banner()
        
        width = self.get_terminal_width()
        
        title = " COMPREHENSIVE HELP "
        title_length = len(title)
        
        print(f"{BC}┌{'─' * ((width - title_length) // 2 - 1)}{title}{'─' * (width - (width - title_length) // 2 - title_length - 2)}┐{RS}")
        
        sections = [
            ("🚀 GETTING STARTED", [
                "1. Select a module by entering its number",
                "2. Enter required inputs when prompted",
                "3. Review results and export if needed",
                "4. Use 'R' to refresh module list"
            ]),
            ("⚙️  SETTINGS GUIDE", [
                "• Proxy Mode: Direct, Rotate, or Random",
                "• Disable Security: Turn off security scanner",
                "• Auto-refresh: Automatically fetch proxies",
                "• Timeout: Adjust request timeout (1-60s)",
                "• Threads: Control concurrent operations",
                "• Output Format: Text, JSON, CSV or HTML"
            ]),
            ("📦 MODULE MANAGEMENT", [
                "• Add modules to 'modules/' directory",
                "• Module format: Python file with run() function",
                "• Define MODULE_INPUTS for custom input fields",
                "• Modules can request specific input types"
            ]),
            ("🛡️  SECURITY FEATURES", [
                "• AST-based security scanner for all modules",
                "• Blocks dangerous imports (os.system, etc.)",
                "• Sandboxed execution environment",
                "• Security status display for each module"
            ]),
            ("🔧 PROXY SYSTEM", [
                "• Direct: No proxy, direct connection",
                "• Rotate: Rotate through proxy list",
                "• Random: Use random proxy each time",
                "• Auto-fetch from multiple sources",
                "• Proxy testing and validation"
            ]),
            ("🎯 UNIVERSAL INPUT SYSTEM", [
                "• Modules define their own input requirements",
                "• Support for: text, number, select, boolean",
                "• Required/optional fields with defaults",
                "• Dynamic input collection"
            ]),
            ("⚠️  SECURITY TIPS", [
                "• Always test on authorized targets only",
                "• Use proxy rotation for anonymity",
                "• Review logs in 'logs/' directory",
                "• Keep framework updated"
            ])
        ]
        
        for title, items in sections:
            print(f"{BC}├{'─' * width}┤{RS}")
            
            # Truncate title if too long
            display_title = f"  {title}"
            if len(display_title) > width - 4:
                display_title = display_title[:width - 7] + "..."
            
            print(f"{BC}│{BW}{display_title}{RS}{' ' * (width - len(display_title) - 2)}{BC}│{RS}")
            print(f"{BC}├{'─' * width}┤{RS}")
            
            for item in items:
                # Handle bullet points
                if item.startswith("• "):
                    display = f"    {item}"
                elif item[0].isdigit() and ". " in item:
                    display = f"  {item}"
                else:
                    display = f"    {item}"
                
                # Truncate long lines
                if len(display) > width - 6:
                    display = display[:width - 9] + "..."
                
                print(f"{BC}│{RS} {display:<{width-3}}{BC}│{RS}")
        
        print(f"{BC}└{'─' * width}┘{RS}")
        
        print(f"\n{BC}🔑 Quick Commands:{RS}")
        print(f"  {G}Number{RS} - Select module  {G}S{RS} - Settings  {G}R{RS} - Refresh")
        print(f"  {G}H{RS} - Help  {G}0{RS} - Exit  {G}Ctrl+C{RS} - Cancel operation")
        
        input(f"\n{G}Press Enter to continue...{RS}")

    def run(self):
        """Main application loop"""
        # Reset exit flag
        self._exit_flag = False
        
        # Initial setup
        if (self.settings.get('auto_refresh_proxies', True) and 
            (not self.proxy_manager or self.proxy_manager.get_count() == 0)):
            print(f"{Y}[*] Initial proxy fetch...{RS}")
            self.fetch_proxies(test_proxies=False)
        
        # Main loop
        while self.running and not self._exit_flag:
            try:
                self.banner()
                
                # Get available modules
                modules = self.brain.get_available_modules()
                
                if not modules:
                    # NO MODULES - Graceful handling
                    width = self.get_terminal_width()
                    
                    title = " WELCOME "
                    title_length = len(title)
                    
                    print(f"{BC}┌{'─' * ((width - title_length) // 2 - 1)}{title}{'─' * (width - (width - title_length) // 2 - title_length - 2)}┐{RS}")
                    print(f"{BC}│{RS}{' ' * width}{BC}│{RS}")
                    
                    no_modules_msg = "⚠️  No modules found!"
                    msg_padding = (width - len(no_modules_msg)) // 2
                    print(f"{BC}│{' ' * msg_padding}{Y}{no_modules_msg}{RS}{' ' * (width - msg_padding - len(no_modules_msg))}{BC}│{RS}")
                    
                    print(f"{BC}│{RS}{' ' * width}{BC}│{RS}")
                    
                    instructions = [
                        "To get started:",
                        "1. Create a 'modules' directory",
                        "2. Add Python files with security tools",
                        "3. Each module should have a run() function",
                        "4. Define MODULE_INPUTS for custom inputs",
                        "5. Avoid dangerous imports (os.system, etc.)",
                        "Example module:",
                        "modules/port_scanner.py"
                    ]
                    
                    for line in instructions:
                        if line.startswith("Example"):
                            line_display = f"  {C}{line}{RS}"
                        else:
                            line_display = f"  {line}"
                        
                        padding = 4
                        print(f"{BC}│{RS}{' ' * padding}{line_display}{' ' * (width - len(line_display) - padding - 2)}{BC}│{RS}")
                    
                    print(f"{BC}│{RS}{' ' * width}{BC}│{RS}")
                    print(f"{BC}└{'─' * width}┘{RS}")
                    
                    print(f"\n{BC}🔑 Quick Actions:{RS}")
                    print(f"  {G}[S]{RS} Settings  {G}[H]{RS} Help  {G}[0]{RS} Exit")
                    
                    choice = input(f"\n{BC}🚀 Sirra » {RS}").strip().lower()
                    
                    if choice == '0':
                        self.confirm_exit()
                    elif choice == 's':
                        self.settings_menu()
                    elif choice == 'h':
                        self.show_help()
                    else:
                        print(f"{R}[!] Invalid choice{RS}")
                        time.sleep(1)
                    
                    continue
                
                # Display modules with security status
                width = self.get_terminal_width()
                
                title = " AVAILABLE TOOLS "
                title_length = len(title)
                
                print(f"{BC}┌{'─' * ((width - title_length) // 2 - 1)}{title}{'─' * (width - (width - title_length) // 2 - title_length - 2)}┐{RS}")
                
                # Calculate columns based on width
                max_name_length = 30
                if width < 70:
                    max_name_length = 25
                if self.settings.get('compact_mode', False):
                    max_name_length = 20
                
                for i, mod in enumerate(modules, 1):
                    # Use custom name or display name
                    name = self.settings['custom_names'].get(mod['path'], mod['display_name'])
                    
                    # Truncate long names
                    if len(name) > max_name_length:
                        name = name[:max_name_length-3] + "..."
                    
                    # Get icon based on category
                    icon = self.get_module_icon(mod.get('category', ''))
                    
                    # Show security status
                    if self.settings['disable_security']:
                        security_icon = "⚪"
                    else:
                        security_icon = "🟢" if mod.get('security_status') == 'SAFE' else "🟡"
                    
                    # Show input count
                    input_count = len(mod.get('inputs', []))
                    input_info = f" [{input_count}]" if input_count > 0 else ""
                    
                    # Show module line
                    line = f"{BC}│{RS}  {G}{i:2}.{RS} {security_icon} {icon} {BW}{name}{RS}{C}{input_info}{RS}"
                    print(f"{line:<{width-3}}{BC}│{RS}")
                
                print(f"{BC}└{'─' * width}┘{RS}")
                
                # Menu options
                print(f"\n{BC}🔧 Quick Menu:{RS}")
                print(f"  {G}[S]{RS} Settings  {G}[R]{RS} Refresh  {G}[H]{RS} Help  {R}[0]{RS} Exit")
                print(f"  {C}[F]{RS} Force Refresh (Skip Cache)")
                
                # Show security status
                security_status = f"{R}SECURITY DISABLED{RS}" if self.settings['disable_security'] else f"{G}SECURITY ENABLED{RS}"
                print(f"  {security_status}")
                
                # Get user choice
                choice = input(f"\n{BC}🚀 Sirra » {RS}").strip().lower()
                
                # Handle choice
                if choice == '0':
                    self.confirm_exit()
                elif choice == 's':
                    self.settings_menu()
                elif choice == 'r':
                    self.brain.refresh_modules()
                    print(f"{G}[✓] Module list refreshed{RS}")
                    time.sleep(1)
                elif choice == 'f':
                    # Force refresh with security scan
                    self.brain._module_cache = []
                    modules = self.brain.get_available_modules(refresh=True)
                    print(f"{G}[✓] Force refresh completed{RS}")
                    time.sleep(1)
                elif choice == 'h':
                    self.show_help()
                elif choice.isdigit():
                    idx = int(choice)
                    if 1 <= idx <= len(modules):
                        self.execute_tool(modules[idx-1])
                    else:
                        print(f"{R}[!] Please select 1-{len(modules)}{RS}")
                        time.sleep(1)
                else:
                    print(f"{R}[!] Invalid input{RS}")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                self._exit_flag = False
                continue
            except Exception as e:
                self.handle_error(f"Main loop error: {e}")

    def confirm_exit(self):
        """Confirm exit"""
        confirm = input(f"\n{Y}Exit Sirra Framework? (y/N): {RS}").strip().lower()
        if confirm == 'y':
            print(f"\n{G}[✓] Thank you for using Sirra Framework!{RS}")
            
            # Show final stats
            if self.stats['total_scans'] > 0:
                success_rate = (self.stats['successful_scans'] / self.stats['total_scans']) * 100
                print(f"{C}📊 Final Stats: {self.stats['successful_scans']}/{self.stats['total_scans']} successful ({success_rate:.1f}%){RS}")
            
            print(f"{C}👋 Goodbye!{RS}")
            self.running = False
        else:
            print(f"{Y}[*] Continue...{RS}")
            time.sleep(1)


if __name__ == "__main__":
    try:
        # Create necessary directories
        BASE_DIR = Path(__file__).resolve().parent
        for dir_name in ["config", "modules", "output", "logs", "core", "utils"]:
            dir_path = BASE_DIR / dir_name
            dir_path.mkdir(exist_ok=True)
        
        # Create __init__.py files
        for init_file in ["core/__init__.py", "utils/__init__.py"]:
            (BASE_DIR / init_file).touch(exist_ok=True)
        
        # Run application
        app = SirraFramework()
        app.run()
        
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Program terminated{RS}")
    except Exception as e:
        print(f"\n{R}[!] Fatal error: {e}{RS}")
        import traceback
        traceback.print_exc()
        sys.exit(1)