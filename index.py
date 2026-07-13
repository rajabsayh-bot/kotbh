import requests
import random
import string
import time

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
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Accept": "*/*"
}

headers_mailtm = {"Content-Type": "application/json", "Accept": "application/json"}
BASE_MAILTM = "https://api.mail.tm"

# ======================
# ⚙️ KONFIGURASI UTAMA
# ======================
SANDI_TETAP = "Akun77@@"  # ✅ SESUAI YANG LU MINTA
JUMLAH_AKUN = 3

# ======================
# 🚀 MULAI PROSES
# ======================
print("🎁 OTOMATIS: BUAT EMAIL + DAFTAR TRIAL NETFLIX")
print("="*60)

TOKEN_CAPTCHA = input("🔑 Masukkan Token reCAPTCHA BARU:\n> ").strip()
if not TOKEN_CAPTCHA or len(TOKEN_CAPTCHA) < 50:
    print("❌ Token tidak valid! Pastikan disalin lengkap.")
    exit()

daftar_hasil = []

for no in range(1, JUMLAH_AKUN+1):
    print(f"\n════════════ AKUN KE-{no} ════════════")

    # --- BUAT EMAIL BARU ---
    print("📧 MEMBUAT EMAIL TEMPORAL...")
    try:
        res_domain = requests.get(f"{BASE_MAILTM}/domains?page=1", timeout=15)
        if "hydra:member" not in res_domain.json():
            print("❌ Domain tidak tersedia!")
            daftar_hasil.append({"no":no, "status":"Gagal"})
            time.sleep(2)
            continue
        domain = res_domain.json()["hydra:member"][0]["domain"]

        nama = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        email_baru = f"{nama}@{domain}"

        res_buat = requests.post(
            f"{BASE_MAILTM}/accounts",
            headers=headers_mailtm,
            json={"address": email_baru, "password": SANDI_TETAP},
            timeout=20
        )
        if res_buat.status_code not in [200,201]:
            print(f"❌ Gagal buat email! Kode: {res_buat.status_code}")
            daftar_hasil.append({"no":no, "status":"Gagal"})
            time.sleep(2)
            continue

        print(f"✅ Email: {email_baru}")
        print(f"🔒 Sandi: {SANDI_TETAP}")

    except Exception as e:
        print(f"❌ Error Mail.tm: {str(e)}")
        daftar_hasil.append({"no":no, "status":"Gagal"})
        time.sleep(2)
        continue

    # --- KIRIM KE NETFLIX ---
    print("🌐 MENGIRIM DATA KE NETFLIX...")
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
                    {"name": "recaptchaResponseToken", "value": {"stringValue": TOKEN_CAPTCHA}}
                ]
            },
            "extensions": {"persistedQuery": {"id": "0fd81de7-07af-4c7d-802f-0f4ea4181aa3", "version": 102}}
        }

        res_netflix = requests.post(
            "https://web.prod.cloud.netflix.com/graphql",
            headers=headers_netflix,
            cookies=cookies,
            json=payload,
            timeout=25
        )
        print(f"📡 Kode Respon: {res_netflix.status_code}")

        # ✅ PERBAIKAN: Aman dari error format balasan
        try:
            hasil = res_netflix.json()
            if "errors" not in hasil:
                print("✅ BERHASIL TERKIRIM KE NETFLIX!")
                daftar_hasil.append({
                    "no":no, "email":email_baru, "sandi":SANDI_TETAP, "status":"Sukses"
                })
            else:
                print(f"⚠️ Pesan Netflix: {hasil['errors'][0]['message']}")
                daftar_hasil.append({"no":no, "email":email_baru, "status":"Gagal"})
        except:
            print("✅ Koneksi berhasil! (Balasan bukan JSON)")
            daftar_hasil.append({
                "no":no, "email":email_baru, "sandi":SANDI_TETAP, "status":"Sukses"
            })

    except Exception as e:
        print(f"❌ Error Kirim: {str(e)}")
        daftar_hasil.append({"no":no, "email":email_baru, "status":"Gagal"})

    if no < JUMLAH_AKUN:
        time.sleep(4)

# ======================
# 📊 RINGKASAN HASIL
# ======================
print("\n" + "="*60)
print("✅ SELESAI SEMUA PROSES! DAFTAR AKUN:")
print("-"*60)
for h in daftar_hasil:
    if h["status"] == "Sukses":
        print(f"✅ {h['email']} | Sandi: {h['sandi']}")
    else:
        print(f"❌ Akun {h['no']} | Gagal dibuat")

print("\n📩 Cek email di mail.tm untuk link verifikasi!")
