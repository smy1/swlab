# Python scripts for SW-Lab <img src="https://github.com/smy1/swlab/blob/main/script/swlogo.jpg" width=auto height="27"> <img src="https://github.com/smy1/swlab/blob/main/script/logo_python.png" width=auto height="27">
- [general requirements](#general-requirements)
- [merge videos](#1-merge-videos)
- [sync videos](#2-sync-videos)
- [helpful resources](#helpful-resources)

## General requirements
In order to run these python scripts, Python and the relevant modules need to be installed. I wrote these codes in Python 3.12.4.
Installation can be done in the command prompt (for Windows users, type "command prompt" in the search box):
```
python --version ## check python version
pip install --upgrade pip setuptools wheel ## check whether pip is installed, then use it to install the necessary modules
pip install moviepy ## this installs the latest version
pip show moviepy ## check the package version
pip install opencv-python ## required for resizing videos if using MoviePy v1.0 https://pypi.org/project/opencv-python/
pip install playsound==1.2.2 ## not necessary, only for notification when video rendering is done
```
>[!NOTE]
>While writing these video-editing scripts, I used [MoviePy v1.0.3](https://zulko.github.io/moviepy/v1.0.3/). As of 2025, [MoviePy v2.0](https://zulko.github.io/moviepy/) has been released. See [here](https://zulko.github.io/moviepy/getting_started/updating_to_v2.html) for details about the differences. To install an earlier version of MoviePy, use the code below.
>```
>pip install moviepy==1.0.3 ## this installs the older version
>```

## 1. Merge videos
In our projects, we often video-record children (and their parents) during the experiment. Before we code their behaviour, we have to edit the videos (e.g., concatenate, synchronise, etc) because our video cameras store these recordings as short clips. 
   - [merge-videos.py](./merge-videos.py) This script concatenates short videos of each video camera into a complete video.
   - [merge-clips.py](./merge-clips.py) This script concatenates short videos which are stored in sub-folders of the video camera. The sub-folders indicate the minute of the recording, e.g., a folder named "09" contains several three-second-long clips recorded at the 9th minute of the hour of experiment.
   - [rename-merge-videos.py](./rename-merge-videos.py) This script adds a chunk of "check-and-rename" code to the _merge-videos_ script so that we rename the video files before merging them. This is necessary because when syncing the videos, I rely on the name of the videos, which contains the minute and second at which the video recording was taken. In some cases, the recording starts at the 59th minute (e.g., 09:59am) and then continues to the next hour (e.g., 10:00am, 10:01am, etc), which will mess up the sequence of the merging (because 00 will be placed before 59). In the _merge-videos_ script, we have to check and rename the files manually. With the check-and-rename chunk, Python will change the "00" in the file name to "60" so that the "59" recording is placed before the originally-named-as-"00" recording. 

## 2. Sync videos
Once we have single, merged videos from each camera, we can sync and juxtapose these videos so that we see the recordings of participants from different angles. 
   - [omi-sync-videos.py](./omi-sync-videos.py) This script downsizes the "screen" video to 25%, then overlays it on the "baby" video at the top left corner. This way, we can see the child's face clearly (to code where they are looking) as well as what is presented on the screen. (_Note_: _Omi_ stands for omission task)
   - [sbr-sync-3videos.py](./sbr-sync-3videos.py) This script displays one video on the left and two (downsized) videos on the right (one on top and the other at the bottom) so that we capture parents' shared reading behaviour from three different angles. (_Note_: _SBR_ stands for shared book reading)
   - [sbr-sync-2videos.py](./sbr-sync-2videos.py) This script is a 2-video version of the _sbr-sync-3videos_ script (because sometimes the third camera failed to record).
   - [crop-sync-2videos.py](./crop-sync-2videos.py) This script adds an additional chunk of code to the _sbr-sync-2videos_ script to crop one of the videos before syncing both of them. It also has an additional line to handle exceptions, which usually happen due to the actual video duration being shorter than the duration written in the script.
   - [sbr-sound.py](./sbr-sound.py) This script just replaces the audio of the juxtaposed video with another audio file (that hopefully has better quality). To sync the timing of the two audio files, I use Audacity. See [here](https://github.com/smy1/swlab/blob/main/script/audacity-sync-audio.pdf) for the instructions.

## Helpful resources
I relied heavily on the links below when writing these codes. Note: These links use MoviePy v1.0. 
- how to [loop multiple videos in a folder](https://stackoverflow.com/a/75788036)
- how to [concatenate multiple videos](https://www.geeksforgeeks.org/moviepy-concatenating-multiple-video-files/)
- how to [calculate time difference](https://www.geeksforgeeks.org/calculate-time-difference-in-python/)
- how to [crop a video](https://stackoverflow.com/a/74586686)
- how to [rename files](https://pynative.com/python-rename-file/)
