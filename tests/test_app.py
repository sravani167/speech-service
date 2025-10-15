import wave
import tempfile
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_transcribe_invalid_file():
    response = client.post("/transcribe", files={"file": ("test.txt", b"Invalid content")})
    assert response.status_code == 400
    assert response.json()["detail"] == "Only .wav files are supported"

def test_transcribe_valid_mono_wav():
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(1)       # mono
            wf.setsampwidth(2)       # 16-bit PCM
            wf.setframerate(16000)   # supported sample rate
            wf.writeframes(b"\x00\x00" * 1600)  # dummy audio data
        
        with open(tmp.name, "rb") as f:
            response = client.post("/transcribe", files={"file": ("test.wav", f.read())})
    
    assert response.status_code == 200
    assert "transcript" in response.json()
    assert response.json()["filename"] == "test.wav"

def test_transcribe_stereo_wav():
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(2)       # stereo
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(b"\x00\x00" * 1600)
        
        with open(tmp.name, "rb") as f:
            response = client.post("/transcribe", files={"file": ("stereo.wav", f.read())})
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Audio file must be mono channel"

def test_transcribe_invalid_sample_width():
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(1)  # invalid sample width
            wf.setframerate(16000)
            wf.writeframes(b"\x00" * 1600)
        
        with open(tmp.name, "rb") as f:
            response = client.post("/transcribe", files={"file": ("wrong_width.wav", f.read())})
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Audio file must have a sample width of 2 bytes"

def test_transcribe_unsupported_sample_rate():
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(22050)  # unsupported rate
            wf.writeframes(b"\x00\x00" * 22050)
        
        with open(tmp.name, "rb") as f:
            response = client.post("/transcribe", files={"file": ("bad_rate.wav", f.read())})
    
    assert response.status_code == 400
    assert "Unsupported sample rate" in response.json()["detail"]