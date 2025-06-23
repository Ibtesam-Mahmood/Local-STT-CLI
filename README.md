# Local-STT-CLI

`v0.1.2`

Performs speech to text translatio using a local Vosk model.

## Prior to running

### Install Vosk Model

Before running [download the vosk-model-en-us-0.42-gigaspeech Model](https://alphacephei.com/vosk/models).

### (Optional) Install poetry

This project was created in [Poetry](https://python-poetry.org/) and you may use it to run the project.

### (Optional) Install ffmpeg

When using the `--convert` flag you must install [ffmpeg](https://ffmpeg.org/) on your system.

## Options

The cli application takes the following options and parameters when running `localstt`

| Argument      | Type       | Description                                                                                       | Required |
| ------------- | ---------- | ------------------------------------------------------------------------------------------------- | -------- |
| file          | Positional | Directory for the audio file to be processed                                                      | Yes      |
| -o, --output  | Optional   | Directory for the output file, by default creates a text file with the same name as the file      | No       |
| -m, --model   | Optional   | Directory for the vosk-model-en-us-0.42-gigaspeech model                                          | No       |
| -c, --convert | Optional   | Determines if the system shoudl convert the audio files to wav before proceeding. Requires ffmpeg | No       |

## Execution

### Running through Poetry

Place the `vosk-model-en-us-0.42-gigaspeech Model` inside the `src/local_stt/model` folder.

Run:

```sh
poetry install
poetry run localstt file_name -o output_file
```

## Installation

When you install this package locally you must move the model into the `local_stt/model/` folder (create this if it is not included) within the package insatllation directory.
Run `pip show local-stt` after insatlling to discover where this was insatlled. Then move the `vosk-model-en-us-0.42-gigaspeech Model` into the correct folder.

### Installing Locally

```sh
git clone https://github.com/Ibtesam-Mahmood/Local-STT-CLI.git
pip install .
localstt file_name -o output_file
```

### Insatlling with Git

```sh
pip install git+https://github.com/Ibtesam-Mahmood/Local-STT-CLI.git
```
