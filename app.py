#!/usr/bin/env python3
# full maked by @keshvexff 
#copyright ©️ @keshvexff
import sys
import os
import json
import base64
import binascii
import time
import atexit
import signal
import warnings
import subprocess

def ensure_dependencies():
    dependencies = {
        'requests': 'requests',
        'Crypto': 'pycryptodome',
        'google.protobuf': 'protobuf',
        'blackboxprotobuf': 'blackboxprotobuf',
        'colorama': 'colorama'
    }
    for mod, pkg in dependencies.items():
        try:
            __import__(mod.split('.')[0])
        except ImportError:
            print(f"\033[93m[>] MISSING DEPENDENCY DETECTED: {pkg}. INITIATING AUTO-INSTALL...\033[0m")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Run pre-flight dependency check
ensure_dependencies()

warnings.filterwarnings("ignore")
import requests
requests.packages.urllib3.disable_warnings()
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from google.protobuf import descriptor_pool, message_factory
import blackboxprotobuf

# ---------- Colour Setup ----------
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    BOLD = Style.BRIGHT
    RESET = Style.RESET_ALL
except ImportError:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# ---------- Host/Port Configuration (must be at top level) ----------
PROXY_HOST = os.environ.get('PROXY_HOST', '0.0.0.0')
PROXY_PORT = int(os.environ.get('PORT', 5030))          # Render uses PORT env
PROXY_BASE_URL = os.environ.get('PROXY_BASE_URL', f'http://{PROXY_HOST}:{PROXY_PORT}/')

# ---------- Embedded Protobuf Descriptors ---------
mYdEsCrIpToR = b'\n\x08my.proto"\xae\t\n\x08GameData\x12\x11\n\ttimestamp\x18\x03 \x01(\t\x12\x11\n\tgame_name\x18\x04 \x01(\t\x12\x14\n\x0cgame_version\x18\x05 \x01(\x05\x12\x14\n\x0cversion_code\x18\x07 \x01(\t\x12\x0f\n\x07os_info\x18\x08 \x01(\t\x12\x13\n\x0bdevice_type\x18\t \x01(\t\x12\x18\n\x10network_provider\x18\n \x01(\t\x12\x17\n\x0fconnection_type\x18\x0b \x01(\t\x12\x14\n\x0cscreen_width\x18\x0c \x01(\x05\x12\x15\n\rscreen_height\x18\r \x01(\x05\x12\x0b\n\x03dpi\x18\x0e \x01(\t\x12\x10\n\x08cpu_info\x18\x0f \x01(\t\x12\x11\n\ttotal_ram\x18\x10 \x01(\x05\x12\x10\n\x08gpu_name\x18\x11 \x01(\t\x12\x13\n\x0bgpu_version\x18\x12 \x01(\t\x12\x0f\n\x07user_id\x18\x13 \x01(\t\x12\x12\n\nip_address\x18\x14 \x01(\t\x12\x10\n\x08language\x18\x15 \x01(\t\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x15\n\rplatform_type\x18\x17 \x01(\x05\x12\x1a\n\x12device_form_factor\x18\x18 \x01(\t\x12\x14\n\x0cdevice_model\x18\x19 \x01(\t\x12\x14\n\x0caccess_token\x18\x1d \x01(\t\x12\x18\n\x10unknown_field_30\x18\x1e \x01(\x05\x12"\n\x1asecondary_network_provider\x18) \x01(\t\x12!\n\x19secondary_connection_type\x18* \x01(\t\x12\x11\n\tunique_id\x18\x39 \x01(\t\x12\x10\n\x08field_60\x18< \x01(\x05\x12\x10\n\x08field_61\x18= \x01(\x05\x12\x10\n\x08field_62\x18> \x01(\x05\x12\x10\n\x08field_63\x18? \x01(\x05\x12\x10\n\x08field_64\x18@ \x01(\x05\x12\x10\n\x08field_65\x18A \x01(\x05\x12\x10\n\x08field_66\x18B \x01(\x05\x12\x10\n\x08field_67\x18C \x01(\x05\x12\x10\n\x08field_70\x18F \x01(\x05\x12\x10\n\x08field_73\x18I \x01(\x05\x12\x14\n\x0clibrary_path\x18J \x01(\t\x12\x10\n\x08field_76\x18L \x01(\x05\x12\x10\n\x08apk_info\x18M \x01(\t\x12\x10\n\x08field_78\x18N \x01(\x05\x12\x10\n\x08field_79\x18O \x01(\x05\x12\x17\n\x0fos_architecture\x18Q \x01(\t\x12\x14\n\x0cbuild_number\x18S \x01(\t\x12\x10\n\x08field_85\x18U \x01(\x05\x12\x18\n\x10graphics_backend\x18V \x01(\t\x12\x19\n\x11max_texture_units\x18W \x01(\x05\x12\x15\n\rrendering_api\x18X \x01(\x05\x12\x18\n\x10encoded_field_89\x18Y \x01(\t\x12\x10\n\x08field_92\x18\\ \x01(\x05\x12\x13\n\x0bmarketplace\x18] \x01(\t\x12\x16\n\x0eencryption_key\x18^ \x01(\t\x12\x15\n\rtotal_storage\x18_ \x01(\x05\x12\x10\n\x08field_97\x18a \x01(\x05\x12\x10\n\x08field_98\x18b \x01(\x05\x12\x10\n\x08field_99\x18c \x01(\t\x12\x11\n\tfield_100\x18d \x01(\tb\x06proto3'

oUtPuTdEsCrIpToR = b'\n\x13jwt_generator.proto"\xd2\x02\n\nGarena_420\x12\x12\n\naccount_id\x18\x01 \x01(\x03\x12\x0e\n\x06region\x18\x02 \x01(\t\x12\r\n\x05place\x18\x03 \x01(\t\x12\x10\n\x08location\x18\x04 \x01(\t\x12\x0e\n\x06status\x18\x05 \x01(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\n\n\x02id\x18\t \x01(\x05\x12\x0b\n\x03api\x18\n \x01(\t\x12\x0e\n\x06number\x18\x0c \x01(\x05\x12\x1e\n\tGarena420\x18\x0f \x01(\x0b\x32\x0b.Garena_420\x12\x0c\n\x04area\x18\x10 \x01(\t\x12\x11\n\tmain_area\x18\x12 \x01(\t\x12\x0c\n\x04city\x18\x13 \x01(\t\x12\x0c\n\x04name\x18\x14 \x01(\t\x12\x11\n\ttimestamp\x18\x15 \x01(\x03\x12\x0e\n\x06binary\x18\x16 \x01(\x0c\x12\x13\n\x0bbinary_data\x18\x17 \x01(\x0c\x1a"\n\x12Decrypted_Payloads\x12\x0c\n\x04type\x18\x01 \x01(\x05b\x06proto3'

pOoL = descriptor_pool.Default()
pOoL.AddSerializedFile(mYdEsCrIpToR)
pOoL.AddSerializedFile(oUtPuTdEsCrIpToR)

_factory = message_factory.MessageFactory(pool=pOoL)
gAmEdAtA = _factory.GetPrototype(pOoL.FindMessageTypeByName('GameData'))
gArEnA420 = _factory.GetPrototype(pOoL.FindMessageTypeByName('Garena_420'))

# ---------- AES Keys ----------
AES_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
AES_IV  = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

MAJOR_LOGIN_URL = "https://loginbp.ggblueshark.com/MajorLogin"

def encrypt(data):
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    return cipher.encrypt(pad(data, AES.block_size))

def decrypt(data):
    if len(data) % 16 != 0:
        return data
    try:
        cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
        return unpad(cipher.decrypt(data), AES.block_size)
    except:
        return data

def decode_protobuf(data):
    decoded, _ = blackboxprotobuf.decode_message(data)
    return decoded

# ---------- Emulator Mode Fields ----------
EMULATOR_FIELDS = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "game_name": "free fire",
    "game_version": 1,
    "version_code": "1.126.15",
    "os_info": "Windows 10",
    "device_type": "PC",
    "network_provider": "WiFi",
    "connection_type": "WIFI",
    "screen_width": 1920,
    "screen_height": 1080,
    "dpi": "96",
    "cpu_info": "Intel Core i7-8700K @ 3.70GHz",
    "total_ram": 16384,
    "gpu_name": "NVIDIA GeForce GTX 1060",
    "gpu_version": "OpenGL ES 3.2",
    "user_id": "Google|emulator-account",
    "ip_address": "192.168.1.100",
    "language": "en",
    "platform_type": 4,
    "device_form_factor": "Desktop",
    "device_model": "Bluestacks",
    "unique_id": "emulator-12345",
    "os_architecture": "x86_64",
    "build_number": "20240815",
    "graphics_backend": "OpenGL",
    "max_texture_units": 16,
    "rendering_api": 1,
    "marketplace": "3rd_party",
    "encryption_key": "emulator-key",
    "total_storage": 256000,
    "field_99": "4",
    "field_100": "4"
}

def build_modified_majorlogin_request(original_fields, open_id, access_token, platform):
    game = gAmEdAtA()
    for field_str, value in original_fields.items():
        field_num = int(field_str)
        field = gAmEdAtA.DESCRIPTOR.fields_by_number.get(field_num)
        if field is None:
            continue
        if field.name in ['timestamp', 'game_name', 'game_version', 'version_code',
                          'os_info', 'device_type', 'network_provider', 'connection_type',
                          'screen_width', 'screen_height', 'dpi', 'cpu_info', 'total_ram',
                          'gpu_name', 'gpu_version', 'user_id', 'ip_address', 'language',
                          'platform_type', 'device_form_factor', 'device_model', 'unique_id',
                          'os_architecture', 'build_number', 'graphics_backend',
                          'max_texture_units', 'rendering_api', 'marketplace', 'encryption_key',
                          'total_storage', 'field_99', 'field_100']:
            continue
        if field.type == field.TYPE_STRING:
            if isinstance(value, bytes):
                try:
                    value = value.decode('utf-8')
                except:
                    value = value.hex()
            setattr(game, field.name, str(value))
        elif field.type in (field.TYPE_INT32, field.TYPE_INT64,
                            field.TYPE_UINT32, field.TYPE_UINT64,
                            field.TYPE_SINT32, field.TYPE_SINT64):
            setattr(game, field.name, int(value))
        elif field.type == field.TYPE_BOOL:
            setattr(game, field.name, bool(value))
        elif field.type == field.TYPE_BYTES:
            if isinstance(value, str):
                try:
                    value = binascii.unhexlify(value)
                except:
                    value = value.encode()
            setattr(game, field.name, value)
        else:
            setattr(game, field.name, value)

    for field_name, value in EMULATOR_FIELDS.items():
        if hasattr(game, field_name):
            try:
                setattr(game, field_name, value)
            except:
                pass

    game.open_id = open_id
    game.access_token = access_token
    game.platform_type = platform
    game.field_99 = str(platform)
    game.field_100 = str(platform)
    game.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return game

def forward_majorlogin_request(modified_game):
    serialized = modified_game.SerializeToString()
    encrypted = encrypt(serialized)
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
        "Content-Type": "application/octet-stream",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA": "v1 1",
        "ReleaseVersion": "OB54"
    }
    resp = requests.post(MAJOR_LOGIN_URL, data=encrypted, headers=headers, verify=False, timeout=10)
    return resp.content if resp.status_code == 200 else None

# ---------- Config Deploy & Cleanup (No ADB) ----------
DEPLOYED_CONFIG_PATHS = []

def deploy_config_adb():
    global DEPLOYED_CONFIG_PATHS
    print(f"{CYAN}[>] {YELLOW}CREATING LOCAL CONFIG FILE...{RESET}")
    config = {"serverUrl": PROXY_BASE_URL}
    with open("localconfig.json", "w") as f:
        json.dump(config, f, indent=2)
    DEPLOYED_CONFIG_PATHS.append("localconfig.json")
    print(f"{GREEN}[+] CONFIG FILE CREATED: localconfig.json{RESET}")
    print(f"{YELLOW}[!] COPY THIS FILE TO THE GAME'S DATA FOLDER:{RESET}")
    print(f"    /storage/emulated/0/Android/data/com.dts.freefiremax/files/")
    print(f"{CYAN}[>] PROXY URL SET TO: {PROXY_BASE_URL}{RESET}")
    # Print content for easy copy
    with open("localconfig.json", "r") as f:
        content = f.read()
    print(f"{CYAN}[>] FILE CONTENT:\n{content}{RESET}")
    return True

def remove_config():
    if not DEPLOYED_CONFIG_PATHS:
        return
    print(f"\n{CYAN}[>] {YELLOW}EXECUTING CLEANUP PROTOCOL...{RESET}")
    for path in DEPLOYED_CONFIG_PATHS:
        try:
            if os.path.exists(path):
                os.remove(path)
                print(f"{GREEN}[+] LOCAL TRACE REMOVED: {path}{RESET}")
        except Exception as e:
            print(f"{RED}[-] FAILED TO REMOVE TRACE: {e}{RESET}")

atexit.register(remove_config)
signal.signal(signal.SIGINT, lambda s, f: (remove_config(), sys.exit(0)))
signal.signal(signal.SIGTERM, lambda s, f: (remove_config(), sys.exit(0)))

# ---------- HTTP Handler ----------
class DynamicHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._handle()
    def do_POST(self):
        self._handle()
    def _handle(self):
        path = self.path
        if path == "/Ping":
            self.send_response(200)
            self.send_header('Content-Length', '0')
            self.send_header('Connection', 'close')
            self.end_headers()
            return
        if path == "/MajorLogin":
            self._handle_majorlogin()
            return
        self.send_response(404)
        self.send_header('Content-Length', '0')
        self.send_header('Connection', 'close')
        self.end_headers()

    def _handle_majorlogin(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length) if length else b''
        try:
            decrypted = decrypt(body)
            decoded_fields = decode_protobuf(decrypted)
        except Exception as e:
            print(f"{RED}        Error decrypting/parsing request: {e}{RESET}")
            self.send_response(500)
            self.end_headers()
            return

        open_id = decoded_fields.get('22', None)
        access_token = decoded_fields.get('29', None)
        if not open_id or not access_token:
            print(f"{RED}        Missing open_id or access_token. Forwarding original.{RESET}")
            try:
                resp = requests.post(MAJOR_LOGIN_URL, data=body, headers=dict(self.headers), verify=False, timeout=10)
                content = resp.content
                self.send_response(resp.status_code)
                self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Length', len(content))
                self.send_header('Connection', 'close')
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                print(f"{RED}        Error: {e}{RESET}")
                self.send_response(500)
                self.end_headers()
            return

        print(f"{CYAN}        Intercepted MajorLogin – open_id: {open_id}{RESET}")
        print(f"{CYAN}        access_token: {access_token[:20]}...{RESET}")

        platforms = [4, 8, 3, 6]
        success = False
        for platform in platforms:
            try:
                modified_game = build_modified_majorlogin_request(decoded_fields, open_id, access_token, platform)
                response_content = forward_majorlogin_request(modified_game)
                if response_content is not None:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/octet-stream')
                    self.send_header('Content-Length', len(response_content))
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    self.wfile.write(response_content)
                    print(f"{GREEN}        ✅ Success with platform {platform} (Emulator mode){RESET}")
                    success = True
                    break
            except Exception as e:
                print(f"{YELLOW}        Platform {platform} failed: {e}{RESET}")
                continue

        if not success:
            print(f"{RED}        All platforms failed. Forwarding original.{RESET}")
            try:
                resp = requests.post(MAJOR_LOGIN_URL, data=body, headers=dict(self.headers), verify=False, timeout=10)
                content = resp.content
                self.send_response(resp.status_code)
                self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Length', len(content))
                self.send_header('Connection', 'close')
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                print(f"{RED}        Error: {e}{RESET}")
                self.send_response(500)
                self.end_headers()

    def log_message(self, *args):
        pass

# ---------- Banner ----------
def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = f"""
{BOLD}{GREEN}
   ▄█   ▄█▄    ▄████████  ▄█    ▄████████    ▄█    █▄    ███▄▄▄▄      ▄████████ 
  ███ ▄███▀   ███    ███ ███   ███    ███   ███    ███   ███▀▀▀██▄   ███    ███ 
  ███▐██▀     ███    ███ ███▌  ███    █▀    ███    ███   ███   ███   ███    ███ 
 ▄█████▀     ▄███▄▄▄▄██▀ ███▌  ███         ▄███▄▄▄▄███▄▄ ███   ███   ███    ███ 
▀▀█████▄    ▀▀███▀▀▀▀▀   ███▌  ▀██████████▀▀███▀▀▀▀███▀  ███   ███ ▀███████████ 
  ███▐██▄   ▀███████████ ███           ███  ███    ███   ███   ███   ███    ███ 
  ███ ▀███▄   ███    ███ ███     ▄█    ███  ███    ███   ███   ███   ███    ███ 
  ███   ▀█▀   ███    ███ █▀    ▄████████▀   ███    █▀     ▀█   █▀    ███    █▀  
              ███    ███                                                          

{CYAN}[>] {YELLOW}SYSTEM OVERRIDE INITIATED...
{CYAN}[>] {YELLOW}AUTHORIZATION: {RED}LEO MDZ PC {YELLOW}(GHOST PROTOCOL)
{CYAN}[>] {YELLOW}ESTABLISHING SECURE UPLINK TO TARGET SERVERS...
{GREEN}=============================================================================={RESET}
"""
    print(banner)

# ---------- Main ----------
if __name__ == '__main__':
    print_banner()

    print(f"""
{BLUE}╔══════════════════════════════════════════════════════════════════╗
║                     {BOLD}{CYAN}PROXY SERVER{RESET}{BLUE}                             ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  {CYAN}Target    :{RESET} {BOLD}Free Fire MAX (Manual file placement){RESET}
║  {CYAN}Method    :{RESET} Generate localconfig.json
║  {CYAN}Host      :{RESET} {PROXY_HOST}
║  {CYAN}Port      :{RESET} {PROXY_PORT}
║  {CYAN}Proxy URL :{RESET} {PROXY_BASE_URL}
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")

    if deploy_config_adb():
        print(f"{GREEN}[+] CONFIG FILE GENERATED. WAITING FOR TRAFFIC...{RESET}")
    else:
        print(f"{RED}[-] CRITICAL FAILURE DURING CONFIG CREATION.{RESET}")

    print(f"\n{BLUE}=============================================================================={RESET}")
    print(f"{CYAN}[>] PROXY SERVER ONLINE // {PROXY_HOST}:{PROXY_PORT}{RESET}")
    print(f"{CYAN}[>] INTERCEPTING TRAFFIC...{RESET}")
    print(f"{BLUE}=============================================================================={RESET}\n")

    server = HTTPServer((PROXY_HOST, PROXY_PORT), DynamicHandler)
    server.handle_error = lambda *args: None

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] CONNECTION SEVERED. INITIATING CLEANUP...{RESET}")
        remove_config()
        server.shutdown()
        print(f"{CYAN}[>] LEO MDZ PC OUT. 💀{RESET}\n")
        sys.exit(0)
