import streamlit as st
import pandas as pd
st.sidebar.title("⚙️ Menü")

menu = st.sidebar.radio(
    "Sayfa Seç",
    [
        "Ana Sayfa",
        "Siparişler",
        "Mother Coil",
        "Optimizasyon",
        "Sonuçlar"
    ]
)

st.set_page_config(
    page_title="GEORG Slitting Optimizer",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ GEORG Slitting Optimizer")

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.header("Makine Ayarları")

    coil_width = st.number_input(
        "Mother Coil Genişliği (mm)",
        value=1100
    )

    left_trim = st.number_input(
        "Sol Fire (mm)",
        value=5
    )

    right_trim = st.number_input(
        "Sağ Fire (mm)",
        value=5
    )

    max_knife = st.number_input(
        "Maksimum Bıçak",
        value=10
    )

with col2:

    st.header("Dosyalar")

    order_file = st.file_uploader(
        "Sipariş Exceli",
        type=["xlsx"]
    )

    coil_file = st.file_uploader(
        "Mother Coil Exceli",
        type=["xlsx"]
    )

st.divider()

if st.button("🚀 OPTİMİZASYONU BAŞLAT", use_container_width=True):
    st.success("Program çalışmaya hazır.")
