import json
import wave 
from vosk import Model, KaldiRecognizer

class Transcriber:
    """
    Speech to text transcription using Vosk.

    Supported audio formats:
      - File type: WAV only
      - Channels: Mono (1 channel)
      - Sample width: 16-bit PCM (2 bytes)
      - Sample rates: 8000, 16000, 32000, 44100, 48000 Hz
    """
        
    def __init__(self, model_path="models/en-us"):
        self.model = Model(model_path)


    def transcribe(self, file_path):
        try:
            wf = wave.open(file_path, "rb")
        except (wave.Error, EOFError) as e:
            raise ValueError("Invalid WAV file") from e

        if wf.getnchannels() != 1:
            raise ValueError("Audio file must be mono channel")

        if wf.getsampwidth() != 2:
            raise ValueError("Audio file must have a sample width of 2 bytes")

        if wf.getframerate() not in [8000, 16000, 32000, 44100, 48000]:
            raise ValueError("Unsupported sample rate. Supported rates are 8000, 16000, 32000, 44100, or 48000 Hz")

        recognizer = KaldiRecognizer(self.model, wf.getframerate())

        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                results.append(result.get("text", ""))

        # Final result
        final_result = json.loads(recognizer.FinalResult())
        results.append(final_result.get("text", ""))

        wf.close()
        return " ".join(results)