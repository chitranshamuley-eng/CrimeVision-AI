import re
STOP = set("what when where who is are the a an of in on to did does was were and or tell me about show find please evidence".split())

def answer_question(question, timeline, image_results=None, audio_results=None, video_results=None):
    terms = set(re.findall(r"[a-z0-9]+", question.lower())) - STOP
    if not terms:
        return {"answer": "Ask a specific question about a detected label, transcript, source, or timeline event.", "matches": []}
    scored = []
    for e in timeline:
        words = set(re.findall(r"[a-z0-9]+", (str(e.get("event",""))+" "+str(e.get("source",""))+" "+str(e.get("modality",""))).lower()))
        score = len(terms & words)
        if score: scored.append((score, e))
    scored.sort(key=lambda x: -x[0]); matches = [e for _, e in scored[:8]]
    if not matches:
        return {"answer": "No matching analyzed observation was found. This does not prove the event or object is absent; review original evidence and confirm analysis completed.", "matches": []}
    lines = [f"- [{e.get('time_label','Time unknown')}] {e.get('modality')} / {e.get('source')}: {e.get('event')}" for e in matches]
    return {"answer": "Matching system-generated records (not verified facts):\\n" + "\\n".join(lines) + "\\nVerify every item against original evidence.", "matches": matches}

def generate_hypothesis_prompts(timeline):
    if not timeline: return ["No analyzed events yet. Upload evidence and run analysis first."]
    prompts = ["Do timestamps from different sources agree after accounting for clock offsets?",
               "Which observations are model outputs versus interpretations requiring review?",
               "Could unsampled video or unclear audio affect the chronology?",
               "Can each interpretation be checked against original, unmodified evidence?"]
    if len({e.get("modality") for e in timeline}) > 1:
        prompts.append("Which events appear across modalities, and could any apparent match be coincidental?")
    return prompts
