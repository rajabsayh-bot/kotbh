from flask import Flask, render_template_string
import requests
import random
import string
import time

app = Flask(__name__)

# ======================
# 🍪 DATA KONFIGURASI LU
# ======================
cookie_str = """flwssn=c582c946-7e27-4cfc-a6f4-48597c0070bc;gsid=34197de4-f1e9-4d42-b254-2865906eaadc;SecureNetflixId=v%3D3%26mac%3DAQEAEQABABScAQhKHK_HuVx13xuvLPOZGaPEwMI39hU.%26dt%3D1783875815871;NetflixId=v%3D3%26ct%3DBgjHlOvcAxK8AQg10SjdRnmbKEnp_JwzTpYamPvvywqzDSxlVbfr7kEfypWwm-YnIOc5UKoMzSoX21d7H6Uv3gi99VO6YFb5yS8MELHcvWaOJ9b7Rgcz65RtCNlX3bVgtCGLl3aDae3Ol7Koi4xyli2Rt9OV9vgYoJ9-JHWXVvLLd9eiKX1t0-9zfo3Mvw_eP1EHlgO0bpMLyPKSDfKIo4eYN03OQPVjOA9OagAVRfudG6cbKKQPmCtnwhtdYrWIoajCsy0vGAYiDgoMqmTj8AHHlLk_smSQ;nfvdid=BQFmAAEBEAOpPCJrtFJLPu3EKNJPsT5glpLRsf9RvpeRRLKb5eyg0OguTiK2I3yonVDQtPZn77s2lTpJx4EFtQlDo52Gt7W0QdkqB0FINaROcR1E4W2ygtkUrA0hpb5CnRJWojAB_dbD8OPclxkUoHpETUwrBKDL;"""

API_KEY_CAPTCHA = "f1dd8bc4-24f5-40f8-b75d-8b719f071db4"
JUMLAH_AKUN = 1

# Proses cookie
cookies = {}
for c in cookie_str.split(';'):
    if '=' in c:
        k, v = c.strip().split('=', 1)
        cookies[k] = v

headers_netflix = {
    "Content-Type": "application/json",
    "Origin": "https://www.netflix.com",
    "Referer": "https://www.netflix.com/id/",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Accept": "*/*"
}

headers_mailtm = {"Content-Type": "application/json", "Accept": "application/json"}
BASE_MAILTM = "https://api.mail.tm"

# ======================
# 🤖 AMBIL TOKEN CAPTCHA (SUDAH DIPERBAIKI PUBLIC KEY)
# ======================
def ambil_token_captcha():
    log = ["🤖 MEMINTA TOKEN CAPTCHA..."]
    try:
        res_buat = requests.post(
            "https://api.2captcha.com/createTask",
            json={
                "clientKey": API_KEY_CAPTCHA,
                "task": {
                    "type": "RecaptchaV2TaskProxyless",
                    "websiteURL": "https://www.netflix.com/id/",
                    "websitePublicKey": "6LeO36obAAAAALJZLbYbKfD0Xb1gXz9eY9hXtQrL"
                }
            }, timeout=15
        )
        data_buat = res_buat.json()
        if data_buat.get("errorId") != 0:
            log.append(f"❌ GAGAL: {data_buat.get('errorDescription', 'Salah API Key / Saldo habis')}")
            return None
        
        task_id = data_buat["taskId"]
        log.append(f"⏳ Tunggu hasil...")
        
        for _ in range(6):
            time.sleep(3)
            res_cek = requests.post(
                "https://api.2captcha.com/getTaskResult",
                json={"clientKey": API_KEY_CAPTCHA, "taskId": task_id}, timeout=10
            )
            data_cek = res_cek.json()
            if data_cek.get("status") == "ready":
                log.append("✅ TOKEN BERHASIL DAPAT!")
                return data_cek["solution"]["gRecaptchaResponse"]
            elif data_cek.get("status") == "failed":
                log.append(f"❌ TASK GAGAL: {data_cek.get('errorDescription')}")
                return None
        
        log.append("⏰ LAMA SEKALI, COBA LAGI NANTI")
        return None
    
    except Exception as e:
        log.append(f"❌ KONEKSI ERROR: {str(e)}")
        return None

# ======================
# 🚀 PROSES UTAMA
# ======================
def proses_semua():
    log = ["🎁 OTOMATIS PENDAFTARAN NETFLIX", "="*55]
    
    token = ambil_token_captcha()
    if not token:
        log.append("\n❌ TIDAK BISA LANJUT KARENA TOKEN GAGAL DAPAT!")
        return "<br>".join(log)
    
    log.append("")
    
    for no in range(1, JUMLAH_AKUN+1):
        log.append(f"════════════ AKUN KE-{no} ════════════")
        log.append("📧 MEMBUAT EMAIL DI mail.tm...")
        
        # Buat email (aman dari error hydra)
        try:
            res_domain = requests.get(f"{BASE_MAILTM}/domains?page=1", timeout=10)
            dom_data = res_domain.json()
            daftar_dom = dom_data.get("hydra:member", [])
            if not daftar_dom:
                log.append("❌ TIDAK BISA AMBIL DOMAIN!")
                continue
            domain = daftar_dom[0]["domain"]
            
            nama = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            email_baru = f"{nama}@{domain}"
            sandi = "UjiCoba99!"
            
            res_buat = requests.post(
                f"{BASE_MAILTM}/accounts",
                headers=headers_mailtm,
                json={"address": email_baru, "password": sandi},
                timeout=15
            )
            if res_buat.status_code in [200, 201]:
                log.append(f"✅ EMAIL: {email_baru}")
                log.append(f"🔑 SANDI: {sandi}")
            else:
                log.append(f"❌ GAGAL BUAT EMAIL! KODE: {res_buat.status_code}")
                continue
        except Exception as e:
            log.append(f"❌ ERROR MAIL.TM: {str(e)}")
            continue
        
        # Kirim ke Netflix (sesuai API terbaru)
        log.append("🌐 MENGIRIM KE SERVER NETFLIX...")
        try:
            payload = {
                "operationName": "CLCSScreenUpdate",
                "variables": {
                    "format": "HTML",
                    "imageFormat": "PNG",
                    "locale": "id-ID",
                    "serverState": "Bgjru+vcAxLTAU5En5gcaO7v7XjiK+rXFXxxInfs8S2xATg1JspUbo5FZiJWBmEvMVgdmR9SZ6ls/tnJzL2DiX1ZpEDzTPySXay5oWh+n159DQ0ZUzEH+DCPYegrj4HGBUH4jrx+k8r4V+RiwbCJri5hIJHBkm0U9DVbKQh6ngOFzJN+5ZyyV+Z0mlhhyhXawaHsrzyGLYsAO6VPXuyv9iRMihw6vAInnOOX5L/1NoByQC8aQQ7pZJ1JFMicXH3Zf1Vekx/pWvjGtP42MFXS+JARtzgeGtGdpeYCzJcYBiIOCgwDpEr8YdrJKDhAXJc=",
                    "serverScreenUpdate": "Bgjru+vcAxKSAn/xAw6MYX1AnpCWZuYykLwpMOkPstB/IWV1LG0TdgJeL6p3V/Rxc0H6Y1AjdGQnoq7pXXz/pvxZNUJBtnSnlEmbjxoi1Kzmx/XG7RjpVbm+CpCfToe6w6XPO3clBmha2mTEuPCtN2XUF1awZle4yJbeK1E1fZe80Zy8AClUxyXf2aR6sxF1YyiizlGzKwz78LudjMDcJwTXchHLkvQsAXelj9/Kvx8dk8d/m8zpx1A2gLeB+laz/WXEcsMvbvrEM8JbIN4+vreqiX2YQTWdORZNOWlKU3EnbkbHpZzClCqM3ij5Yr8PiCaSuR4wM82XYaw/7R1Z3ofu1oAKXIRRHCmdvvhdiy3w8/b+zCDCYOtsL7YYBiIOCgxMBpdIbc9NcH5VZOM=",
                    "inputFields": [
                        {"name": "email", "value": {"stringValue": email_baru}},
                        {"name": "pipcConsent", "value": {"booleanValue": False}},
                        {"name": "emailConsent", "value": {"booleanValue": False}},
                        {"name": "recaptchaResponseTime", "value": {"intValue": 1150}},
                        {"name": "recaptchaResponseToken", "value": {"stringValue": token}}
                    ]
                },
                "extensions": {
                    "persistedQuery": {"id": "0fd81de7-07af-4c7d-802f-0f4ea4181aa3", "version": 102}
                }
            }
            
            res_netflix = requests.post(
                "https://web.prod.cloud.netflix.com/graphql",
                headers=headers_netflix,
                cookies=cookies,
                json=payload,
                timeout=20
            )
            data = res_netflix.json()
            if "errors" not in data:
                log.append("✅ BERHASIL TERKIRIM KE NETFLIX!")
                log.append("📩 CEK EMAIL DI mail.tm DALAM 1-2 MENIT!")
            else:
                log.append(f"⚠️ RESPON NETFLIX: {data['errors'][0]['message']}")
        
        except Exception as e:
            log.append(f"❌ ERROR KIRIM: {str(e)}")
    
    log.append("")
    log.append("="*55)
    log.append("✅ SELESAI!")
    return "<br>".join(log)

# ======================
# 🌐 HALAMAN VERCEL
# ======================
@app.route('/')
def index():
    hasil = proses_semua()
    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DAFTAR NETFLIX OTOMATIS</title>
        <style>
            * {{box-sizing:border-box;margin:0;padding:0;}}
            body {{background:#111;color:#0f0;font-family:monospace;padding:15px;max-width:550px;margin:auto;}}
            h2 {{text-align:center;color:#e50914;margin-bottom:20px;font-size:22px;}}
            .log {{background:#000;padding:15px;border-radius:8px;white-space:pre-wrap;word-break:break-all;line-height:1.6;}}
        </style>
    </head>
    <body>
        <h2>🎁 OTOMATIS PENDAFTARAN</h2>
        <div class="log">{hasil}</div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ != "__main__":
    application = app
        
