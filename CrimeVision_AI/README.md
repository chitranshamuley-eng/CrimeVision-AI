# CrimeVision AI — Multimodal Forensic Analysis Platform

Educational prototype for organizing image, audio, and video observations into a reviewable timeline. Includes optional YOLO object detection, optional faster-whisper transcription, sampled video-frame analysis, keyword-based evidence Q&A, Streamlit dashboard, and PDF review reports.

> **Responsible use:** This is not a validated forensic tool. Model outputs may be wrong and must be checked against original evidence. Do not use it alone to identify suspects, determine guilt, or make legal conclusions. Preserve originals and follow approved chain-of-custody procedures. Do not upload real or confidential evidence to GitHub.

## Features and task mapping
- Prerequisites, environment setup, and `requirements.txt`: README, `requirements.txt`, `config.py`, `.env.example`
- Activity 2.1: image object detection: `src/image_analysis.py`
- Activity 2.2: scene summaries and review prompts: dashboard and `src/evidence_chat.py`
- Activity 3.1: audio transcription: `src/audio_analysis.py`
- Activity 3.2: timestamped transcript events and timeline: `src/fusion.py`
- Activity 4.1: video frame sampling and object detection: `src/video_analysis.py`
- Activity 4.2: timestamped frame events. **Validated crime-type classification and trained action recognition are not implemented**; see limitations.
- Activity 5.1: multimodal fusion: `src/fusion.py`
- Activity 5.2: evidence-context Q&A and hypothesis prompts: `src/evidence_chat.py`
- Activity 6.1: dashboard: `app.py`
- Activity 6.2: tests: `tests/test_core.py`
- Activity 6.3: PDF report and deployment instructions: `src/report.py`, this README
- Conclusion: modular demonstration; all results need independent review.

## Project layout
```text
CrimeVision_AI/
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── LICENSE
├── src/ (image, audio, video, fusion, chat, report modules)
├── tests/
├── docs/
└── sample_data/
```

## Prerequisites and setup (Windows PowerShell)
Install Python 3.10–3.12 and Git. Open this folder in VS Code, then run:
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```
If activation is blocked, use Command Prompt: `.venv\Scripts\activate.bat`. Streamlit usually opens `http://localhost:8501`.

First use of YOLO or faster-whisper may download model weights. Use small, non-sensitive test files first. General-purpose detectors are not validated weapon detectors; missing detections do not prove absence. Supported image types: PNG/JPG/JPEG/WEBP; audio: WAV/MP3/M4A/FLAC/OGG; video: MP4/MOV/AVI/MKV (codec support varies).

## Tests
```powershell
python -m unittest discover -s tests -v
```
Tests do not require model downloads.

## GitHub upload
Create an empty repository, then from this project root:
```bash
git init
git add .
git status
git commit -m "Initial commit: CrimeVision AI"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/CrimeVision_AI.git
git push -u origin main
```
Replace the URL with your own. Before committing, ensure `.env`, private evidence, generated reports, model weights, and virtual environments are excluded.

## Limitations
This is a student prototype. Chat uses keyword retrieval, not an LLM. Video processing samples frames rather than recognizing actions. No validated crime-type classifier, weapon detector, speaker identification, causal reconstruction, authenticity verification, or chain-of-custody logging is provided. Validate accuracy, bias, security, privacy, and reproducibility independently before any real-world use.
