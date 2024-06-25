# swlab
This repo contains codes (mostly Python) that I wrote for various projects that I lead as a postdoc in SW-Lab. The codes are stored in their respective 
project folders.  
As of 24.06.2024 (long count: 13.0.11.12.3, 8 Aq'ab'al), the repo only has one project folder, "Peekaboo". The repo and this readme are still under 
construction and will be constantly updated.

## List of codes within each project folder
1. Peekaboo
   - [merge-videos.py](#merge-videospy)
   - [merge-clips.py](#merge-clipspy)
   - [omi-sync-videos.py](#omi-sync-videospy)
   - [sbr-sync-3videos.py](#sbr-sync-3videospy)
   - [sbr-sync-2videos.py](#sbr-sync-2videospy)

## 1. Peekaboo
In this project, we examine whether interactive shared reading, also known as dialogic reading, is positively linked to children's productive vocabulary
size, and whether this relationship is mediated by children's predictive brain signal as measured using fNIRS. This project is a follow-up study of this
[paper](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0272438). As we video recorded children during the experiment, we have to 
process the videos (e.g., concatenate, synchronise, etc) before we can code the videos. The python scripts uploaded to this project folder allows us to automatise 
the task of processing videos.

### General requirements
In order to run the python scripts, you will need to install Python and the relevant modules. The codes were written in Python 3.12.4.
Installation can be done in the command prompt (for Windows users, type "command prompt" in the search box):
```
python --version ##check python version
pip install --upgrade pip setuptools wheel ## check whether pip is installed, then use it to install the necessary modules
pip install moviepy ## https://zulko.github.io/moviepy/install.html
pip install opencv-python ## https://pypi.org/project/opencv-python/
```

When syncing the videos, I relied on the name of the videos, which contains the minute and second at which the video recording was taken. In some special
cases, there could be a video recording that started at the 59th minute (e.g., 09:58am) and the other recordings that started in the next hour (e.g., 
10:00am, 10:01am, etc). We will have to manually change the "00" in the file name to 60 so that the "59" recording is placed before the "00" recording. 
I might improvise the code to deal with this problem in the future.

### Very helpful resources
I relied heavily on the links below when writing these codes. You might also find them useful in some ways:
- how to [overlay videos, etc](https://zulko.github.io/moviepy/getting_started/compositing.html)
- how to [loop multiple videos in a folder](https://stackoverflow.com/a/75788036)
- how to [concatenate multiple videos](https://www.geeksforgeeks.org/moviepy-concatenating-multiple-video-files/)
- how to [calculate time difference](https://www.geeksforgeeks.org/calculate-time-difference-in-python/)

### merge-videos.py
- **What [the script](https://github.com/smy1/swlab/blob/main/peekaboo/merge-videos.py) does**: Concatenate short videos in each camera folder into a long complete video.
- **Why I wrote it**: The cameras that we are currently using to video record our test sessions store the recorded videos in short clips of one minute
  duration each. Hence, we need to combine these short videos into one complete and coherent video for each participant.

### merge-clips.py
- **What [the script](https://github.com/smy1/swlab/blob/main/peekaboo/merge-clips.py) does**: Concatenate short videos in sub-folders which are stored in a camera folder into a long complete video
- **Why I wrote it**: The same reason as why I wrote _merge-videos.py_. We need a slightly different script because there is a camera that stores the recorded
  videos in short clips of three seconds each. These super short video clips are stored in folders that indicate the minute of the recording, e.g., a
  folder named "09" contains several three-second-long clips recorded at the 9th minute of the hour of experiment while another folder named "10" contains
  several three-second-long clips recorded at the 10th minute of the hour of experiment. Hence, we need to first combine the super short clips in each
  "minute" folder before combining them into one complete and coherent video for each participant.

### omi-sync-videos.py
- **What [the script](https://github.com/smy1/swlab/blob/main/peekaboo/omi-sync-videos.py) does**: Downsize the screen video to 25%, then overlay (and sync) it on the baby video at the top left corner
- **Why I wrote it**: We need to code infants' gaze per trial to determine for each trial whether the infants were looking at the screen.

### sbr-sync-3videos.py
- **What [the script](https://github.com/smy1/swlab/blob/main/peekaboo/sbr-sync-3videos.py) does**: Synchronise and display the main SBR (shared book reading) video on the left and two (downsized) minor SBR videos on the right (one on top and the other on the bottom)
- **Why I wrote it**: We need to code parent-child interaction during SBR. We have three cameras positions at different locations of the lab to capture different
  angles of the parent-child dyads (so that they are free to move around, change position, etc. while we still manage to record their interaction without physically
  moving the camera).
  
### sbr-sync-2videos.py
- **What [the script](https://github.com/smy1/swlab/blob/main/peekaboo/sbr-sync-2videos.py) does**: Synchronise and display the main SBR (shared book reading) video on the left and the (downsized) minor SBR video on the right
- **Why I wrote it**: The same reason as why I wrote _sbr-sync-3videos.py_. The difference is that this script syncs only two of our three cameras. Sometimes,
  one of the cameras failed to record the reading session or is problematic, hence, it has to be excluded from the final joined video.
