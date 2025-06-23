
import argparse
from .stt import STTParser

def get_cli_args():
  #  Define the args
  parser = argparse.ArgumentParser(description="A project uses a vosk model to parse speech to text")

  # Positional argument
  parser.add_argument("file", help="Directory for the audio file to be processed")
  
  # Optional flag
  parser.add_argument('-o', '--output', help="Directory for the output file, by default creates a text file with the same name as the file", default=None)

  # Parse the args and return them
  args = parser.parse_args()
  return args

def main():
  
  # Get the CLI Args
  args = get_cli_args()
  file = args.file
  output = args.output
  
  # Create the parser
  output_file = output if output else file.split('.')[0] + '.txt'
  parser = STTParser(output_file)
  
  # Run the parser
  parser.parse(file)
  