from flask import Flask, render_template_string, request
import requests
import random
import string
import time
import re

app = Flask(__name__)

# ======================
# ⚙️ SEMUA JEDA 5 DETIK SAJA!
# ======================
BASE_MAILTM = "https://api.mail.tm"
JEDA_SEMUA = 5  # ✅ SEMUA JEDA DISET 5 DETIK

COOKIE_PANCING = """flwssn=c582c946-7e27-4cfc-a6f4-48597c0070bc;gsid=34197de4-f1e9-4d42-b254-2865906eaadc;SecureNetflixId=v%3D3%26mac%3DAQEAEQABABScAQhKHK_HuVx13xuvLPOZGaPEwMI39hU.%26dt%3D1783875815871;NetflixId=v%3D3%26ct%3DBgjHlOvcAxK8AQg10SjdRnmbKEnp_JwzTpYamPvvywqzDSxlVbfr7kEfypWwm-YnIOc5UKoMzSoX21d7H6Uv3gi99VO6YFb5yS8MELHcvWaOJ9b7Rgcz65RtCNlX3bVgtCGLl3aDae3Ol7Koi4xyli2Rt9OV9vgYoJ9-JHWXVvLLd9eiKX1t0-9zfo3Mvw_eP1EHlgO0bpMLyPKSDfKIo4eYN03OQPVjOA9OagAVRfudG6cbKKQPmCtnwhtdYrWIoajCsy0vGAYiDgoMqmTj8AHHlLk_smSQ;nfvdid=BQFmAAEBEAOpPCJrtFJLPu3EKNJPsT5glpLRsf9RvpeRRLKb5eyg0OguTiK2I3yonVDQtPZn77s2lTpJx4EFtQlDo52Gt7W0QdkqB0FINaROcR1E4W2ygtkUrA0hpb5CnRJWojAB_dbD8OPclxkUoHpETUwrBKDL;"""
TOKEN_CAPTCHA = "0cAFcWeA5m7857yGu6XxJv3lLY7F0vBLZndiRsGdamrmRN2KVhxoDra7f10jlFc-xYUW6EWuNhr1VhrW-Tjgg0GZIkmkPrYAxcaxjih20kbWuQ5S9n3p4ff8E8ueGDuPOnQ2o-IvF5Rl5-Dt6n-Kd8J7w587_x1b3Su4TUfcHCRhXyIgQQobvZyhcqP6S20THtv5Eovo_cDC9-6jtoWRrRVTmUgAJMC2mYY6UDJOTjNLpV-O_oZVJwLBTqQGVgOFVimrf5pWQiQidkOi8t5-QeLUR2P6sR-jiXFwm7rvF-fAcvetOdejovw8pA2u7WXMqeFy1PKghSRKquTYJpZnLksA-Vl7rgTVhlGEFpUxybuESY2nY3B3VvZQG7-RkvpJK14qJY6J4Y2pgqki8pMEpyDmsgGB4Tk2r89TNEZ5-Tm5agZ7G3r1NF6N8egWgd-QGAUW5te3Crh8AnheQxGK8nwMh-Xg9npo6bKhAcoP59Lc7K3wstwFuezDxxSXwGKdnWQeb9V3dk4EEIM8ay8Fu36VcVvayB-viOXSYamlVk9MDyL-bd5JEeIJw0SLsKxT7q_JLvi5ZoG2y9lekU_14Nf6gRcPE4gSJbbeIhimDFmlabQ2xlfyv4Q0xS-sBwjzNFaWJpyzc9kLwX65QyzxHzaxcVG-4uAEm2NmTYL6owdX4N6N7Q0HL0DX2EW2au-eUdUMVV4FIBZX3grTahwqQLmbNwOP_TAtAhC0ot5LzscGYiMYXvUSrQGLCvu7JM4qGo4wDEPKV98_8OXL8gjPd3jEN8y7ScvgYlQCX-9zrBFDChg9eMtyQRiL4s8s4BLAJj98ZXqZvcUxJgroexmCInuSuVpeSB2kMRq_hiVawyTgjbbu0mp_pnk9MOwnNZQDNfvMNV-bFACrY26B4el5VMoxifIj15m30jAJyeo_8xYB04IAGuPFAFBCBWsT1YvOxuafB_zWq7Y91WXw5CYBdNnuTMP0GoR6zfdzQ5ovWqPmDJYBhIO0C9Z-BZcIT3YQkz8-P_2MIUnlFk7QposqW71pCF5K0AaF2LSHlb80pjnM5B5jDKt-BmmK9c311ZMgIRsCb3_fs5rwfr5PIDDjPB_UhqeKG4lcuRkK5X36STOnPJ6gNyQeKSYX0eJovs-sTXybV6d_j_c62Rk7WYHE9yLL5b4XqIgHrOSZhrpnGTluyYkX6zSIOsCuPeCJfbSoOPERbvfZ4pcJn9Z4XnQ4GWlq-E7630Br2tYaRgzl_eznzXU7TkiEemUeHy00S_MCsuLM5fau8ZyyWamAQu4AkBN5aazZ5m90W92_S2_B5DkEY8Up2QgKELEAKdmlbvlov7q_g8t2-KTJTJ8nqrZvu3YXomEgCIEo-nGQf53an0icvx6Xhe8SHd4tn5OFBYRuceR2Xe6V4ZvaIa02MI5-qwWN5c9MsEwZpVTaFGzlUDefyXXmzFMaRYado7eHX8C4P4D8Aaxy6AQk1DCm__fRsZ_S3HrYuVwrzv5W6a7-xnUVL3j3ZK6uMHKPDdDEGAQCeoyMSWCpsw6uGdXQ4K3dDBTLxiWQKMMnv1YPEHyi0avYVpil-La90mkLbQKAhOi15lohL1ZzLNLlHqq0geRVXyJ-TpOAKMsjgCmraCcaFBqgxUUkMAP6FCXkVATTETewFi1SalNFPkfmKKrl9wdvRPeK1VZzH1Pp8bxRQEPQ6G9bgjeuJGUYAHtO6hOVd1hHHJaDxB9Xj8tW-xvxb00uRStLVCDeIH8syIiMVK5wOKsmzUAqYbTb44OgQAItYvpVrXcZkTx3JfruCkd6eg9JhndWa2FuIXBln3hq1Zd6eZZHufW-H9ulJmXIF3U4itiOH5cgarEBG3IsgiBYfFBrqtFArFlyjFbBzdv92zO9b_rkBRxpR2qbQSxU4F7ks5Tba6lz9re_2eAh4qv0SHrg5PTUP4GMcOwD8zy5lSSgoQaG6GrIf1HQVFYmik_sLZ4wfdkCCKUJwoxEuxvyHUsEn4IfYMhcbxoQqLAmmdTxtRPLbJ30ggTIxmzGptv--jnV4ZXs5tGBnXwoyJ6Z9IhparJ_isyVe-zMqhmwBcxPLzpviKjONmoI99K2RM0eh4389lnDwMxEAoh3RiuxVuWdv185h1"""

cookie_pancing = {}
for c in COOKIE_PANCING.split(';'):
    if '=' in c:
        k, v = c.strip().split('=', 1)
        cookie_pancing[k] = v

headers_netflix = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36",
    "Referer": "https://www.netflix.com/id/",
    "Accept": "*/*"
}
headers_mailtm = {"Content-Type": "application/json", "Accept": "application/json"}

def bersihkan_link(link_kotor):
    link_bersih = re.sub(r'[^\w\?\=\&\%\/\:\.\+\-]', '', link_kotor)
    link_bersih = re.sub(r'#.*$', '', link_bersih)
    return link_bersih

def kirim_pancing(email_target):
    try:
        payload = {
            "operationName": "CLCSScreenUpdate",
            "variables": {
                "format": "HTML", "imageFormat": "PNG", "locale": "id-ID",
                "serverState": "Bgjru+vcAxLTAU5En5gcaO7v7XjiK+rXFXxxInfs8S2xATg1JspUbo5FZiJWBmEvMVgdmR9SZ6ls/tnJzL2DiX1ZpEDzTPySXay5oWh+n159DQ0ZUzEH+DCPYegrj4HGBUH4jrx+k8r4V+RiwbCJri5hIJHBkm0U9DVbKQh6ngOFzJN+5ZyyV+Z0mlhhyhXawaHsrzyGLYsAO6VPXuyv9iRMihw6vAInnOOX5L/1NoByQC8aQQ7pZJ1JFMicXH3Zf1Vekx/pWvjGtP42MFXS+JARtzgeGtGdpeYCzJcYBiIOCgwDpEr8YdrJKDhAXJc=",
                "serverScreenUpdate": "Bgjru+vcAxKSAn/xAw6MYX1AnpCWZuYykLwpMOkPstB/IWV1LG0TdgJeL6p3V/Rxc0H6Y1AjdGQnoq7pXXz/pvxZNUJBtnSnlEmbjxoi1Kzmx/XG7RjpVbm+CpCfToe6w6XPO3clBmha2mTEuPCtN2XUF1awZle4yJbeK1E1fZe80Zy8AClUxyXf2aR6sxF1YyiizlGzKwz78LudjMDcJwTXchHLkvQsAXelj9/Kvx8dk8d/m8zpx1A2gLeB+laz/WXEcsMvbvrEM8JbIN4+vreqiX2YQTWdORZNOWlKU3EnbkbHpZzClCqM3ij5Yr8PiCaSuR4wM82XYaw/7R1Z3ofu1oAKXIRRHCmdvvhdiy3w8/b+zCDCYOtsL7YYBiIOCgxMBpdIbc9NcH5VZOM=",
                "inputFields": [
                    {"name": "email", "value": {"stringValue": email_target}},
                    {"name": "pipcConsent", "value": {"booleanValue": False}},
                    {"name": "emailConsent", "value": {"booleanValue": False}},
                    {"name": "recaptchaResponseTime", "value": {"intValue": 1096}},
                    {"name": "recaptchaResponseToken", "value": {"stringValue": TOKEN_CAPTCHA}}
                ]
            },
            "extensions": {"persistedQuery": {"id": "0fd81de7-07af-4c7d-802f-0f4ea4181aa3", "version": 102}}
        }
        requests.post("https://web.prod.cloud.netflix.com/graphql", headers=headers_netflix, cookies=cookie_pancing, json=payload, timeout=25)
        return True, "✅ Pancingan event 30 hari BERHASIL dikirim!"
    except Exception as e:
        return False, f"❌ Gagal: {str(e)[:50]}"

# ======================
# 🎨 HALAMAN WEB: KOLOM EMAIL BERTAMBAH SESUAI JUMLAH!
# ======================
HALAMAN_HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Netflix Event - Versi Vercel</title>
    <style>
        *{box-sizing:border-box; font-family:Arial, sans-serif; margin:0; padding:0;}
        body{background:#121212; color:#fff; padding:15px; max-width:700px; margin:0 auto;}
        h1{color:#e50914; text-align:center; margin-bottom:15px; font-size:22px;}
        .running{background:#ff9800; color:#000; padding:12px; border-radius:8px; text-align:center; font-weight:bold; font-size:18px; margin-bottom:15px; display:none;}
        .menu{background:#1e1e1e; padding:15px; border-radius:8px; margin-bottom:15px;}
        .pilihan{margin:8px 0; padding:12px; border:1px solid #444; border-radius:6px; cursor:pointer; font-size:16px;}
        .pilihan:hover{background:#333; border-color:#e50914;}
        .form{background:#1e1e1e; padding:15px; border-radius:8px; margin-bottom:15px; display:none;}
        input, button{width:100%; padding:12px; margin:6px 0; border:none; border-radius:6px; font-size:15px;}
        input{background:#333; color:#fff; border:1px solid #444;}
        button{background:#e50914; color:#fff; font-weight:bold; margin-top:10px;}
        button:hover{background:#b20710;}
        .hasil{background:#1e1e1e; padding:15px; border-radius:8px; margin-bottom:15px; white-space:pre-wrap; font-family:monospace; font-size:13px; border-left:4px solid #e50914;}
        .input-bebas{background:#1e1e1e; padding:15px; border-radius:8px;}
        textarea{width:100%; background:#333; color:#fff; padding:10px; border-radius:6px; border:none; min-height:80px; margin-top:8px;}
        .label{font-weight:bold; margin-top:10px; display:block; color:#aaa;}
    </style>
</head>
<body>
    <h1>🔥 NETFLIX EVENT 30 HARI 🔥</h1>

    <!-- ✅ TULISAN RUN DI ATAS LAYAR -->
    <div id="running" class="running">⏳ SEDANG DIJALANKAN / RUNNING... HARAP TUNGGU!</div>

    <div class="menu">
        <h3>📋 PILIHAN:</h3>
        <div class="pilihan" onclick="tampilForm(1)">
            <b>1. OTOMATIS BUAT</b> - Masukkan jumlah akun
        </div>
        <div class="pilihan" onclick="tampilForm(2)">
            <b>2. MANUAL KIRIM</b> - Masukkan jumlah email
        </div>
    </div>

    <!-- FORM 1: OTOMATIS -->
    <div id="form1" class="form">
        <h3>⚙️ OTOMATIS BUAT AKUN</h3>
        <form method="POST" onsubmit="tampilRun()">
            <input type="hidden" name="tipe" value="1">
            <input type="number" name="jumlah" placeholder="MASUKKAN JUMLAH AKUN" min="1" max="15" required>
            <input type="text" name="sandi" placeholder="MASUKKAN SANDI UNTUK SEMUA AKUN" required>
            <button type="submit">🚀 MULAI PROSES</button>
        </form>
    </div>

    <!-- FORM 2: MANUAL (KOLOM EMAIL BERTAMBAH) -->
    <div id="form2" class="form">
        <h3>⚙️ MANUAL KIRIM PANCINGAN</h3>
        <form method="POST" onsubmit="tampilRun()">
            <input type="hidden" name="tipe" value="2">
            <input type="number" name="jumlah" id="jml_email" placeholder="MASUKKAN JUMLAH EMAIL" min="1" max="15" required oninput="buatKolomEmail(this.value)">
            <div id="daftar_email"></div>
            <button type="submit">📤 KIRIM SEMUA</button>
        </form>
    </div>

    {% if hasil %}
    <div class="hasil">
        <h3>📝 HASIL PROSES:</h3>
        {{ hasil }}
    </div>
    {% endif %}

    <div class="input-bebas">
        <h3>✏️ KOLOM INPUT BEBAS:</h3>
        <textarea placeholder="Tulis catatan, simpan link, atau ketik apapun disini..."></textarea>
    </div>

    <script>
        function tampilForm(no){
            document.getElementById("form1").style.display = "none";
            document.getElementById("form2").style.display = "none";
            document.getElementById("form"+no).style.display = "block";
        }
        // ✅ Buat kolom email sebanyak jumlah yang diminta
        function buatKolomEmail(jumlah){
            const wadah = document.getElementById("daftar_email");
            wadah.innerHTML = "";
            if(jumlah >=1 && jumlah <=15){
                for(let i=1; i<=jumlah; i++){
                    const kolom = document.createElement("input");
                    kolom.type = "email";
                    kolom.name = "email_"+i;
                    kolom.placeholder = "MASUKKAN EMAIL KE-"+i;
                    kolom.required = true;
                    wadah.appendChild(kolom);
                }
            }
        }
        // ✅ Tampilkan tulisan RUN saat proses mulai
        function tampilRun(){
            document.getElementById("running").style.display = "block";
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def utama():
    hasil_teks = ""
    if request.method == 'POST':
        tipe = request.form.get('tipe')

        # ======================
        # PILIHAN 1: OTOMATIS BUAT
        # ======================
        if tipe == '1':
            jumlah = int(request.form.get('jumlah', 1))
            sandi = request.form.get('sandi', 'Akun77@@')
            hasil_teks += f"✅ === PROSES OTOMATIS BUAT {jumlah} AKUN ===\n"
            hasil_teks += f"🔑 Sandi: {sandi}\n\n"

            for no in range(1, jumlah+1):
                hasil_teks += f"--- AKUN KE-{no}} ---\n"
                try:
                    res_domain = requests.get(f"{BASE_MAILTM}/domains?page=1", timeout=15)
                    domain = res_domain.json()["hydra:member"][0]["domain"]
                    nama = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
                    email_baru = f"{nama}@{domain}"

                    res_buat = requests.post(f"{BASE_MAILTM}/accounts", headers=headers_mailtm, json={"address": email_baru, "password": sandi}, timeout=20)
                    if res_buat.status_code not in [200,201]:
                        hasil_teks += f"❌ Gagal buat email: {email_baru}\n\n"
                        continue
                    hasil_teks += f"✅ Berhasil buat: {email_baru}\n"

                    ok, pesan = kirim_pancing(email_baru)
                    hasil_teks += f"📤 Kirim event: {pesan}\n"
                    time.sleep(JEDA_SEMUA)

                    # Ambil link
                    login_res = requests.post(f"{BASE_MAILTM}/token", headers=headers_mailtm, json={"address": email_baru, "password": sandi}, timeout=20)
                    token = login_res.json()["token"]
                    auth_header = {**headers_mailtm, "Authorization": f"Bearer {token}"}
                    pesan_netflix = None
                    for _ in range(6):
                        pesan_res = requests.get(f"{BASE_MAILTM}/messages?page=1", headers=auth_header, timeout=20)
                        data = pesan_res.json()
                        daftar = data if isinstance(data, list) else data.get("hydra:member", [])
                        pesan_netflix = next((p for p in daftar if "netflix.com" in str(p.get("from", ""))), None)
                        if pesan_netflix: break
                        time.sleep(JEDA_SEMUA)

                    if pesan_netflix:
                        isi = requests.get(f"{BASE_MAILTM}/messages/{pesan_netflix['id']}", headers=auth_header, timeout=15).json()
                        teks = isi.get("text", "") or isi.get("html", "")
                        link_kotor = re.search(r"https?://[^\s\)\<\>\"']+netflix\.com/epr\?code=[^\s\)\<\>\"']+", teks).group(0)
                        link_bersih = bersihkan_link(link_kotor)
                        hasil_teks += f"🔗 Link verifikasi: {link_bersih}\n⚠️ Link TIDAK dibuka otomatis!\n"
                    else:
                        hasil_teks += "❌ Pesan verifikasi belum masuk\n"
                    hasil_teks += "\n"

                except Exception as e:
                    hasil_teks += f"❌ Error: {str(e)[:60]}\n\n"

        # ======================
        # PILIHAN 2: MANUAL KIRIM (KOLOM TERPISAH)
        # ======================
        if tipe == '2':
            jumlah = int(request.form.get('jumlah', 1))
            hasil_teks += f"✅ === PROSES MANUAL KIRIM {jumlah} EMAIL ===\n"
            hasil_teks += "⚠️ TIDAK PERLU SANDI! Cukup email saja\n\n"

            for no in range(1, jumlah+1):
                email = request.form.get(f'email_{no}', '').strip()
                if not email:
                    hasil_teks += f"--- EMAIL KE-{no}: KOSONG, DILEWATI ---\n\n"
                    continue
                hasil_teks += f"--- EMAIL KE-{no}: {email} ---\n"
                ok, pesan = kirim_pancing(email)
                hasil_teks += f"📤 Hasil: {pesan}\n\n"
                time.sleep(JEDA_SEMUA)

    return render_template_string(HALAMAN_HTML, hasil=hasil_teks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
