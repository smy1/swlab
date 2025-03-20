# swlab <img src="./misc/swlogo.jpg" width=auto height="27">
This repo contains codes that I wrote to automatise some tasks for projects that I lead as a postdoc in [SW-Lab](https://www.facebook.com/p/%E5%AC%B0%E5%B9%BC%E5%85%92%E5%A4%A7%E8%85%A6%E7%99%BC%E5%B1%95%E8%88%87%E5%AD%B8%E7%BF%92%E5%AF%A6%E9%A9%97%E5%AE%A4-100093631808042) (09.2023 - current). 

_Last update: 20.03.2025_

## List of scripts
1. Python: [Edit videos](https://github.com/smy1/swlab/blob/main/python/)
2. Jupyter: [Transcribe audio files](#jupyter-notebook)
3. MATLAB: [Prepare data before preprocessing](https://github.com/smy1/swlab/blob/main/matlab/)

---

## Jupyter notebook
- [audio2xlsx.ipynb](https://github.com/smy1/swlab/blob/main/script/audio2xlsx.ipynb) This notebook transcribes an audio file using Whisper from OpenAI (_Note_: This part of the code was not written by me - my lab manager, Yingyu Chen, found it online), then exports the transcript into an excel file using Python.

---

## MATLAB script
   - [remove_stim.m](https://github.com/smy1/swlab/blob/main/script/remove_stim.m) This script rejects stimuli in snirf data files based on gaze data stored as an excel file (e.g., whether the child was looking at the screen). (_Note_: I didn't write this from scratch) The script was originally written by Chi-Chuan Chen to toggle off stimuli. However, her script is for .nirs files, which works slightly differently from .snirf files. Furthermore, her script requires a .mat file for gaze data and I prefer loading the raw excel file instead.

### General requirements
- Download and install MATLAB (probably with an institution account). According to online tutorials, Homer3 is only compatible with MATLAB R2017b.
- Download and add [Homer3](https://github.com/BUNPC/Homer3/wiki/Download-and-Installation) to the MATLAB path.

### Helpful resources
- Introduction to MATLAB: [youtube link](https://www.youtube.com/watch?v=MYRkBoojh_Y&list=PLx_IWc-RN82tw_J9nYqIc0tjvaMjowRVi&pp=iAQB)
- SNIRF: [documentation](https://github.com/fNIRS/snirf/blob/master/snirf_specification.md)
- Homer3: [documentation](https://github.com/BUNPC/Homer3/wiki/), video tutorials by [NIRx](https://www.youtube.com/watch?v=I_eH0_ed8I4),
  [Prof. CF Lu](https://www.youtube.com/watch?v=bHhn2vBXF0Y) (slides in English, explanation in Mandarin)
