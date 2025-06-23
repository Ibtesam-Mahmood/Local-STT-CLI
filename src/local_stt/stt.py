import os
import importlib.resources as pkg_resources
from pathlib import Path
from local_stt import model
import wave
import json
from vosk import Model, KaldiRecognizer, SetLogLevel

# Get the absolute path of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Use it to locate your Vosk model and audio file
model_dir = pkg_resources.files(model) / "vosk-model-en-us-0.42-gigaspeech"
MODEL_PATH = str(model_dir)

class STTParser:
  def __init__(self, output_file: str, model_path: str | None = MODEL_PATH):
    self.output_file = output_file
    self.model_path = MODEL_PATH if model_path is None else model_path
    self.model = self._load_model()
    pass
  
  def _load_model(self):
    SetLogLevel(0)  # Set log level to suppress unnecessary logs
    model = Model(self.model_path)
    return model
  
  def load_audio(self, audio_file: str) -> wave.Wave_read:
    # Check if the audio file exists
    if not os.path.exists(audio_file):
      raise FileNotFoundError(f"Audio file {audio_file} does not exist.")
    
    # Only works on .wav files
    if not audio_file.endswith('.wav'):
      raise ValueError("The file must be a .wav file")
    
    wf = wave.open(audio_file, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
      raise ValueError("Audio file must be WAV format, 16-bit PCM, mono")
    
    return wf

  def parse(self, audio_file: str) -> None:
    print(f"Processing audio file: {audio_file}")
    
    # Load the audio file
    wf = self.load_audio(audio_file)
    
    # Initialize the recognizer using the input's sample rate
    rec = KaldiRecognizer(self.model, wf.getframerate())
    
    # Process the audio file in chunks
    print("Starting speech recognition...")
    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        # Process chunk; if a full utterance is detected, Result() is returned
        if rec.AcceptWaveform(data):
            r = json.loads(rec.Result())
            results.append(r.get("text", ""))
    
    # Grab any leftover speech
    final = json.loads(rec.FinalResult())
    results.append(final.get("text", ""))
    print("Speech recognition completed.")
    
    # Write the results to the output file
    text = " ".join(filter(None, results))
    with open(self.output_file, 'w') as f:
      f.write(text)

    print(f"Results written to {self.output_file}")