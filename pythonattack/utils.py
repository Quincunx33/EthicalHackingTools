import os
import sys
import time
import json
import random
import socket
import requests
import warnings
from urllib.parse import urljoin, urlparse, quote
from urllib3.exceptions import InsecureRequestWarning
from config import *

warnings.filterwarnings("ignore", category=DeprecationWarning)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# USER AGENT MANAGEMENT
def get_random_ua():
    """Get random user agent"""
    try:
        from fake_useragent import UserAgent
        ua = UserAgent(fallback="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        return ua.random
    except ImportError:
        return random.choice(UA_LIST_BACKUP)

def clean():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def get_headers():
    """Get headers with random user agent"""
    return {
        'User-Agent': get_random_ua(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }

def get_session(proxy_manager=None):
    """Get requests session with proxy support"""
    session = requests.Session()
    session.headers.update(get_headers())
    session.verify = False
    session.timeout = 10
    
    if proxy_manager:
        proxy = proxy_manager.get_proxy()
        if proxy:
            session.proxies = {
                'http': proxy,
                'https': proxy
            }
    
    return session

def save_finding(finding_type, target, details):
    """Save findings to JSON report"""
    try:
        data = {}
        if os.path.exists(REPORT_FILE):
            with open(REPORT_FILE, 'r') as f:
                data = json.load(f)
        
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        if target not in data:
            data[target] = {}
        if finding_type not in data[target]:
            data[target][finding_type] = []
        
        details['timestamp'] = timestamp
        data[target][finding_type].append(details)
        
        with open(REPORT_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        
        return True
    except Exception as e:
        print(f"{R}[!] Error saving report: {e}{W}")
        return False

def get_local_ip():
    """Get local IP address automatically"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "192.168.1.100"