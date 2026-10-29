# Project Workflow
1. Install Python and create a virtual environment.
2. Install `requirements.txt`.
3. Upload authorized image/audio/video test files in the Streamlit dashboard.
4. Run analysis, review detections/transcripts, and inspect the unified timeline.
5. Ask evidence-grounded questions and export a PDF review report.
6. Run `python -m unittest discover -s tests -v`.

## Requested activities
- Prerequisites / requirements / environment: README, `requirements.txt`, `config.py`, `.env.example`.
- 2.1 image object detection: `src/image_analysis.py`.
- 2.2 scene summaries and hypotheses: image summaries and review prompts.
- 3.1 audio transcription: `src/audio_analysis.py`.
- 3.2 events and timeline: transcript segments and `src/fusion.py`.
- 4.1 video frame processing: `src/video_analysis.py`.
- 4.2 timestamped events: video frame timestamps. A validated crime-type classifier is not included.
- 5.1 multimodal fusion: `src/fusion.py`.
- 5.2 natural-language querying / hypothesis prompts: `src/evidence_chat.py`.
- 6.1 dashboard: `app.py`.
- 6.2 tests: `tests/test_core.py`.
- 6.3 PDF report / deployment: `src/report.py` and README.
- Conclusion: modular educational demonstration; independent validation is required.
