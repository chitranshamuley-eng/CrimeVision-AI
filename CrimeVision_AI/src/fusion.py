def _time(value):
    if value is None: return "Time unknown"
    n = max(0, int(float(value))); h, rem = divmod(n, 3600); m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def build_timeline(image_results=None, audio_results=None, video_results=None):
    events = []
    for r in image_results or []:
        for d in r.get("detections", []):
            events.append({"time_seconds": None, "time_label": "Time unknown", "modality": "image",
                "source": r.get("source", "image"), "event": "Detected object label: " + d.get("label", "unknown"),
                "confidence": d.get("confidence")})
        if r.get("summary"):
            events.append({"time_seconds": None, "time_label": "Time unknown", "modality": "image",
                "source": r.get("source", "image"), "event": r["summary"], "confidence": None})
    for r in audio_results or []:
        for s in r.get("segments", []):
            events.append({"time_seconds": s.get("start"), "time_label": _time(s.get("start")), "modality": "audio",
                "source": r.get("source", "audio"), "event": "Transcript: " + s.get("text", ""), "confidence": None})
    for r in video_results or []:
        for f in r.get("frames", []):
            a = f.get("analysis", {}); ts = f.get("timestamp_seconds")
            ds = a.get("detections", [])
            if ds:
                for d in ds:
                    events.append({"time_seconds": ts, "time_label": _time(ts), "modality": "video",
                        "source": r.get("source", "video"), "event": "Frame object label: " + d.get("label", "unknown"),
                        "confidence": d.get("confidence")})
            else:
                events.append({"time_seconds": ts, "time_label": _time(ts), "modality": "video",
                    "source": r.get("source", "video"), "event": a.get("summary", "Sampled frame analyzed"), "confidence": None})
    return sorted(events, key=lambda e: (e["time_seconds"] is None, e["time_seconds"] if e["time_seconds"] is not None else 1e20, e["modality"]))
