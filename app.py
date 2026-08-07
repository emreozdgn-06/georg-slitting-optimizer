import streamlit as st
import pandas as pd
import re
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

        siparis_df = pd.DataFrame(
            {
                "En (mm)": list(siparisler.keys()),
                "Kg": list(siparisler.values())
            }
        )

        siparis_df = siparis_df.sort_values("En (mm)")

        st.dataframe(
            siparis_df,
            use_container_width=True
        )
          
        
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
        
        ilk_coil = df_coil.iloc[0]

        st.write("### Seçilen İlk Mother Coil")

        st.write(ilk_coil)

        st.write("### Mother Coil Bilgileri")

        st.write(f"Toplam Coil : {len(df_coil)}")

        st.write("Kolonlar")

        st.write(list(df_coil.columns))

        st.write("### Mother Coil Listesi")

        st.dataframe(
            df_coil,
            use_container_width=True
        )

st.divider()

# -----------------------------
# MAKİNE AYARLARI
# -----------------------------
st.header("⚙️ Makine Ayarları")

coil_width = st.number_input(
    "Mother Coil Genişliği (mm)",
    value=1100
)
coil_kg = st.number_input(
    "Mother Coil Kilogramı (kg)",
    value=4000
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
    st.write(f"Mother Coil Kg : {coil_kg} kg")
    st.write(f"Sol Fire : {left_trim} mm")
    st.write(f"Sağ Fire : {right_trim} mm")
    st.write(f"Kullanılabilir Genişlik : {kullanilabilir_genislik} mm")

    if siparis_dosyasi is not None:

        st.write("## En Uygun Kombinasyon")

        enler = list(siparisler.keys())

        hedef = kullanilabilir_genislik

        en_iyi = []

        kalan = hedef

        sirali_enler = sorted(
            enler,
            key=lambda x: siparisler[x],
            reverse=True
        )

        while len(en_iyi) < max_knife:

            uygun_enler = [
                en for en in sirali_enler
                if en <= kalan
            ]

            if not uygun_enler:
                break

            secilen_en = max(uygun_enler)

            en_iyi.append(secilen_en)

            kalan -= secilen_en

        en_fire = kalan

        if en_iyi:

            st.success("En uygun kombinasyon bulundu")

            st.write(f"Kombinasyon : {en_iyi}")
            st.write(f"Toplam Genişlik : {sum(en_iyi)} mm")
            st.write(f"Fire : {en_fire} mm")

            st.write("### Dilme Planı")

            bicak_sayisi = len(en_iyi)

            st.write(f"Bıçak Sayısı : {bicak_sayisi}")

            plan = []

            for sira, genislik in enumerate(en_iyi, start=1):

                plan.append(
                    {
                        "Bıçak No": sira,
                        "En (mm)": genislik,
                        "Sipariş Kg": round(siparisler[genislik], 2)
                    }
                )

            plan_df = pd.DataFrame(plan)

            st.dataframe(
                plan_df,
                use_container_width=True
            )

            st.write("### Bıçak Dizilimi")

            dizilim = [f"Sol Fire {left_trim} mm"]

            for genislik in en_iyi:
                dizilim.append(f"{genislik} mm")

            dizilim.append(f"Sağ Fire {right_trim} mm")

            st.write(" | ".join(dizilim))

            toplam_kontrol = (
                left_trim
                + sum(en_iyi)
                + right_trim
            )

            st.write(
                f"Toplam Kontrol : {toplam_kontrol} mm / Mother Coil : {coil_width} mm"
            )

            st.write("### Üretilecek Kilogramlar")

            uretim_plan = []

            for genislik in sorted(set(en_iyi)):

                adet = en_iyi.count(genislik)

                tek_bant_kg = (
                    coil_kg
                    * genislik
                    / coil_width
                )

                toplam_uretim_kg = tek_bant_kg * adet

                uretim_plan.append(
                    {
                        "En (mm)": genislik,
                        "Adet": adet,
                        "Tek Bant Kg": round(tek_bant_kg, 2),
                        "Toplam Üretim Kg": round(toplam_uretim_kg, 2)
                    }
                )

            uretim_df = pd.DataFrame(uretim_plan)

            st.dataframe(
                uretim_df,
                use_container_width=True
            )
        kalan_siparisler = siparisler.copy()

        for satir in uretim_plan:

            genislik = satir["En (mm)"]
            uretilen_kg = satir["Toplam Üretim Kg"]

            kalan_siparisler[genislik] = (
                kalan_siparisler[genislik]
                - uretilen_kg
            )

            if kalan_siparisler[genislik] < 0:
                kalan_siparisler[genislik] = 0

        st.write("### Kalan Siparişler")

        kalan_plan = []

        for genislik in sorted(kalan_siparisler):

            kalan_plan.append(
                {
                    "En (mm)": genislik,
                    "İlk Sipariş Kg": round(siparisler[genislik], 2),
                    "Kalan Kg": round(kalan_siparisler[genislik], 2)
                }
            )

        kalan_df = pd.DataFrame(kalan_plan)

        st.dataframe(
            kalan_df,
            use_container_width=True
        )
