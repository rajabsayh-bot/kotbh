from flask import Flask, render_template_string
import requests
import random
import string
import time

app = Flask(__name__)

# ======================
# 🍪 KONFIGURASI (ISI DI SINI)
# ======================
cookie_str = """flwssn=c582c946-7e27-4cfc-a6f4-48597c0070bc;gsid=34197de4-f1e9-4d42-b254-2865906eaadc;SecureNetflixId=v%3D3%26mac%3DAQEAEQABABScAQhKHK_HuVx13xuvLPOZGaPEwMI39hU.%26dt%3D1783875815871;NetflixId=v%3D3%26ct%3DBgjHlOvcAxK8AQg10SjdRnmbKEnp_JwzTpYamPvvywqzDSxlVbfr7kEfypWwm-YnIOc5UKoMzSoX21d7H6Uv3gi99VO6YFb5yS8MELHcvWaOJ9b7Rgcz65RtCNlX3bVgtCGLl3aDae3Ol7Koi4xyli2Rt9OV9vgYoJ9-JHWXVvLLd9eiKX1t0-9zfo3Mvw_eP1EHlgO0bpMLyPKSDfKIo4eYN03OQPVjOA9OagAVRfudG6cbKKQPmCtnwhtdYrWIoajCsy0vGAYiDgoMqmTj8AHHlLk_smSQ;nfvdid=BQFmAAEBEAOpPCJrtFJLPu3EKNJPsT5glpLRsf9RvpeRRLKb5eyg0OguTiK2I3yonVDQtPZn77s2lTpJx4EFtQlDo52Gt7W0QdkqB0FINaROcR1E4W2ygtkUrA0hpb5CnRJWojAB_dbD8OPclxkUoHpETUwrBKDL;"""
TOKEN_CAPTCHA = "ISI_TOKEN_RECAPTCHA_KAMU_DI_SINI"
JUMLAH_AKUN = 1

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
# 🚀 PROSES UTAMA
# ======================
def jalankan_proses():
    hasil = []
    hasil.append("🎁 OTOMATIS: BUAT EMAIL + KIRIM LINK (WEB VERSI)")
    hasil.append("="*55)

    if not TOKEN_CAPTCHA or "ISI_" in TOKEN_CAPTCHA:
        hasil.append("❌ ISI DULU TOKEN CAPTCHA DI KODE!")
        return "<br>".join(hasil)

    for no in range(1, JUMLAH_AKUN+1):
        hasil.append(f"<br>════════════ AKUN KE-{no} ════════════")
        hasil.append("📧 MEMBUAT EMAIL TEMPORAL...")

        try:
            res_domain = requests.get(f"{BASE_MAILTM}/domains?page=1", timeout=15)
            domain = res_domain.json()["hydra:member"][0]["domain"]
            nama = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            email_baru = f"{nama}@{domain}"
            sandi = "UjiCoba99!"

            res_buat = requests.post(
                f"{BASE_MAILTM}/accounts",
                headers=headers_mailtm,
                json={"address": email_baru, "password": sandi},
                timeout=20
            )
            if res_buat.status_code in [200,201]:
                hasil.append(f"✅ Email: {email_baru}")
            else:
                hasil.append(f"❌ Gagal buat email!")
                continue
        except Exception as e:
            hasil.append(f"❌ Error Mail.tm: {str(e)}")
            continue

        hasil.append("🌐 MENGIRIM LINK KE NETFLIX...")
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
                        {"name": "recaptchaResponseToken", "value": {"stringValue": TOKEN_CAPTCHA}}
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
                timeout=25
            )
            data = res_netflix.json()
            if "errors" not in data:
                hasil.append(f"✅ LINK BERHASIL! {email_baru} | Sandi: {sandi}")
            else:
                hasil.append(f"⚠️ Gagal: {data['errors'][0]['message']}")
        except Exception as e:
            hasil.append(f"❌ Error Netflix: {str(e)}")

    hasil.append("<br>"+"="*55)
    hasil.append("✅ SELESAI!")
    return "<br>".join(hasil)

# ======================
# 🌐 HALAMAN WEB
# ======================
@app.route('/')
def index():
    output = jalankan_proses()
    html = f"""
    <html>
    <body style="background:#111;color:#0f0;font-family:monospace;padding:20px;">
        <h2>🎁 OTOMATIS PENDAFTARAN NETFLIX (WEB VERSI)</h2>
        <pre>{output}</pre>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run()
    