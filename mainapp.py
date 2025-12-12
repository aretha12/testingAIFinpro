import streamlit as st
import joblib
import numpy as np

model = joblib.load("cobaBayi_random_forest.pkl")
scaler = joblib.load("cobaBayi_scaler.pkl")

AKURASI_MODEL = 0.8712

st.set_page_config(page_title="Prediksi Stunting Balita 🤱🏻", layout="centered")
st.title("🧒 Prediksi Stunting Balita")

st.markdown(
    """
Aplikasi ini memprediksi apakah balita terindikasi **stunting atau tidak**  
berdasarkan beberapa faktor seperti **jenis kelamin, usia, berat lahir, panjang lahir, berat badan, tinggi badan, dan ASI**.  
"""
)

gender_map = {"Laki-laki": 0, "Perempuan": 1}
gender = st.selectbox("Jenis Kelamin", list(gender_map.keys()))

age = st.number_input("Usia Anak (bulan)", 0, 60, 12)
birth_weight = st.number_input("Berat Lahir (kg)", 0.5, 5.0, 3.0)
birth_length = st.number_input("Panjang Lahir (cm)", 30, 60, 49)
body_weight = st.number_input("Berat Badan Saat Ini (kg)", 1.0, 25.0, 10.0)
body_length = st.number_input("Tinggi Badan Saat Ini (cm)", 40, 120, 70)

breastfeeding = st.selectbox("ASI Eksklusif?", ["Ya", "Tidak"])
bf = 1 if breastfeeding == "Ya" else 0

g = gender_map[gender]

data = np.array([[g, age, birth_weight, birth_length, body_weight, body_length, bf]])
data_scaled = scaler.transform(data)

if st.button("Prediksi Stunting"):
    pred = model.predict(data_scaled)[0]
    st.metric("Akurasi Model (Validasi)", f"{AKURASI_MODEL*100:.2f}%")
    if pred == 1:
        st.error("⚠️ Balita **terindikasi stunting**.")
    else:
        st.success("✅ Balita **tidak stunting**.")

    st.subheader("🩺 Rekomendasi Kesehatan")
    if pred == 1:
        st.markdown(
            f"""
            **Analisis:**  
            Balita usia **{age} bulan** dengan tinggi **{body_length} cm** berisiko *stunting*.

            **Kemungkinan penyebab:**
            - Asupan gizi kurang  
            - Berat lahir rendah  
            - Tidak mendapat ASI eksklusif  
            - Sanitasi kurang baik  

            **Rekomendasi:**
            1. Tingkatkan makanan tinggi protein (telur, ikan, ayam, tempe)  
            2. Perbanyak buah & sayuran  
            3. Cek rutin di posyandu  
            4. Perbaiki sanitasi rumah  
            5. Konsultasi dengan dokter anak  
            """
        )
    else:
        st.markdown(
            f"""
            **Analisis:**  
            Pertumbuhan balita **normal** untuk usia **{age} bulan**.

            **Saran menjaga pertumbuhan optimal:**
            - Konsumsi makanan seimbang  
            - Batasi makanan manis & instan  
            - Stimulasi perkembangan (bermain, membaca)  
            - Tidur cukup 10–12 jam  
            - Periksa rutin di posyandu  
            """
        )
    st.subheader("📊 Detail Input")
    col1, col2, col3 = st.columns(3)
    col1.metric("Usia", f"{age} bulan")
    col2.metric("Berat Badan", f"{body_weight} kg")
    col3.metric("Tinggi Badan", f"{body_length} cm")

st.markdown("---")
st.caption("Aplikasi ini hanya alat bantu. Konsultasikan hasil dengan tenaga medis.")
