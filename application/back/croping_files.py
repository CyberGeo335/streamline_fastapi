from ultralytics import YOLO
from PIL import Image
import io
import tempfile


model_path = '/Users/g.kozin/projects/Hackatons/2024/kalinengrad/application/model_repository/models/1/model.onnx'

def crop_image(image_data):
    # Конвертация входного изображения в JPEG с помощью Pillow для совместимости с моделью
    image = Image.open(io.BytesIO(image_data))

    with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
        # Конвертируем изображение в RGB (если, например, это PNG с альфа-каналом) и сохраняем во временный файл
        image = image.convert("RGB")
        image.save(temp_file, format="JPEG")
        temp_file.flush()

        # Загрузка модели
        model = YOLO(model_path)

        # Выполнение предсказания
        results = model.predict(temp_file.name,)
        cropped_images = []

        for result in results:
            image = result.plot()  # Получаем изображение с нарисованными bbox

            # Проверяем, что у result есть атрибут boxes для обработки bbox
            if hasattr(result, 'boxes'):
                for box in result.boxes:
                    # Проверяем, что box имеет атрибут xyxy для извлечения координат
                    if hasattr(box, 'xyxy') and box.xyxy.shape[-1] == 4:
                        x_min, y_min, x_max, y_max = box.xyxy[0].tolist()
                        padding = 0.1  # Процент увеличения рамки

                        # Расширяем рамки с учетом padding
                        height, width, _ = image.shape
                        x_min = max(0, int(x_min - padding * (x_max - x_min)))
                        y_min = max(0, int(y_min - padding * (y_max - y_min)))
                        x_max = min(width, int(x_max + padding * (x_max - x_min)))
                        y_max = min(height, int(y_max + padding * (y_max - y_min)))

                        # Обрезаем изображение по расширенным рамкам
                        cropped_image = image[y_min:y_max, x_min:x_max]
                        cropped_images.append(cropped_image)

    return cropped_images
