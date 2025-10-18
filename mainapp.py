import streamlit as st
import joblib
import numpy as np

model = joblib.load("stunting_model.pkl")

st.title("🌾 Prediksi Stunting Balita")

umur = st.number_input("Umur (bulan)", min_value=0)
tinggi = st.number_input("Tinggi Badan (cm)", min_value=0.0)
jenis_kelamin = st.selectbox("Jenis Kelamin", ["laki-laki", "perempuan"])

jk = 0 if jenis_kelamin == "laki-laki" else 1
data = np.array([[umur, jk, tinggi]])

pred = model.predict(data)[0]

if pred == 1:
    st.error("⚠️ Bayi terindikasi stunting.")
else:
    st.success("✅ Bayi tidak stunting.")
