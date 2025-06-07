import streamlit as st
import requests
import base64

# Ganti ini dengan URL webhook n8n kamu
WEBHOOK_URL = "https://nominally-picked-grubworm.ngrok-free.app/webhook/stockanalysis"

# Judul aplikasi
st.set_page_config(page_title="Analisis Saham Otomatis", page_icon="📈")
# Fungsi untuk encode file gambar ke base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Fungsi untuk set background dari image
def set_background(jpg_file):
    bin_str = get_base64_of_bin_file(jpg_file)
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Set background
set_background("./background_image.jpg")
st.title("📈 Analisis Saham Otomatis")
# Form input
with st.form("stock_form"):
    user_message = st.text_input("🔍 Masukkan kode saham (contoh: BBCA, AAPL, MSFT, TSLA):", "")
    submitted = st.form_submit_button("📤 Kirim dan Analisis")

if submitted:
    if user_message.strip() == "":
        st.warning("⚠️ Pesan tidak boleh kosong!")
    else:
        with st.spinner("⏳ Mengirim data dan menunggu analisis..."):
            try:
                # Kirim request ke webhook n8n
                response = requests.post(WEBHOOK_URL, json={"ticker": user_message})

                if response.status_code == 200:
                    data = response.json()

                    # Tampilkan hasil gambar dan analisis
                    # col1, col2 = st.columns([1, 2])

                    # with col1:
                    st.subheader("🖼️ Grafik Saham")
                    for b64_image in data.get("base64StringImage", []):
                        try:
                            image_bytes = base64.b64decode(b64_image)
                            st.image(image_bytes, caption="📉 Chart Analysis", use_column_width=True)
                        except Exception as e:
                            st.error(f"❌ Gagal decode gambar: {e}")

                    # with col2:
                    st.subheader("📊 Hasil Analisis Teknis")
                    for item in data.get("content", []):
                        st.markdown(f"<div style='font-size: 16px; line-height: 1.6;'>{item}</div>", unsafe_allow_html=True)

                    st.success("✅ Analisis selesai!")
                else:
                    st.error(f"❌ Gagal mengirim pesan. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"🚨 Terjadi error saat request: {e}")
