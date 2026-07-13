from flask import Flask, render_template_string, request
import requests
import random

app = Flask(__name__)

# ======================
# ⚙️ KONFIGURASI TETAP
# ======================
PASSWORD_TETAP = "Akun77@@"
cookie_str = """OTSessionTracking=87b6a5c0-0104-4e96-a291-092c11350111; flwssn=c582c946-7e27-4cfc-a6f4-48597c0070bc; gsid=caa4812a-9963-4def-9167-b601f191cfc5; SecureNetflixId=v%3D3%26mac%3DAQEAEQABABTMKUJlBSG58EwKUNjiShKCe17fTYodiuw.%26dt%3D1783874192221; NetflixId=v%3D3%26ct%3DBgjHlOvcAxKZAzqyryoyc-LUwUPJGQ5fZsrSnWZKhhoZQ5QSbAVuvxOmjIbYLIPwphmVjqR52wXdNUeJLfj1di75k2kDQO_-SLbErGFnhksSd_px2DedqbL5wTY3x9_D06bcMvFvfAO9KVd2o82wXvZNWOab0m59UcBLLwLJR--c63hvWAojhmcs4U_Xi14hF3AgcShP_WPXZBefLbw3enLhO-InUu5lJRjEWPQbbb7DOYOpgOwnz-njq86uyYS7zSqFuw2N_cT4sMdmJ1_V23oAKg9AAg3bnBb7z9ieiel2YsAWGKfMSwgtRppBfZKc0TpNU6En_4NOwAvLfrXWX7E3GQg_43W7p3dxRTQhc1VfrPJrRV451iKt6u5lYoaq7qq4noI5sdwAr5amI-OBnQuw50YU2dKMVxOSnq6LsgMyGPHBMd4qU7yzwhfBAQQoiO_0jODWWtlQmQKE2skBkdL9GSpPm2cEj7Wx7pbxnnA878J3-cAPeShoY1uP86TLrSJZjGJcS-UdlVsPhQ3IxI3KSC0uJHFS5P-oesbCemi39m0YBiIOCgz-AG1K_HfI7lXWnsw.%26pg%3DE4UQOPLUERGP5H5TLQIITEVZ4I%26ch%3DAQEAEAABABT5WQX5qvSo_DRWohsHzrOAZR-NqaIaa78.; OptanonConsent=isGpcEnabled"""

cookies = {}
for c in cookie_str.split(';'):
    if '=' in c:
        k, v = c.strip().split('=', 1)
        cookies[k] = v

headers = {
    "Content-Type": "application/json",
    "Referer": "https://www.netflix.com/id/",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}

# ======================
# 📧 BUAT EMAIL OTOMATIS
# ======================
def buat_email():
    try:
        domain = requests.get("https://api.mail.tm/domains").json()["hydra:member"][0]["domain"]
        alamat = f"nf{random.randint(100000,999999)}@{domain}"
        requests.post("https://api.mail.tm/accounts", json={"address": alamat, "password": PASSWORD_TETAP})
        return alamat, "✅ Email berhasil dibuat"
    except Exception as e:
        return None, f"❌ Gagal buat email: {str(e)}"

# ======================
# 🚀 PERBAIKAN: TIDAK ERROR LAGI SAAT BACA BALASAN
# ======================
def kirim_netflix(email_baru, token_captcha):
    log = []
    log.append(f"📧 Email: {email_baru}")
    log.append(f"🔒 Sandi: {PASSWORD_TETAP}")
    
    try:
        url_api = "https://www.netflix.com/signup/api/register"
        data_kirim = {
            "email": email_baru,
            "password": PASSWORD_TETAP,
            "recaptchaToken": token_captcha.strip(),
            "country": "ID",
            "locale": "id-ID",
            "flow": "signup"
        }
        
        res = requests.post(url_api, headers=headers, cookies=cookies, json=data_kirim, timeout=25)
        log.append(f"📡 Kode Respon: {res.status_code}")

        # ✅ PERBAIKAN: Cek dulu apakah balasannya JSON
        try:
            hasil = res.json()
            if hasil.get("success") or "nextAction" in hasil or "user" in hasil:
                log.append("✅ BERHASIL TERDAFTAR!")
                log.append("📩 Cek inbox email untuk verifikasi akun!")
            else:
                pesan = hasil.get('message', hasil.get('error', 'Tidak ada info tambahan'))
                log.append(f"⚠️ Info Netflix: {pesan}")
        except:
            # Kalau bukan JSON, tampilkan teks biasa
            log.append("ℹ️ Balasan bukan format JSON, tapi koneksi BERHASIL!")
            log.append(f"📝 Isi balasan: {res.text[:150]}...")
    
    except Exception as e:
        log.append(f"❌ Error Koneksi: {str(e)}")
    
    return "<br>".join(log)

# ======================
# 🌐 HALAMAN DENGAN ANIMASI
# ======================
@app.route('/', methods=['GET','POST'])
def index():
    hasil = ""
    email_tampil = ""
    
    if request.method == 'POST':
        token = request.form.get('token_cap','').strip()
        if not token or len(token) < 50:
            hasil = "⚠️ TOKEN CAPTCHA TIDAK LENGKAP! Pastikan disalin penuh."
        else:
            email_baru, pesan = buat_email()
            hasil = pesan + "<br>"
            if email_baru:
                email_tampil = email_baru
                hasil += kirim_netflix(email_baru, token)
    
    return render_template_string(f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Buat Akun Netflix Trial</title>
        <style>
            *{{box-sizing:border-box;margin:0;padding:0;}}
            body{{
                background:linear-gradient(135deg,#1a1a1a,#000);
                color:#fff;
                font-family:'Segoe UI',monospace;
                padding:20px;
                max-width:500px;
                margin:auto;
                min-height:100vh;
            }}
            h2{{
                color:#e50914;
                text-align:center;
                margin-bottom:20px;
                text-shadow:0 0 10px #e5091480;
            }}
            .kotak{{
                background:#2229;
                padding:20px;
                border-radius:15px;
                border:1px solid #ffb70040;
                backdrop-filter:blur(10px);
                box-shadow:0 0 20px #0008;
            }}
            textarea{{
                width:100%;
                min-height:120px;
                padding:12px;
                border-radius:8px;
                border:1px solid #444;
                background:#111;
                color:#0f0;
                font-size:13px;
                margin:10px 0;
                resize:vertical;
            }}
            button{{
                width:100%;
                padding:14px;
                background:linear-gradient(90deg,#e50914,#ff3333);
                color:#fff;
                border:none;
                border-radius:8px;
                font-weight:bold;
                font-size:16px;
                cursor:pointer;
                transition:all 0.3s;
                box-shadow:0 4px 15px #e5091460;
            }}
            button:hover{{transform:translateY(-2px);box-shadow:0 6px 20px #e5091480;}}
            button:disabled{{background:#555;cursor:not-allowed;transform:none;}}

            /* ANIMASI LOADING */
            .loading{{
                display:none;
                flex-direction:column;
                align-items:center;
                gap:15px;
                margin:20px 0;
                padding:20px;
                background:#1119;
                border-radius:10px;
                border:1px dashed #ffb700;
            }}
            .aktif{{display:flex;}}
            .spinner{{
                width:50px;
                height:50px;
                border:4px solid #333;
                border-top:4px solid #e50914;
                border-right:4px solid #ffb700;
                border-radius:50%;
                animation:putar 0.8s linear infinite;
            }}
            @keyframes putar{{100%{{transform:rotate(360deg);}}}}
            .teks-loading{{
                color:#ffb700;
                font-weight:bold;
                animation:kedip 1s infinite;
            }}
            @keyframes kedip{{0%,100%{{opacity:1;}}50%{{opacity:0.4;}}}}

            .info{{
                background:#2a2a2a;
                padding:12px;
                border-radius:8px;
                margin:15px 0;
                color:#ffb700;
                border-left:4px solid #ffb700;
            }}
            .log{{
                margin-top:15px;
                padding:12px;
                background:#000;
                border-radius:8px;
                color:#0f0;
                word-break:break-all;
                border:1px solid #333;
            }}
        </style>
    </head>
    <body>
        <h2>🎁 BUAT AKUN TRIAL NETFLIX</h2>
        <div class="kotak">
            <form method="POST" id="formUtama">
                <label>🔑 Tempel Token CAPTCHA:</label>
                <textarea name="token_cap" placeholder="Ambil token dari skrip Tampermonkey, tempel di sini..." required></textarea>
                
                <div class="info">
                    ⚙️ Pengaturan Otomatis:<br>
                    • Sandi Akun: <b>{PASSWORD_TETAP}</b><br>
                    • Email: Dibuat otomatis
                </div>

                <button type="submit" id="btnKirim">🚀 MULAI PEMBUATAN AKUN</button>
            </form>

            <div class="loading" id="animasiLoad">
                <div class="spinner"></div>
                <div class="teks-loading">⏳ SEDANG MEMBUAT EMAIL...</div>
                <div class="teks-loading">⏳ MENGIRIM DATA KE NETFLIX...</div>
            </div>

            {f'<div class="info">📧 EMAIL BARU: {email_tampil}</div>' if email_tampil else ''}
            <div class="log">{hasil or "Siap untuk membuat akun baru!"}</div>
        </div>

        <script>
            const form = document.getElementById('formUtama');
            const btn = document.getElementById('btnKirim');
            const load = document.getElementById('animasiLoad');
            form.addEventListener('submit', ()=>{{
                btn.disabled = true;
                btn.textContent = "⏳ MEMPROSES...";
                load.classList.add('aktif');
            }});
        </script>
    </body>
    </html>
    """)

application = app
        
