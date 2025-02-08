# swlab
This repo contains codes that I wrote to automatise some tasks for projects that I lead as a postdoc in SW-Lab. The repo and readme are still under construction and will be constantly updated. 

_Last update: 07.02.2025_

## List of scripts
1. Python: [Merging videos](#1-merging-videos)
2. Python: [Syncing videos](#2-syncing-videos)
3. Jupyter: [Transcribe audio files](#3-transcribing-audio-files)
4. MATLAB: [Toggle stimuli in snirf](#matlab-script)

---

## Python scripts
See [general requirements](#general-requirements) and [helpful resources](#helpful-resources) below.
### 1. Merging videos
In our projects, we often video-record children (and their parents) during the experiment. Before we code their behaviour, we have to process the videos (e.g., concatenate, synchronise, etc) because our video cameras store these recrdings as short clips. 
   - [merge-videos.py](https://github.com/smy1/swlab/blob/main/peekaboo/merge-videos.py) This script concatenates short videos in each camera folder into a long complete video.
   - [merge-clips.py](https://github.com/smy1/swlab/blob/main/peekaboo/merge-clips.py) This script concatenates short videos which are stored in sub-folders of the camera folder. The sub-folders indicate the minute of the recording, e.g., a folder named "09" contains several three-second-long clips recorded at the 9th minute of the hour of experiment. 

### 2. Syncing videos
Once we have single, merged videos from each camera, we can sync and juxtapose these videos so that we see the recordings of every participant from different angles. 
   - [omi-sync-videos.py](https://github.com/smy1/swlab/blob/main/peekaboo/omi-sync-videos.py) This script downsizes the "screen" video to 25%, then overlays it on the "baby" video at the top left corner. This way, we can see the child's face clearly (to code where they are looking) as well as what is presented on the screen. (_Note_: _Omi_ stands for omission task)
   - [sbr-sync-3videos.py](https://github.com/smy1/swlab/blob/main/peekaboo/sbr-sync-3videos.py) This script displays one video on the left and two (downsized) videos on the right (one on top and the other at the bottom) so that we capture parents' shared reading behaviour from three different angles. (_Note_: _SBR_ stands for shared book reading)
   - [sbr-sync-2videos.py](https://github.com/smy1/swlab/blob/main/peekaboo/sbr-sync-2videos.py) This script is a 2-video version of the _sbr-sync-3videos_ script (because sometimes the third camera failed to record).
   - [solo-sbr-video.py](https://github.com/smy1/swlab/blob/main/mochi/solo-sbr-video.py) This script adds an additional chunk of codes to the _sbr-sync-2videos_ script to crop one of the videos. It renders two videos: one for each reading condition. (_Note_: _solo_ stands for solo-reading condition)

>[!NOTE]
>When syncing the videos, I relied on the name of the videos, which contains the minute and second at which the video recording was taken. In some cases, there could be a video recording that started at the 59th minute (e.g., 09:59am) and the other recordings that started in the next hour (e.g., 10:00am, 10:01am, etc). For now, we have to manually change the "00" in the file name to "60" so that the "59" recording is placed before the "00" recording. I might improvise the code to deal with this problem in the future.

### 3. Transcribing audio files
The [script](https://github.com/smy1/swlab/blob/main/peekaboo/audio2xlsx.ipynb) transcribes an audio file using Whisper from OpenAI (This part of the code was not written by me - my lab manager, Yingyu Chen, found it online), then exports the transcript into an excel file.

### General requirements
In order to run the python scripts, Python and the relevant modules need to be installed. The codes were written in Python 3.12.4.
Installation can be done in the command prompt (for Windows users, type "command prompt" in the search box):
```
python --version ## check python version
pip install --upgrade pip setuptools wheel ## check whether pip is installed, then use it to install the necessary modules
pip install moviepy ## this installs the latest version
pip install opencv-python ## https://pypi.org/project/opencv-python/
pip show moviepy ## check the package version
```
>[!NOTE]
>The video-editing python scripts use _moviepy v1.0.3_. As of 2025, _moviepy v2.0_ has been released. See [here](https://zulko.github.io/moviepy/getting_started/updating_to_v2.html) for details about the updates. To install an earlier version of moviepy, use the code below.
>```
>pip install moviepy==1.0.3 ## this installs the older version
>```

### Helpful resources
I relied heavily on the links below when writing these codes. Except for the main page of moviepy, the other links explain how to use moviepy v1.0.
- the main page of [moviepy](https://zulko.github.io/moviepy/)
- how to [loop multiple videos in a folder](https://stackoverflow.com/a/75788036)
- how to [concatenate multiple videos](https://www.geeksforgeeks.org/moviepy-concatenating-multiple-video-files/)
- how to [calculate time difference](https://www.geeksforgeeks.org/calculate-time-difference-in-python/)
- how to [crop a video](https://stackoverflow.com/a/74586686)

---

## MATLAB script
There is also a MATLAB script (I didn't write this from scratch, see below for details) which toggles off rejected stimuli in .snirf files to be further processed in Homer3. 
If the child was not looking at the screen for a particular trial (coded from the merged videos mentioned above), the trial (i.e., the stimulus in .snirf files) will be removed from future analysis.
   - [remove_stim.m](https://github.com/smy1/swlab/blob/main/peekaboo/remove_stim.m) This script rejects stimuli in snirf data files based on an excel file. The script was originally written by Chi-Chuan Chen to toggle off stimuli. However, her script is for .nirs files, which works slightly differently from .snirf files. Furthermore, her input for gaze data was a .mat file and I prefer loading the raw excel file instead.

### General requirements
- Download and install MATLAB (you'll need an institution account). Online tutorials suggest that Homer3 is only compatible with MATLAB R2017b.
- Download and add Homer3 to the MATLAB path. Link [here](https://github.com/BUNPC/Homer3/wiki/Download-and-Installation)

### Helpful resources
- Introduction to MATLAB: [youtube link](https://www.youtube.com/watch?v=MYRkBoojh_Y&list=PLx_IWc-RN82tw_J9nYqIc0tjvaMjowRVi&pp=iAQB)
- SNIRF: [documentation](https://github.com/fNIRS/snirf/blob/master/snirf_specification.md)
- Homer3: [documentation](https://github.com/BUNPC/Homer3/wiki/), video tutorials by [NIRx](https://www.youtube.com/watch?v=I_eH0_ed8I4),
  [Prof. CF Lu](https://www.youtube.com/watch?v=bHhn2vBXF0Y) (slides in English, explanation in Mandarin)
