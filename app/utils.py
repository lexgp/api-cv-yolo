import base64
import cv2
import numpy as np
from io import BytesIO
from PIL import Image

def read_imagefile(file) -> np.ndarray:
    """Читает загруженный файл и возвращает cv2-изображение (BGR)."""
    image = Image.open(BytesIO(file))
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def image_to_base64(img: np.ndarray) -> str:
    """Конвертирует OpenCV изображение в base64 строку (JPEG)."""
    _, buffer = cv2.imencode(".jpg", img)
    return base64.b64encode(buffer).decode("utf-8")
