from flask import Flask, render_template_string, request
import requests, random, string, time, re, base64

app = Flask(__name__)

# ======================
# 🍪 COOKIE TERBARU
# ======================
cookie_str = """OTSessionTracking=87b6a5c0-0104-4e96-a291-092c11350111; flwssn=c582c946-7e27-4cfc-a6f4-48597c0070bc; gsid=caa4812a-9963-4def-9167-b601f191cfc5; netflix-sans-normal-3-loaded=true; netflix-sans-bold-3-loaded=true; nfvdid=BQFmAAEBEFECklCXwPof2v9oq0m-kSRgvhoBMFMGUDA7VDqWzhfh6d_0vpcH50lGalU_bxnBEk7nNy4QPSA0ConA19vDmIPnohyqr0WFLyg2fo0JhJEX0UUhy4k43S3wDJHceiqeKmXpBSFCFSBK5HyuCGBHr7-t; SecureNetflixId=v%3D3%26mac%3DAQEAEQABABTMKUJlBSG58EwKUNjiShKCe17fTYodiuw.%26dt%3D1783874192221; NetflixId=v%3D3%26ct%3DBgjHlOvcAxKZAzqyryoyc-LUwUPJGQ5fZsrSnWZKhhoZQ5QSbAVuvxOmjIbYLIPwphmVjqR52wXdNUeJLfj1di75k2kDQO_-SLbErGFnhksSd_px2DedqbL5wTY3x9_D06bcMvFvfAO9KVd2o82wXvZNWOab0m59UcBLLwLJR--c63hvWAojhmcs4U_Xi14hF3AgcShP_WPXZBefLbw3enLhO-InUu5lJRjEWPQbbb7DOYOpgOwnz-njq86uyYS7zSqFuw2N_cT4sMdmJ1_V23oAKg9AAg3bnBb7z9ieiel2YsAWGKfMSwgtRppBfZKc0TpNU6En_4NOwAvLfrXWX7E3GQg_43W7p3dxRTQhc1VfrPJrRV451iKt6u5lYoaq7qq4noI5sdwAr5amI-OBnQuw50YU2dKMVxOSnq6LsgMyGPHBMd4qU7yzwhfBAQQoiO_0jODWWtlQmQKE2skBkdL9GSpPm2cEj7Wx7pbxnnA878J3-cAPeShoY1uP86TLrSJZjGJcS-UdlVsPhQ3IxI3KSC0uJHFS5P-oesbCemi39m0YBiIOCgz-AG1K_HfI7lXWnsw.%26pg%3DE4UQOPLUERGP5H5TLQIITEVZ4I%26ch%3DAQEAEAABABT5WQX5qvSo_DRWohsHzrOAZR-NqaIaa78.; OptanonConsent=isGpcEnabled; netflix-sans-normal-3-loaded=true; netflix-sans-bold-3-loaded=true; OTSessionTracking=87b6a5c0-0104-4e96-a291-092c11350111; netflix-mfa-nonce=BgjKu-vcAxKVAc0DUXYgDqIWVIzhYsnCKqapNSXdcVFK9cYXWP6nwuKKUEVHr8XYgaZqtljG2irj4VyLBbfEULpMUyUUccoCDGtb-HJUsjLXCqHU0YmP5kh7hBtXeNHmVOC_2lJoKiIwmsV_PK3EZLhj3NiTqa7InlZ4mgQ1-pyduR8jj2UDl3yEOqee7Z9P2B2-wl99zKnU-xyiv2n9GAYiDgoMssZccgelFQF52LGT; flwssn=c582c946-7e27-4cfc-a6f4-48597c0070bc; nfvdid=BQFmAAEBEAOpPCJrtFJLPu3EKNJPsT5glpLRsf9RvpeRRLKb5eyg0OguTiK2I3yonVDQtPZn77s2lTpJx4EFtQlDo52Gt7W0QdkqB0FINaROcR1E4W2ygtkUrA0hpb5CnRJWojAB_dbD8OPclxkUoHpETUwrBKDL; SecureNetflixId=v%3D3%26mac%3DAQEAEQABABQUf1AVs_qg5_qXuBMl5XBvTk8z3KiPLIU.%26dt%3D1783908403395; NetflixId=v%3D3%26ct%3DBgjHlOvcAxLEAa165jG28xojVluZFEqg5hdmfbmhvtFX3Ns-5X3myeqyycqLhWe5RCkaCPpem8Yoes_2CsJ8-rPhrWACl0Hc0oPQ4OdKMCRWKRo7BiQWoExmBNl0d7zB7e4oiEk6z7MHtMtYGKPZ0B2xvvdcMRe3U_Hkj0zxisOgKlhJUdawnEVjVDWHiN1J8ANN7NpLGmmamPBNQZJp23BrtWqfVIML3Zr4PM5Z1YDn5LthRdDcq1XSzlj9PY6iLWStftvPhnJeWVtC1kYYBiIOCgwvtoGR1vVu9TLWAdk.; OptanonConsent=isGpcEnabled=undefined&hosts=&datestamp=Mon+Jul+13+2026+09%3A42%3A03+GMT%2B0700+(Waktu+Indonesia+Barat)&version=202604.2.0"""

cookies = {c.strip().split('=',1)[0]:c.strip().split('=',1)[1] for c in cookie_str.split(';') if '=' in c}
headers_netflix = {"Content-Type":"application/json","Origin":"https://www.netflix.com","Referer":"https://www.netflix.com/id/","User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36","Accept":"*/*"}
headers_mailtm = {"Content-Type":"application/json","Accept":"application/json"}
BASE_MAILTM = "https://api.mail.tm"

# ======================
# 📧 BACA EMAIL OTOMATIS
# ======================
def baca_email(email, sandi):
    log = ["📥 MENUNGGU PESAN VERIFIKASI..."]
    try:
        login = requests.post(f"{BASE_MAILTM}/token", json={"address":email,"password":sandi}, timeout=15)
        if login.status_code != 200:
            log.append("❌ Gagal masuk ke email!")
            return "<br>".join(log)
        token = login.json()["token"]
        h = {"Authorization":f"Bearer {token}","Accept":"application/json"}

        for cek in range(8):
            time.sleep(3)
            pesan = requests.get(f"{BASE_MAILTM}/messages?page=1", headers=h, timeout=10).json()
            if pesan["hydra:totalItems"] > 0:
                id_pesan = pesan["hydra:member"][0]["id"]
                isi = requests.get(f"{BASE_MAILTM}/messages/{id_pesan}", headers=h, timeout=10).json()
                log.append("✅ PESAN DITERIMA DARI NETFLIX!")
                log.append(f"📝 Subjek: {isi['subject']}")
                teks = isi.get("text","") or isi.get("html","")
                link = re.search(r'https?://[^\s<>"]+verification[^\s<>"]+|https?://www.netflix.com/[^\s<>"]+', teks)
                if link:
                    log.append(f"🔗 LINK VERIFIKASI: {link.group()}")
                else:
                    log.append("⚠️ Link tidak ditemukan")
                return "<br>".join(log)
        log.append("⏰ Pesan tidak masuk!")
        return "<br>".join(log)
    except Exception as e:
        log.append(f"❌ Error: {str(e)}")
        return "<br>".join(log)

# ======================
# 🚀 PROSES UTAMA
# ======================
def proses_utama(token_input):
    log = ["🎁 MEMULAI PROSES PENDAFTARAN...", "="*50]
    
    if not token_input.strip():
        log.append("❌ SILAKAN ISI TOKEN CAPTCHA TERLEBIH DAHULU!")
        return "<br>".join(log)
    token = token_input.strip()
    log.append("✅ TOKEN DITERIMA!")

    # Buat email
    log.append("📧 MEMBUAT EMAIL TEMPORAL...")
    try:
        dom = requests.get(f"{BASE_MAILTM}/domains?page=1", timeout=10).json()["hydra:member"][0]["domain"]
        nama = ''.join(random.choices(string.ascii_lowercase+string.digits,k=8))
        email = f"{nama}@{dom}"
        sandi = "UjiCoba99!"
        requests.post(f"{BASE_MAILTM}/accounts", headers=headers_mailtm, json={"address":email,"password":sandi}, timeout=15)
        log.append(f"✅ Email: {email}")
        log.append(f"🔑 Sandi: {sandi}")
    except Exception as e:
        log.append(f"❌ Gagal buat email: {str(e)}")
        return "<br>".join(log)

    # Kirim ke Netflix
    log.append("🌐 MENGIRIM KE NETFLIX...")
    try:
        payload = {"operationName":"CLCSScreenUpdate","variables":{"format":"HTML","imageFormat":"PNG","locale":"id-ID","serverState":"Bgjru+vcAxLTAU5En5gcaO7v7XjiK+rXFXxxInfs8S2xATg1JspUbo5FZiJWBmEvMVgdmR9SZ6ls/tnJzL2DiX1ZpEDzTPySXay5oWh+n159DQ0ZUzEH+DCPYegrj4HGBUH4jrx+k8r4V+RiwbCJri5hIJHBkm0U9DVbKQh6ngOFzJN+5ZyyV+Z0mlhhyhXawaHsrzyGLYsAO6VPXuyv9iRMihw6vAInnOOX5L/1NoByQC8aQQ7pZJ1JFMicXH3Zf1Vekx/pWvjGtP42MFXS+JARtzgeGtGdpeYCzJcYBiIOCgwDpEr8YdrJKDhAXJc=","serverScreenUpdate":"Bgjru+vcAxKSAn/xAw6MYX1AnpCWZuYykLwpMOkPstB/IWV1LG0TdgJeL6p3V/Rxc0H6Y1AjdGQnoq7pXXz/pvxZNUJBtnSnlEmbjxoi1Kzmx/XG7RjpVbm+CpCfToe6w6XPO3clBmha2mTEuPCtN2XUF1awZle4yJbeK1E1fZe80Zy8AClUxyXf2aR6sxF1YyiizlGzKwz78LudjMDcJwTXchHLkvQsAXelj9/Kvx8dk8d/m8zpx1A2gLeB+laz/WXEcsMvbvrEM8JbIN4+vreqiX2YQTWdORZNOWlKU3EnbkbHpZzClCqM3ij5Yr8PiCaSuR4wM82XYaw/7R1Z3ofu1oAKXIRRHCmdvvhdiy3w8/b+zCDCYOtsL7YYBiIOCgxMBpdIbc9NcH5VZOM=","inputFields":[{"name":"email","value":{"stringValue":email}},{"name":"pipcConsent","value":{"booleanValue":False}},{"name":"emailConsent","value":{"booleanValue":False}},{"name":"recaptchaResponseTime","value":{"intValue":1096}},{"name":"recaptchaResponseToken","value":{"stringValue":token}}]},"extensions":{"persistedQuery":{"id":"0fd81de7-07af-4c7d-802f-0f4ea4181aa3","version":102}}}
        res = requests.post("https://web.prod.cloud.netflix.com/graphql", headers=headers_netflix, cookies=cookies, json=payload, timeout=15)
        if "errors" in res.json():
            log.append(f"⚠️ {res.json()['errors'][0]['message']}")
        else:
            log.append("✅ PENDAFTARAN BERHASIL DIKIRIM!")
    except Exception as e:
        log.append(f"❌ Error: {str(e)}")
        return "<br>".join(log)

    log.append("")
    log.append(baca_email(email, sandi))
    log.append("<br>✅ SELESAI!")
    return "<br>".join(log)

# ======================
# 🌐 HALAMAN DENGAN INPUT & TAMPIL HASIL
# ======================
@app.route('/', methods=['GET','POST'])
def index():
    hasil_log = ""
    if request.method == 'POST':
        hasil_log = proses_utama(request.form.get('token',''))

    html = f"""
    <html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>INPUT TOKEN & HASIL</title>
    <style>
    *{{box-sizing:border-box;margin:0;padding:0;}}
    body{{background:#111;color:#0f0;font-family:monospace;padding:20px;max-width:550px;margin:auto;}}
    h1{{text-align:center;color:#ff3355;margin-bottom:20px;font-size:22px;}}
    .form{{background:#222;padding:20px;border-radius:10px;margin-bottom:20px;}}
    label{{font-size:16px;color:#fff;display:block;margin-bottom:8px;}}
    #token{{width:100%;padding:12px;border:1px solid #444;border-radius:6px;background:#333;color:#fff;font-size:14px;margin-bottom:12px;}}
    button{{width:100%;padding:14px;background:#e50914;color:#fff;border:none;border-radius:6px;font-size:16px;font-weight:bold;cursor:pointer;}}
    button:active{{transform:scale(0.98);}}
    .hasil{{background:#000;padding:15px;border-radius:8px;white-space:pre-wrap;word-break:break-all;font-size:14px;line-height:1.7;margin-top:15px;}}
    .info{{color:#ffaa00;margin-top:10px;font-size:13px;}}
    </style>
    </head><body>
    <h1>🎁 OTOMATIS PENDAFTARAN NETFLIX</h1>

    <div class="form">
        <form method="POST">
            <label for="token">✍️ MASUKKAN TOKEN CAPTCHA DI SINI:</label>
            <input type="text" id="token" name="token" placeholder="Tempel token reCAPTCHA lu di sini...">
            <button type="submit">🚀 MULAI PROSES</button>
            <div class="info">💡 Nanti di bawah akan tampil semua proses & hasilnya</div>
        </form>
    </div>

    <div class="hasil">
    {hasil_log if hasil_log else '📝 HASIL PROSES AKAN MUNCUL DI SINI...\n\n(Setelah klik tombol di atas ya jir!)'}
    </div>

    </body></html>
    """
    return render_template_string(html)

if __name__ != "__main__":
    application = app
