import streamlit as st
import pandas as pd
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
# BAŞLANGIÇ DEĞERLERİ
# -----------------------------

siparisler = defaultdict(float)

df_coil = None
coil_width = None
coil_kg = None

# -----------------------------
# DOSYA YÜKLEME
# -----------------------------

col1, col2 = st.columns(2)

with col1:

    st.header("📄 Sipariş Dosyası")

    siparis_dosyasi = st.file_uploader(
        "Sipariş Excel Dosyası",
        type=["xlsx"],
        key="siparis"
    )

    if siparis_dosyasi is not None:

        df = pd.read_excel(siparis_dosyasi)

        st.dataframe(
            df,
            use_container_width=True
        )

        if "En (mm)" in df.columns and "Kg" in df.columns:

            for _, satir in df.iterrows():

                genislik = int(satir["En (mm)"])
                kg = float(satir["Kg"])

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

        else:

            st.error(
                "Sipariş Excelinde 'En (mm)' ve 'Kg' kolonları bulunmalıdır."
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

        st.dataframe(
            df_coil,
            use_container_width=True
        )

        if "En (mm)" in df_coil.columns and "Kg" in df_coil.columns:

            ilk_coil = df_coil.iloc[0]

            coil_width = float(
                ilk_coil["En (mm)"]
            )

            coil_kg = float(
                ilk_coil["Kg"]
            )

            st.write("### Seçilen İlk Mother Coil")

            st.write(
                f"Coil Genişliği : {coil_width:.0f} mm"
            )

            st.write(
                f"Coil Ağırlığı : {coil_kg:.2f} kg"
            )

            st.write(
                f"Toplam Mother Coil : {len(df_coil)} adet"
            )

        else:

            st.error(
                "Mother Coil Excelinde 'En (mm)' ve 'Kg' kolonları bulunmalıdır."
            )


st.divider()

# -----------------------------
# MAKİNE AYARLARI
# -----------------------------

st.header("⚙️ Makine Ayarları")

left_trim = st.number_input(
    "Sol Fire (mm)",
    min_value=0,
    value=5
)

right_trim = st.number_input(
    "Sağ Fire (mm)",
    min_value=0,
    value=5
)

max_knife = st.number_input(
    "Maksimum Bıçak Sayısı",
    min_value=1,
    max_value=20,
    value=10
)

# -----------------------------
# OPTİMİZASYON
# -----------------------------

if st.button(
    "🚀 Optimizasyonu Başlat",
    use_container_width=True
):

    if len(siparisler) == 0:

        st.error(
            "Önce Sipariş Excel dosyasını yükleyin."
        )

    elif coil_width is None or coil_kg is None:

        st.error(
            "Önce Mother Coil Excel dosyasını yükleyin."
        )

    else:

        kullanilabilir_genislik = (
            coil_width
            - left_trim
            - right_trim
        )

        st.success("Optimizasyon Başladı")

        st.write("## Makine Bilgileri")

        st.write(
            f"Mother Coil : {coil_width:.0f} mm"
        )

        st.write(
            f"Mother Coil Kg : {coil_kg:.2f} kg"
        )

        st.write(
            f"Sol Fire : {left_trim} mm"
        )

        st.write(
            f"Sağ Fire : {right_trim} mm"
        )

        st.write(
            f"Kullanılabilir Genişlik : "
            f"{kullanilabilir_genislik:.0f} mm"
        )

        # -----------------------------
        # HIZLI KOMBİNASYON
        # -----------------------------

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
                en
                for en in sirali_enler
                if en <= kalan
                and siparisler[en] > 0
            ]

            if not uygun_enler:
                break

            secilen_en = max(uygun_enler)

            en_iyi.append(secilen_en)

            kalan -= secilen_en

        en_fire = kalan

        # -----------------------------
        # SONUÇ
        # -----------------------------

        if en_iyi:

            st.write("## En Uygun Kombinasyon")

            st.success(
                "En uygun kombinasyon bulundu"
            )

            st.write(
                f"Kombinasyon : {en_iyi}"
            )

            st.write(
                f"Toplam Bant Genişliği : "
                f"{sum(en_iyi)} mm"
            )

            st.write(
                f"Ek Fire : {en_fire} mm"
            )

            st.write(
                f"Bant Sayısı : {len(en_iyi)}"
            )

            # -----------------------------
            # DİLME PLANI
            # -----------------------------

            st.write("### Dilme Planı")

            plan = []

            for sira, genislik in enumerate(
                en_iyi,
                start=1
            ):

                plan.append(
                    {
                        "Bant No": sira,
                        "En (mm)": genislik,
                        "Sipariş Kg":
                            round(
                                siparisler[genislik],
                                2
                            )
                    }
                )

            plan_df = pd.DataFrame(plan)

            st.dataframe(
                plan_df,
                use_container_width=True
            )

            # -----------------------------
            # DİZİLİM
            # -----------------------------

            st.write("### Dilme Dizilimi")

            dizilim = [
                f"Sol Fire {left_trim} mm"
            ]

            for genislik in en_iyi:

                dizilim.append(
                    f"{genislik} mm"
                )

            dizilim.append(
                f"Sağ Fire {right_trim} mm"
            )

            st.write(
                " | ".join(dizilim)
            )

            toplam_kontrol = (
                left_trim
                + sum(en_iyi)
                + right_trim
            )

            st.write(
                f"Toplam Kontrol : "
                f"{toplam_kontrol} mm / "
                f"Mother Coil : {coil_width:.0f} mm"
            )

            # -----------------------------
            # ÜRETİLECEK KG
            # -----------------------------

            st.write(
                "### Üretilecek Kilogramlar"
            )

            uretim_plan = []

            for genislik in sorted(
                set(en_iyi)
            ):

                adet = en_iyi.count(
                    genislik
                )

                tek_bant_kg = (
                    coil_kg
                    * genislik
                    / coil_width
                )

                toplam_uretim_kg = (
                    tek_bant_kg
                    * adet
                )

                uretim_plan.append(
                    {
                        "En (mm)": genislik,
                        "Adet": adet,
                        "Tek Bant Kg":
                            round(
                                tek_bant_kg,
                                2
                            ),
                        "Toplam Üretim Kg":
                            round(
                                toplam_uretim_kg,
                                2
                            )
                    }
                )

            uretim_df = pd.DataFrame(
                uretim_plan
            )

            st.dataframe(
                uretim_df,
                use_container_width=True
            )

            # -----------------------------
            # KALAN SİPARİŞ
            # -----------------------------

            kalan_siparisler = (
                siparisler.copy()
            )

            for satir in uretim_plan:

                genislik = satir[
                    "En (mm)"
                ]

                uretilen_kg = satir[
                    "Toplam Üretim Kg"
                ]

                kalan_siparisler[
                    genislik
                ] -= uretilen_kg

                if (
                    kalan_siparisler[
                        genislik
                    ] < 0
                ):

                    kalan_siparisler[
                        genislik
                    ] = 0

            st.write(
                "### Kalan Siparişler"
            )

            kalan_plan = []

            for genislik in sorted(
                kalan_siparisler
            ):

                kalan_plan.append(
                    {
                        "En (mm)":
                            genislik,

                        "İlk Sipariş Kg":
                            round(
                                siparisler[
                                    genislik
                                ],
                                2
                            ),

                        "Kalan Kg":
                            round(
                                kalan_siparisler[
                                    genislik
                                ],
                                2
                            )
                    }
                )

            kalan_df = pd.DataFrame(
                kalan_plan
            )

            st.dataframe(
                kalan_df,
                use_container_width=True
            )

        else:

            st.error(
                "Uygun dilme kombinasyonu bulunamadı."
            )
