import wave
import tempfile
import pytest
from transcriber import Transcriber
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_transcriber_initialization():
    transcriber = Transcriber(model_path="models/en-us")
    assert transcriber is not None

def test_transcriber_invalid_file():
    transcriber = Transcriber(model_path="models/en-us")

    # Create a temporary file that exists but is not a WAV
    with tempfile.NamedTemporaryFile(suffix=".txt") as tmp:
        tmp.write(b"not a real wav file")
        tmp.flush()
        
        with pytest.raises(ValueError) as e_info:
            transcriber.transcribe(tmp.name)
        
        assert str(e_info.value) == "Invalid WAV file"

def test_transcriber_stereo_file():
    # Create a temporary stereo WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(2)  # stereo
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(b"\x00\x00" * 16000)
        
        transcriber = Transcriber(model_path="models/en-us")
        with pytest.raises(ValueError) as e_info:
            transcriber.transcribe(tmp.name)
        assert str(e_info.value) == "Audio file must be mono channel"

def test_transcriber_invalid_sample_width():
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(1)  # mono
            wf.setsampwidth(1)  # wrong width
            wf.setframerate(16000)
            wf.writeframes(b"\x00" * 16000)
        
        transcriber = Transcriber(model_path="models/en-us")
        with pytest.raises(ValueError) as e_info:
            transcriber.transcribe(tmp.name)
        assert str(e_info.value) == "Audio file must have a sample width of 2 bytes"

def test_transcriber_unsupported_sample_rate():
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(1)  # mono
            wf.setsampwidth(2)  # correct
            wf.setframerate(22050)  # unsupported
            wf.writeframes(b"\x00\x00" * 22050)
        
        transcriber = Transcriber(model_path="models/en-us")
        with pytest.raises(ValueError) as e_info:
            transcriber.transcribe(tmp.name)
        assert "Unsupported sample rate" in str(e_info.value)

def test_transcriber_valid_mono_wav():
    """Test a valid mono WAV file returns a transcript"""
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(1)       # mono
            wf.setsampwidth(2)       # 16-bit PCM
            wf.setframerate(16000)   # supported sample rate
            wf.writeframes(b"\x00\x00" * 1600)  # small dummy data
        
        transcriber = Transcriber(model_path="models/en-us")
        transcript = transcriber.transcribe(tmp.name)
        
        # Should return a string (even if empty)
        assert isinstance(transcript, str)

def test_transcribe_endpoint_valid_file():
    # Create a valid mono WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(b"\x00\x00" * 1600)
        
        with open(tmp.name, "rb") as f:
            response = client.post("/transcribe", files={"file": ("test.wav", f.read())})
    
    assert response.status_code == 200
    assert "transcript" in response.json()

def test_transcribe_endpoint_invalid_file():
    # Upload a non-WAV file
    response = client.post("/transcribe", files={"file": ("test.txt", b"not a wav")})
    assert response.status_code == 400
    assert response.json()["detail"] == "Only .wav files are supported"