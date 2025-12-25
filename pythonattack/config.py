# --- ADVANCED CONFIG & COLORS ---
class Colors:
    R = "\033[31m"
    G = "\033[32m"
    Y = "\033[33m"
    B = "\033[34m"
    C = "\033[36m"
    W = "\033[0m"
    M = "\033[35m"
    BL = "\033[94m"
    CYAN = "\033[96m"
    ORANGE = "\033[38;5;214m"

R, G, Y, B, C, W, M, BL, CY, OR = Colors.R, Colors.G, Colors.Y, Colors.B, Colors.C, Colors.W, Colors.M, Colors.BL, Colors.CYAN, Colors.ORANGE

# --- GLOBAL CONFIG VARIABLES ---
REPORT_FILE = "hackerai_scan_report.json"
THREADS = 50
TIMEOUT = 10  # সেকেন্ডে টাইমআউট
LHOST = "192.168.1.100"
LPORT = 4444
BANNER = f"""{B}
    █░█ ▄▀█ █▀▀ █▄▀ █▀▀ █▀█ ▄▀█ █
    █▀█ █▀█ █▄▄ █░█ ██▄ █▀▄ █▀█ █ {W}{Y}v20.0 ADVANCED{W}
{Y}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{W}"""

# --- USER AGENTS ---
UA_LIST_BACKUP = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
]