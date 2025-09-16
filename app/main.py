
import cv2

from app.model import model, class_names
from app.utils import read_imagefile, image_to_base64

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post(
    "/predict",
    summary="Обнаружение объектов на изображении",
    description="""
Принимает изображение, выполняет детекцию объектов с помощью YOLOv8 и возвращает:

- исходное изображение с разметкой в base64
- список найденных объектов с именами и координатами
"""
)
async def predict(file: UploadFile = File(..., description="Изображение для анализа")):
    image_bytes = await file.read()
    img = read_imagefile(image_bytes)

    # прогон через YOLOv8
    results = model(img)
    detections = results[0].boxes.xyxy.cpu().numpy()   # [[x1,y1,x2,y2], ...]
    classes = results[0].boxes.cls.cpu().numpy()       # классы
    confs   = results[0].boxes.conf.cpu().numpy()      # уверенности

    # рисуем и собираем items
    items = []
    for (x1, y1, x2, y2), cls_id, conf in zip(detections, classes, confs):
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
        name = class_names[int(cls_id)]
        items.append({"name": name, "bbox": [x1, y1, x2, y2]})
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(img, name, (x1, max(y1 - 6, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    photo_base64 = image_to_base64(img)

    return {
        "photo": photo_base64,
        "items": items
    }