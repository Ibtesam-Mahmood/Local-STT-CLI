import os
import importlib.resources as pkg_resources
from local_stt import model
import wave
import json
from vosk import Model, KaldiRecognizer, SetLogLevel
import tqdm

# Get the absolute path of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Use it to locate your Vosk model and audio file
model_dir = pkg_resources.files(model) / "vosk-model-en-us-0.42-gigaspeech"
MODEL_PATH = str(model_dir)

class STTParser:
  def __init__(self, audio_file: str, output_file: str, model_path: str | None = MODEL_PATH, convert: bool = False):
    self.output_file = output_file
    self.convert = convert
    self.wf = self.load_audio(audio_file)
    self.model_path = MODEL_PATH if model_path is None else model_path
    self.model = self._load_model()
    pass
  
  def _load_model(self):
    print("Loading model from:", self.model_path)
    SetLogLevel(0)  # Set log level to suppress unnecessary logs
    model = Model(self.model_path)
    return model
  
  def convert_to_wav(self, audio_file: str) -> str:
    # If the audio file is already a .wav file, return it
    if audio_file.endswith('.wav'):
      return audio_file
    
    # If the file is not a .wav file and convert is False, raise an error
    if not self.convert:
      raise ValueError("The file must be a .wav file, or set convert to True")
    
    # Convert the audio file to .wav format using ffmpeg with correct format
    import subprocess
    output_path = audio_file.rsplit('.', 1)[0] + '.wav'
    command = [
        "ffmpeg",
        "-i", audio_file,
        "-ac", "1",           # mono
        "-ar", "16000",       # 16kHz sample rate (vosk default)
        "-sample_fmt", "s16", # 16-bit PCM
        output_path
    ]
    print("Convert flag is set. Performing conversion...")
    subprocess.run(command, check=True)
    print(f"Converted {audio_file} to {output_path}")
    return output_path
  
  def load_audio(self, audio_file: str) -> wave.Wave_read:
    print("Loading audio file:", audio_file)
    
    # Check if the audio file exists
    if not os.path.exists(audio_file):
      raise FileNotFoundError(f"Audio file {audio_file} does not exist.")
    
    # If convert is True then conver the file to .wav format
    wav_path = self.convert_to_wav(audio_file)
    
    if not os.path.exists(wav_path):
      raise FileNotFoundError(f"WAV file not found: {wav_path}")
    
    wf = wave.open(wav_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
      raise ValueError("Audio file must be WAV format, 16-bit PCM, mono")
    
    return wf

  def parse(self) -> None:
    print("Processing audio file")
    
    # Initialize the recognizer using the input's sample rate
    rec = KaldiRecognizer(self.model, self.wf.getframerate())
    
    # Process the audio file in chunks with tqdm progress bar
    print("Starting speech recognition...")
    results = []
    total_frames = self.wf.getnframes()
    chunk_size = 4000
    with tqdm.tqdm(total=total_frames, unit="frames", desc="Recognizing") as pbar:
        frames_read = 0
        while True:
            data = self.wf.readframes(chunk_size)
            if len(data) == 0:
                break
            frames_read += chunk_size
            pbar.update(min(chunk_size, total_frames - pbar.n))
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