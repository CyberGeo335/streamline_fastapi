from fastapi import FastAPI, File, UploadFile
import base64
import cv2

from croping_files import crop_image

app = FastAPI()

@app.post("/back/")
async def upload_photo(file: UploadFile = File(...)):
    # Прочитать содержимое файла как байты
    image_data = await file.read()
    cropped_images = crop_image(image_data)  # Передать image_data, а не BytesIO(image_data)

    # Кодируем изображения в base64 для передачи в JSON
    cropped_images_base64 = []
    for img in cropped_images:
        _, img_encoded = cv2.imencode('.jpg', img)
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')
        cropped_images_base64.append(img_base64)

    # Кодируем оригинальное изображение
    original_image_base64 = base64.b64encode(image_data).decode('utf-8')

    return {"original_image": original_image_base64, "cropped_images": cropped_images_base64}

# uvicorn main:app --reload
