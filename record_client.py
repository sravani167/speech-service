import sounddevice as sd
from scipy.io.wavfile import write
from transcriber import Transcriber
import argparse

def record_audio(output_file, duration=5, sample_rate=16000):
    """
    Records audio from the microphone and saves it to a file.
    """
    print(f"Recording for {duration} seconds...")
    try:
        # Record audio using sounddevice
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')

        # Wait until recording is finished
        sd.wait()  
        print("Recording complete.")

        # Save the recorded audio to a file
        write(output_file, sample_rate, audio_data)
        print(f"Audio saved to {output_file}")
    except Exception as e:
        print(f"An error occurred while recording audio: {e}")


def transcribe_audio(audio_file, model_path="models/en-us"):
    """
    Transcribes the given audio file using the Transcriber class.
    """
    transcriber = Transcriber(model_path=model_path)
    return transcriber.transcribe(audio_file)


def main():
    parser = argparse.ArgumentParser(description="Record and transcribe audio")
    parser.add_argument("--duration", type=int, default=5, help="Duration of the recording in seconds")
    parser.add_argument("--output", type=str, default="recorded_audio.wav", help="Output WAV file name")
    args = parser.parse_args()  

    # Use parsed arguments
    duration = args.duration
    audio_file = args.output

    print(f"Recording will be saved to: {audio_file}")
    print(f"Recording duration set to: {duration} seconds")

    if args.duration <= 0:
        print("Error: Duration must be greater than 0 seconds.")
        return

    # Record audio
    record_audio(audio_file, duration)

    # Transcribe the recorded audio
    transcription = transcribe_audio(audio_file)

    print(f"Transcription: {transcription}")


if __name__ == "__main__":
    main()