# Python scripts for SW-Lab <img src="https://github.com/smy1/swlab/blob/main/script/swlogo.jpg" width=auto height="27"> <img src="https://github.com/smy1/swlab/blob/main/script/logo_python.png" width=auto height="27">
The previous scripts have now been compiled into a function script called [editvid.py](./editvid.py). This function script should be downloaded and stored in the same folder as where we will be running our code. The [examples.py](./examples.py) script shows how and when to call for these functions. These examples are explained in detail [below](#examples).

- [General requirements](#general-requirements)
- [Example 1: Merge videos](#1-merge-videos)
- [Example 2: Sync and overlay videos](#2-overlay-videos)
- [Example 3: Crop videos](#3-crop-videos)
- [Example 4: Sync and juxtapose videos](#4-juxtapose-videos)
- [Helpful resources](#helpful-resources)

## General requirements
In order to run these python scripts, Python and the relevant modules need to be installed. I wrote these codes in Python 3.12.4.
Installation can be done in the command prompt (for Windows users, type "command prompt" in the search box):
```
python --version ## check python version
pip install --upgrade pip setuptools wheel ## check whether pip is installed, then use it to install the necessary modules
pip show <package name> ## check whether a particular package has been install and what version
pip install openpyxl ## required if we want python to extract information from an excel file
pip install opencv-python ## required for resizing videos if using MoviePy v1.0 https://pypi.org/project/opencv-python/
```
>[!NOTE]
>While writing these video-editing scripts, I used [MoviePy v1.0.3](https://zulko.github.io/moviepy/v1.0.3/). As of 2025, [MoviePy v2.0](https://zulko.github.io/moviepy/) has been released. See [here](https://zulko.github.io/moviepy/getting_started/updating_to_v2.html) for details about the differences. The code below allows you to install either the earlier or the latest version.
>```
>pip install moviepy==1.0.3 ## this installs the older version
>pip install moviepy ## this installs the latest version
>```

## Examples
### 1. Merge videos
To concatenate several videos into one long video, we use the following code.
```
from editvid import merge
merge(folder="C:/Users/user/Desktop/mc_vid", 
      children=["a62_c62", "a63_c63", "a64_c64"], 
      camera=["BABY", "front", "SBR1", "SCREEN", "影片二"])
```
In the merge function, we need to enter three information:
- **folder: Where is the main project folder that stores all the videos?** In this example, the main project folder is called "mc_vid", stored in the desktop by a user named "user".
- **children: What are the names of the first-level subfolders?** These subfolders are stored within main project folder and are presumably named after the participants' ID (in this example, "a62_c62", "a63_c63", and "a64_c64"). By listing all the subfolders here, the merge function will loop through them one by one.
- **camera: What are the names of the second-level subfolders?** These subfolders are stored within the first-level child subfolders. These second-level subfolders should be the name of the cameras/video recorders. Within these camera subfolders should be all the short, truncated videos that we want to concatenate into one complete long video.
>[!NOTE]
>If a camera subfolder does not exist within one or more of the child subfolders, the function will just return a statement that there is nothing to merge for that child's camera. This means that we can list all the possible camera subfolders even if these subfolders exist only in some of the child subfolders but not in other child subfolders. 

Additional merging script not included in the function: 
   - [merge-clips.py](./merge-clips.py): This script concatenates short videos which are stored in third-level subfolders of the second-level camera subfolders. The third-level subfolders indicate the minute of the recording, e.g., a folder named "09" contains several three-second-long clips recorded at the 9th minute of the hour of experiment.

### 2. Overlay videos
The following code extracts information from an excel file.
```
from editvid import overlay
overlay(folder = "C:/Users/user/Desktop/mc_vid", 
        attempts = 1, 
        bgcam = "baby", 
        topcam = "screen",
        newname = "OMI", 
        propsize = 0.25, 
        dur = None,
        excel = "C:/Users/user/Desktop/mc_vid/peekbaby.xlsx",
        children=None, start=None, end=None, corr=None) 
```
The following code enters information into the function.
```
overlay(folder = "C:/Users/user/Desktop/mc_vid", 
        attempts = 1, 
        bgcam = "baby", 
        topcam = "screen", 
        newname = "OMI", 
        propsize = 0.25, 
        dur = None,
        excel = None, 
        children = ["076", "078"],
        start = [20, 19], 
        end = [238, 609], 
        corr = [-1, 0.9]) 
```

### 3. Crop videos
Coming soon.

### 4. Juxtapose videos
Once we have single, merged videos from each camera, we can sync and juxtapose these videos so that we see the recordings of participants from different angles. 
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

Previously used but actually unnecessary modules:
- pip install playsound==1.2.2 ## not necessary, only for notification when video rendering is done
- [merge-videos.py](./obsolete/merge-videos.py): This script concatenates short videos of each video camera into a complete video.
- [rename-merge-videos.py](./obsolete/rename-merge-videos.py): This script adds a chunk of "check-and-rename" code to the _merge-videos_ script so that we rename the video files before merging them. This is necessary because when syncing the videos, I rely on the name of the videos, which contains the minute and second at which the video recording was taken. In some cases, the recording starts at the 59th minute (e.g., 09:59am) and then continues to the next hour (e.g., 10:00am, 10:01am, etc), which will mess up the sequence of the merging (because 00 will be placed before 59). In the _merge-videos_ script, we have to check and rename the files manually. With the check-and-rename chunk, Python will change the "00" in the file name to "60" so that the "59" recording is placed before the originally-named-as-"00" recording. 
- [omi-sync-videos.py](./obsolete/omi-sync-videos.py): This script downsizes the "screen" video to 25%, then overlays it on the "baby" video at the top left corner. This way, we can see the child's face clearly (to code where they are looking) as well as what is presented on the screen. (_Note_: _Omi_ stands for omission task)
