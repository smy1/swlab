# Jupyter notebook
[audio2xlsx.ipynb](./audio2xlsx.ipynb) 
- This notebook transcribes an audio file using Whisper from OpenAI ([GitHub page here](https://github.com/openai/whisper/tree/main?tab=readme-ov-file)),
- extracts the time of each utterance from .srt,
- then exports the transcript into an excel file using Python.

To convert the excel file into a csv file with UTF-8 encoding, simply use [this script](./convert_xl_csv_utf8.py).
