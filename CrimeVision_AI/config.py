import os
from dotenv import load_dotenv
load_dotenv()
YOLO_MODEL = os.getenv("CRIMEVISION_YOLO_MODEL", "yolov8n.pt")
WHISPER_MODEL = os.getenv("CRIMEVISION_WHISPER_MODEL", "base")
VIDEO_SAMPLE_SECONDS = max(1, int(os.getenv("CRIMEVISION_VIDEO_SAMPLE_SECONDS", "2")))
