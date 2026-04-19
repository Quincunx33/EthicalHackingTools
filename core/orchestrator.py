"""
UniversalOrchestrator - Professional Module Manager
Enhanced with Security Scanning and Warning System
Fixed: ImportError, loader issues, security vulnerabilities
"""

import os
import importlib
import time
import ast
import sys
import re
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

# Dynamic base path setup
BASE_DIR = Path(__file__).resolve().parent.parent


class SecurityScanner:
    """Security scanner for module validation with warning system only"""
    
    DANGEROUS_KEYWORDS = [
        'os.system', 'subprocess', 'eval', 'exec', '__import__',
        'compile', 'globals', 'locals', 'getattr', 'setattr',
        'open', 'file', 'input', 'raw_input', 'execfile',
        'reload', '__builtins__', '__import__', 'pty.spawn',
        'os.popen', 'os.spawn', 'os.exec', 'os.kill'
    ]
    
    DANGEROUS_MODULES = [
        'os', 'subprocess', 'sys', 'shutil', 'ctypes',
        'socket', 'pickle', 'marshal', 'builtins', 'pty',
        'fcntl', 'mmap', 'signal', 'resource', 'threading',
        'multiprocessing', 'concurrent.futures'
    ]
    
    DANGEROUS_ATTRIBUTES = [
        'system', 'Popen', 'call', 'run', 'check_output',
        'spawn', 'exec', 'kill', 'popen', 'spawnlp',
        'spawnlpe', 'spawnv', 'spawnve', 'spawnvp', 'spawnvpe'
    ]
    
    ALLOWED_IMPORTS = [
        'time', 'random', 're', 'json', 'hashlib',
        'datetime', 'collections', 'itertools', 'math',
        'string', 'urllib.parse', 'base64', 'csv',
        'typing', 'pathlib', 'ssl', 'http.client',
        'urllib.request', 'urllib.error'
    ]
    
    @staticmethod
    def scan_module(module_path, disable_security=False):
        """Scan module for dangerous code - Warning system only"""
        if disable_security:
            return [], "SECURITY_DISABLED"
        
        try:
            with open(module_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Calculate file hash for tracking
            file_hash = hashlib.md5(content.encode()).hexdigest()[:8]
            
            # Parse AST for detailed analysis
            tree = ast.parse(content)
            
            issues = []
            warning_level = "SAFE"
            
            # Check for dangerous imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in SecurityScanner.DANGEROUS_MODULES:
                            issues.append(f"Dangerous import detected: {alias.name}")
                            warning_level = "WARNING"
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module in SecurityScanner.DANGEROUS_MODULES:
                        issues.append(f"Dangerous import from: {node.module}")
                        warning_level = "WARNING"
                    
                    # Check for specific dangerous imports
                    if node.module and any(dm in node.module for dm in ['os', 'subprocess', 'sys']):
                        for alias in node.names:
                            if alias.name in SecurityScanner.DANGEROUS_ATTRIBUTES:
                                issues.append(f"Dangerous function import: {node.module}.{alias.name}")
                                warning_level = "WARNING"
                
                # Check for dangerous function calls
                elif isinstance(node, ast.Call):
                    try:
                        if isinstance(node.func, ast.Name):
                            if node.func.id in ['eval', 'exec', 'compile', 'input']:
                                issues.append(f"Dangerous function call: {node.func.id}")
                                warning_level = "WARNING"
                        
                        elif isinstance(node.func, ast.Attribute):
                            attr_name = node.func.attr
                            if attr_name in SecurityScanner.DANGEROUS_ATTRIBUTES:
                                # Check if it's from a dangerous module
                                if isinstance(node.func.value, ast.Name):
                                    module_name = node.func.value.id
                                    if module_name in ['os', 'subprocess', 'sys']:
                                        issues.append(f"Dangerous method call: {module_name}.{attr_name}")
                                        warning_level = "WARNING"
                    except:
                        pass
                
                # Check for dangerous assignments
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            if target.id == '__builtins__':
                                issues.append("Dangerous assignment: __builtins__")
                                warning_level = "WARNING"
            
            # Regex check for dangerous patterns
            for pattern in SecurityScanner.DANGEROUS_KEYWORDS:
                if re.search(rf'\b{pattern}\b', content):
                    if pattern not in [f"{issue.split(': ')[1]}" for issue in issues if ': ' in issue]:
                        issues.append(f"Dangerous keyword found: {pattern}")
                        warning_level = "WARNING"
            
            # Check for suspicious code patterns
            suspicious_patterns = [
                (r'__import__\(', "Dynamic import detected"),
                (r'getattr\(.*?\)', "Dynamic attribute access"),
                (r'setattr\(.*?\)', "Dynamic attribute modification"),
                (r'globals\(\)', "Global namespace access"),
                (r'locals\(\)', "Local namespace access"),
                (r'\.read\(\)', "File read operation"),
                (r'\.write\(\)', "File write operation"),
                (r'exec\(.*?\)', "Exec function call"),
                (r'__code__', "Code object access"),
                (r'__dict__', "Dictionary access"),
                (r'__subclasses__', "Subclass traversal")
            ]
            
            for pattern, message in suspicious_patterns:
                if re.search(pattern, content):
                    if message not in issues:
                        issues.append(f"Suspicious pattern: {message}")
                        warning_level = "WARNING"
            
            # Check for obfuscated code
            obfuscated_patterns = [
                (r'base64\.b64decode', "Base64 decoding detected"),
                (r'exec\(.*decode', "Exec with decoding"),
                (r'eval\(.*decode', "Eval with decoding"),
                (r'compile\(', "Dynamic compilation"),
                (r'getattr\(.*__builtins__', "Builtins access via getattr")
            ]
            
            for pattern, message in obfuscated_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    issues.append(f"Obfuscation detected: {message}")
                    warning_level = "WARNING"
            
            return issues, warning_level
            
        except SyntaxError as e:
            return [f"Syntax error in module: {e}"], "ERROR"
        except Exception as e:
            return [f"Security scan error: {str(e)}"], "ERROR"

    @staticmethod
    def is_module_safe(module_path, disable_security=False):
        """Check if module has warnings - NO BLOCKING, only warnings"""
        issues, warning_level = SecurityScanner.scan_module(module_path, disable_security)
        
        if disable_security:
            return True, issues, "SECURITY_DISABLED"
        
        # Always return True for execution (no blocking)
        # warning_level indicates the severity for user awareness
        is_safe = True  # Always allow execution
        return is_safe, issues, warning_level


class UniversalOrchestrator:
    def __init__(self):
        self.modules_path = BASE_DIR / "modules"
        self._module_cache = []
        self._last_scan_time = 0
        self._security_scanner = SecurityScanner()
        
        # Create modules directory if it doesn't exist
        if not self.modules_path.exists():
            print(f"[*] Creating modules directory: {self.modules_path}")
            self.modules_path.mkdir(exist_ok=True, parents=True)

    def get_available_modules(self, refresh=False, disable_security=False):
        """Get available modules with intelligent caching and security scan"""
        current_time = time.time()
        
        # Use cache if valid (5 minutes) and security setting hasn't changed
        if (self._module_cache and not refresh and 
            current_time - self._last_scan_time < 300):
            return self._module_cache
        
        modules = []
        
        if not self.modules_path.exists():
            print(f"[!] Modules directory not found: {self.modules_path}")
            return modules
        
        try:
            security_status = "DISABLED" if disable_security else "ENABLED"
            print(f"[*] Scanning modules directory (Security: {security_status})...")
            
            # Check if directory is empty
            if not any(self.modules_path.iterdir()):
                print(f"[*] No modules found. Add Python files to: {self.modules_path}")
                return modules
            
            # Get all .py files
            py_files = list(self.modules_path.glob("*.py"))
            py_files.extend(self.modules_path.rglob("*.py"))
            
            safe_modules = 0
            warning_modules = 0
            error_modules = 0
            
            for full_path in py_files:
                # Skip __init__.py and other special files
                if full_path.name.startswith("_") or not full_path.is_file():
                    continue
                
                try:
                    # Security scan
                    is_safe, security_issues, warning_level = self._security_scanner.is_module_safe(
                        full_path, 
                        disable_security
                    )
                    
                    # Handle security status
                    if disable_security:
                        security_status_str = "SECURITY_DISABLED"
                    elif warning_level == "WARNING":
                        security_status_str = "WARNING"
                        warning_modules += 1
                    elif warning_level == "ERROR":
                        security_status_str = "ERROR"
                        error_modules += 1
                    else:
                        security_status_str = "SAFE"
                        safe_modules += 1
                    
                    # Extract metadata
                    metadata = self._extract_module_metadata(full_path)
                    
                    # Get relative category
                    rel_path = full_path.relative_to(self.modules_path)
                    category = str(rel_path.parent) if str(rel_path.parent) != '.' else "General"
                    
                    # Extract input configuration
                    input_config = self._extract_input_config(full_path)
                    
                    module_info = {
                        "name": full_path.stem,
                        "display_name": metadata.get('display_name', 
                            full_path.stem.replace("_", " ").title()),
                        "path": str(full_path),
                        "category": category,
                        "description": metadata.get('description', 'No description available'),
                        "author": metadata.get('author', 'Unknown'),
                        "version": metadata.get('version', '1.0.0'),
                        "inputs": input_config,
                        "size": full_path.stat().st_size,
                        "modified": time.ctime(full_path.stat().st_mtime),
                        "security_status": security_status_str,
                        "security_issues": security_issues[:5] if security_issues else [],  # Store first 5 issues
                        "security_warning_count": len(security_issues),
                        "file_hash": hashlib.md5(full_path.read_bytes()).hexdigest()[:12],
                        "scan_time": time.ctime()
                    }
                    
                    modules.append(module_info)
                    
                except Exception as e:
                    print(f"[!] Error reading {full_path.name}: {e}")
                    continue
            
            if modules:
                # Sort by display name
                modules.sort(key=lambda x: x['display_name'].lower())
                
                status_msg = f"[✓] Found {len(modules)} module(s)"
                if not disable_security:
                    if warning_modules > 0:
                        status_msg += f", {warning_modules} with warnings"
                    if error_modules > 0:
                        status_msg += f", {error_modules} with errors"
                
                print(status_msg)
                
                # Cache the results
                self._module_cache = modules
                self._last_scan_time = current_time
                
            else:
                print(f"[*] No valid modules found in {self.modules_path}")
            
        except Exception as e:
            print(f"[!] Critical error scanning modules: {e}")
        
        return self._module_cache

    def _extract_input_config(self, module_path):
        """Extract input configuration from module file"""
        input_config = []
        
        try:
            with open(module_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Parse with AST
            try:
                tree = ast.parse(content)
                
                # Look for MODULE_INPUTS variable
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name) and target.id == 'MODULE_INPUTS':
                                if isinstance(node.value, ast.List):
                                    for item in node.value.elts:
                                        if isinstance(item, ast.Dict):
                                            input_item = {}
                                            
                                            for key, val in zip(item.keys, item.values):
                                                if isinstance(key, ast.Constant):
                                                    key_name = key.value
                                                    
                                                    if isinstance(val, ast.Constant):
                                                        input_item[key_name] = val.value
                                                    elif isinstance(val, ast.Str):
                                                        input_item[key_name] = val.s
                                                    elif isinstance(val, ast.List):
                                                        # Handle list values (for choices)
                                                        choices = []
                                                        for elem in val.elts:
                                                            if isinstance(elem, ast.Constant):
                                                                choices.append(elem.value)
                                                            elif isinstance(elem, ast.Str):
                                                                choices.append(elem.s)
                                                        input_item[key_name] = choices
                                                    elif isinstance(val, ast.NameConstant):  # Python 3.7-
                                                        input_item[key_name] = val.value
                                                    elif isinstance(val, ast.Name):
                                                        # Handle True/False/None
                                                        if val.id in ['True', 'False', 'None']:
                                                            input_item[key_name] = eval(val.id)
                                            
                                            if input_item:
                                                input_config.append(input_item)
                
            except SyntaxError:
                # Fallback to simple parsing
                input_config = self._simple_input_extraction(content)
        
        except Exception:
            # If no input config found, use default
            input_config = [{
                'name': 'target',
                'type': 'text',
                'prompt': 'Target URL/IP',
                'required': True,
                'default': ''
            }]
        
        return input_config

    def _simple_input_extraction(self, content):
        """Simple input configuration extraction as fallback"""
        input_config = []
        
        try:
            lines = content.split('\n')
            in_inputs = False
            current_input = {}
            brace_count = 0
            
            for line in lines:
                line = line.strip()
                
                if 'MODULE_INPUTS' in line and '=' in line:
                    in_inputs = True
                    continue
                
                if in_inputs and '[' in line:
                    brace_count += 1
                
                if in_inputs and ']' in line:
                    brace_count -= 1
                    if brace_count == 0:
                        break
                
                if in_inputs and '{' in line:
                    current_input = {}
                
                if in_inputs and '}' in line and current_input:
                    input_config.append(current_input.copy())
                    current_input = {}
                
                if in_inputs and ':' in line and current_input is not None:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        key = parts[0].strip().strip('\'"')
                        value = parts[1].strip().strip(', \'"')
                        
                        # Convert string booleans
                        if value.lower() in ['true', 'false']:
                            value = value.lower() == 'true'
                        # Convert string numbers
                        elif value.isdigit():
                            value = int(value)
                        
                        current_input[key] = value
        
        except Exception:
            pass
        
        return input_config or [{
            'name': 'target',
            'type': 'text',
            'prompt': 'Target URL/IP',
            'required': True,
            'default': ''
        }]

    def _extract_module_metadata(self, module_path):
        """Extract metadata from module file safely"""
        metadata = {}
        
        try:
            with open(module_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Parse with AST
            try:
                tree = ast.parse(content)
                
                # Look for module-level assignments
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                var_name = target.id
                                
                                # Check for metadata variables
                                if var_name in ['display_name', 'description', 'author', 'version']:
                                    if isinstance(node.value, ast.Constant):
                                        metadata[var_name] = node.value.value
                                    elif isinstance(node.value, ast.Str):
                                        metadata[var_name] = node.value.s
                                    elif isinstance(node.value, ast.NameConstant):  # Python 3.7-
                                        metadata[var_name] = node.value.value
                                    elif isinstance(node.value, ast.Name):
                                        if node.value.id in ['True', 'False', 'None']:
                                            metadata[var_name] = eval(node.value.id)
                
                # Check for docstring
                if (tree.body and isinstance(tree.body[0], ast.Expr) and 
                    isinstance(tree.body[0].value, ast.Constant)):
                    docstring = tree.body[0].value.value
                    if docstring and 'description' not in metadata:
                        # Use first non-empty line of docstring
                        lines = docstring.strip().split('\n')
                        for line in lines:
                            if line.strip():
                                metadata['description'] = line.strip()
                                break
            
            except SyntaxError:
                # Fallback to simple parsing for syntax errors
                metadata = self._simple_metadata_extraction(content)
        
        except Exception:
            pass  # Silent fail for metadata extraction
        
        return metadata

    def _simple_metadata_extraction(self, content):
        """Simple metadata extraction as fallback"""
        metadata = {}
        
        try:
            lines = content.split('\n')
            
            for i, line in enumerate(lines[:50]):
                line = line.strip()
                
                # Skip comments and empty lines
                if line.startswith('#') or not line:
                    continue
                
                # Look for assignments
                if '=' in line and not line.startswith(' '):
                    parts = line.split('=', 1)
                    var_name = parts[0].strip()
                    var_value = parts[1].strip()
                    
                    # Clean up value
                    var_value = var_value.strip('"\'').strip()
                    
                    # Handle comments after value
                    if '#' in var_value:
                        var_value = var_value.split('#')[0].strip()
                    
                    # Convert types
                    if var_value.lower() in ['true', 'false']:
                        var_value = var_value.lower() == 'true'
                    elif var_value.isdigit():
                        var_value = int(var_value)
                    
                    if var_name in ['display_name', 'description', 'author', 'version']:
                        metadata[var_name] = var_value
                
                # Look for triple-quoted strings (docstring)
                if line.startswith('"""') or line.startswith("'''"):
                    if 'description' not in metadata:
                        # Extract first line of docstring
                        docstring_line = line[3:].strip()
                        if docstring_line:
                            metadata['description'] = docstring_line
                            break
        
        except Exception:
            pass
        
        return metadata

    def run_module(self, module_path, module_inputs, options=None, disable_security=False):
        """Execute a module safely with FIXED import system and warning display"""
        print(f"\n[*] Starting module execution...")
        print(f"[*] Security Scanner: {'DISABLED' if disable_security else 'ENABLED'}")
        
        if not module_path or not isinstance(module_path, str):
            print(f"[!] Invalid module path")
            return {"success": False, "error": "Invalid module path"}
        
        if options is None:
            options = {}
        
        start_time = time.time()
        
        try:
            # Resolve and validate path
            full_module_path = Path(module_path).resolve()
            
            if not full_module_path.exists():
                print(f"[!] Module file not found: {module_path}")
                return {"success": False, "error": "Module file not found"}
            
            # Check file extension
            if full_module_path.suffix != '.py':
                print(f"[!] File must have .py extension: {full_module_path}")
                return {"success": False, "error": "Invalid file extension"}
            
            # Security check unless disabled - WARNING ONLY, NO BLOCKING
            if not disable_security:
                is_safe, security_issues, warning_level = self._security_scanner.is_module_safe(
                    full_module_path, 
                    disable_security
                )
                
                if warning_level == "WARNING" and security_issues:
                    print(f"[!] ⚠️ SECURITY WARNINGS DETECTED (Module will still run):")
                    for i, issue in enumerate(security_issues[:5], 1):
                        print(f"    {i}. {issue}")
                    if len(security_issues) > 5:
                        print(f"    ... and {len(security_issues) - 5} more warnings")
                    print(f"[*] Proceed with caution...\n")
                
                elif warning_level == "ERROR":
                    print(f"[!] Module has syntax errors")
                    for issue in security_issues[:3]:
                        print(f"    - {issue}")
                    print(f"[!] Module may not execute properly\n")
            
            print(f"[✓] Module loaded: {full_module_path.name}")
            print(f"[*] Loading module...")
            
            # FIXED: Use simple import method instead of importlib.util
            module_name = full_module_path.stem
            
            # Add module directory to sys.path temporarily
            module_dir = str(full_module_path.parent)
            original_sys_path = sys.path.copy()
            
            if module_dir not in sys.path:
                sys.path.insert(0, module_dir)
            
            try:
                # Import the module directly
                module = __import__(module_name)
                
                # Reload to ensure fresh import
                import importlib
                module = importlib.reload(module)
                
                print(f"[✓] Module loaded successfully")
                
                # Check for required run function
                if not hasattr(module, 'run'):
                    print(f"[!] Module missing 'run' function")
                    print(f"[*] Module must contain: def run(inputs, options)")
                    return {"success": False, "error": "Module missing 'run' function"}
                
                # Verify run function is callable
                if callable(module.run):
                    print(f"[*] Executing with provided inputs...")
                    
                    # Execute the run function with proper error handling
                    try:
                        # Call the run function
                        result = module.run(module_inputs, options)
                        execution_time = time.time() - start_time
                        
                        print(f"[✓] Execution completed in {execution_time:.2f} seconds")
                        
                        # Format result
                        if isinstance(result, dict):
                            result['success'] = result.get('success', True)
                            result['execution_time'] = execution_time
                            result['security_warnings'] = security_issues if not disable_security and security_issues else []
                        elif result is not None:
                            result = {
                                'success': True,
                                'result': result,
                                'execution_time': execution_time,
                                'security_warnings': security_issues if not disable_security and security_issues else []
                            }
                        else:
                            result = {
                                'success': True,
                                'execution_time': execution_time,
                                'message': 'Execution completed with no return value',
                                'security_warnings': security_issues if not disable_security and security_issues else []
                            }
                        
                        return result
                        
                    except Exception as e:
                        execution_time = time.time() - start_time
                        print(f"[!] Error during run(): {type(e).__name__}: {e}")
                        return {
                            'success': False,
                            'error': f"{type(e).__name__}: {str(e)}",
                            'execution_time': execution_time,
                            'security_warnings': security_issues if not disable_security and security_issues else []
                        }
                else:
                    print(f"[!] 'run' is not a callable function")
                    return {"success": False, "error": "'run' is not a callable function"}
                
            except ImportError as e:
                print(f"[!] Failed to import module: {e}")
                return {"success": False, "error": f"Import error: {e}"}
            
            finally:
                # Restore sys.path
                sys.path = original_sys_path
                
                # Clean up module from sys.modules
                if module_name in sys.modules:
                    del sys.modules[module_name]
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"[!] Unexpected error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': f"Unexpected error: {type(e).__name__}: {e}",
                'execution_time': execution_time
            }

    def _create_safe_environment(self):
        """Create a sandboxed execution environment - Optional"""
        # Safe builtins - very restricted
        safe_builtins = {
            'print': print,
            'len': len,
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'list': list,
            'dict': dict,
            'tuple': tuple,
            'set': set,
            'range': range,
            'enumerate': enumerate,
            'zip': zip,
            'sorted': sorted,
            'reversed': reversed,
            'min': min,
            'max': max,
            'sum': sum,
            'abs': abs,
            'round': round,
            'isinstance': isinstance,
            'type': type,
            'Exception': Exception,
            'ValueError': ValueError,
            'TypeError': TypeError,
            'AttributeError': AttributeError,
            'KeyError': KeyError,
            'IndexError': IndexError,
            'StopIteration': StopIteration,
            'any': any,
            'all': all,
            'filter': filter,
            'map': map,
            'iter': iter,
            'next': next,
            'id': id,
            'hash': hash,
            'repr': repr,
            'ascii': ascii,
            'format': format,
            'divmod': divmod,
            'pow': pow,
            'complex': complex,
            'bin': bin,
            'hex': hex,
            'oct': oct,
            'chr': chr,
            'ord': ord,
            'slice': slice,
        }
        
        # Create a custom __import__ that only allows safe modules
        def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name in SecurityScanner.ALLOWED_IMPORTS:
                return __import__(name, globals, locals, fromlist, level)
            else:
                raise ImportError(f"Import of '{name}' is not allowed in sandbox")
        
        safe_builtins['__import__'] = safe_import
        
        # Safe globals dictionary
        safe_globals = {
            '__builtins__': safe_builtins,
            '__name__': '__main__',
            '__file__': None,
            '__doc__': None,
            '__package__': None,
            '__loader__': None,
            '__spec__': None
        }
        
        # Add safe modules to namespace
        try:
            import time as time_module
            import random as random_module
            import re as re_module
            import json as json_module
            import hashlib as hashlib_module
            import math as math_module
            import string as string_module
            import datetime as datetime_module
            import collections as collections_module
            import itertools as itertools_module
            import base64 as base64_module
            import csv as csv_module
            
            safe_globals['time'] = time_module
            safe_globals['random'] = random_module
            safe_globals['re'] = re_module
            safe_globals['json'] = json_module
            safe_globals['hashlib'] = hashlib_module
            safe_globals['math'] = math_module
            safe_globals['string'] = string_module
            safe_globals['datetime'] = datetime_module
            safe_globals['collections'] = collections_module
            safe_globals['itertools'] = itertools_module
            safe_globals['base64'] = base64_module
            safe_globals['csv'] = csv_module
            
            # Limited urllib modules
            from urllib import parse as urllib_parse
            safe_globals['urllib.parse'] = urllib_parse
            
        except ImportError as e:
            print(f"[!] Warning: Could not import safe module: {e}")
        
        return safe_globals

    def refresh_modules(self, disable_security=False):
        """Force refresh of module cache"""
        security_status = "DISABLED" if disable_security else "ENABLED"
        print(f"[*] Refreshing module cache (Security: {security_status})...")
        self._module_cache = []
        self._last_scan_time = 0
        modules = self.get_available_modules(refresh=True, disable_security=disable_security)
        
        if modules:
            safe_count = len([m for m in modules if m['security_status'] in ['SAFE', 'SECURITY_DISABLED']])
            warning_count = len([m for m in modules if m['security_status'] == 'WARNING'])
            error_count = len([m for m in modules if m['security_status'] == 'ERROR'])
            
            status_msg = f"[✓] Found {len(modules)} module(s)"
            if not disable_security:
                if warning_count > 0:
                    status_msg += f", {warning_count} with warnings"
                if error_count > 0:
                    status_msg += f", {error_count} with errors"
            
            print(status_msg)
        else:
            print(f"[*] No modules found")
        
        return modules

    def get_module_security_report(self, module_path, disable_security=False):
        """Get detailed security report for a module"""
        if disable_security:
            return {"status": "SECURITY_DISABLED", "issues": [], "message": "Security scanning is disabled"}
        
        try:
            is_safe, issues, warning_level = self._security_scanner.is_module_safe(module_path, disable_security)
            
            report = {
                "module": Path(module_path).name,
                "scan_time": time.ctime(),
                "security_status": warning_level,
                "issues_found": len(issues),
                "issues": issues,
                "recommendation": "Module is safe to use" if warning_level == "SAFE" else 
                                "Use with caution - security warnings detected" if warning_level == "WARNING" else
                                "Module has syntax errors",
                "allow_execution": True  # Always allow execution
            }
            
            return report
            
        except Exception as e:
            return {
                "module": Path(module_path).name,
                "scan_time": time.ctime(),
                "security_status": "ERROR",
                "issues_found": 0,
                "issues": [f"Error during security scan: {str(e)}"],
                "recommendation": "Unable to complete security scan",
                "allow_execution": True  # Still allow execution
            }


# Singleton pattern for brain instance
_brain_instance = None

def get_brain():
    """Get the global orchestrator instance"""
    global _brain_instance
    if _brain_instance is None:
        _brain_instance = UniversalOrchestrator()
    return _brain_instance