import argparse
from .stt import STTParser
from . import __version__

def get_cli_args():
  #  Define the args
  parser = argparse.ArgumentParser(description="A project uses a vosk model to parse speech to text from wav files")

  # Version flag
  parser.add_argument('-v', '--version', action='store_true', help="Print the version and exit.")

  # Positional argument
  parser.add_argument("file", nargs='?', help="Directory for the audio file to be processed")
  
  # Optional flag
  parser.add_argument('-o', '--output', help="Directory for the output file, by default creates a text file with the same name as the file", default=None)
  parser.add_argument('-m', '--model', help="Directory for the vosk-model-en-us-0.42-gigaspeech model", default=None)
  parser.add_argument('-c', '--convert', action='store_true', help="If set, perform conversion operation in addition to parsing.")

  # Parse the args and return them
  args = parser.parse_args()
  return args

def main():
  # Get the CLI Args
  args = get_cli_args()

  if getattr(args, 'version', False):
    print(f"local-stt v{__version__}")
    return

  file = args.file
  output = args.output
  model = args.model
  convert = args.convert
  
  # Create the parser
  output_file = output if output else file.split('.')[0] + '.txt'
  parser = STTParser(
    audio_file=file,
    output_file=output_file, 
    model_path=model, 
    convert=convert
  )
  
  # Run the parser
  print(f"Processing file: {file}")
  print(f"Output will be saved to: {output_file}")
  parser.parse()
  # poetry run localstt input\TestRecording.wav -o output\TestRecording.txt