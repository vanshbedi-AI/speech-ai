from faster_whisper import WhisperModel
import tempfile
import os

class AudioTranscriber:

    def __init__(self):
        # Load once
        self.model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )

    def transcribe(self, uploaded_file):

        # Save uploaded audio temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded_file.getbuffer())
            temp_path = tmp.name

        segments, info = self.model.transcribe(
            temp_path,
            beam_size=5
        )

        transcript = ""

        for segment in segments:
            transcript += segment.text + " "

        os.remove(temp_path)

        return transcript.strip(), info.language