from io import BytesIO
from PIL import Image
from config import YOLO_MODEL

def analyze_image(image_bytes: bytes, source_name="image"):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    result = {"source": source_name, "modality": "image", "width": image.width, "height": image.height,
              "detections": [], "status": "unavailable", "summary": "",
              "limitations": ["General-purpose detections are not verified forensic findings.",
                              "A missing detection does not prove an object is absent."]}
    try:
        from ultralytics import YOLO
        model = YOLO(YOLO_MODEL)
        preds = model.predict(image, verbose=False)
        for pred in preds:
            for box in (getattr(pred, "boxes", None) or []):
                idx = int(box.cls[0].item())
                result["detections"].append({"label": str(pred.names.get(idx, idx)),
                    "confidence": round(float(box.conf[0].item()), 4),
                    "bbox_xyxy": [round(float(x), 2) for x in box.xyxy[0].tolist()]})
        result["status"] = "completed"
        labels = [x["label"] for x in result["detections"]]
        result["summary"] = "Model detected: " + ", ".join(labels[:12]) if labels else "No objects returned above the configured threshold."
    except Exception as exc:
        result["summary"] = "Image loaded, but model inference is unavailable: " + str(exc)[:250]
    return result
