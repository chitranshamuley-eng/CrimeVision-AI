import os, tempfile
import cv2
from config import VIDEO_SAMPLE_SECONDS
from src.image_analysis import analyze_image

def analyze_video(video_bytes: bytes, source_name="video", sample_seconds=None):
    interval = max(1, int(sample_seconds or VIDEO_SAMPLE_SECONDS))
    out = {"source": source_name, "modality": "video", "status": "unavailable", "frames": [],
           "fps": None, "duration_seconds": None,
           "limitations": ["Frame sampling may miss events between sampled frames.",
                           "This prototype does not run a trained action-recognition model."]}
    path = None; cap = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(source_name)[1] or ".mp4") as f:
            f.write(video_bytes); path = f.name
        cap = cv2.VideoCapture(path)
        if not cap.isOpened(): raise RuntimeError("Video could not be opened; check file or codec.")
        fps = cap.get(cv2.CAP_PROP_FPS) or 1
        count = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
        out["fps"] = round(fps, 3); out["duration_seconds"] = round(count / fps, 3) if count else None
        step = max(1, int(fps * interval)); index = 0
        while len(out["frames"]) < 300:
            cap.set(cv2.CAP_PROP_POS_FRAMES, index)
            ok, frame = cap.read()
            if not ok: break
            ok, encoded = cv2.imencode(".jpg", frame)
            if ok:
                ts = round(index / fps, 3)
                out["frames"].append({"timestamp_seconds": ts,
                    "analysis": analyze_image(encoded.tobytes(), f"{source_name}@{ts:.2f}s")})
            index += step
        out["status"] = "completed"
    except Exception as exc: out["error"] = str(exc)[:350]
    finally:
        if cap: cap.release()
        if path and os.path.exists(path):
            try: os.remove(path)
            except OSError: pass
    return out
