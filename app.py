import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="GEORG Slitting Optimizer",
    page_icon="⚙️",
    layout="wide"
)

st.sidebar.title("⚙️ Menü")

sayfa = st.sidebar.selectbox(
    "Sayfa Seç",
    [
        "Ana Sayfa",
        "Siparişler",
        "Mother Coil",
        "Optimizasyon",
        "Sonuçlar"
    ]
)
col1, col2 = st.columns(2)

with col1:

    st.header("📄 Sipariş Dosyası")

    siparis_dosyasi = st.file_uploader(
        "Sipariş Excel Dosyası",
        type=["xlsx"]
    )

    if siparis_dosyasi is not None:

        df = pd.read_excel(siparis_dosyasi)

        st.dataframe(df, use_container_width=True)

with col2:

    st.header("📦 Mother Coil Dosyası")

    coil_dosyasi = st.file_uploader(
        "Mother Coil Excel Dosyası",
        type=["xlsx"],
        key="coil"
    )

    if coil_dosyasi is not None:

        df_coil = pd.read_excel(coil_dosyasi)

        st.dataframe(df_coil, use_container_width=True)
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
