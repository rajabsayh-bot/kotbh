from flask import Flask, render_template_string, request
import requests
import json

app = Flask(__name__)

# ======================
# 🍪 COOKIE SESION LU
# ======================
cookie_str = """OTSessionTracking=87b6a5c0-0104-4e96-a291-092c11350111; flwssn=c582c946-7e27-4cfc-a6f4-48597c0070bc; gsid=caa4812a-9963-4def-9167-b601f191cfc5; netflix-sans-normal-3-loaded=true; netflix-sans-bold-3-loaded=true; nfvdid=BQFmAAEBEFECklCXwPof2v9oq0m-kSRgvhoBMFMGUDA7VDqWzhfh6d_0vpcH50lGalU_bxnBEk7nNy4QPSA0ConA19vDmIPnohyqr0WFLyg2fo0JhJEX0UUhy4k43S3wDJHceiqeKmXpBSFCFSBK5HyuCGBHr7-t; SecureNetflixId=v%3D3%26mac%3DAQEAEQABABTMKUJlBSG58EwKUNjiShKCe17fTYodiuw.%26dt%3D1783874192221; NetflixId=v%3D3%26ct%3DBgjHlOvcAxKZAzqyryoyc-LUwUPJGQ5fZsrSnWZKhhoZQ5QSbAVuvxOmjIbYLIPwphmVjqR52wXdNUeJLfj1di75k2kDQO_-SLbErGFnhksSd_px2DedqbL5wTY3x9_D06bcMvFvfAO9KVd2o82wXvZNWOab0m59UcBLLwLJR--c63hvWAojhmcs4U_Xi14hF3AgcShP_WPXZBefLbw3enLhO-InUu5lJRjEWPQbbb7DOYOpgOwnz-njq86uyYS7zSqFuw2N_cT4sMdmJ1_V23oAKg9AAg3bnBb7z9ieiel2YsAWGKfMSwgtRppBfZKc0TpNU6En_4NOwAvLfrXWX7E3GQg_43W7p3dxRTQhc1VfrPJrRV451iKt6u5lYoaq7qq4noI5sdwAr5amI-OBnQuw50YU2dKMVxOSnq6LsgMyGPHBMd4qU7yzwhfBAQQoiO_0jODWWtlQmQKE2skBkdL9GSpPm2cEj7Wx7pbxnnA878J3-cAPeShoY1uP86TLrSJZjGJcS-UdlVsPhQ3IxI3KSC0uJHFS5P-oesbCemi39m0YBiIOCgz-AG1K_HfI7lXWnsw.%26pg%3DE4UQOPLUERGP5H5TLQIITEVZ4I%26ch%3DAQEAEAABABT5WQX5qvSo_DRWohsHzrOAZR-NqaIaa78.; OptanonConsent=isGpcEnabled; netflix-mfa-nonce=BgjKu-vcAxKVAc0DUXYgDqIWVIzhYsnCKqapNSXdcVFK9cYXWP6nwuKKUEVHr8XYgaZqtljG2irj4VyLBbfEULpMUyUUccoCDGtb-HJUsjLXCqHU0YmP5kh7hBtXeNHmVOC_2lJoKiIwmsV_PK3EZLhj3NiTqa7InlZ4mgQ1-pyduR8jj2UDl3yEOqee7Z9P2B2-wl99zKnU-xyiv2n9GAYiDgoMssZccgelFQF52LGT; SecureNetflixId=v%3D3%26mac%3DAQEAEQABABQUf1AVs_qg5_qXuBMl5XBvTk8z3KiPLIU.%26dt%3D1783908403395; NetflixId=v%3D3%26ct%3DBgjHlOvcAxLEAa165jG28xojVluZFEqg5hdmfbmhvtFX3Ns-5X3myeqyycqLhWe5RCkaCPpem8Yoes_2CsJ8-rPhrWACl0Hc0oPQ4OdKMCRWKRo7BiQWoExmBNl0d7zB7e4oiEk6z7MHtMtYGKPZ0B2xvvdcMRe3U_Hkj0zxisOgKlhJUdawnEVjVDWHiN1J8ANN7NpLGmmamPBNQZJp23BrtWqfVIML3Zr4PM5Z1YDn5LthRdDcq1XSzlj9PY6iLWStftvPhnJeWVtC1kYYBiIOCgwvtoGR1vVu9TLWAdk.; OptanonConsent=isGpcEnabled=undefined&hosts=&datestamp=Mon+Jul+13+2026+09%3A42%3A03+GMT%2B0700+(Waktu+Indonesia+Barat)&version=202604.2.0"""

# Proses cookie jadi dict
cookies = {}
for c in cookie_str.split(';'):
    if '=' in c:
        k, v = c.strip().split('=', 1)
        cookies[k] = v

headers_netflix = {
    "Content-Type": "application/json",
    "Origin": "https://www.netflix.com",
    "Referer": "https://www.netflix.com/id/",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}

# ======================
# 📧 BUAT EMAIL BARU OTOMATIS (mail.tm)
# ======================
def buat_email_baru():
    try:
        # Ambil domain tersedia
        domain = requests.get("https://api.mail.tm/domains").json()["hydra:member"][0]["domain"]
        # Buat akun baru
        data = {
            "address": f"netflix_{__import__('random').randint(10000,99999)}@{domain}",
            "password": "Netfl!x12345"
        }
        res = requests.post("https://api.mail.tm/accounts", json=data)
        if res.status_code == 201:
            return data["address"], "✅ EMAIL BERHASIL DIBUAT!"
        return None, "❌ Gagal buat email"
    except Exception as e:
        return None, f"❌ Error email: {str(e)}"

# ======================
# 🚀 KIRIM KE NETFLIX DENGAN TOKEN MANUAL
# ======================
def kirim_ke_netflix(email_baru, token_manual):
    log = []
    log.append(f"📧 EMAIL BARU: {email_baru}")
    log.append("🌐 MENGIRIM KE NETFLIX...")
    
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
                    {"name": "recaptchaResponseTime", "value": {"intValue": 1200}},
                    {"name": "recaptchaResponseToken", "value": {"stringValue": token_manual.strip()}}
                ]
            },
            "extensions": {"persistedQuery": {"id": "0fd81de7-07af-4c7d-802f-0f4ea4181aa3", "version": 102}}
        }
        
        res = requests.post(
            "https://web.prod.cloud.netflix.com/graphql",
            headers=headers_netflix,
            cookies=cookies,
            json=payload,
            timeout=20
        )
        data = res.json()
        
        if "errors" not in data:
            log.append("✅ BERHASIL TERDAFTAR!")
            log.append("📩 Cek inbox email di atas untuk lanjut verifikasi!")
        else:
            log.append(f"⚠️ Pesan Netflix: {data['errors'][0]['message']}")
    
    except Exception as e:
        log.append(f"❌ Error kirim: {str(e)}")
    
    return "<br>".join(log)

# ======================
# 🌐 HALAMAN UTAMA
# ======================
@app.route('/', methods=['GET','POST'])
def index():
    hasil = ""
    token_input = ""
    email_hasil = ""
    
    if request.method == 'POST':
        token_input = request.form.get('token_captcha','').strip()
        if not token_input or len(token_input) < 50:
            hasil = "⚠️ MASUKKAN TOKEN CAPTCHA YANG VALID!"
        else:
            email_baru, pesan = buat_email_baru()
            hasil = pesan + "<br>"
            if email_baru:
                email_hasil = email_baru
                hasil += kirim_ke_netflix(email_baru, token_input)
    
    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Buat Akun Netflix Trial</title>
        <style>
            *{{box-sizing:border-box;margin:0;padding:0;}}
            body{{background:#111;color:#fff;font-family:monospace;padding:20px;max-width:500px;margin:auto;}}
            h2{{text-align:center;color:#e50914;margin-bottom:15px;}}
            .box{{background:#222;padding:15px;border-radius:10px;margin-bottom:10px;}}
            input,textarea{{width:100%;padding:10px;margin:5px 0;border:none;border-radius:6px;font-size:14px;}}
            textarea{{min-height:100px;resize:vertical;}}
            button{{width:100%;padding:12px;background:#e50914;color:#fff;border:none;border-radius:6px;font-weight:bold;font-size:16px;cursor:pointer;margin-top:5px;}}
            .log{{background:#000;padding:15px;border-radius:8px;margin-top:15px;color:#0f0;word-break:break-all;}}
            .email{{background:#2a2a2a;padding:10px;border-radius:6px;margin:10px 0;color:#ffb700;font-weight:bold;}}
        </style>
    </head>
    <body>
        <h2>🎁 BUAT AKUN TRIAL NETFLIX</h2>
        <div class="box">
            <form method="POST">
                <label>🔑 TEMPEL TOKEN CAPTCHA DI BAWAH:</label>
                <textarea name="token_captcha" placeholder="Ambil token dari skrip Tampermonkey lu, lalu tempel di sini..." required>{token_input}</textarea>
                <button type="submit">🚀 BUAT & DAFTARKAN</button>
            </form>
        </div>
        {f'<div class="email">📧 EMAIL DIBUAT: {email_hasil}</div>' if email_hasil else ''}
        <div class="log">{hasil or "Masukkan token reCAPTCHA lu lalu klik tombol di atas"}</div>
    </body>
    </html>
    """
    return render_template_string(html)

# WAJIB UNTUK VERCEL
if __name__ != "__main__":
    application = app
