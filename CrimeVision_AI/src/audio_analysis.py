import os, tempfile
from config import WHISPER_MODEL

def transcribe_audio(audio_bytes: bytes, source_name="audio"):
    out = {"source": source_name, "modality": "audio", "status": "unavailable", "transcript": "",
           "segments": [], "language": None, "limitations": [
           "Check transcription against the original recording.",
           "Speaker identity and truthfulness are not determined."]}
    path = None
    try:
        from faster_whisper import WhisperModel
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(source_name)[1] or ".audio") as f:
            f.write(audio_bytes); path = f.name
        model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
        segments, info = model.transcribe(path, vad_filter=True)
        out["segments"] = [{"start": round(float(s.start), 3), "end": round(float(s.end), 3), "text": str(s.text).strip()} for s in segments]
        out["transcript"] = " ".join(s["text"] for s in out["segments"])
        out["language"] = getattr(info, "language", None)
        out["status"] = "completed"
    except Exception as exc:
        out["error"] = str(exc)[:350]
    finally:
        if path and os.path.exists(path):
            try: os.remove(path)
            except OSError: pass
    return out
