# swlab
This repo contains codes (mostly Python) that I wrote to automatise some video-editing tasks for various projects that I lead as a postdoc in SW-Lab. The repo and this readme are still under construction and will be constantly updated. _Last update: 07.02.2025_

## List of Python scripts
1. [Merging videos](#1-merging-videos)
2. [Syncing videos](#2-syncing-videos)

### Very helpful resources
I relied heavily on the links below when writing these codes. You might also find them useful in some ways:
- the main page of [moviepy](https://zulko.github.io/moviepy/)
- how to [loop multiple videos in a folder](https://stackoverflow.com/a/75788036)
- how to [concatenate multiple videos](https://www.geeksforgeeks.org/moviepy-concatenating-multiple-video-files/)
- how to [calculate time difference](https://www.geeksforgeeks.org/calculate-time-difference-in-python/)
- how to [crop a video](https://stackoverflow.com/a/74586686)

### General requirements
In order to run the python scripts, you will need to install Python and the relevant modules. The codes were written in Python 3.12.4.
Installation can be done in the command prompt (for Windows users, type "command prompt" in the search box):
```
python --version ## check python version
pip install --upgrade pip setuptools wheel ## check whether pip is installed, then use it to install the necessary modules
pip install moviepy ## this installs the latest version
pip install opencv-python ## https://pypi.org/project/opencv-python/
pip show moviepy ## check the package version
```
>[!NOTE]
>The following python scripts were written using _moviepy v1.0.3_. As of 2025, moviepy v2.x has been released. See [here](https://zulko.github.io/moviepy/getting_started/updating_to_v2.html) for more. To install an earlier version, use the code below.
>```
>pip install moviepy==1.0.3 ## this installs the older version
>```

When syncing the videos, I relied on the name of the videos, which contains the minute and second at which the video recording was taken. In some special
cases, there could be a video recording that started at the 59th minute (e.g., 09:58am) and the other recordings that started in the next hour (e.g., 
10:00am, 10:01am, etc). We will have to manually change the "00" in the file name to 60 so that the "59" recording is placed before the "00" recording. 
I might improvise the code to deal with this problem in the future.

### 1. Merging videos
In our projects, we often video-record children (and their parents) during the experiment. Before we can code their behaviour, we have to process the videos (e.g., concatenate, synchronise, etc) because our video-recorder stores these videos as short clips. 
   - [merge-videos.py](https://github.com/smy1/swlab/blob/main/peekaboo/merge-videos.py) This script concatenates short videos in each camera folder into a long complete video.
   - [merge-clips.py](https://github.com/smy1/swlab/blob/main/peekaboo/merge-clips.py) This script concatenates short videos which are stored in sub-folders of the camera folder. The sub-folders indicate the minute of the recording, e.g., a folder named "09" contains several three-second-long clips recorded at the 9th minute of the hour of experiment. 

### 2. Syncing videos
Once we have single, merged videos from each camera, we can sync and juxtapose these videos for every participant so that we see the recordings from different angles. 
   - [omi-sync-videos.py](https://github.com/smy1/swlab/blob/main/peekaboo/omi-sync-videos.py) This script downsizes the screen video to 25%, then overlay it on the baby video at the top left corner. This way, we can see the child's face clearly (and where they are looking) as well as what is presented on the screen.
   - [sbr-sync-3videos.py](https://github.com/smy1/swlab/blob/main/peekaboo/sbr-sync-3videos.py) This script displays one video on the left and two (downsized) videos on the right (one on top and the other on the bottom) so that we capture parents' shared reading practice from all angles.
   - [sbr-sync-2videos.py](https://github.com/smy1/swlab/blob/main/peekaboo/sbr-sync-2videos.py) This scripts is a 2-video version of the _sbr-sync-3videos_ script (because sometimes the third camera failed to start recording).
   - [solo-sbr-video.py](https://github.com/smy1/swlab/blob/main/mochi/solo-sbr-video.py) This script crops and extracts the front video for both solo and SBR conditions, then extract the side video to be displayed beside the front video for the SBR condition. In short, it adds an additional chunk of codes (i.e., cropping) to the _sbr-sync-2videos_ script. Two videos will be rendered: the front video for the solo condition and a juxtaposed front-side video for the SBR condition.

---

## MATLAB script
There is also a MATLAB script (I didn't write this from scratch, see below for details) which toggles off rejected stimuli in .snirf files to be further processed in Homer3. 
If the child was not looking at the screen for a particular trial (coded from the merged videos mentioned above), the trial (i.e., the stimulus in .snirf files) will be removed from future analysis.
   - [remove_stim.m](#remove_stimm)

### General requirements
- Download and install MATLAB (you'll need an institution account). Online tutorials suggest that Homer3 is only compatible with MATLAB R2017b.
- Download and add Homer3 to the MATLAB path. Link [here](https://github.com/BUNPC/Homer3/wiki/Download-and-Installation)

### Very helpful resources
- Introduction to MATLAB: [youtube link](https://www.youtube.com/watch?v=MYRkBoojh_Y&list=PLx_IWc-RN82tw_J9nYqIc0tjvaMjowRVi&pp=iAQB)
- SNIRF: [documentation](https://github.com/fNIRS/snirf/blob/master/snirf_specification.md)
- Homer3: [documentation](https://github.com/BUNPC/Homer3/wiki/), video tutorials by [NIRx](https://www.youtube.com/watch?v=I_eH0_ed8I4),
  [Prof. CF Lu](https://www.youtube.com/watch?v=bHhn2vBXF0Y) (slides in English, explanation in Mandarin)

### remove_stim.m
- **What [the script](https://github.com/smy1/swlab/blob/main/peekaboo/remove_stim.m) does**: Reject stimuli in snirf data files based on an excel file
- **Why I wrote it**: The script was originally written by Chi-Chuan Chen to toggle off stimuli. However, her script is for .nirs files, which works slightly differently from .snirf files. Furthermore, 
  her input for gaze data was a .mat file and I prefer loading the raw excel file instead.
