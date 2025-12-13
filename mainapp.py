import streamlit as st
import joblib
import numpy as np

model = joblib.load("cobaBayi_random_forest.pkl")
scaler = joblib.load("cobaBayi_scaler.pkl")

AKURASI_MODEL = 0.8712 
st.set_page_config(
    page_title="Prediksi Stunting Balita 🤱🏻",
    layout="centered"
)

st.title("🧒 Prediksi Stunting Balita")

st.markdown("""
Aplikasi ini memprediksi apakah balita terindikasi **stunting atau tidak**  
berdasarkan beberapa faktor seperti **jenis kelamin, usia, berat lahir, panjang lahir, berat badan, tinggi badan, dan ASI**.
""")
gender_map = {"Laki-laki": 0, "Perempuan": 1}
gender = st.selectbox("Jenis Kelamin", list(gender_map.keys()))

age = st.number_input("Usia Anak (bulan)", min_value=0, max_value=60, value=12)
birth_weight = st.number_input("Berat Lahir (kg)", min_value=0.5, max_value=5.0, value=3.0)
birth_length = st.number_input("Panjang Lahir (cm)", min_value=30, max_value=60, value=49)
body_weight = st.number_input("Berat Badan Saat Ini (kg)", min_value=1.0, max_value=25.0, value=10.0)
body_length = st.number_input("Tinggi Badan Saat Ini (cm)", min_value=40, max_value=120, value=70)

breastfeeding = st.selectbox("ASI Eksklusif?", ["Ya", "Tidak"])
g = gender_map[gender]
bf = 1 if breastfeeding == "Ya" else 0

data = np.array([[g, age, birth_weight, birth_length, body_weight, body_length, bf]])
data_scaled = scaler.transform(data)
if st.button("Prediksi Stunting"):
    pred_model = model.predict(data_scaled)[0]
    is_override_normal = (
        age >= 12 and
        body_length >= 75 and
        body_weight >= 9
    )

    if is_override_normal:
        final_pred = 0
        decision_source = "Rule-based override (pertumbuhan sesuai usia)"
    else:
        final_pred = pred_model
        decision_source = "Prediksi model machine learning"
    st.metric("Akurasi Model (Validasi)", f"{AKURASI_MODEL*100:.2f}%")
    if final_pred == 1:
        st.error("⚠️ Balita **terindikasi stunting**.")
    else:
        st.success("✅ Balita **tidak stunting**.")

    st.caption(f"Sumber keputusan: {decision_source}")
    st.subheader("🩺 Rekomendasi Kesehatan")

    if final_pred == 1:
        st.markdown(f"""
        **Analisis:**  
        Balita usia **{age} bulan** dengan tinggi **{body_length} cm** berisiko mengalami *stunting*.

        **Kemungkinan penyebab:**
        - Asupan gizi kurang atau tidak seimbang  
        - Berat lahir rendah  
        - Tidak mendapat ASI eksklusif  
        - Sanitasi lingkungan kurang baik  

        **Rekomendasi:**
        1. Tingkatkan asupan protein (telur, ikan, ayam, tempe, tahu)  
        2. Perbanyak buah dan sayur  
        3. Pantau pertumbuhan rutin di posyandu  
        4. Jaga kebersihan dan sanitasi rumah  
        5. Konsultasi dengan tenaga medis  

        💡 *Pemantauan rutin sangat penting pada 1000 HPK.*
        """)
    else:
        st.markdown(f"""
        **Analisis:**  
        Pertumbuhan balita **normal** untuk usia **{age} bulan**.

        **Saran menjaga pertumbuhan optimal:**
        - Konsumsi makanan bergizi seimbang  
        - Batasi makanan manis dan instan  
        - Stimulasi perkembangan (bermain, membaca, berbicara)  
        - Tidur cukup (10–12 jam per hari)  
        - Pemeriksaan rutin di posyandu  

        💡 *Pertumbuhan optimal dipengaruhi gizi, stimulasi, dan pola asuh.*
        """)
    st.subheader("📊 Detail Input")
    col1, col2, col3 = st.columns(3)

    col1.metric("Usia", f"{age} bulan")
    col2.metric("Berat Badan", f"{body_weight} kg")
    col3.metric("Tinggi Badan", f"{body_length} cm")
st.markdown("---")
st.caption(
    "⚠️ Aplikasi ini hanya alat bantu skrining awal dan **tidak menggantikan diagnosis dokter**."
)
