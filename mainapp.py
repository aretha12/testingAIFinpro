import streamlit as st
import joblib
import numpy as np

model = joblib.load("stunting_model.pkl")
scaler = joblib.load("scaler.pkl")

st.set_page_config(page_title="Prediksi Stunting Balita", layout="centered")
st.title("🌾 Prediksi Stunting Balita (Offline Version)")

st.markdown("""
Aplikasi ini memprediksi apakah balita terindikasi **stunting atau tidak**  
berdasarkan **umur**, **tinggi badan**, dan **jenis kelamin**.  
Dilengkapi juga dengan rekomendasi kesehatan dasar untuk orang tua 👨‍👩‍👧‍👦
""")

umur = st.number_input("Umur (bulan)", min_value=0, max_value=120, step=1)
tinggi = st.number_input("Tinggi Badan (cm)", min_value=30.0, max_value=150.0, step=0.1)
jenis_kelamin = st.selectbox("Jenis Kelamin", ["laki-laki", "perempuan"])

jk = 0 if jenis_kelamin == "laki-laki" else 1
data = np.array([[umur, jk, tinggi]])
data_scaled = scaler.transform(data)

if tinggi < 40 or tinggi > 130:
    st.warning("⚠️ Nilai tinggi tidak realistis. Mohon masukkan data yang wajar (40–130 cm).")
elif umur == 0:
    st.warning("⚠️ Umur 0 bulan tidak bisa diprediksi.")
else:
    pred = model.predict(data_scaled)[0]

    if pred == 1:
        st.error("⚠️ Bayi terindikasi *stunting*.")
    else:
        st.success("✅ Bayi tidak stunting.")

    st.subheader("🩺 Rekomendasi Kesehatan")
    
    if pred == 1:
        st.markdown(f"""
        **Analisis:**  
        Balita berumur **{umur} bulan** dengan tinggi **{tinggi} cm** terindikasi mengalami *stunting*.

        **Kemungkinan penyebab:**
        - Asupan gizi kurang atau tidak seimbang.
        - Riwayat infeksi yang berulang.
        - Lingkungan rumah tidak bersih atau sanitasi buruk.
        - Kurangnya stimulasi perkembangan anak.

        **Intervensi yang disarankan:**
        1. Pastikan balita mendapatkan makanan padat gizi tinggi protein (telur, ikan, tempe, tahu, daging ayam).
        2. Tambahkan sayur dan buah setiap hari.
        3. Pastikan pemberian ASI eksklusif (jika < 6 bulan).
        4. Konsultasi rutin ke posyandu atau dokter anak.
        5. Perbaiki sanitasi (air bersih, cuci tangan).

        💡 *Pantau berat badan dan tinggi anak minimal sekali setiap bulan.*
        """)
    else:
        st.markdown(f"""
        **Analisis:**  
        Balita berumur **{umur} bulan** dengan tinggi **{tinggi} cm** memiliki pertumbuhan **normal**.

        **Saran untuk mempertahankan pertumbuhan optimal:**
        1. Jaga pola makan seimbang dengan sumber karbohidrat, protein, dan sayur.
        2. Batasi konsumsi gula dan makanan olahan.
        3. Pastikan tidur cukup (10–12 jam per hari).
        4. Berikan stimulasi (bermain, berbicara, membaca).
        5. Lakukan pemeriksaan rutin di posyandu setiap bulan.

        💡 *Pertumbuhan optimal didukung oleh kasih sayang, stimulasi, dan gizi seimbang.*
        """)

    st.subheader("📊 Detail Input")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Umur", f"{umur} bulan")
    with col2:
        st.metric("Tinggi Badan", f"{tinggi} cm")
    with col3:
        st.metric("Jenis Kelamin", "Laki-laki" if jk == 0 else "Perempuan")

st.markdown("---")
st.caption("Aplikasi ini tidak menggantikan diagnosis dokter. Gunakan hasil sebagai alat bantu awal untuk skrining stunting.")
