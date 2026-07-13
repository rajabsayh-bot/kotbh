from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# ======================
# 🍪 DATA SESI NETFLIX
# ======================
cookie_str = """flwssn=c582c946-7e27-4cfc-a6f4-48597c0070bc;gsid=34197de4-f1e9-4d42-b254-2865906eaadc;SecureNetflixId=v%3D3%26mac%3DAQEAEQABABScAQhKHK_HuVx13xuvLPOZGaPEwMI39hU.%26dt%3D1783875815871;NetflixId=v%3D3%26ct%3DBgjHlOvcAxK8AQg10SjdRnmbKEnp_JwzTpYamPvvywqzDSxlVbfr7kEfypWwm-YnIOc5UKoMzSoX21d7H6Uv3gi99VO6YFb5yS8MELHcvWaOJ9b7Rgcz65RtCNlX3bVgtCGLl3aDae3Ol7Koi4xyli2Rt9OV9vgYoJ9-JHWXVvLLd9eiKX1t0-9zfo3Mvw_eP1EHlgO0bpMLyPKSDfKIo4eYN03OQPVjOA9OagAVRfudG6cbKKQPmCtnwhtdYrWIoajCsy0vGAYiDgoMqmTj8AHHlLk_smSQ;nfvdid=BQFmAAEBEAOpPCJrtFJLPu3EKNJPsT5glpLRsf9RvpeRRLKb5eyg0OguTiK2I3yonVDQtPZn77s2lTpJx4EFtQlDo52Gt7W0QdkqB0FINaROcR1E4W2ygtkUrA0hpb5CnRJWojAB_dbD8OPclxkUoHpETUwrBKDL;"""

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
# 🚀 HALAMAN UTAMA
# ======================
@app.route('/', methods=['GET','POST'])
def index():
    hasil = ""
    email_input = ""
    
    if request.method == 'POST':
        email_input = request.form.get('email_lu','').strip()
        token = request.form.get('token_cap','').strip()
        
        if not email_input or "@" not in email_input:
            hasil = "⚠️ MASUKKAN EMAIL YANG VALID!"
        elif not token or len(token) < 50:
            hasil = "⚠️ MASUKKAN TOKEN CAPTCHA LENGKAP!"
        else:
            hasil = f"📧 Email tujuan: {email_input}<br>⏳ SEDANG MENGIRIM KE NETFLIX...<br>"
            
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
                            {"name": "email", "value": {"stringValue": email_input}},
                            {"name": "pipcConsent", "value": {"booleanValue": False}},
                            {"name": "emailConsent", "value": {"booleanValue": False}},
                            {"name": "recaptchaResponseTime", "value": {"intValue": 1200}},
                            {"name": "recaptchaResponseToken", "value": {"stringValue": token}}
                        ]
                    },
                    "extensions": {"persistedQuery": {"id": "0fd81de7-07af-4c7d-802f-0f4ea4181aa3", "version": 102}}
                }
                
                res = requests.post(
                    "https://web.prod.cloud.netflix.com/graphql",
                    headers=headers_netflix,
                    cookies=cookies,
                    json=payload,
                    timeout=25
                )
                
                hasil += f"📡 Respon Server: {res.status_code}<br>"
                if res.status_code == 200:
                    hasil += "✅ BERHASIL TERKIRIM!<br>📩 Cek inbox email lu untuk pesan dari Netflix!"
                else:
                    hasil += f"⚠️ Balasan: {res.text[:200]}"
            
            except Exception as e:
                hasil += f"❌ Error: {str(e)}"
    
    return render_template_string(f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Kirim Link Netflix</title>
        <style>
            *{{box-sizing:border-box;margin:0;padding:0;}}
            body{{background:#111;color:#fff;font-family:monospace;padding:20px;max-width:500px;margin:auto;}}
            h2{{color:#e50914;text-align:center;margin-bottom:20px;}}
            .kotak{{background:#222;padding:20px;border-radius:12px;border:1px solid #ffb700;}}
            input,textarea{{width:100%;padding:12px;margin:8px 0;border-radius:8px;border:none;background:#000;color:#fff;font-size:14px;}}
            button{{width:100%;padding:14px;background:linear-gradient(90deg,#e50914,#ff3333);color:#fff;border:none;border-radius:8px;font-weight:bold;font-size:16px;margin-top:10px;}}
            .log{{margin-top:20px;padding:12px;background:#000;border-radius:8px;color:#0f0;word-break:break-all;}}
        </style>
    </head>
    <body>
        <h2>📤 KIRIM LINK PENDAFTARAN</h2>
        <div class="kotak">
            <form method="POST">
                <label>📧 Masukkan Email Tujuan:</label>
                <input type="email" name="email_lu" value="{email_input}" placeholder="contoh: nama@gmail.com" required>
                
                <label>🔑 Tempel Token CAPTCHA:</label>
                <textarea name="token_cap" placeholder="Ambil dari skrip Tampermonkey..." required></textarea>
                
                <button type="submit">🚀 KIRIM KE EMAIL</button>
            </form>
            <div class="log">{hasil}</div>
        </div>
    </body>
    </html>
    """)

application = app
        
