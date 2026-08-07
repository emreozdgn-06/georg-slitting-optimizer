import streamlit as st
import pandas as pd
import re
from itertools import combinations_with_replacement
from collections import defaultdict
st.set_page_config(
    page_title="GEORG Slitting Optimizer",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ GEORG Dilme Optimizasyon Sistemi")

# -----------------------------
# SOL MENÜ
# -----------------------------
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

st.divider()

# -----------------------------
# DOSYA YÜKLEME
# -----------------------------
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

        st.write("### Sipariş Bilgileri")
        st.write(f"Toplam Satır : {len(df)}")
        st.write("Kolonlar")
        st.write(list(df.columns))

        siparisler = defaultdict(float)

        for _, satir in df.iterrows():

            stok = str(satir["Stok Adı"])
            kg = float(satir["Gereken Miktar"])

            sonuc = re.search(r"x(\d+)\s*mm", stok)

            if sonuc:

                genislik = int(sonuc.group(1))
                siparisler[genislik] += kg

        st.write("### Toplanmış Siparişler")

        for genislik in sorted(siparisler):

            st.write(f"{genislik} mm → {siparisler[genislik]:.2f} kg")
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

st.divider()

# -----------------------------
# MAKİNE AYARLARI
# -----------------------------
st.header("⚙️ Makine Ayarları")

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
    "Maksimum Bıçak Sayısı",
    value=10
)

# -----------------------------
# OPTİMİZASYON
# -----------------------------
if st.button("🚀 Optimizasyonu Başlat"):

    kullanilabilir_genislik = coil_width - left_trim - right_trim

    st.success("Optimizasyon Başladı")

    st.write("## Makine Bilgileri")

    st.write(f"Mother Coil : {coil_width} mm")
    st.write(f"Sol Fire : {left_trim} mm")
    st.write(f"Sağ Fire : {right_trim} mm")
    st.write(f"Kullanılabilir Genişlik : {kullanilabilir_genislik} mm")
    if siparis_dosyasi is not None:

        st.write("## En Uygun Kombinasyon")

        enler = list(siparisler.keys())

        hedef = kullanilabilir_genislik

        en_iyi = None
        en_fire = 99999

        for adet in range(1, max_knife + 1):

            for komb in combinations_with_replacement(enler, adet):

                toplam = sum(komb)

                if toplam <= hedef:

                    fire = hedef - toplam

                    if fire < en_fire:

                        en_fire = fire
                        en_iyi = komb

        if en_iyi:

            st.success("En uygun kombinasyon bulundu")

            st.write(f"Kombinasyon : {list(en_iyi)}")

            st.write(f"Toplam Genişlik : {sum(en_iyi)} mm")
st.write("### Dilme Planı")

plan = []

for genislik in sorted(set(en_iyi)):

    adet = en_iyi.count(genislik)

    plan.append(
        {
            "En (mm)": genislik,
            "Adet": adet,
            "Toplam (mm)": genislik * adet
        }
    )

plan_df = pd.DataFrame(plan)

st.dataframe(plan_df, use_container_width=True)
            st.write(f"Fire : {en_fire} mm")
