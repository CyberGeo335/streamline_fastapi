import streamlit as st
import requests
from PIL import Image
import io
import base64

URL = "http://localhost:8000/back/"

st.title("Загрузка фотографии")

# Загрузка файла
uploaded_file = st.file_uploader("Выберите фото...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Отправка файла на backend
    response = requests.post(
        URL,
        files={"file": uploaded_file.getvalue()}
    )
    if response.status_code == 200:
        data = response.json()
        # Декодируем и показываем оригинальную фотографию
        original_image = Image.open(io.BytesIO(base64.b64decode(data["original_image"])))
        st.image(original_image, caption="Оригинальная фотография", use_column_width=True)

        # Декодируем и показываем обрезанные фотографии
        st.write("Обрезанные фотографии:")
        for cropped_image_data in data["cropped_images"]:
            cropped_image = Image.open(io.BytesIO(base64.b64decode(cropped_image_data)))
            st.image(cropped_image, caption="Обрезанная фотография", use_column_width=True)
    else:
        st.write("Произошла ошибка при загрузке фотографии.")