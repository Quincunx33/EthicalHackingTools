"""
Common Utilities for Sirra Framework
Version: 1.0.0
"""

import os
import sys
import time
import json
import hashlib
import random
import socket
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import urllib.parse


class Colors:
    """
    ANSI Color Codes for Terminal Output
    Professional color scheme for security tools
    """
    # Reset all formatting
    RESET = '\033[0m'
    
    # Standard colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Text styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    
    # Aliases for common colors
    INFO = CYAN
    SUCCESS = GREEN
    WARNING = YELLOW
    ERROR = RED
    DEBUG = MAGENTA
    HEADER = BRIGHT_CYAN


# Export commonly used color combinations
R = Colors.RED
G = Colors.GREEN
Y = Colors.YELLOW
B = Colors.BLUE
M = Colors.MAGENTA
C = Colors.CYAN
W = Colors.WHITE

BR = Colors.BRIGHT_RED
BG = Colors.BRIGHT_GREEN
BY = Colors.BRIGHT_YELLOW
BB = Colors.BRIGHT_BLUE
BM = Colors.BRIGHT_MAGENTA
BC = Colors.BRIGHT_CYAN
BW = Colors.BRIGHT_WHITE

RS = Colors.RESET


def clean_screen():
    """
    Clear terminal screen cross-platform
    
    Returns:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def get_local_ip() -> str:
    """
    Get local IP address of the machine
    
    Returns:
        str: Local IP address or 127.0.0.1 if not found
    """
    try:
        # Create a temporary socket to get local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Connect to Google DNS (doesn't actually send data)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            return ip_address
    except Exception:
        return "127.0.0.1"


def get_random_user_agent() -> str:
    """
    Generate a random user agent string
    
    Returns:
        str: Random user agent
    """
    user_agents = [
        # Windows browsers
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36",
        
        # macOS browsers
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        
        # Linux browsers
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0",
        
        # Mobile browsers
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 14; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    ]
    
    return random.choice(user_agents)


def validate_url(url: str) -> str:
    """
    Validate and normalize a URL
    
    Args:
        url (str): URL to validate
        
    Returns:
        str: Normalized URL
        
    Raises:
        ValueError: If URL is invalid
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")
    
    url = url.strip()
    
    # Remove extra whitespace
    url = ' '.join(url.split())
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Parse and validate URL
    try:
        parsed = urllib.parse.urlparse(url)
        
        if not parsed.netloc:
            raise ValueError("Invalid URL: no network location")
        
        # Reconstruct URL with proper scheme
        if not parsed.scheme:
            url = 'https://' + parsed.geturl()
        else:
            url = parsed.geturl()
        
        return url.rstrip('/')
        
    except Exception as e:
        raise ValueError(f"Invalid URL format: {e}")


def calculate_hash(data: str, algorithm: str = 'sha256') -> str:
    """
    Calculate hash of data using specified algorithm
    
    Args:
        data (str): Data to hash
        algorithm (str): Hash algorithm (md5, sha1, sha256, sha512)
        
    Returns:
        str: Hexadecimal hash string
        
    Raises:
        ValueError: If data is empty or algorithm is unsupported
    """
    if not data:
        raise ValueError("Data cannot be empty")
    
    algorithm = algorithm.lower()
    
    if algorithm == 'md5':
        return hashlib.md5(data.encode()).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(data.encode()).hexdigest()
    elif algorithm == 'sha256':
        return hashlib.sha256(data.encode()).hexdigest()
    elif algorithm == 'sha512':
        return hashlib.sha512(data.encode()).hexdigest()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")


def save_json(data: Any, filename: Union[str, Path]) -> bool:
    """
    Save data to JSON file with error handling
    
    Args:
        data: Data to save (must be JSON serializable)
        filename: Path to save file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        filename = Path(filename)
        
        # Create parent directories if they don't exist
        filename.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=True)
        
        return True
        
    except TypeError as e:
        print(f"{R}[!] Data type error: {e}{RS}")
        return False
    except PermissionError as e:
        print(f"{R}[!] Permission error: {e}{RS}")
        return False
    except Exception as e:
        print(f"{R}[!] Error saving JSON: {e}{RS}")
        return False


def load_json(filename: Union[str, Path]) -> Optional[Any]:
    """
    Load data from JSON file
    
    Args:
        filename: Path to JSON file
        
    Returns:
        Loaded data or None if error
    """
    try:
        filename = Path(filename)
        
        if not filename.exists():
            print(f"{Y}[*] File not found: {filename}{RS}")
            return None
        
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    except json.JSONDecodeError as e:
        print(f"{R}[!] JSON syntax error in {filename}: {e}{RS}")
        return None
    except UnicodeDecodeError as e:
        print(f"{R}[!] Encoding error in {filename}: {e}{RS}")
        return None
    except Exception as e:
        print(f"{R}[!] Error loading JSON: {e}{RS}")
        return None


def format_bytes(size: int) -> str:
    """
    Convert bytes to human readable format
    
    Args:
        size (int): Size in bytes
        
    Returns:
        str: Formatted string (e.g., "1.23 MB")
        
    Raises:
        ValueError: If size is negative
    """
    if size < 0:
        raise ValueError("Size cannot be negative")
    
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    
    if size == 0:
        return "0 B"
    
    for unit in units:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    
    return f"{size:.2f} {units[-1]}"


def get_timestamp(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Get current timestamp
    
    Args:
        fmt (str): Format string (default: YYYY-MM-DD HH:MM:SS)
        
    Returns:
        str: Formatted timestamp
    """
    return time.strftime(fmt)


def create_directory(path: Union[str, Path]) -> bool:
    """
    Create directory if it doesn't exist
    
    Args:
        path: Directory path
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except PermissionError as e:
        print(f"{R}[!] Permission denied creating directory {path}: {e}{RS}")
        return False
    except Exception as e:
        print(f"{R}[!] Error creating directory {path}: {e}{RS}")
        return False


def is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    """
    Check if a TCP port is open on a host
    
    Args:
        host (str): Hostname or IP address
        port (int): Port number
        timeout (float): Connection timeout in seconds
        
    Returns:
        bool: True if port is open, False otherwise
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return result == 0
    except socket.gaierror:
        print(f"{Y}[*] Cannot resolve hostname: {host}{RS}")
        return False
    except socket.timeout:
        print(f"{Y}[*] Connection timeout to {host}:{port}{RS}")
        return False
    except Exception:
        return False


def generate_id(prefix: str = "id") -> str:
    """
    Generate a unique ID
    
    Args:
        prefix (str): ID prefix
        
    Returns:
        str: Unique ID string
    """
    timestamp = int(time.time() * 1000)
    random_num = random.randint(1000, 9999)
    return f"{prefix}_{timestamp}_{random_num}"


def safe_execute(func, *args, **kwargs):
    """
    Safely execute a function with error handling
    
    Args:
        func: Function to execute
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        Function result or None if error
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        func_name = getattr(func, '__name__', 'unknown')
        print(f"{R}[!] Error in {func_name}: {type(e).__name__}: {e}{RS}")
        return None


def backup_file(filepath: Union[str, Path]) -> bool:
    """
    Create backup of a file
    
    Args:
        filepath: Path to file
        
    Returns:
        bool: True if backup successful, False otherwise
    """
    try:
        src = Path(filepath)
        if not src.exists():
            return False
        
        # Create backup filename with timestamp
        timestamp = get_timestamp("%Y%m%d_%H%M%S")
        dst = src.with_suffix(f".{timestamp}.bak")
        
        shutil.copy2(src, dst)
        print(f"{G}[✓] Backup created: {dst.name}{RS}")
        return True
        
    except Exception as e:
        print(f"{R}[!] Error backing up {filepath}: {e}{RS}")
        return False


def is_valid_ip(ip: str) -> bool:
    """
    Check if string is a valid IPv4 address
    
    Args:
        ip (str): IP address string
        
    Returns:
        bool: True if valid IPv4 address
    """
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def print_progress(iteration: int, total: int, prefix: str = '', suffix: str = '', 
                   length: int = 50, fill: str = '█') -> None:
    """
    Print progress bar
    
    Args:
        iteration (int): Current iteration
        total (int): Total iterations
        prefix (str): Prefix string
        suffix (str): Suffix string
        length (int): Progress bar length
        fill (str): Fill character
    """
    if total == 0:
        return
    
    percent = int(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    
    if iteration == total:
        print()


def get_file_size(filepath: Union[str, Path]) -> int:
    """
    Get file size in bytes
    
    Args:
        filepath: Path to file
        
    Returns:
        int: File size in bytes, 0 if error
    """
    try:
        return Path(filepath).stat().st_size
    except Exception:
        return 0


def read_file_lines(filepath: Union[str, Path], max_lines: int = 1000) -> List[str]:
    """
    Read first N lines from a file
    
    Args:
        filepath: Path to file
        max_lines: Maximum lines to read
        
    Returns:
        List[str]: List of lines
    """
    lines = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                lines.append(line.rstrip('\n'))
    except Exception as e:
        print(f"{R}[!] Error reading {filepath}: {e}{RS}")
    
    return lines


def print_section(title: str, width: int = 60) -> None:
    """
    Print a section header
    
    Args:
        title (str): Section title
        width (int): Width of section
    """
    print(f"\n{BC}{'=' * width}{RS}")
    print(f"{BW}  {title.center(width - 4)}  {RS}")
    print(f"{BC}{'=' * width}{RS}")


def print_info(message: str, icon: str = "ℹ️") -> None:
    """
    Print info message with icon
    
    Args:
        message (str): Message text
        icon (str): Icon emoji
    """
    print(f"{C}{icon}  {message}{RS}")


def print_success(message: str, icon: str = "✅") -> None:
    """
    Print success message with icon
    
    Args:
        message (str): Message text
        icon (str): Icon emoji
    """
    print(f"{G}{icon}  {message}{RS}")


def print_warning(message: str, icon: str = "⚠️") -> None:
    """
    Print warning message with icon
    
    Args:
        message (str): Message text
        icon (str): Icon emoji
    """
    print(f"{Y}{icon}  {message}{RS}")


def print_error(message: str, icon: str = "❌") -> None:
    """
    Print error message with icon
    
    Args:
        message (str): Message text
        icon (str): Icon emoji
    """
    print(f"{R}{icon}  {message}{RS}")


def print_table(headers: List[str], rows: List[List[str]], 
                align: List[str] = None) -> None:
    """
    Print a formatted table
    
    Args:
        headers (List[str]): Column headers
        rows (List[List[str]]): Table rows
        align (List[str]): Alignment for each column (L/R/C)
    """
    if not headers or not rows:
        return
    
    # Calculate column widths
    col_count = len(headers)
    col_widths = [len(str(h)) for h in headers]
    
    for row in rows:
        for i, cell in enumerate(row[:col_count]):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Print header
    header_line = " | ".join(
        f"{str(headers[i]):{col_widths[i]}}" 
        for i in range(col_count)
    )
    print(f"{BW}{header_line}{RS}")
    
    # Print separator
    separator = "-+-".join("-" * w for w in col_widths)
    print(f"{BC}{separator}{RS}")
    
    # Print rows
    for row in rows:
        row_line = " | ".join(
            f"{str(row[i]):{col_widths[i]}}" 
            for i in range(min(len(row), col_count))
        )
        print(row_line)


def is_network_available() -> bool:
    """
    Check if network is available
    
    Returns:
        bool: True if network is available
    """
    try:
        # Try to connect to Google DNS
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False


def get_system_info() -> Dict[str, str]:
    """
    Get basic system information
    
    Returns:
        Dict[str, str]: System information
    """
    info = {
        "platform": sys.platform,
        "python_version": sys.version.split()[0],
        "executable": sys.executable,
        "cwd": str(Path.cwd()),
        "home": str(Path.home())
    }
    
    try:
        import platform
        info.update({
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor()
        })
    except:
        pass
    
    return info


def human_readable_time(seconds: float) -> str:
    """
    Convert seconds to human readable time
    
    Args:
        seconds (float): Time in seconds
        
    Returns:
        str: Human readable time string
    """
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    
    return " ".join(parts)