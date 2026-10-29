import streamlit as st
import pandas as pd
from src.image_analysis import analyze_image
from src.audio_analysis import transcribe_audio
from src.video_analysis import analyze_video
from src.fusion import build_timeline
from src.evidence_chat import answer_question, generate_hypothesis_prompts
from src.report import generate_pdf_report

st.set_page_config(page_title="CrimeVision AI", page_icon="🔎", layout="wide")
st.title("🔎 CrimeVision AI")
st.caption("Intelligent Multimodal Forensic Analysis Platform · Human-reviewed decision support")
st.warning("Educational prototype only. Outputs can be inaccurate and are not forensic conclusions. Do not use this system alone to identify suspects, determine guilt, or make legal decisions. Use authorized test evidence and preserve originals.")
with st.sidebar:
    case_label = st.text_input("Case label", "Demo Case 001")
    do_img = st.checkbox("Analyze images", True)
    do_audio = st.checkbox("Transcribe audio", True)
    do_video = st.checkbox("Sample video frames", True)
    sample_s = st.slider("Video interval (seconds)", 1, 10, 2)
imgs = st.file_uploader("Image evidence", ["png","jpg","jpeg","webp"], accept_multiple_files=True)
audios = st.file_uploader("Audio evidence", ["wav","mp3","m4a","flac","ogg"], accept_multiple_files=True)
videos = st.file_uploader("Video evidence", ["mp4","mov","avi","mkv"], accept_multiple_files=True)
for key in ("images_result","audio_result","video_result","timeline"):
    if key not in st.session_state: st.session_state[key] = []
if st.button("Analyze uploaded evidence", type="primary"):
    ir, ar, vr = [], [], []
    if do_img:
        for f in imgs or []:
            with st.spinner("Analyzing image "+f.name): ir.append(analyze_image(f.getvalue(), f.name))
    if do_audio:
        for f in audios or []:
            with st.spinner("Transcribing audio "+f.name): ar.append(transcribe_audio(f.getvalue(), f.name))
    if do_video:
        for f in videos or []:
            with st.spinner("Sampling video "+f.name): vr.append(analyze_video(f.getvalue(), f.name, sample_s))
    st.session_state.images_result, st.session_state.audio_result, st.session_state.video_result = ir, ar, vr
    st.session_state.timeline = build_timeline(ir, ar, vr)
    st.success("Pipeline finished. Review all outputs; completion does not mean findings are accurate.")
ir, ar, vr, tl = (st.session_state[k] for k in ("images_result","audio_result","video_result","timeline"))
if not (ir or ar or vr):
    st.info("Upload one or more files, then click Analyze uploaded evidence.")
    st.markdown("**Workflow:** upload → analyze → review results → inspect unified timeline → ask evidence questions → export PDF.")
else:
    tabs = st.tabs(["Overview","Image Analysis","Audio Analysis","Video Analysis","Unified Timeline","Evidence Chat","PDF Report"])
    with tabs[0]:
        a,b,c,d = st.columns(4); a.metric("Images",len(ir)); b.metric("Audio",len(ar)); c.metric("Videos",len(vr)); d.metric("Timeline records",len(tl))
        st.subheader("Review prompts")
        for p in generate_hypothesis_prompts(tl): st.markdown("- "+p)
    with tabs[1]:
        for r in ir:
            with st.expander(f"{r['source']} — {r['status']}"):
                st.write(r["summary"]); st.json({"dimensions":[r["width"],r["height"]],"detections":r["detections"],"limitations":r["limitations"]})
    with tabs[2]:
        for r in ar:
            with st.expander(f"{r['source']} — {r['status']}"):
                st.write("Language:",r.get("language") or "Unknown")
                st.text_area("Transcript — verify against original",r.get("transcript",""),key="trans_"+r["source"])
                if r.get("error"): st.error(r["error"])
                if r.get("segments"): st.dataframe(pd.DataFrame(r["segments"]),use_container_width=True)
    with tabs[3]:
        for r in vr:
            with st.expander(f"{r['source']} — {r['status']}"):
                st.write("Duration:",r.get("duration_seconds"),"seconds · FPS:",r.get("fps"))
                if r.get("error"): st.error(r["error"])
                st.dataframe(pd.DataFrame([{"time_seconds":f["timestamp_seconds"],"objects":", ".join(d["label"] for d in f["analysis"].get("detections",[]))} for f in r.get("frames",[])]),use_container_width=True)
                st.caption("Sampled-frame object detection only; not validated action recognition.")
    with tabs[4]:
        df = pd.DataFrame([{k:e.get(k) for k in ["time_label","time_seconds","modality","source","event","confidence"]} for e in tl])
        st.dataframe(df,use_container_width=True,hide_index=True)
        st.download_button("Download timeline CSV",df.to_csv(index=False).encode(), "crimevision_timeline.csv","text/csv")
    with tabs[5]:
        q = st.text_input("Ask about analyzed records",placeholder="Which labels were detected in the image?")
        if st.button("Search evidence"):
            result = answer_question(q,tl,ir,ar,vr); st.markdown(result["answer"])
    with tabs[6]:
        st.write("The PDF includes the timeline and human-review limitations.")
        if st.button("Generate PDF"):
            try:
                pdf = generate_pdf_report(case_label,tl,ir,ar,vr)
                st.download_button("Download PDF report",pdf,"CrimeVision_AI_Report.pdf","application/pdf")
            except Exception as e: st.error("PDF generation failed: "+str(e))
