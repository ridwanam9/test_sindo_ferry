import socket
import ssl
import requests
import subprocess
import platform

DOMAIN = "api.test.sindoferry.com.sg"
PORT = 443
TEST_URL = f"https://{DOMAIN}/agent/Agent/Login"


def check_dns():
    try:
        ip = socket.gethostbyname(DOMAIN)
        print(f"✅ DNS Resolve: {DOMAIN} -> {ip}")
        return ip
    except socket.gaierror as e:
        print(f"❌ DNS Error: {e}")
        return None


def check_ping(ip):
    try:
        param = "-n" if platform.system().lower() == "windows" else "-c"
        result = subprocess.run(["ping", param, "3", ip],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print("✅ Ping sukses:\n", result.stdout)
        else:
            print("⚠️ Ping gagal (mungkin ICMP diblok):\n", result.stdout)
    except Exception as e:
        print(f"❌ Error ping: {e}")


def check_tcp(ip):
    try:
        sock = socket.create_connection((ip, PORT), timeout=5)
        context = ssl.create_default_context()
        with context.wrap_socket(sock, server_hostname=DOMAIN) as s:
            print(f"✅ TCP connect ke {DOMAIN}:{PORT} berhasil (SSL OK)")
    except Exception as e:
        print(f"❌ TCP connect gagal: {e}")


def check_https():
    try:
        resp = requests.get(TEST_URL, timeout=10)
        print(f"✅ HTTPS request berhasil, status code: {resp.status_code}")
    except Exception as e:
        print(f"❌ HTTPS request gagal: {e}")


if __name__ == "__main__":
    ip = check_dns()
    if ip:
        check_ping(ip)
        check_tcp(ip)
        check_https()
