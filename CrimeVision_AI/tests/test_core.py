import unittest
from src.fusion import build_timeline
from src.evidence_chat import answer_question, generate_hypothesis_prompts

class CoreTests(unittest.TestCase):
    def test_timeline_sorts_times(self):
        audio=[{"source":"witness.wav","segments":[{"start":5,"end":6,"text":"sound"},{"start":1,"end":2,"text":"entered"}]}]
        tl=build_timeline([],audio,[])
        self.assertEqual([1,5],[e["time_seconds"] for e in tl])
    def test_chat_matches_record(self):
        tl=[{"time_seconds":2,"time_label":"00:00:02","modality":"video","source":"clip.mp4","event":"Frame object label: person","confidence":.9}]
        self.assertTrue(answer_question("Was a person detected in the video?",tl)["matches"])
    def test_no_match_is_cautious(self):
        self.assertIn("does not prove",answer_question("Where is bicycle?",[])["answer"])
    def test_prompts_exist(self):
        self.assertTrue(generate_hypothesis_prompts([{"modality":"image"}]))
if __name__ == "__main__": unittest.main()
