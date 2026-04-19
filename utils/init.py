"""
Sirra Framework Utilities Module
"""

from .common import (
    Colors, clean_screen, get_local_ip, get_random_user_agent,
    validate_url, calculate_hash, save_json, load_json,
    format_bytes, get_timestamp, create_directory, is_port_open,
    generate_id, safe_execute, backup_file, is_valid_ip,
    print_progress, get_file_size, read_file_lines,
    print_section, print_info, print_success, print_warning,
    print_error, print_table, is_network_available,
    get_system_info, human_readable_time
)

# Export color aliases
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

__version__ = "1.0.0"
__author__ = "Security Team"
__all__ = [
    'Colors', 'clean_screen', 'get_local_ip', 'get_random_user_agent',
    'validate_url', 'calculate_hash', 'save_json', 'load_json',
    'format_bytes', 'get_timestamp', 'create_directory', 'is_port_open',
    'generate_id', 'safe_execute', 'backup_file', 'is_valid_ip',
    'print_progress', 'get_file_size', 'read_file_lines',
    'print_section', 'print_info', 'print_success', 'print_warning',
    'print_error', 'print_table', 'is_network_available',
    'get_system_info', 'human_readable_time',
    'R', 'G', 'Y', 'B', 'M', 'C', 'W',
    'BR', 'BG', 'BY', 'BB', 'BM', 'BC', 'BW', 'RS'
]