from GetScreenshot import GetScreenshot
from ObjectExtractor import ObjectExtractor
import streamlit as st

st.title("Müze Eser Takip Sistemi")

video_url = st.text_input("Lütfen içerisinden objeleri çıkartmak istediğiniz Pexels videosu linkini giriniz.",
                          placeholder="https://www.pexels.com/video/close-up-video-of-man-wearing-red-hoodie-3249935/")
button = st.button("Objeleri Getir", type="primary")
if button:
    with st.spinner('Videodan ekran görüntüsü alınıyor...'):
        gs = GetScreenshot()
        gs.get_video_screenshot(video_url, "pexels001", 5)
        last_ss_path = gs.get_latest_screenshot("pexels001")
    st.success('Videodan ekran görüntüsü alındı!')

    with st.spinner('Objeler Getiriliyor...'):
        oe = ObjectExtractor()
        generated_output = oe.object_extractor_from_image(last_ss_path)

    st.success('Objeler Getirildi!')
    st.write(generated_output)
