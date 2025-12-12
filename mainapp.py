import streamlit as st
import joblib
import numpy as np

model = joblib.load("testingBayi_random_forest.pkl")
scaler = joblib.load("testingBayi.pkl")

st.set_page_config(page_title="Prediksi Stunting Balita 🤱🏻", layout="centered")
st.title("🧒 Prediksi Stunting Balita")

st.markdown(
    """
Aplikasi ini memprediksi apakah balita terindikasi **stunting atau tidak**  
berdasarkan **umur**, **tinggi badan**, dan **jenis kelamin**.  

Dilengkapi rekomendasi kesehatan untuk orang tua 👨‍👩‍👧‍👦
"""
)

umur = st.number_input("Umur (bulan)", min_value=0, max_value=120, step=1)
tinggi = st.number_input("Tinggi Badan (cm)", min_value=30.0, max_value=150.0, step=0.1)
jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])

jk = 0 if jenis_kelamin == "Laki-laki" else 1

data = np.array([[umur, jk, tinggi]])
data_scaled = scaler.transform(data)
if st.button("Prediksi Stunting"):
    if tinggi < 40 or tinggi > 130:
        st.warning("⚠️ Nilai tinggi tidak realistis. Masukkan data antara **40–130 cm**.")
    elif umur == 0:
        st.warning("⚠️ Umur 0 bulan tidak dapat dilakukan prediksi.")
    else:
        pred = model.predict(data_scaled)[0]
        if pred == 1:
            st.error("⚠️ Balita **terindikasi stunting**.")
        else:
            st.success("✅ Balita **tidak stunting**.")

        st.subheader("🩺 Rekomendasi Kesehatan")

        if pred == 1:
            st.markdown(
                f"""
                **Analisis:**  
                Balita berumur **{umur} bulan** dengan tinggi **{tinggi} cm** terindikasi mengalami *stunting*.

                **Kemungkinan penyebab:**
                - Asupan gizi kurang atau tidak seimbang  
                - Riwayat infeksi berulang  
                - Sanitasi lingkungan buruk  
                - Kurangnya stimulasi perkembangan  

                **Intervensi yang disarankan:**
                1. Tingkatkan konsumsi makanan tinggi protein (telur, ikan, ayam, tahu, tempe)  
                2. Berikan buah dan sayuran setiap hari  
                3. Cek pertumbuhan rutin di posyandu  
                4. Perbaiki sanitasi rumah (air bersih, cuci tangan)  
                5. Konsultasi dokter bila pertumbuhan tidak sesuai  

                💡 *Pantau tinggi & berat badan setiap bulan.*
                """
            )
            
        else:
            st.markdown(
                f"""
                **Analisis:**  
                Balita berumur **{umur} bulan** dengan tinggi **{tinggi} cm** memiliki pertumbuhan **normal**.

                **Saran untuk menjaga pertumbuhan optimal:**
                1. Berikan makanan seimbang dengan protein dan sayur  
                2. Batasi makanan manis dan olahan instan  
                3. Pastikan tidur cukup (10–12 jam per hari)  
                4. Berikan stimulasi perkembangan (bermain, berbicara, membaca)  
                5. Periksa rutin ke posyandu setiap bulan  

                💡 *Pertumbuhan anak dipengaruhi gizi, stimulasi, dan pola asuh.*
                """
            )

        st.subheader("📊 Detail Input")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Umur", f"{umur} bulan")
        with col2:
            st.metric("Tinggi Badan", f"{tinggi} cm")
        with col3:
            st.metric("Jenis Kelamin", jenis_kelamin)

st.markdown("---")
st.caption("Aplikasi prediksi ini hanya alat bantu. Konsultasikan hasil dengan tenaga medis.")
