import streamlit as st

st.set_page_config(
    page_title="GEORG Optimizer",
    page_icon="⚙️"
)

st.title("⚙️ GEORG Slitting Optimizer")

st.write("İlk web uygulamam çalışıyor!")

if st.button("Test Butonu"):
    st.success("Butona başarıyla tıklandı!")
