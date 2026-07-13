from flask import Flask, render_template_string
import requests
import random
import string
import time

app = Flask(__name__)

# ======================
# 🍪 COOKIE BARU DARI LU (SUDAH LENGKAP UNTUK TRIAL)
# ======================
cookie_str = """OTSessionTracking=87b6a5c0-0104-4e96-a291-092c11350111; flwssn=c582c946-7e27-4cfc-a6f4-48597c0070bc; gsid=caa4812a-9963-4def-9167-b601f191cfc5; netflix-sans-normal-3-loaded=true; netflix-sans-bold-3-loaded=true; nfvdid=BQFmAAEBEFECklCXwPof2v9oq0m-kSRgvhoBMFMGUDA7VDqWzhfh6d_0vpcH50lGalU_bxnBEk7nNy4QPSA0ConA19vDmIPnohyqr0WFLyg2fo0JhJEX0UUhy4k43S3wDJHceiqeKmXpBSFCFSBK5HyuCGBHr7-t; SecureNetflixId=v%3D3%26mac%3DAQEAEQABABTMKUJlBSG58EwKUNjiShKCe17fTYodiuw.%26dt%3D1783874192221; NetflixId=v%3D3%26ct%3DBgjHlOvcAxKZAzqyryoyc-LUwUPJGQ5fZsrSnWZKhhoZQ5QSbAVuvxOmjIbYLIPwphmVjqR52wXdNUeJLfj1di75k2kDQO_-SLbErGFnhksSd_px2DedqbL5wTY3x9_D06bcMvFvfAO9KVd2o82wXvZNWOab0m59UcBLLwLJR--c63hvWAojhmcs4U_Xi14hF3AgcShP_WPXZBefLbw3enLhO-InUu5lJRjEWPQbbb7DOYOpgOwnz-njq86uyYS7zSqFuw2N_cT4sMdmJ1_V23oAKg9AAg3bnBb7z9ieiel2YsAWGKfMSwgtRppBfZKc0TpNU6En_4NOwAvLfrXWX7E3GQg_43W7p3dxRTQhc1VfrPJrRV451iKt6u5lYoaq7qq4noI5sdwAr5amI-OBnQuw50YU2dKMVxOSnq6LsgMyGPHBMd4qU7yzwhfBAQQoiO_0jODWWtlQmQKE2skBkdL9GSpPm2cEj7Wx7pbxnnA878J3-cAPeShoY1uP86TLrSJZjGJcS-UdlVsPhQ3IxI3KSC0uJHFS5P-oesbCemi39m0YBiIOCgz-AG1K_HfI7lXWnsw.%26pg%3DE4UQOPLUERGP5H5TLQIITEVZ4I%26ch%3DAQEAEAABABT5WQX5qvSo_DRWohsHzrOAZR-NqaIaa78.; OptanonConsent=isGpcEnabled; netflix-sans-normal-3-loaded=true; netflix-sans-bold-3-loaded=true; OTSessionTracking=87b6a5c0-0104-4e96-a291-092c11350111; netflix-mfa-nonce=BgjKu-vcAxKVAc0DUXYgDqIWVIzhYsnCKqapNSXdcVFK9cYXWP6nwuKKUEVHr8XYgaZqtljG2irj4VyLBbfEULpMUyUUccoCDGtb-HJUsjLXCqHU0YmP5kh7hBtXeNHmVOC_2lJoKiIwmsV_PK3EZLhj3NiTqa7InlZ4mgQ1-pyduR8jj2UDl3yEOqee7Z9P2B2-wl99zKnU-xyiv2n9GAYiDgoMssZccgelFQF52LGT; flwssn=c582c946-7e27-4cfc-a6f4-48597c0070bc; nfvdid=BQFmAAEBEAOpPCJrtFJLPu3EKNJPsT5glpLRsf9RvpeRRLKb5eyg0OguTiK2I3yonVDQtPZn77s2lTpJx4EFtQlDo52Gt7W0QdkqB0FINaROcR1E4W2ygtkUrA0hpb5CnRJWojAB_dbD8OPclxkUoHpETUwrBKDL; SecureNetflixId=v%3D3%26mac%3DAQEAEQABABQUf1AVs_qg5_qXuBMl5XBvTk8z3KiPLIU.%26dt%3D1783908403395; NetflixId=v%3D3%26ct%3DBgjHlOvcAxLEAa165jG28xojVluZFEqg5hdmfbmhvtFX3Ns-5X3myeqyycqLhWe5RCkaCPpem8Yoes_2CsJ8-rPhrWACl0Hc0oPQ4OdKMCRWKRo7BiQWoExmBNl0d7zB7e4oiEk6z7MHtMtYGKPZ0B2xvvdcMRe3U_Hkj0zxisOgKlhJUdawnEVjVDWHiN1J8ANN7NpLGmmamPBNQZJp23BrtWqfVIML3Zr4PM5Z1YDn5LthRdDcq1XSzlj9PY6iLWStftvPhnJeWVtC1kYYBiIOCgwvtoGR1vVu9TLWAdk.; OptanonConsent=isGpcEnabled=undefined&hosts=&datestamp=Mon+Jul+13+2026+09%3A42%3A03+GMT%2B0700+(Waktu+Indonesia+Barat)&version=202604.2.0"""

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
# 🤖 FUNGSI AMBIL TOKEN CAPTCHA
# ======================
def ambil_token_captcha():
    log = ["🤖 MEMINTA TOKEN CAPTCHA OTOMATIS..."]
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
            }, timeout=12
        )
        data_buat = res_buat.json()
        if data_buat.get("errorId") != 0:
            log.append(f"⚠️ Layanan captcha: {data_buat.get('errorDescription', 'Gagal')}")
            log.append("🔄 Lanjut dengan token cadangan...")
            return "token_cadangan_sementara"
        
        task_id = data_buat["taskId"]
        log.append(f"⏳ Tunggu tugas selesai...")
        
        for _ in range(4):
            time.sleep(2)
            res_cek = requests.post(
                "https://api.2captcha.com/getTaskResult",
                json={"clientKey": API_KEY_CAPTCHA, "taskId": task_id}, timeout=10
            )
            data_cek = res_cek.json()
            if data_cek.get("status") == "ready":
                log.append("✅ TOKEN CAPTCHA BERHASIL DAPAT!")
                return data_cek["solution"]["gRecaptchaResponse"]
        
        log.append("⏰ Waktu tunggu habis!")
        return "token_cadangan_sementara"
    
    except Exception as e:
        log.append(f"⚠️ Koneksi captcha: {str(e)}")
        log.append("🔄 Lanjut dengan token cadangan...")
        return "token_cadangan_sementara"

# ======================
# 🚀 PROSES UTAMA
# ======================
def proses_semua():
    log = ["🎁 OTOMATIS: BUAT EMAIL + KIRIM LINK (COOKIE TRIAL)", "="*55]
    
    token = ambil_token_captcha()
    log.append("")
    
    for no in range(1, JUMLAH_AKUN+1):
        log.append(f"════════════ AKUN KE-{no} ════════════")
        log.append("📧 MEMBUAT EMAIL TEMPORAL...")
        
        # Buat email Mail.tm
        try:
            res_domain = requests.get(f"{BASE_MAILTM}/domains?page=1", timeout=10)
            domain = res_domain.json()["hydra:member"][0]["domain"]
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
                log.append(f"✅ Email: {email_baru}")
                log.append(f"🔑 Sandi: {sandi}")
            else:
                log.append(f"❌ Gagal buat email! Kode: {res_buat.status_code}")
                continue
        except Exception as e:
            log.append(f"❌ Error Mail.tm: {str(e)}")
            continue
        
        # Kirim ke Netflix
        log.append("🌐 MENGIRIM LINK PENDAFTARAN...")
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
                        {"name": "recaptchaResponseTime", "value": {"intValue": 1096}},
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
                timeout=15
            )
            data = res_netflix.json()
            if "errors" not in data:
                log.append("✅ LINK BERHASIL DIKIRIM!")
                log.append("🎁 SESI MENDUKUNG PENDAFTARAN UJI COBA GRATIS")
            else:
                log.append(f"⚠️ Gagal: {data['errors'][0]['message']}")
        
        except Exception as e:
            log.append(f"❌ Error: {str(e)}")
    
    log.append("")
    log.append("="*55)
    log.append("✅ SELESAI! SILAKAN BUKA EMAIL UNTUK VERIFIKASI")
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
        <title>TRIAL NETFLIX OTOMATIS</title>
        <style>
            * {{box-sizing:border-box;margin:0;padding:0;}}
            body {{background:#111;color:#0f0;font-family:monospace;padding:15px;max-width:500px;margin:auto;}}
            h2 {{text-align:center;color:#ff0055;margin-bottom:20px;}}
            .log {{background:#000;padding:15px;border-radius:8px;white-space:pre-wrap;word-break:break-all;}}
        </style>
    </head>
    <body>
        <h2>🎁 PENDAFTARAN UJI COBA GRATIS OTOMATIS</h2>
        <div class="log">{hasil}</div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ != "__main__":
    application = app
