from ultralytics import YOLO

# TODO: вынести в .env
MODEL_PATH = "mlmodels/PotatoBeetleAI-10epochs-640px.pt"

model = YOLO(MODEL_PATH)
class_names = model.names
