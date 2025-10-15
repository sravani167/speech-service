# Speech Transcription Service

## Overview
This project provides a speech to text transcription service using an open-source library (e.g., Vosk). It includes:
- A FastAPI based HTTP service for transcription.
- A client script for recording and transcribing audio locally or via the service.

## Features
- Record audio from the microphone.
- Transcribe `.wav` audio files.
- Expose an HTTP API for transcription.
- Health check endpoint.

## Supported Audio Formats
The transcription service accepts only WAV files with the following constraints:
- Mono channel
- 16-bit PCM
- Sample rates: 8000, 16000, 32000, 44100, or 48000 Hz


## Setup

### Prerequisites
- Python 3.9 or higher
- `pip` (Python package manager)

### Installation
    ```bash
    git clone https://github.com/your-username/speech_service.git
    cd speech_service
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
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

4. Run the application:
    ```bash
    uvicorn app.main:app --reload
    ```

## Usage

### Run the Service
To start the transcription service, use the following command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
This will launch the service on `http://0.0.0.0:8000`. You can then use the endpoints described below to interact with the service.

### Transcribe Audio File
Send a POST request to the `/transcribe` endpoint with a `.wav` file:
```bash
curl -X POST "http://0.0.0.0:8080/transcribe" -F "file=@path_to_audio.wav"
```

### Health Check
Check if the service is running:
```bash
curl "http://0.0.0.0:8080/health"
```
### 

### Local Transcription
Use the client script to transcribe audio locally:
```bash
python client.py --file path_to_audio.wav
```

### Deployment
You can deploy the service using Docker. Follow these steps:

1. Build the Docker image:
    ```bash
    docker build -t speech-transcription-service .
    ```

2. Run the Docker container:
    ```bash
    docker run -d -p 8000:8000 --name speech_service_container speech-transcription-service
    ```

This will start the service on `http://0.0.0.0:8000`.


### Cloud Deployment
For cloud deployment, you can use platforms like AWS, Azure, or Google Cloud. Package the application as a Docker container and deploy it using their respective container services (e.g., AWS ECS, Azure Container Instances, or Google Cloud Run).

## Testing
Run the test suite using `pytest`:
```bash
pytest
```
## Future Improvements

### Trade-Offs
- **Model Size vs. Accuracy**: The current implementation uses a smaller Vosk model for faster performance, but this may compromise transcription accuracy. A larger model could improve accuracy at the cost of increased resource usage.
- **Real-Time Processing**: The service processes audio files after they are uploaded. Real-time transcription could be implemented but would require more computational resources and optimization.

### Next Steps
- **Support for Additional Languages**: Extend the service to support multiple languages by integrating additional Vosk models.
- **Authentication and Authorization**: Add security features to restrict access to the API endpoints.
- **Scalability**: Implement horizontal scaling using container orchestration tools like Kubernetes.
- **Improved Error Handling**: Enhance error messages and logging for better debugging and user experience.
- **Web Interface**: Develop a simple web-based UI for users to upload audio files and view transcriptions.
- **Streaming Support**: Enable live audio streaming for real-time transcription.
- **Integration with Cloud Storage**: Allow users to upload audio files directly from cloud storage services like AWS S3 or Google Drive.
- **Benchmarking and Optimization**: Profile the application to identify bottlenecks and optimize performance.
- **Mobile Client**: Build a mobile application to interact with the transcription service.