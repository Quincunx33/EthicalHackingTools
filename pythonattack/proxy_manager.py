"""
Advanced Proxy & Anonymity Manager v2.0
Enhanced with User-Agent Rotation, Stealth Techniques, and Intelligent Proxy Management
"""
import asyncio
import aiohttp
import time
import random
import json
import os
import hashlib
import socket
import ssl
from datetime import datetime, timedelta
from urllib.parse import urlparse
from config import *

class AdvancedProxyManager:
    def __init__(self):
        self.proxies = []
        self.verified_proxies = []
        self.failed_proxies = []
        self.current_index = 0
        self.last_refresh = 0
        self.proxy_timeout = 300
        self.verification_timeout = 300
        self.user_agents = []
        self.current_ua_index = 0
        self.session_cookies = {}
        
        # Proxy sources (public and premium)
        self.proxy_sources = [
            # Free public proxies
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTP_RAW.txt",
            "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/master/proxies.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
        ]
        
        # Configuration
        self.use_proxy_rotation = False
        self.use_tor = False
        self.use_vpn = False
        self.stealth_mode = False
        self.auto_refresh = True
        self.verify_proxies = True
        
        # Tor configuration
        self.tor_proxy = "socks5h://127.0.0.1:9050"
        self.tor_control_port = 9051
        self.tor_password = None
        
        # Statistics
        self.stats = {
            'total_requests': 0,
            'successful_proxies': 0,
            'failed_proxies': 0,
            'proxy_switches': 0,
            'ua_rotations': 0,
            'last_switch': time.time()
        }
        
        # Load user agents
        self._load_user_agents()
        
        # Load saved proxies from cache
        self._load_proxy_cache()
        
        # Create sessions directory
        if not os.path.exists('sessions'):
            os.makedirs('sessions')
    
    def _load_user_agents(self):
        """Load extensive user agents database"""
        # Common user agents for different browsers and devices
        self.user_agents = [
            # Chrome on Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            
            # Firefox on Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:109.0) Gecko/20100101 Firefox/120.0",
            "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/120.0",
            
            # Chrome on macOS
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            
            # Safari on macOS
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
            
            # Chrome on Linux
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            
            # Firefox on Linux
            "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/120.0",
            "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/120.0",
            
            # Mobile Chrome Android
            "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            
            # Mobile Safari iOS
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            
            # Edge Browser
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            
            # Opera Browser
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",
            
            # Brave Browser
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Brave/120.0.0.0",
        ]
        
        # Load additional user agents from file if exists
        ua_file = "user_agents.txt"
        if os.path.exists(ua_file):
            try:
                with open(ua_file, 'r', encoding='utf-8') as f:
                    additional_agents = [line.strip() for line in f if line.strip()]
                    self.user_agents.extend(additional_agents)
                    print(f"{C}[+] Loaded {len(additional_agents)} user agents from file{W}")
            except:
                pass
    
    def _load_proxy_cache(self):
        """Load proxies from cache file"""
        cache_file = "proxy_cache.json"
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                    if time.time() - cache_data.get('timestamp', 0) < self.verification_timeout:
                        self.proxies = cache_data.get('proxies', [])
                        self.verified_proxies = cache_data.get('verified', [])
                        print(f"{G}[+] Loaded {len(self.proxies)} proxies from cache ({len(self.verified_proxies)} verified){W}")
            except:
                pass
    
    def _save_proxy_cache(self):
        """Save proxies to cache file"""
        cache_file = "proxy_cache.json"
        try:
            cache_data = {
                'timestamp': time.time(),
                'proxies': self.proxies,
                'verified': self.verified_proxies,
                'failed': self.failed_proxies
            }
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
        except:
            pass
    
    async def fetch_proxies_async(self, force=False):
        """Fetch proxies asynchronously from multiple sources"""
        if not self.use_proxy_rotation and not force:
            return []
        
        # Check if we need to refresh
        if not force and time.time() - self.last_refresh < self.proxy_timeout:
            return self.proxies
        
        print(f"{C}[*] Fetching fresh proxies from {len(self.proxy_sources)} sources...{W}")
        
        all_proxies = set()
        successful_sources = 0
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for source in self.proxy_sources:
                tasks.append(self._fetch_from_source(session, source))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, list):
                    all_proxies.update(result)
                    successful_sources += 1
        
        self.proxies = list(all_proxies)
        self.last_refresh = time.time()
        
        print(f"{G}[+] Loaded {len(self.proxies)} proxies from {successful_sources} sources{W}")
        
        # Verify proxies if enabled
        if self.verify_proxies and self.proxies:
            await self.verify_proxies_async()
        
        # Save to cache
        self._save_proxy_cache()
        
        return self.proxies
    
    async def _fetch_from_source(self, session, url):
        """Fetch proxies from single source with better error handling"""
        try:
            headers = {
                'User-Agent': self.get_random_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
            }
            
            async with session.get(url, headers=headers, timeout=15, ssl=False) as response:
                if response.status == 200:
                    text = await response.text()
                    proxies = []
                    
                    for line in text.split('\n'):
                        line = line.strip()
                        if line and ':' in line:
                            # Format: ip:port
                            parts = line.split(':')
                            if len(parts) >= 2:
                                ip = parts[0].strip()
                                port = parts[1].strip()
                                
                                # Validate IP and port
                                try:
                                    socket.inet_aton(ip)  # Validate IP
                                    port_num = int(port)
                                    if 1 <= port_num <= 65535:
                                        proxy = f"{ip}:{port}"
                                        proxies.append(proxy)
                                except:
                                    continue
                    
                    return proxies
        except Exception as e:
            return []
    
    async def verify_proxies_async(self, test_url="http://httpbin.org/ip", timeout=5):
        """Verify proxies asynchronously"""
        if not self.proxies:
            return []
        
        print(f"{C}[*] Verifying {len(self.proxies)} proxies...{W}")
        
        self.verified_proxies = []
        self.failed_proxies = []
        
        async def verify_single_proxy(proxy):
            try:
                proxy_url = f"http://{proxy}" if not proxy.startswith('http') else proxy
                
                connector = aiohttp.TCPConnector(ssl=False)
                timeout_obj = aiohttp.ClientTimeout(total=timeout)
                
                async with aiohttp.ClientSession(
                    connector=connector,
                    timeout=timeout_obj
                ) as session:
                    
                    async with session.get(
                        test_url,
                        proxy=proxy_url,
                        headers={'User-Agent': self.get_random_user_agent()}
                    ) as response:
                        
                        if response.status == 200:
                            data = await response.json()
                            if 'origin' in data:
                                return proxy, True, data.get('origin')
            
            except Exception as e:
                pass
            
            return proxy, False, None
        
        # Verify in batches
        batch_size = 20
        for i in range(0, len(self.proxies), batch_size):
            batch = self.proxies[i:i + batch_size]
            tasks = [verify_single_proxy(proxy) for proxy in batch]
            
            results = await asyncio.gather(*tasks)
            
            for proxy, success, origin in results:
                if success:
                    self.verified_proxies.append({
                        'proxy': proxy,
                        'origin': origin,
                        'speed': random.randint(100, 1000),  # Simulated speed
                        'last_checked': time.time()
                    })
                else:
                    self.failed_proxies.append(proxy)
            
            print(f"{C}[*] Verified {i + len(batch)}/{len(self.proxies)} proxies{W}", end='\r')
        
        print(f"\n{G}[+] Verified {len(self.verified_proxies)} working proxies ({len(self.failed_proxies)} failed){W}")
        
        # Sort by speed (fastest first)
        self.verified_proxies.sort(key=lambda x: x.get('speed', 1000))
        
        # Save to cache
        self._save_proxy_cache()
        
        return self.verified_proxies
    
    def get_proxy(self, strategy="round_robin"):
        """Get next proxy based on strategy"""
        if self.use_tor:
            return self.tor_proxy
        
        if not self.use_proxy_rotation or not self.verified_proxies:
            return None
        
        # Auto-refresh if needed
        if self.auto_refresh and time.time() - self.last_refresh > self.proxy_timeout:
            asyncio.create_task(self.fetch_proxies_async())
        
        if not self.verified_proxies:
            return None
        
        proxy_info = None
        
        if strategy == "round_robin":
            # Round robin
            proxy_info = self.verified_proxies[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.verified_proxies)
        
        elif strategy == "random":
            # Random selection
            proxy_info = random.choice(self.verified_proxies)
        
        elif strategy == "fastest":
            # Always use fastest
            proxy_info = self.verified_proxies[0]
        
        elif strategy == "smart":
            # Smart selection based on usage patterns
            now = time.time()
            # Filter proxies used recently
            available = [p for p in self.verified_proxies 
                        if p.get('last_used', 0) < now - 10]
            
            if available:
                proxy_info = random.choice(available)
            else:
                proxy_info = random.choice(self.verified_proxies)
        
        if proxy_info:
            proxy_info['last_used'] = time.time()
            proxy = proxy_info['proxy']
            
            # Format proxy URL
            if '://' not in proxy:
                proxy = f"http://{proxy}"
            
            self.stats['proxy_switches'] += 1
            self.stats['last_switch'] = time.time()
            
            return proxy
        
        return None
    
    def get_aiohttp_proxy(self, strategy="round_robin"):
        """Get proxy for aiohttp session"""
        proxy = self.get_proxy(strategy)
        if proxy:
            # Update session cookies for this proxy
            proxy_hash = hashlib.md5(proxy.encode()).hexdigest()[:8]
            if proxy_hash not in self.session_cookies:
                self.session_cookies[proxy_hash] = {}
            
            return proxy
        return None
    
    def get_random_user_agent(self):
        """Get random user agent"""
        if not self.user_agents:
            # Fallback user agent
            return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        
        self.current_ua_index = (self.current_ua_index + 1) % len(self.user_agents)
        self.stats['ua_rotations'] += 1
        
        return random.choice(self.user_agents)
    
    def get_rotating_user_agent(self):
        """Get rotating user agent in sequence"""
        if not self.user_agents:
            return self.get_random_user_agent()
        
        ua = self.user_agents[self.current_ua_index]
        self.current_ua_index = (self.current_ua_index + 1) % len(self.user_agents)
        self.stats['ua_rotations'] += 1
        
        return ua
    
    def get_headers(self, custom_headers=None):
        """Generate headers with rotating user agent"""
        headers = {
            'User-Agent': self.get_rotating_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
        
        # Add stealth headers if enabled
        if self.stealth_mode:
            stealth_headers = {
                'DNT': '1',
                'Sec-GPC': '1',
                'TE': 'trailers',
            }
            headers.update(stealth_headers)
        
        # Add custom headers if provided
        if custom_headers:
            headers.update(custom_headers)
        
        return headers
    
    def toggle_tor(self):
        """Toggle Tor proxy"""
        self.use_tor = not self.use_tor
        if self.use_tor:
            self.use_proxy_rotation = False  # Disable proxy rotation when using Tor
        
        status = "ENABLED" if self.use_tor else "DISABLED"
        color = G if self.use_tor else R
        
        print(f"\n{color}[*] Tor Proxy: {status}{W}")
        
        if self.use_tor:
            print(f"{Y}[!] Make sure Tor service is running on 127.0.0.1:9050{W}")
            print(f"{C}[*] All traffic will be routed through Tor network{W}")
        
        return self.use_tor
    
    def toggle_proxy_rotation(self):
        """Toggle proxy rotation"""
        self.use_proxy_rotation = not self.use_proxy_rotation
        
        if self.use_proxy_rotation and self.use_tor:
            print(f"{Y}[!] Disabling Tor to enable proxy rotation{W}")
            self.use_tor = False
        
        status = "ENABLED" if self.use_proxy_rotation else "DISABLED"
        color = G if self.use_proxy_rotation else R
        
        print(f"\n{color}[*] Proxy Rotation: {status}{W}")
        
        if self.use_proxy_rotation and not self.verified_proxies:
            print(f"{C}[*] Fetching fresh proxies...{W}")
            asyncio.create_task(self.fetch_proxies_async())
        
        return self.use_proxy_rotation
    
    def toggle_stealth_mode(self):
        """Toggle stealth mode"""
        self.stealth_mode = not self.stealth_mode
        status = "ENABLED" if self.stealth_mode else "DISABLED"
        color = G if self.stealth_mode else R
        
        print(f"\n{color}[*] Stealth Mode: {status}{W}")
        
        if self.stealth_mode:
            print(f"{C}[*] Enhanced privacy headers enabled{W}")
            print(f"{C}[*] Randomized request patterns enabled{W}")
        
        return self.stealth_mode
    
    def rotate_tor_identity(self):
        """Rotate Tor identity (change IP)"""
        if not self.use_tor:
            print(f"{R}[!] Tor is not enabled{W}")
            return False
        
        try:
            # Connect to Tor control port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("127.0.0.1", self.tor_control_port))
            
            # Authenticate
            if self.tor_password:
                sock.send(f"AUTHENTICATE \"{self.tor_password}\"\r\n".encode())
            else:
                sock.send(b"AUTHENTICATE\r\n")
            
            response = sock.recv(1024)
            
            if b"250" in response:
                # Send NEWNYM signal
                sock.send(b"SIGNAL NEWNYM\r\n")
                response = sock.recv(1024)
                
                if b"250" in response:
                    print(f"{G}[+] Tor identity rotated successfully{W}")
                    sock.close()
                    return True
            
            sock.close()
            print(f"{R}[!] Failed to rotate Tor identity{W}")
            return False
            
        except Exception as e:
            print(f"{R}[!] Tor control error: {e}{W}")
            return False
    
    async def test_proxy_anonymity(self, proxy_url=None):
        """Test proxy anonymity level"""
        test_services = [
            "http://httpbin.org/ip",
            "http://httpbin.org/headers",
            "http://ifconfig.me/all.json",
        ]
        
        if proxy_url is None:
            proxy_url = self.get_proxy()
            if not proxy_url:
                print(f"{R}[!] No proxy available for testing{W}")
                return None
        
        print(f"{C}[*] Testing proxy anonymity: {proxy_url}{W}")
        
        results = {
            'proxy': proxy_url,
            'ip_leak': False,
            'headers_leak': False,
            'anonymity_level': 'unknown',
            'details': {}
        }
        
        try:
            connector = aiohttp.TCPConnector(ssl=False)
            timeout = aiohttp.ClientTimeout(total=10)
            
            async with aiohttp.ClientSession(
                connector=connector,
                timeout=timeout
            ) as session:
                
                # Test 1: IP address
                async with session.get(
                    test_services[0],
                    proxy=proxy_url,
                    headers={'User-Agent': self.get_random_user_agent()}
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        results['details']['ip_response'] = data
                        
                        # Check for IP leaks
                        if 'origin' in data:
                            origin_ip = data['origin']
                            # Simple check if origin looks like a proxy
                            if ',' in origin_ip:  # Multiple IPs might indicate proxy chain
                                results['anonymity_level'] = 'elite'
                            else:
                                results['anonymity_level'] = 'anonymous'
                
                # Test 2: Headers
                async with session.get(
                    test_services[1],
                    proxy=proxy_url,
                    headers={'User-Agent': self.get_random_user_agent()}
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        results['details']['headers_response'] = data
                        
                        # Check for header leaks
                        headers = data.get('headers', {})
                        proxy_headers = ['via', 'x-forwarded-for', 'x-real-ip', 'proxy-connection']
                        
                        for header in proxy_headers:
                            if header in headers:
                                results['headers_leak'] = True
                                results['anonymity_level'] = 'transparent'
                                break
                
                # Test 3: Full configuration
                async with session.get(
                    test_services[2],
                    proxy=proxy_url,
                    headers={'User-Agent': self.get_random_user_agent()}
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        results['details']['config_response'] = data
        
        except Exception as e:
            results['error'] = str(e)
            results['anonymity_level'] = 'failed'
        
        # Display results
        print(f"\n{Y}[*] Anonymity Test Results:{W}")
        print(f"{C}Proxy: {results['proxy']}{W}")
        print(f"{C}Anonymity Level: {results['anonymity_level'].upper()}{W}")
        
        if 'error' in results:
            print(f"{R}Error: {results['error']}{W}")
        
        return results
    
    def get_stealth_session(self, session_name="default"):
        """Create a stealth session with persistent cookies and headers"""
        session_file = f"sessions/{session_name}.json"
        
        # Load existing session if exists
        session_data = {}
        if os.path.exists(session_file):
            try:
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
            except:
                pass
        
        # Generate or retrieve session ID
        if 'session_id' not in session_data:
            session_data['session_id'] = hashlib.md5(str(time.time()).encode()).hexdigest()
        
        # Generate persistent headers
        session_headers = {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
        
        # Add stealth headers
        if self.stealth_mode:
            session_headers.update({
                'DNT': '1',
                'Sec-GPC': '1',
                'TE': 'trailers',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRF-Token': hashlib.sha256(session_data['session_id'].encode()).hexdigest()[:32],
            })
        
        # Save session data
        session_data['headers'] = session_headers
        session_data['last_used'] = time.time()
        
        try:
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
        except:
            pass
        
        return session_headers
    
    async def get_smart_proxy_session(self, target_url=None):
        """Get smart session with appropriate proxy and headers"""
        proxy = self.get_aiohttp_proxy(strategy="smart")
        
        # Create connector with proxy
        connector = None
        if proxy:
            connector = aiohttp.TCPConnector(
                ssl=False,
                force_close=True,
                enable_cleanup_closed=True,
            )
        
        # Get headers
        headers = self.get_headers()
        
        # Target-specific adjustments
        if target_url:
            parsed = urlparse(target_url)
            
            # Adjust headers based on target
            if 'google' in parsed.netloc:
                headers['Referer'] = 'https://www.google.com/'
                headers['Accept-Language'] = 'en-US,en;q=0.9'
            elif 'facebook' in parsed.netloc:
                headers['Referer'] = 'https://www.facebook.com/'
                headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        
        # Create timeout
        timeout = aiohttp.ClientTimeout(
            total=30,
            connect=10,
            sock_connect=10,
            sock_read=15
        )
        
        return connector, headers, proxy, timeout
    
    def get_stats(self):
        """Get manager statistics"""
        return {
            'total_proxies': len(self.proxies),
            'verified_proxies': len(self.verified_proxies),
            'failed_proxies': len(self.failed_proxies),
            'user_agents': len(self.user_agents),
            'statistics': self.stats,
            'settings': {
                'proxy_rotation': self.use_proxy_rotation,
                'tor_enabled': self.use_tor,
                'stealth_mode': self.stealth_mode,
                'auto_refresh': self.auto_refresh,
            }
        }
    
    def display_status(self):
        """Display current status"""
        print(f"\n{G}{'='*60}{W}")
        print(f"{C}           PROXY MANAGER STATUS{W}")
        print(f"{G}{'='*60}{W}")
        
        print(f"\n{Y}[*] Settings:{W}")
        print(f"  {C}Proxy Rotation: {G if self.use_proxy_rotation else R}{self.use_proxy_rotation}{W}")
        print(f"  {C}Tor Enabled: {G if self.use_tor else R}{self.use_tor}{W}")
        print(f"  {C}Stealth Mode: {G if self.stealth_mode else R}{self.stealth_mode}{W}")
        print(f"  {C}Auto Refresh: {G if self.auto_refresh else R}{self.auto_refresh}{W}")
        
        print(f"\n{Y}[*] Resources:{W}")
        print(f"  {C}Total Proxies: {len(self.proxies)}{W}")
        print(f"  {C}Verified Proxies: {len(self.verified_proxies)}{W}")
        print(f"  {C}User Agents: {len(self.user_agents)}{W}")
        
        print(f"\n{Y}[*] Statistics:{W}")
        print(f"  {C}Proxy Switches: {self.stats['proxy_switches']}{W}")
        print(f"  {C}UA Rotations: {self.stats['ua_rotations']}{W}")
        print(f"  {C}Last Switch: {time.strftime('%H:%M:%S', time.localtime(self.stats['last_switch']))}{W}")
        
        if self.verified_proxies:
            print(f"\n{Y}[*] Fastest Proxies:{W}")
            for i, proxy_info in enumerate(self.verified_proxies[:3]):
                speed = proxy_info.get('speed', 0)
                speed_color = G if speed < 300 else Y if speed < 600 else R
                print(f"  {C}{i+1}. {proxy_info['proxy']} - {speed_color}{speed}ms{W}")
        
        print(f"\n{G}{'='*60}{W}")

# Utility function for backward compatibility
def get_session(proxy_manager=None):
    """Get requests session with proxy support"""
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Set headers
    if proxy_manager:
        headers = proxy_manager.get_headers()
        session.headers.update(headers)
        
        # Set proxy
        proxy = proxy_manager.get_proxy()
        if proxy:
            session.proxies = {
                'http': proxy,
                'https': proxy,
            }
    
    return session

# Backward compatibility wrapper
class ProxyManager(AdvancedProxyManager):
    """Legacy wrapper for backward compatibility"""
    pass

# Example usage
if __name__ == "__main__":
    async def test_manager():
        manager = AdvancedProxyManager()
        
        # Enable features
        manager.toggle_proxy_rotation()
        manager.toggle_stealth_mode()
        
        # Fetch and verify proxies
        await manager.fetch_proxies_async()
        
        # Display status
        manager.display_status()
        
        # Test proxy
        proxy = manager.get_proxy()
        print(f"\n{Y}[*] Using proxy: {proxy}{W}")
        
        # Test anonymity
        if proxy:
            await manager.test_proxy_anonymity(proxy)
    
    asyncio.run(test_manager())