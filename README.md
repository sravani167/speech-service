# Speech Transcription Service

## Overview
This project provides a speech to text transcription service using an open-source library (e.g., Vosk). It includes:
- A FastAPI based HTTP service for transcription.
- A client script for recording and transcribing audio locally or via the service.

## Architecture Overview
This service provides speech to text transcription using the open-source Vosk engine. 
The FastAPI application exposes two main endpoints: 
- `GET /health` for service readiness
- `POST /transcribe` to accept a WAV audio file and return a transcript in JSON format. 
When a file is posted, the service loads the audio, passes it to the Vosk recognizer, and returns the transcription in JSON format. 
```json
{
  "filename":"recorded_audio.wav",
  "transcript": "transcribed text here"
}
```
An optional client script allows users to record audio locally and either save it or send it directly to the service for transcription. 

## Features
- Record audio from the microphone.
- Transcribe `.wav` audio files.
- Expose an HTTP API for transcription.
- Health check endpoint.

## Supported Audio Formats and Limits

### Accepted Format
- **File type:** WAV (`.wav`) only  
- **Encoding:** PCM (16-bit, mono channel)  
- **Supported sample rates:** 8000, 16000, 32000, 44100, or 48000 Hz  

### Reason
The Vosk engine requires uncompressed PCM audio for accurate transcription.  
Stereo or compressed formats (e.g., MP3, AAC) are not supported.

### Runtime Limits
- **Recommended maximum file size:** ~10 MB (≈ 1–2 minutes of audio at 16 kHz mono).  
- Larger files may increase memory usage or processing time.  
- Real time transcription speed depends on CPU performance — typically near 1× real time for small models.

### Recording constraints:
- The client script (record_client.py) records mono audio at 16 kHz sample rate.
- Default duration: 5 seconds (can be changed via --duration).
- Audio is saved as int16 PCM format and is fully compatible with the transcription endpoint.


## Setup

### Prerequisites
- Python 3.12+
- `pip` (Python package manager)

### Installation
1. Clone Repository:
    ```bash
    git clone https://github.com/sravani167/speech_service.git
    cd speech_service
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. Download the Vosk model and place it in the models/ directory:
    ```bash
    mkdir -p models
    # Download the model from https://alphacephei.com/vosk/models
    # Example for English model
    wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
    unzip vosk-model-small-en-us-0.15.zip -d models
    mv models/vosk-model-small-en-us-0.15 models/english
    ```

## Usage

### Testing
Run the test suite using `pytest`:
```bash
PYTHONPATH=. pytest
```

### Run the Service
To start the transcription service, use the following command:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
This will launch the service on `http://127.0.0.1:8000`. You can then use the endpoints described below to interact with the service.

### Health Check
Check if the service is running:
```bash
curl -X GET http://127.0.0.1:8000/health
```

### Transcribe Audio File
Send a POST request to the `/transcribe` endpoint with a `.wav` file:
```bash
curl -X POST "http://127.0.0.1:8000/transcribe" -F "file=@path_to_audio.wav"
```

### Optional Local Transcription
Use the client script to transcribe audio locally:
```bash
python record_client.py --duration 10 --file path_to_audio.wav
```

## Deployment
You can deploy the service using Docker. Follow these steps:

1. Build the Docker image:
    ```bash
    docker build -t speech_service .
    ```

2. Run the Docker container:
    ```bash
    docker run -d -p 8000:8000 --name speech_service_container speech_service
    ```

This will start the service on `http://127.0.0.1:8000`.


## Cloud Deployment
For cloud deployment, you can use platforms like AWS, Azure, or Google Cloud. Package the application as a Docker container and deploy it using their respective container services (e.g., AWS ECS, Azure Container Instances, or Google Cloud Run).

## Notes & Trade-offs
- **Audio Format**: Only mono WAV files (16-bit PCM) are supported. Other formats will raise an error.
- **Performance**: Vosk is lightweight but may be slower on long recordings. Faster transcription could be achieved using GPU-based models like Whisper.
- **Scalability**: Current design is single-instance; for multiple concurrent users, a load balancer or async queue processing could be added.
- **Security**: No authentication or rate limiting is implemented. For production, API keys or OAuth should be considered.
- **Future Improvements**:
    - Support for streaming audio.
    - Client-side recording using the browser.
    - Containerized deployment with CI/CD auto-deploy to cloud.

## Next Steps
- **Support for Additional Languages**: Extend the service to support multiple languages by integrating additional Vosk models.
- **Authentication and Authorization**: Add security features to restrict access to the API endpoints.
- **Scalability**: Implement horizontal scaling using container orchestration tools like Kubernetes.
- **Improved Error Handling**: Enhance error messages and logging for better debugging and user experience.
- **Web Interface**: Develop a simple web-based UI for users to upload audio files and view transcriptions.
- **Streaming Support**: Enable live audio streaming for real-time transcription.
- **Integration with Cloud Storage**: Allow users to upload audio files directly from cloud storage services like AWS S3 or Google Drive.
- **Benchmarking and Optimization**: Profile the application to identify bottlenecks and optimize performance.
- **Mobile Client**: Build a mobile application to interact with the transcription service.

## License
This project uses open-source libraries and is free to use.