import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from joblib import load

# Veriyi yükle
data = pd.read_excel("islenmisarabailanlar_data.xlsx")

# Seri için eşleme
seri_mapping = {0: "1 Serisi", 1: "2 Serisi", 2: "3 Serisi", 3: "4 Serisi", 4: "5 Serisi", 5: "6 Serisi", 6: "7 Serisi", 7: "8 Serisi",
                8: "İ Serisi", 9: "M Serisi", 10: "Z Serisi"}

def map_seri(seri):
    return seri_mapping.get(seri, seri)

# Eğitilmiş modeli yükle
rf = load("ridge_model.joblib")

# Fiyat tahminini gerçekleştiren fonksiyon
def predict_price(input_features):
    predicted_price = rf.predict(input_features)
    return predicted_price

# Yakıt tipi seçenekleri
fuel_type_options = {0: "Benzin", 1: "Dizel", 2: "Elektrik", 3: "Hibrit", 4: "Lpg % Benzin"}

# Kasa tipi seçenekleri
body_type_options = {0: "Bilinmiyor", 1: "Cabrio", 2: "Coupe", 3: "Hatchback/3", 4: "Hatchback/5", 5: "Mpv", 6: "Roadaster", 7: "Sedan",
                     8: "Station wagon"}

# Renk seçenekleri
color_options = {0: "Bej", 1: "Beyaz", 2: "Bordo", 3: "Diğer", 4: "Füme", 5: "Gri", 6: "Gümüş", 7: "Gri(Metalik)", 8: "Gri (Titanyum)",
                9: "Kahverengi", 10: "Kırmızı", 11: "Lacivert", 12: "Mavi", 13: "Mavi(Metalik)", 14: "Mor", 15: "Sarı", 16: "Siyah", 17: "Turkuaz", 19: "Yeşil",
                20: "Yeşil (Metalik)", 21: "Şampanya"}

# Vites tipi seçenekleri
transmission_type_options = {
    "Otomatik": 1,
    "Düz": 0,
}

# Uygulama başlığı
st.title("Bmw Fiyat Tahmini Uygulaması")

# Seri seçim kutusu
seri_names = list(seri_mapping.values())
seri = st.selectbox("Seri", seri_names)
seri_number = next(key for key, value in seri_mapping.items() if value == seri)

# Yıl girişi
year = st.number_input("Yıl", min_value=1950, max_value=2023, step=1, value=2020)

# Kilometre girişi
mileage = st.number_input("Kilometre", min_value=0, max_value=500000, step=1000, value=50000)

# Vites tipi seçim kutusu
transmission_type = st.selectbox("Vites Tipi", list(transmission_type_options.keys()))

# Yakıt tipi seçim kutusu
fuel_type = st.selectbox("Yakıt Tipi", list(fuel_type_options.values()))
fuel_type_value = next(key for key, value in fuel_type_options.items() if value == fuel_type)

# Kasa tipi seçim kutusu
body_type = st.selectbox("Kasa Tipi", list(body_type_options.values()))
body_type_value = next(key for key, value in body_type_options.items() if value == body_type)

# Renk seçim kutusu
color = st.selectbox("Renk", list(color_options.values()))
color_value = next(key for key, value in color_options.items() if value == color)

# Motor gücü girişi
engine_power = st.number_input("Motor Gücü", min_value=50, max_value=1000, step=1, value=150)

# Tahmin butonu
if st.button("Fiyatı Tahmin Et"):

    input_features = [[seri_number, year, mileage, transmission_type_options[transmission_type], fuel_type_value, body_type_value, color_value, engine_power]]
    prediction = predict_price(input_features)

    # Tahmini fiyatı göster
    st.success(f"Tahmini Fiyat: {prediction[0]:,.2f} TL")
