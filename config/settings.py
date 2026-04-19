"""
Configuration settings for Sirra Framework
Clean and optimized version - No dead code
"""

import os
import sys
from pathlib import Path


class ConfigManager:
    """Centralized configuration management"""
    
    def __init__(self):
        self.project_root = self._detect_project_root()
        self._setup_paths()
        self._create_directories()
        self._load_environment()
    
    def _detect_project_root(self):
        """Dynamically detect project root directory"""
        # Try multiple detection methods
        possible_paths = [
            Path(__file__).parent.parent,  # settings.py -> core -> project_root
            Path.cwd(),                     # Current working directory
            Path(sys.argv[0]).parent if sys.argv else Path.cwd()  # Script location
        ]
        
        # Look for project structure markers
        for path in possible_paths:
            if (path / "main.py").exists() and (path / "core").exists():
                return path
        
        # Fallback to current file's parent
        return Path(__file__).parent.parent
    
    def _setup_paths(self):
        """Setup all required paths"""
        self.MODULES_DIR = self.project_root / "modules"
        self.CORE_DIR = self.project_root / "core"
        self.UTILS_DIR = self.project_root / "utils"
        self.CONFIG_DIR = self.project_root / "config"
        self.OUTPUT_DIR = self.project_root / "output"
        self.LOGS_DIR = self.OUTPUT_DIR / "logs"
        self.REPORTS_DIR = self.OUTPUT_DIR / "reports"
        self.EXPORTS_DIR = self.OUTPUT_DIR / "exports"
    
    def _create_directories(self):
        """Create all necessary directories"""
        directories = [
            self.MODULES_DIR,
            self.CONFIG_DIR,
            self.LOGS_DIR,
            self.REPORTS_DIR,
            self.EXPORTS_DIR
        ]
        
        created = []
        failed = []
        
        for directory in directories:
            try:
                directory.mkdir(parents=True, exist_ok=True)
                created.append(str(directory.relative_to(self.project_root)))
            except Exception as e:
                failed.append((str(directory.relative_to(self.project_root)), str(e)))
        
        if failed:
            print(f"[!] Failed to create directories: {failed}")
    
    def _load_environment(self):
        """Load environment variables if any"""
        # Can be extended to load from .env file
        pass
    
    def validate(self):
        """Validate configuration"""
        issues = []
        
        # Check essential directories
        if not self.MODULES_DIR.exists():
            issues.append(f"Modules directory missing: {self.MODULES_DIR}")
        
        if not self.CONFIG_DIR.exists():
            issues.append(f"Config directory missing: {self.CONFIG_DIR}")
        
        # Check main.py
        if not (self.project_root / "main.py").exists():
            issues.append(f"main.py not found in project root: {self.project_root}")
        
        if issues:
            print("[!] Configuration issues found:")
            for issue in issues:
                print(f"  • {issue}")
            return False
        
        return True
    
    def get_config_file(self, filename="settings.json"):
        """Get path to config file"""
        return self.CONFIG_DIR / filename
    
    def get_log_file(self):
        """Get path to log file"""
        return self.LOGS_DIR / "sirra.log"


# Create global instance
config = ConfigManager()

# Export commonly used paths and functions
PROJECT_ROOT = config.project_root
MODULES_DIR = config.MODULES_DIR
CONFIG_DIR = config.CONFIG_DIR
OUTPUT_DIR = config.OUTPUT_DIR
LOGS_DIR = config.LOGS_DIR

__all__ = [
    'config',
    'PROJECT_ROOT',
    'MODULES_DIR',
    'CONFIG_DIR',
    'OUTPUT_DIR',
    'LOGS_DIR'
]


# Quick validation on import
if __name__ != "__main__":
    # Only validate when imported as module
    try:
        if not config.validate():
            print("[*] Some configuration issues found. The application may not work correctly.")
    except Exception as e:
        print(f"[!] Configuration validation failed: {e}")