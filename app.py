from fastapi import FastAPI, File, UploadFile, HTTPException
from transcriber import Transcriber
import tempfile, os, logging

# Initialize FastAPI app
app = FastAPI(title="Speech Transcription Service")

# Initialize the transcriber
transcriber = Transcriber()

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.get("/health")
def health():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "ok"}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """
    Endpoint to accept an audio file and return its transcript.
    """
    temp_file_path = None  
    try:
        if not file.filename or not file.filename.endswith(".wav"):
            raise HTTPException(status_code=400, detail="Only .wav files are supported")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(await file.read())
            temp_file.flush()
            # Save the file path for cleanup
            temp_file_path = temp_file.name  
            
        # Transcribe the audio file
        transcript = transcriber.transcribe(temp_file_path)

        return {"filename": file.filename, "transcript": transcript}
    
    except HTTPException as e:
        logging.error(f"Http Exception: {e}")
        raise 
    except ValueError as e:
        logging.error(f"ValueError: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.exception(f"Error during transcription: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)