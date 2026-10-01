#!/usr/bin/env python3
"""
PRN CODEX VIP — GUEST GEN  ::  ULTRA MULTI-REGION PREMIUM
Ultra Fast | Multi-Region | Premium Boxed UI | Complete Flow
"""

import os, sys, json, time, random, string, hashlib, hmac, uuid, re
import threading
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from datetime import datetime, timezone

import requests, urllib3
from requests.adapters import HTTPAdapter
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

try:
    import blackboxprotobuf
except ImportError:
    os.system("pip install blackboxprotobuf -q")
    import blackboxprotobuf

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
if os.name == "nt":
    os.system("chcp 65001 > nul")
    os.system("")

# ============================================================
# RGB COLOR & STYLING SYSTEM
# ============================================================
class C:
    RST     = "\033[0m"
    B       = "\033[1m"
    DIM     = "\033[2m"
    ITALIC  = "\033[3m"
    RED     = "\033[38;5;196m"
    GRN     = "\033[38;5;46m"
    YEL     = "\033[38;5;226m"
    CYA     = "\033[38;5;51m"
    PURPLE  = "\033[38;5;141m"
    PINK    = "\033[38;5;201m"
    ORANGE  = "\033[38;5;208m"
    BLUE    = "\033[38;5;39m"
    SILVER  = "\033[38;5;250m"
    GREY    = "\033[38;5;239m"
    WHITE   = "\033[38;5;255m"
    LIME    = "\033[38;5;154m"
    MAGENTA = "\033[38;5;198m"

    @staticmethod
    def rgb(r, g, b):
        return f"{chr(27)}[38;2;{r};{g};{b}m"

    @staticmethod
    def bg(r, g, b):
        return f"{chr(27)}[48;2;{r};{g};{b}m"

def hsv_to_rgb(h, s=1.0, v=1.0):
    h = h % 360
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    if   h < 60:  r,g,b = c,x,0
    elif h < 120: r,g,b = x,c,0
    elif h < 180: r,g,b = 0,c,x
    elif h < 240: r,g,b = 0,x,c
    elif h < 300: r,g,b = x,0,c
    else:         r,g,b = c,0,x
    return int((r+m)*255), int((g+m)*255), int((b+m)*255)

def rainbow(text, offset=0, step=20):
    out = ""
    for i, ch in enumerate(text):
        r, g, b = hsv_to_rgb((offset + i * step) % 360)
        out += f"{C.rgb(r,g,b)}{ch}"
    return out + C.RST

def gradient_text(text, start_rgb=(140, 0, 255), end_rgb=(0, 230, 255)):
    lines = text.split('\n')
    out_str = ""
    total = len(lines)
    for i, line in enumerate(lines):
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * (i / max(1, total - 1)))
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * (i / max(1, total - 1)))
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * (i / max(1, total - 1)))
        out_str += f"{C.rgb(r,g,b)}{C.B}{line}{C.RST}\n"
    return out_str

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def strip_ansi(s): return re.sub(r'\033\[[0-9;]*m', '', s)
def visible_len(s): return len(strip_ansi(s))

# ============================================================
# ANIMATION
# ============================================================
def gradient_banner(text, fps=40, fps_speed=0.025):
    for frame in range(fps):
        line = ""
        for i, ch in enumerate(text):
            r, g, b = hsv_to_rgb((i * 12 + frame * 25) % 360)
            line += f"{C.rgb(r,g,b)}{C.B}{ch}"
        sys.stdout.write(f"\r{line}{C.RST}")
        sys.stdout.flush()
        time.sleep(fps_speed)
    print()

class Spinner:
    FRAMES = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
    def __init__(self, text="Working"):
        self.text = text
        self.running = False
        self._thread = None

    def _spin(self):
        i = 0
        while self.running:
            frame = self.FRAMES[i % len(self.FRAMES)]
            r, g, b = hsv_to_rgb((i * 25) % 360)
            sys.stdout.write(f"\r  {C.rgb(r,g,b)}{frame}{C.RST} {C.WHITE}{self.text}...{C.RST}")
            sys.stdout.flush()
            time.sleep(0.07)
            i += 1

    def start(self):
        self.running = True
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()

    def stop(self, success=True, note=""):
        self.running = False
        if self._thread: self._thread.join()
        mark = f"{C.GRN}[+]{C.RST}" if success else f"{C.RED}[-]{C.RST}"
        extra = f" {C.DIM}{note}{C.RST}" if note else ""
        sys.stdout.write(f"\r  {mark} {C.WHITE}{self.text}{C.RST}{extra}\n")
        sys.stdout.flush()

# ============================================================
# PREMIUM BOXED HEADER (for live session)
# ============================================================
def premium_session_header():
    reg = REGIONS[CONFIG["region"]]
    width = 66
    border_top = f"{C.MAGENTA}╔" + "═" * (width - 2) + f"╗{C.RST}"
    border_mid = f"{C.MAGENTA}╠" + "═" * (width - 2) + f"╣{C.RST}"
    border_bot = f"{C.MAGENTA}╚" + "═" * (width - 2) + f"╝{C.RST}"

    title = "◈  LIVE SESSION  ◈"
    pad = (width - 2 - len(title)) // 2
    tline = f"{C.MAGENTA}║{C.RST}" + " " * pad + rainbow(title) + " " * (width - 2 - len(title) - pad) + f"{C.MAGENTA}║{C.RST}"

    def kv(k, v, col):
        raw = f"  {k} : {v}"
        pad_r = max(width - 2 - len(raw) - 1, 0)
        return f"{C.MAGENTA}║{C.RST}  {C.DIM}{k}{C.RST} : {col}{C.B}{v}{C.RST}" + " " * pad_r + f"{C.MAGENTA}║{C.RST}"

    print(border_top)
    print(tline)
    print(border_mid)
    print(kv("Target ", str(CONFIG["target"]), C.PINK))
    print(kv("Threads", str(CONFIG["threads"]), C.CYA))
    print(kv("Region ", f"{CONFIG['region']} ({reg['name']})", C.ORANGE))
    print(kv("Carrier", reg["carrier"], C.YEL))
    print(kv("Lang   ", reg["lang"], C.LIME))
    print(kv("Output ", CONFIG["output_file"], C.GRN))
    print(border_bot)
    print()

# ============================================================
# URLS / CONSTANTS
# ============================================================
URL_GUEST_REGISTER = "https://ffmconnect.live.gop.garenanow.com/api/v2/oauth/guest:register"
URL_TOKEN_GRANT    = "https://ffmconnect.live.gop.garenanow.com/api/v2/oauth/guest/token:grant"
URL_MAJOR_LOGIN    = "https://loginbp.ppmainecoonghj.com/MajorLogin"
URL_MAJOR_REGISTER = "https://loginbp.ppmainecoonghj.com/MajorRegister"
URL_NEWBIE_CHOICE  = "https://loginbp.ppmainecoonghj.com/ChooseNewbieChoice"

MAIN_KEY = bytes.fromhex(
    '326565343438313965396234353938383435313431303637'
    '6232383136323138373464306435643761663964386637653030'
    '6331653534373135623764316533'
)
AES_KEY = bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
AES_IV  = bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])
CLIENT_SECRET = "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
APP_ID        = 100067
RELEASE_VER   = "OB55"
GAME_VERSION  = "2.132.4"

HTTP_TIMEOUT       = (4, 8)
FAIL_WAIT          = 0.05
MAX_RETRIES        = 4
POOL_CONN          = 400
POOL_MAX           = 800
PACE_PER_PROXY     = 0.05
PROXY_COOLDOWN_429 = 15
PROXY_COOLDOWN_503 = 30

# ============================================================
# MULTI-REGION DATABASE
# ============================================================
REGIONS = {
    "BD": {
        "name": "Bangladesh", "code": "BGD",
        "carrier": "Grameenphone", "wifi": "WIFI",
        "ips": [
            "103.230.104.10","103.230.104.22","103.230.105.15",
            "103.108.144.10","103.108.144.25","103.108.145.14",
            "103.87.208.10","103.87.208.22","103.87.209.30",
            "119.30.32.10","119.30.32.25","119.30.33.40",
            "103.148.60.10","103.148.60.22","103.148.61.15",
            "202.134.8.10","202.134.8.25","202.134.9.14",
            "203.76.96.10","203.76.96.22","203.76.97.30",
            "103.4.146.10","103.4.146.25","103.4.147.40",
        ],
        "lang": "bn",
        "alt_carriers": ["Robi", "Banglalink", "Airtel"],
    },
    "IND": {
        "name": "India", "code": "IND",
        "carrier": "Jio", "wifi": "WIFI",
        "ips": [
            "49.36.180.10","49.36.180.22","49.36.181.15","49.36.182.45",
            "103.87.24.10","103.87.24.25","103.87.25.14","103.87.25.30",
            "115.99.10.20","115.99.10.35","115.99.11.40","115.99.11.55",
            "49.36.83.10","49.36.83.22","49.36.84.15","49.36.84.30",
        ],
        "lang": "en",
        "alt_carriers": ["Airtel", "Vi", "BSNL"],
    },
    "SG": {
        "name": "Singapore", "code": "SGP",
        "carrier": "Singtel", "wifi": "WIFI",
        "ips": [
            "118.201.10.20","118.201.10.35","118.201.11.40",
            "116.12.50.10","116.12.50.22","116.12.51.15",
            "103.6.150.10","103.6.150.25","103.6.151.14",
            "165.21.50.10","165.21.50.22","165.21.51.30",
        ],
        "lang": "en",
        "alt_carriers": ["StarHub", "M1"],
    },
    "TH": {
        "name": "Thailand", "code": "THA",
        "carrier": "AIS", "wifi": "WIFI",
        "ips": [
            "171.100.10.20","171.100.10.35","171.100.11.40",
            "49.228.10.10","49.228.10.22","49.228.11.15",
            "110.164.50.10","110.164.50.25","110.164.51.14",
            "203.150.50.10","203.150.50.22","203.150.51.30",
        ],
        "lang": "th",
        "alt_carriers": ["TrueMove", "dtac"],
    },
    "BR": {
        "name": "Brazil", "code": "BRA",
        "carrier": "Vivo", "wifi": "WIFI",
        "ips": [
            "177.10.20.10","177.10.20.22","177.10.21.15",
            "189.30.50.10","189.30.50.25","189.30.51.14",
            "200.150.10.10","200.150.10.22","200.150.11.30",
            "201.20.50.10","201.20.50.25","201.20.51.40",
        ],
        "lang": "pt",
        "alt_carriers": ["Claro", "TIM", "Oi"],
    },
    "ID": {
        "name": "Indonesia", "code": "IDN",
        "carrier": "Telkomsel", "wifi": "WIFI",
        "ips": [
            "114.79.10.20","114.79.10.35","114.79.11.40",
            "180.240.50.10","180.240.50.22","180.240.51.15",
            "202.60.10.10","202.60.10.25","202.60.11.14",
            "103.10.50.10","103.10.50.22","103.10.51.30",
        ],
        "lang": "id",
        "alt_carriers": ["Indosat", "XL", "Tri"],
    },
    "MY": {
        "name": "Malaysia", "code": "MYS",
        "carrier": "Maxis", "wifi": "WIFI",
        "ips": [
            "115.164.10.20","115.164.10.35","115.164.11.40",
            "175.139.50.10","175.139.50.22","175.139.51.15",
            "60.48.10.10","60.48.10.25","60.48.11.14",
            "203.115.50.10","203.115.50.22","203.115.51.30",
        ],
        "lang": "ms",
        "alt_carriers": ["Celcom", "Digi", "U Mobile"],
    },
    "VN": {
        "name": "Vietnam", "code": "VNM",
        "carrier": "Viettel", "wifi": "WIFI",
        "ips": [
            "113.160.10.20","113.160.10.35","113.160.11.40",
            "171.244.50.10","171.244.50.22","171.244.51.15",
            "203.113.10.10","203.113.10.25","203.113.11.14",
            "118.70.50.10","118.70.50.22","118.70.51.30",
        ],
        "lang": "vi",
        "alt_carriers": ["Vinaphone", "Mobifone"],
    },
    "PH": {
        "name": "Philippines", "code": "PHL",
        "carrier": "Globe", "wifi": "WIFI",
        "ips": [
            "49.145.10.20","49.145.10.35","49.145.11.40",
            "110.54.50.10","110.54.50.22","110.54.51.15",
            "203.177.10.10","203.177.10.25","203.177.11.14",
            "121.58.50.10","121.58.50.22","121.58.51.30",
        ],
        "lang": "en",
        "alt_carriers": ["Smart", "Sun"],
    },
}

DEVICES = [
    ("Asus ASUS_AI2501_B", "Android OS 12 / API-31 (SP1A.210812.016.C2/user.dxu.20260701.180839)", "Adreno (TM) 640", "OpenGL ES 3.2"),
    ("Redmi Note 12 Pro",  "Android OS 13 / API-33 (TP1A.220624.014)", "Adreno (TM) 618", "OpenGL ES 3.2"),
    ("Samsung SM-M135F",   "Android OS 13 / API-33 (TP1A.220624.014)", "Mali-G68", "OpenGL ES 3.2"),
    ("Realme RMX3630",     "Android OS 12 / API-31 (SP1A.210812.016)", "Adreno (TM) 610", "OpenGL ES 3.2"),
    ("OnePlus CPH2411",    "Android OS 13 / API-33 (TP1A.220624.014)", "Adreno (TM) 730", "OpenGL ES 3.2"),
]

CONFIG = {
    "target":        100,
    "threads":       120,
    "output_file":   "accounts.json",
    "nick_prefix":   "FF",
    "nick_max_len":  12,
    "use_proxy":     True,
    "proxy_file":    "working_proxies.txt",
    "region":        "BD",
}

ALL_ACCOUNTS = []
FILE_LOCK    = threading.Lock()
COUNTER_LOCK = threading.Lock()
PRINT_LOCK   = threading.Lock()
PROXY_LOCK   = threading.Lock()
PACE_LOCK    = {}
LAST_PACE    = {}

TOTAL         = 0
PROXIES       = []
PROXY_COOLDOWN = {}
CURRENT_PROXY = None

DONE_COUNT    = 0
SUCCESS_COUNT = 0
FAIL_COUNT    = 0
_PROGRESS_LOCK = threading.Lock()

START_TIME    = 0.0

# ============================================================
# LOG HELPERS
# ============================================================
def out(m):
    with PRINT_LOCK:
        print(m, flush=True)

def ts(): return f"{C.GREY}[{time.strftime('%H:%M:%S')}]{C.RST}"
def info(m): out(f"{ts()} {C.CYA}{C.B}[i]{C.RST} {m}")
def warn(m): out(f"{ts()} {C.ORANGE}{C.B}[!]{C.RST} {m}")
def err(m):  out(f"{ts()} {C.RED}{C.B}[!!]{C.RST} {m}")

def ok_line(idx, region, acc_id, uid, nick, worker_id):
    out(
        f"{ts()} {C.GRN}{C.B}[✓]{C.RST} "
        f"{C.MAGENTA}┃{C.RST} "
        f"{C.PURPLE}W{worker_id:03d}{C.RST} "
        f"{C.DIM}>>{C.RST} "
        f"{C.PINK}#{idx:05d}{C.RST} "
        f"{C.DIM}>>{C.RST} "
        f"{C.bg(50,20,90)}{C.WHITE} {region} {C.RST} "
        f"{C.DIM}>>{C.RST} "
        f"{C.DIM}ID:{C.RST} {C.CYA}{acc_id}{C.RST} "
        f"{C.DIM}>>{C.RST} "
        f"{C.DIM}UID:{C.RST} {C.YEL}{uid}{C.RST} "
        f"{C.DIM}>>{C.RST} "
        f"{C.DIM}Nick:{C.RST} {C.WHITE}{C.B}{nick}{C.RST}"
    )

# ============================================================
# PROXY & ENCRYPTION
# ============================================================
def load_proxies():
    global PROXIES, CURRENT_PROXY
    PROXIES = []
    if not CONFIG["use_proxy"]:
        PROXIES = [None]; CURRENT_PROXY = None
        info(f"{C.PINK}DIRECT Mode Enabled{C.RST} (No Proxy)")
        return
    pf = CONFIG["proxy_file"]
    if not os.path.exists(pf):
        warn(f"Proxy file not found ({pf}) -> {C.PINK}DIRECT Mode{C.RST}")
        PROXIES = [None]; CURRENT_PROXY = None
        return
    with open(pf, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                PROXIES.append({"http": line, "https": line})
    if not PROXIES:
        PROXIES = [None]; CURRENT_PROXY = None
    else:
        CURRENT_PROXY = PROXIES[0]
        info(f"Loaded {C.CYA}{len(PROXIES)}{C.RST} working proxies")

def _pk(p): return p.get("http", "?") if p else "__direct__"

def get_proxy():
    global CURRENT_PROXY
    if len(PROXIES) <= 1:
        return PROXIES[0] if PROXIES else None
    if CURRENT_PROXY is not None:
        with PROXY_LOCK:
            if time.time() >= PROXY_COOLDOWN.get(_pk(CURRENT_PROXY), 0):
                return CURRENT_PROXY
    now = time.time()
    with PROXY_LOCK:
        healthy = [p for p in PROXIES if now >= PROXY_COOLDOWN.get(_pk(p), 0)]
        return random.choice(healthy) if healthy else random.choice(PROXIES)

def cooldown(p, sec):
    if p is None: return
    with PROXY_LOCK:
        k = _pk(p)
        PROXY_COOLDOWN[k] = max(PROXY_COOLDOWN.get(k, 0), time.time() + sec)

def pace_proxy(p):
    if PACE_PER_PROXY <= 0: return
    k = _pk(p)
    if k not in PACE_LOCK: PACE_LOCK[k] = threading.Lock()
    with PACE_LOCK[k]:
        now = time.time()
        el = now - LAST_PACE.get(k, 0)
        if el < PACE_PER_PROXY: time.sleep(PACE_PER_PROXY - el)
        LAST_PACE[k] = time.time()

def gen_password():
    return hashlib.sha256(
        ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32)).encode()
    ).hexdigest().upper()

def gen_nickname():
    prefix, max_len = CONFIG["nick_prefix"], CONFIG["nick_max_len"]
    avail = max_len - len(prefix)
    if avail < 1: return prefix[:max_len].encode()
    digits = "".join(random.choice("0123456789") for _ in range(avail))
    return f"{prefix}{digits}".encode()

def enc_aes(data):
    return AES.new(AES_KEY, AES.MODE_CBC, AES_IV).encrypt(pad(data, AES.block_size))

def encode_f14(s):
    ks = [0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30]
    return bytes(ord(c) ^ ks[i % len(ks)] for i, c in enumerate(s))

# ============================================================
# TYPEDEFS & HEADERS
# ============================================================
def _tf(t): return {'type': t, 'name': ''}
typedef_login = {'3':_tf('bytes'),'4':_tf('bytes'),'5':_tf('int'),'7':_tf('bytes'),'8':_tf('bytes'),'9':_tf('bytes'),'10':_tf('bytes'),'11':_tf('bytes'),'12':_tf('int'),'13':_tf('int'),'14':_tf('bytes'),'15':_tf('bytes'),'16':_tf('int'),'17':_tf('bytes'),'18':_tf('bytes'),'19':_tf('bytes'),'20':_tf('bytes'),'21':_tf('bytes'),'22':_tf('bytes'),'23':_tf('bytes'),'24':_tf('bytes'),'25':_tf('bytes'),'26':_tf('bytes'),'29':_tf('bytes'),'30':_tf('int'),'41':_tf('bytes'),'42':_tf('bytes'),'57':_tf('bytes'),'60':_tf('int'),'61':_tf('int'),'62':_tf('int'),'63':_tf('int'),'64':_tf('int'),'65':_tf('int'),'66':_tf('int'),'67':_tf('int'),'73':_tf('int'),'74':_tf('bytes'),'76':_tf('int'),'77':_tf('bytes'),'78':_tf('int'),'79':_tf('int'),'81':_tf('bytes'),'83':_tf('bytes'),'85':_tf('int'),'86':_tf('bytes'),'87':_tf('int'),'88':_tf('int'),'92':_tf('int'),'93':_tf('bytes'),'94':_tf('bytes'),'96':_tf('bytes'),'97':_tf('int'),'98':_tf('int'),'99':_tf('bytes'),'100':_tf('bytes'),'102':_tf('bytes'),'104':_tf('int'),'105':_tf('int'),'106':_tf('bytes'),'107':_tf('bytes')}
typedef_reg = {'1':_tf('bytes'),'2':_tf('bytes'),'3':_tf('bytes'),'5':_tf('int'),'6':_tf('int'),'7':_tf('int'),'13':_tf('int'),'14':_tf('bytes'),'15':_tf('bytes'),'16':_tf('int'),'20':_tf('bytes'),'21':_tf('int'),'22':_tf('bytes')}
typedef_newbie = {'1':_tf('int'),'2':_tf('int'),'3':_tf('int')}

FIELD_22 = bytes.fromhex("4747524501010100620200001052aa0d669c6a368f08338060d2ee0690053af84a41edcd3558556ec10f24f46c93ac64ca41a16732c46a2cb071246a79b8929032f9e1b6f4ef331bd53cabf29b09b97349a46e9863c0314e1a0d80819fef8aabf03876b3d037db354a7ccb5c1bce96411fb3753f6f50e44c69c4ed617fa30efb8ffc0517ff2f636739be1f304d999cfd6fd48bf69454199794c3dc88f55a4bdbd66534d5a061359cdfd1fb680cd37918df9fdb3cf7d80067b0a3506c90063cf62b2ccec11e23913a2fd7c4ef091331967bb518a5ad1e551146b90821be800883abadde39d6c80a5d798611466c748f075481806c5842ce45e6bd4e3368ec08fe2ec41ceb880cd86249eb71693f79f0bccf9e590c3fae12519fe08c7a1905d0927690109e0df28574bb14847225db1a59230e6662ed7730e15ff9a6c815cb41b420edeada735a4b03e181037c37c2c850257311df2f07b0a56e759372cbd0268e3f13a292ee4373e38ab5096e0342a5e0d7fec6da2bbc265d74baadd2b24ee4f74862f82c21d6694bac53f8ce80312a30068a6276a641c19b11d0305c6fe2f531ac7de578b29f543697f5c73663e6f23aa15277b6122dcd4d4171e38f9ac0b173f39c58416a16c5c1f4a35acd065ce78f449cf538a249339e763272d458e4ed86c976591a9c066b3a37111e44091eb6b5a795249f3e5145db022a6055f2cc675936391312f688f89627845df222a91156555225be36f9714a0ba50246d0f003bda3c9c1292ab73b4f79635ddd023218eda93a302d79e023404c14396544a930b98ed54771aca7fec10d095587685b473e81a9619764fad9256529dcd6e911f4f4629612287d4ee3ec5389f6ec4ec020b0e2aac017232a9197be9e46239ce690fe5d4872b2e98e651510c971667f3aca8b59f3e9d50e43")

HEADERS_MSDK = {
    "User-Agent": "GarenaMSDK/4.0.44(ASUS_AI2501_B ;Android 12;en;US;app 2.132.1 2019118525;)",
    "Content-Type": "application/json; charset=utf-8",
    "Connection": "keep-alive",
}
HEADERS_LOGINBP = {
    'Host': 'loginbp.ppmainecoonghj.com',
    'User-Agent': 'UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)',
    'Accept': '*/*',
    'Accept-Encoding': 'deflate, gzip',
    'Authorization': 'Bearer',
    'X-GA': 'v1 1',
    'ReleaseVersion': RELEASE_VER,
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Unity-Version': '2018.4.12f1',
}

_tl = threading.local()
def get_session():
    s = getattr(_tl, "s", None)
    if s: return s
    s = requests.Session()
    a = HTTPAdapter(pool_connections=POOL_CONN, pool_maxsize=POOL_MAX, max_retries=0)
    s.mount("https://", a); s.mount("http://", a)
    _tl.s = s
    return s

def _build_login_meta(open_id, access_token):
    reg = REGIONS[CONFIG["region"]]
    ip = random.choice(reg["ips"])
    carrier_name = random.choice([reg["carrier"]] + reg.get("alt_carriers", []))
    carrier = carrier_name.encode()
    wifi = reg["wifi"].encode()
    country = reg["code"].encode()
    lang = reg["lang"].encode()
    model, os_str, gpu, gpu_full = random.choice(DEVICES)
    return {
        '3': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S').encode(),
        '4': b'free fire', '5': 1, '7': GAME_VERSION.encode(),
        '8': os_str.encode(), '9': b'Handheld',
        '10': carrier, '11': wifi,
        '12': 1280, '13': 720, '14': b'240',
        '15': b'x86-64 SSE3 SSE4.1 SSE4.2 AVX AVX2 | 2400 | 4',
        '16': random.choice([5951, 6000, 6100, 5500]),
        '17': gpu.encode(), '18': gpu_full.encode(),
        '19': f'Google|{uuid.uuid4()}'.encode(),
        '20': ip.encode(), '21': lang,
        '22': open_id.encode(),
        '23': b'4', '24': b'Handheld',
        '25': model.encode(),
        '26': country,
        '29': access_token.encode(), '30': 1,
        '41': carrier, '42': wifi,
        '57': b'1ac4b80ecf0478a44203bf8fac6120f5',
        '60': 30000, '61': 30000, '62': 2519, '63': 243,
        '64': 32357, '65': 34308, '66': 32357, '67': 34308, '73': 1,
        '74': b'/data/app/~~iw-K-GR3srU7dLE-UxJ4bg==/com.dts.freefiremax-kbPhw3SUYautW0I_oayB_A==/lib/arm',
        '76': 2,
        '77': b'428775ab8c8845bd341b5357ec61d15e|/data/app/~~iw-K-GR3srU7dLE-UxJ4bg==/com.dts.freefiremax-kbPhw3SUYautW0I_oayB_A==/base.apk',
        '78': 2, '79': 1, '81': b'32', '83': b'2019118525', '85': 3,
        '86': b'OpenGLES3', '87': 4095, '88': 4,
        '92': random.choice([19788, 20000, 21000]),
        '93': b'android_max',
        '94': b'KqsHT2gyPt7vUCc9SCjv2ioi3WEZSEL86ErvXB38suVVK/Z4IVt78ESl/r2S15C1pqu/j6ZmgFL7HbwoFiiVconX08ooKiisQffvEAPCo/C+Lahr',
        '96': b'{"cur_rate":null,"support_etc2":true}',
        '97': 1, '98': 1, '99': b'4', '100': b'4', '102': b'',
        '104': 77149, '105': 1,
        '106': b'https://dl.cdn.freefiremobile.com/live/ABHotUpdates/|https://dl-core.cdn.freefiremobile.com/live/ABHotUpdates/|6b2078db9d22dd98f8e9386a39af8462',
        '107': b'c8e41b7a93f02d56e1a94c7b8203f5d1',
    }

def save_account(acc):
    with FILE_LOCK:
        ALL_ACCOUNTS.append(acc)
        tmp = CONFIG["output_file"] + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(ALL_ACCOUNTS, f, indent=2, ensure_ascii=False)
            os.replace(tmp, CONFIG["output_file"])
        except Exception as e:
            err(f"save: {e}")

# ============================================================
# WORKER
# ============================================================
def register_one(worker_id):
    global TOTAL, SUCCESS_COUNT, FAIL_COUNT
    session = get_session()
    proxy = get_proxy()

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            pace_proxy(proxy)
            password = gen_password()

            # 1. GUEST REGISTER
            reg_body = json.dumps(
                {"app_id": APP_ID, "client_type": 2, "password": password, "source": 2},
                separators=(",", ":"),
            )
            reg_sig = hmac.new(MAIN_KEY, reg_body.encode(), hashlib.sha256).hexdigest()
            r = session.post(
                URL_GUEST_REGISTER,
                headers={**HEADERS_MSDK, "Authorization": "Signature " + reg_sig},
                data=reg_body, verify=False, proxies=proxy, timeout=HTTP_TIMEOUT,
            )
            if r.status_code in (429, 503):
                cooldown(proxy, PROXY_COOLDOWN_429 if r.status_code == 429 else PROXY_COOLDOWN_503)
                proxy = get_proxy(); continue
            if r.status_code != 200:
                raise Exception(f"reg HTTP {r.status_code}")
            uid = r.json()["data"]["uid"]

            # 2. TOKEN GRANT
            dev_id = f"02-{uuid.uuid4()}"
            grant_body = {
                "client_id": APP_ID, "client_secret": CLIENT_SECRET,
                "client_type": 2, "device_id": dev_id,
                "password": password, "response_type": "token",
                "uid": int(uid),
            }
            r2 = session.post(
                URL_TOKEN_GRANT, headers=HEADERS_MSDK, json=grant_body,
                verify=False, proxies=proxy, timeout=HTTP_TIMEOUT,
            )
            if r2.status_code == 429:
                cooldown(proxy, PROXY_COOLDOWN_429); proxy = get_proxy(); continue
            if r2.status_code != 200:
                raise Exception(f"grant HTTP {r2.status_code}")
            gd = r2.json()["data"]
            access_token, open_id = gd["access_token"], gd["open_id"]

            hdr = dict(HEADERS_LOGINBP)
            hdr["X-GA-SV"] = str(int(time.time()))

            # 3. MAJOR LOGIN
            try:
                session.post(
                    URL_MAJOR_LOGIN, headers=hdr,
                    data=enc_aes(blackboxprotobuf.encode_message(
                        _build_login_meta(open_id, access_token), typedef_login)),
                    verify=False, proxies=proxy, timeout=HTTP_TIMEOUT,
                )
            except Exception:
                pass

            # 4. MAJOR REGISTER
            nick = gen_nickname()
            reg_msg = {
                '1': nick, '2': access_token.encode(), '3': open_id.encode(),
                '5': 102000007, '6': 4, '7': 1, '13': 1,
                '14': encode_f14(open_id), '15': b'en', '16': 2,
                '20': GAME_VERSION.encode(), '21': 1, '22': FIELD_22,
            }
            rr = session.post(
                URL_MAJOR_REGISTER, headers=hdr,
                data=enc_aes(blackboxprotobuf.encode_message(reg_msg, typedef_reg)),
                verify=False, proxies=proxy, timeout=HTTP_TIMEOUT,
            )
            if rr.status_code == 429:
                cooldown(proxy, PROXY_COOLDOWN_429); proxy = get_proxy(); continue
            if rr.status_code != 200:
                raise Exception(f"majorreg HTTP {rr.status_code}")

            res, _ = blackboxprotobuf.decode_message(rr.content)
            account_id = None
            if isinstance(res, dict):
                account_id = res.get('3') or res.get(b'3')
            if not account_id:
                raise Exception("no account_id")

            # 5. NEWBIE CHOICE
            try:
                session.post(
                    URL_NEWBIE_CHOICE, headers=hdr,
                    data=enc_aes(blackboxprotobuf.encode_message(
                        {'1': int(account_id), '2': 2, '3': 3}, typedef_newbie)),
                    verify=False, proxies=proxy, timeout=HTTP_TIMEOUT,
                )
            except Exception:
                pass

            with COUNTER_LOCK:
                TOTAL += 1
                idx = TOTAL

            nick_str = nick.decode('utf-8', errors='ignore')
            acc = {
                "region": CONFIG["region"],
                "uid": str(uid),
                "password": str(password),
                "name": nick_str,
                "account_id": str(account_id),
                "status": "registered",
            }
            save_account(acc)

            with _PROGRESS_LOCK:
                SUCCESS_COUNT += 1

            ok_line(idx, CONFIG["region"], account_id, uid, nick_str, worker_id)
            return acc

        except Exception:
            time.sleep(FAIL_WAIT)

    with _PROGRESS_LOCK:
        FAIL_COUNT += 1
    return None

# ============================================================
# BATCH RUNNER  (progress bar removed)
# ============================================================
def run_batch():
    global TOTAL, DONE_COUNT, SUCCESS_COUNT, FAIL_COUNT, START_TIME
    target, threads = CONFIG["target"], CONFIG["threads"]

    DONE_COUNT = 0
    SUCCESS_COUNT = 0
    FAIL_COUNT = 0

    sp = Spinner("Booting ULTRA engine"); sp.start(); time.sleep(0.4); sp.stop(True)
    sp = Spinner("Loading proxy pool");   sp.start(); time.sleep(0.35); sp.stop(True, note=f"{len(PROXIES)} loaded")
    print()

    premium_session_header()

    reg_name = REGIONS[CONFIG["region"]]["name"]
    info(f"Session started — {C.PINK}{target}{C.RST} target | "
         f"{C.CYA}{threads}{C.RST} threads | "
         f"Region: {C.ORANGE}{CONFIG['region']}{C.RST} ({reg_name})")
    print()
    START_TIME = time.time()
    start = START_TIME

    def worker_wrapper(wid):
        global DONE_COUNT
        try:
            result = register_one(wid)
        except Exception:
            result = None
        with _PROGRESS_LOCK:
            DONE_COUNT += 1
        return result

    with ThreadPoolExecutor(max_workers=threads) as ex:
        futures = {ex.submit(worker_wrapper, i + 1) for i in range(min(threads, target))}
        while futures:
            done, futures = wait(futures, return_when=FIRST_COMPLETED)
            for f in done:
                try: f.result()
                except Exception: pass
            with COUNTER_LOCK:
                done_n = TOTAL
            remaining = target - done_n - len(futures)
            if remaining > 0:
                for _ in range(min(threads - len(futures), remaining)):
                    futures.add(ex.submit(worker_wrapper, random.randint(1, threads)))
            if done_n >= target:
                break

    dt = time.time() - start
    print()
    generation_summary(target, SUCCESS_COUNT, FAIL_COUNT, dt, CONFIG["region"])

# ============================================================
# SUMMARY BOX (premium)
# ============================================================
def generation_summary(total, success, failed, elapsed, region):
    width = 52
    top    = f"{C.GRN}╔" + "═" * (width - 2) + f"╗{C.RST}"
    mid    = f"{C.GRN}╠" + "═" * (width - 2) + f"╣{C.RST}"
    bottom = f"{C.GRN}╚" + "═" * (width - 2) + f"╝{C.RST}"
    title  = "ULTRA GENERATION COMPLETE"
    pad_t  = (width - 2 - len(title)) // 2
    tline = (
        f"{C.GRN}║{C.RST}" + " " * pad_t +
        rainbow(title) +
        " " * (width - 2 - len(title) - pad_t) +
        f"{C.GRN}║{C.RST}"
    )
    rate = success / max(elapsed, 1) * 60
    ratio = (success / max(success + failed, 1)) * 100
    rows = [
        (C.GRN,  "Success ", str(success)),
        (C.RED,  "Failed  ", str(failed)),
        (C.CYA,  "Time    ", f"{elapsed:.2f}s"),
        (C.PINK, "Speed   ", f"{rate:.1f} acc/min"),
        (C.YEL,  "Ratio   ", f"{ratio:.1f}%"),
        (C.PURPLE, "Region", region),
    ]
    print(f"\n{top}")
    print(tline)
    print(mid)
    for col, k, v in rows:
        raw_len = 2 + len(k) + 3 + len(v) + 1
        pad = max(width - 2 - raw_len, 0)
        print(f"{C.GRN}║{C.RST}  {C.DIM}{k}{C.RST} : {col}{C.B}{v}{C.RST}" + " " * pad + f"{C.GRN}║{C.RST}")
    print(bottom + "\n")

# ============================================================
# UI
# ============================================================
BANNER_TEXT = r"""
    ██████╗ ██████╗  █████╗  ██████╗  ██████╗ ███╗   ██╗
    ██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔═══██╗████╗  ██║
    ██║  ██║██████╔╝███████║██║  ███╗██║   ██║██╔██╗ ██║
    ██║  ██║██╔══██╗██╔══██║██║   ██║██║   ██║██║╚██╗██║
    ██████╔╝██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝
"""

def show_banner():
    clear_screen()
    print()
    gradient_banner("      ◈ DGN CODEX VIP — GUEST GEN PREMIUM ◈      ", fps=42, fps_speed=0.025)
    print(gradient_text(BANNER_TEXT, start_rgb=(255, 0, 128), end_rgb=(0, 230, 255)))

    border = f"{C.MAGENTA}╔" + "═" * 66 + f"╗{C.RST}"
    border_b = f"{C.MAGENTA}╚" + "═" * 66 + f"╝{C.RST}"
    print(border)
    line = f"{C.MAGENTA}║{C.RST}  {C.B}{C.PINK}PREMIUM GENERATOR{C.RST}  {C.DIM}│{C.RST}  {C.WHITE}Version: OB55{C.RST}  {C.DIM}│{C.RST}  {C.GRN}Status: ONLINE{C.RST}   {C.MAGENTA}║{C.RST}"
    print(line)
    print(border_b + "\n")

def ask_box(prompt, default):
    try:
        v = input(f" {C.PURPLE}❯{C.RST} {C.WHITE}{prompt}{C.RST} [{C.PINK}{default}{C.RST}]: ").strip()
        return v if v else str(default)
    except (EOFError, KeyboardInterrupt):
        return str(default)

def ask_int_box(prompt, default, lo=1, hi=999999):
    try:
        v = input(f" {C.PURPLE}❯{C.RST} {C.WHITE}{prompt}{C.RST} [{C.PINK}{default}{C.RST}]: ").strip()
        if not v: return default
        return max(lo, min(hi, int(v)))
    except Exception:
        return default

def ask_region_box():
    keys = list(REGIONS.keys())
    print(f" {C.ORANGE}╭─ [ REGION SELECT ] {'─' * 30}{C.RST}")
    for i, k in enumerate(keys, 1):
        reg = REGIONS[k]
        print(f" {C.ORANGE}│{C.RST}  {C.PINK}[{i}]{C.RST}  {C.WHITE}{C.B}{k:<4}{C.RST}  {C.DIM}→{C.RST}  {C.CYA}{reg['name']:<14}{C.RST}  {C.DIM}({reg['carrier']}){C.RST}")
    print(f" {C.ORANGE}╰{'─' * 48}{C.RST}")
    try:
        v = input(f" {C.PURPLE}❯{C.RST} {C.WHITE}Choose Region{C.RST} [{C.PINK}1-{len(keys)}{C.RST}]: ").strip()
        if not v: return keys[0]
        idx = int(v) - 1
        if 0 <= idx < len(keys):
            return keys[idx]
        return keys[0]
    except Exception:
        return keys[0]

def menu_generate():
    show_banner()

    print(f" {C.CYA}╭─ [ CONFIGURATION ] {'─' * 30}{C.RST}")
    CONFIG["target"] = ask_int_box("Target Account Count", 100)
    CONFIG["threads"] = ask_int_box("Multi-threads (ULTRA)", 120, lo=1, hi=500)
    CONFIG["output_file"] = ask_box("Output File Path", "accounts.json")
    print(f" {C.CYA}╰{'─' * 48}{C.RST}\n")

    print(f" {C.PURPLE}╭─ [ NICKNAME SETTINGS ] {'─' * 28}{C.RST}")
    CONFIG["nick_prefix"] = ask_box("Nickname Prefix", "FF")
    CONFIG["nick_max_len"] = ask_int_box("Max Length (4-12)", 12, lo=4, hi=12)
    ex = gen_nickname().decode('utf-8', errors='ignore')
    print(f" {C.PURPLE}│{C.RST}  {C.DIM}Preview:{C.RST} {C.GRN}{C.B}{ex}{C.RST}")
    print(f" {C.PURPLE}╰{'─' * 48}{C.RST}\n")

    CONFIG["region"] = ask_region_box()
    reg_info = REGIONS[CONFIG["region"]]
    print()
    print(f" {C.GRN}│{C.RST}  Selected: {C.ORANGE}{C.B}{CONFIG['region']}{C.RST} {C.DIM}({reg_info['name']}){C.RST}  "
          f"{C.DIM}│{C.RST}  Carrier: {C.CYA}{reg_info['carrier']}{C.RST}  "
          f"{C.DIM}│{C.RST}  IPs: {C.PINK}{len(reg_info['ips'])}{C.RST}\n")

    print(f" {C.GREY}╭{'─' * 60}{C.RST}")
    print(f" {C.GREY}│{C.RST}  {C.DIM}Target :{C.RST} {C.PINK}{C.B}{CONFIG['target']:<8}{C.RST}  {C.DIM}Threads :{C.RST} {C.CYA}{C.B}{CONFIG['threads']:<6}{C.RST}  {C.DIM}Region :{C.RST} {C.ORANGE}{C.B}{CONFIG['region']:<4}{C.RST} {C.GREY}│{C.RST}")
    print(f" {C.GREY}│{C.RST}  {C.DIM}File   :{C.RST} {C.YEL}{C.B}{CONFIG['output_file']:<18}{C.RST}  {C.DIM}Prefix :{C.RST} {C.GRN}{C.B}{CONFIG['nick_prefix']:<8}{C.RST}       {C.GREY}│{C.RST}")
    print(f" {C.GREY}╰{'─' * 60}{C.RST}\n")

    confirm = input(f" {C.B}{C.PINK}❯ Start ULTRA Process? (Y/n): {C.RST}").strip().lower()
    if confirm not in ("", "y", "yes"): return

    if os.path.exists(CONFIG["output_file"]):
        try: os.remove(CONFIG["output_file"])
        except Exception: pass

    ALL_ACCOUNTS.clear()
    load_proxies()

    print()
    try: run_batch()
    except KeyboardInterrupt: warn("Process Aborted by User")

    print()
    input(f" {C.DIM}Press Enter to return to main menu...{C.RST}")

# ============================================================
# MAIN LOOP
# ============================================================
def main():
    while True:
        show_banner()
        print(f" {C.MAGENTA}╭─ [ MAIN MENU ] {'─' * 34}{C.RST}")
        print(f" {C.MAGENTA}│{C.RST}")
        print(f" {C.MAGENTA}│{C.RST}   {C.PINK}[1]{C.RST}  {C.B}Start Premium Generator{C.RST}")
        print(f" {C.MAGENTA}│{C.RST}   {C.RED}[0]{C.RST}  {C.B}Exit Application{C.RST}")
        print(f" {C.MAGENTA}│{C.RST}")
        print(f" {C.MAGENTA}╰{'─' * 48}{C.RST}")
        print()

        ch = input(f" {C.PINK}❯ Selection: {C.RST}").strip()
        if ch == "1":
            menu_generate()
        elif ch == "0":
            print(f"\n {C.PINK}Exiting... Have a good day boss man!{C.RST}\n")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(0)