# Python scripts for SW-Lab <img src="https://github.com/smy1/swlab/blob/main/script/swlogo.jpg" width=auto height="27"> <img src="https://github.com/smy1/swlab/blob/main/script/logo_python.png" width=auto height="27">
The previous scripts have now been compiled into a module called [editvid.py](./editvid.py). This module should be downloaded and stored in the same folder as where we will be running our code. Briefly, the functions in this module edit videos in bulk, allowing the video-editing task to be automatised. Needless to say, the videos and folders (in which the videos are stored) should be named in a consistent manner for the batch processing task to be run smoothly and successfully. The [examples.py](./examples.py) script shows how and when to call for various video-editing functions of the module. These examples are explained in detail [below](#examples).

- [General requirements](#general-requirements)
- [Example 1: Merge videos](#1-merge-videos)
- [Example 2: Sync and overlay videos](#2-overlay-videos)
- [Example 3: Crop videos](#3-crop-videos)
- [Example 4: Sync and juxtapose videos](#4-juxtapose-videos)
- [Helpful resources](#helpful-resources)

## General requirements
In order to run the functions in this module, Python and the relevant packages need to be installed. I wrote these codes in Python 3.12.4.
Installation can be done in the command prompt (for Windows users, type "command prompt" or "cmd" in the search box):
```
python --version ## check python version
pip install --upgrade pip setuptools wheel ## check whether pip is installed
pip show <package name> ## check whether a particular package (and what version) has been install 
pip install openpyxl ## required if we want python to extract information from an excel file
pip install opencv-python ## required for resizing videos if using MoviePy v1.0
pip install DateTime ## required when syncing the timing of two videos
pip install pathlib ## required for Python to locate a path of a file
```
>[!NOTE]
>When I first started writing these video-editing scripts, I used [MoviePy v1.0.3](https://zulko.github.io/moviepy/v1.0.3/). As of 2025, [MoviePy v2.0](https://zulko.github.io/moviepy/) has been released. See [here](https://zulko.github.io/moviepy/getting_started/updating_to_v2.html) for details about the differences. The code below allows you to install either the earlier or the latest version.
>```
>pip install moviepy==1.0.3 ## this installs the older version
>pip install moviepy ## this installs the latest version
>```

## Examples
### 1. Merge videos
The following code calls for the __merge function__ to concatenate several videos into one long video. 
```
from editvid import merge
merge(folder="C:/Users/user/Desktop/mc_vid", 
      children=["a62_c62", "a63_c63", "a64_c64"], 
      camera=["BABY", "front", "SBR1", "SCREEN", "影片二"])
```
As shown in the code above, the merge function has three parameters:
- __folder__: Where is the main project folder that stores all the videos? In this example, the main project folder is called "mc_vid", stored in the desktop by a user named "user".
- __children__: What are the names of the first-level subfolders? These subfolders are stored within main project folder and are presumably named after the participants' ID (in this example, "a62_c62", "a63_c63", and "a64_c64"). By listing all the subfolders here, the merge function will loop through them one by one.
- __camera__: What are the names of the second-level subfolders? These subfolders are stored within the first-level child subfolders. These second-level subfolders should be the name of the cameras/video recorders. Within these camera subfolders should be all the short, truncated videos that we want to concatenate into one complete long video.
>[!TIP]
>If a camera subfolder does not exist within one or more of the child subfolders, the function will just return a statement that there is nothing to merge for that child's camera. This means that we can list all the possible camera subfolders even if these subfolders exist only in some of the child subfolders but not in other child subfolders. 

> [!IMPORTANT]  
> Even if there is only one first-level "children" subfolder, the argument must be given within a square bracket [ ] so that Python treats it like a list, otherwise, the function will return an error. This is true for all other parameters in which the function is supposed to loop through, like the second-level "camera" subfolder in this example or the start time information in Example 2 below.

An additional merging script that is not included in the module: 
   - [merge-clips.py](./merge-clips.py): This script concatenates short videos which are stored in third-level subfolders, that is, within the second-level camera subfolders. The third-level subfolders indicate the minute of the recording, e.g., a folder named "09" contains several three-second-long clips recorded at the 9th minute of the hour of experiment.

---

### 2. Overlay videos
__(2A)__ The following code calls for the __overlay function__ to overlay one video on top of another. Here, we provide an Excel file (see a sample [here](./example_overlay.xlsx)) for the function to extract information regarding subfolder names and video timing. 
```
from editvid import overlay
overlay(folder = "C:/Users/user/Desktop/mc_vid", 
        attempts = 1, 
        bgcam = "baby", 
        topcam = "screen",
        newname = "OMI", 
        propsize = 0.25, 
        dur = None,
        excel = "C:/Users/user/Desktop/mc_vid/example_overlay.xlsx",
        children=None, start=None, end=None, corr=None) 
```
As shown in the code above, the overlay function has many parameters, one of which requires us to have an Excel file ready.
- __folder__: Where is the main project folder that stores all the videos? In this example, the main project folder is called "mc_vid", which is stored in the desktop by a user named "user".
- __attempts__: Is this the first attempt to sync and overlay videos? If yes, enter 1, and the function will ignore the argument given to the parameter "corr" (stands for "correction", see below). If the number entered here is 2 or larger, we need to provide the correction argument, otherwise, the function will return an error.
- __bgcam__: Stands for "background-camera". What is the name of the video recording that will be used as the "base" of the new composite video? In this example, Python will search for a video file that has the word "baby" in the name and use it as the base video. These base videos should be stored in their respective first-level subfolders with each subfolder indicating an individual participant. The names of subfolders can either be provided in the first column of the Excel file (see below for details) or manually given to the parameter "children" (see Example 2B below).
- __topcam__: Stands for "top-camera". What is the name of the video recording that will be overlaid on top of the base video? In this example, Python will search for a video file that has the word "screen" in the name and overlay it on top of the base video to create a new composite video. As with the base videos, these top videos should be stored in their respective subfolders.
- __newname__: How should Python name the new composite video? In this example, Python will name the new composite video as "OMI" (which stands for "omission task").
- __propsize__: Stands for "proportion-size". How small should be top video be? In this example, 0.25 means 25% of its original size.
- __dur__: Stands for "duration". If the recorded task has a standard length (e.g., 3 mintues), enter the duration here in seconds (i.e., 180). If the duration of the recorded task differs between participants, leave it as "None". 
- __excel__: What is the path and name of the Excel file that contains information regarding subfolder names and video timing? Leave this as "None" if we want to enter this information manually (see Example 2B below).
- the other parameters: Leave them as "None" since the information should be found in the Excel file.

In the __excel file__, we should have four columns, the first row being the names of these columns: "children", "start", "end", and "corr" (see Image 1 below). These columns are essentially the last few parameters of this function. While these names can be changed to something else that is more intuitive (or even written in another language), the information _must_ be in entered in this order. 

<img src="https://github.com/smy1/swlab/blob/main/script/py_eg_xl_overlay.png" width=auto height="280">

__Image 1__: _An example of an Excel file for the overlay function._  

In Image 1 above: 
- The _first column_ (named as "children" in this example) must contain the name of the first-level subfolders in which the base video and top video are stored. The name of the subfolders is usually the participants' ID, hence, I sometimes call these subfolders "child subfolders". In this example, the subfolders are "076" and "078".
- The _second column_ (named as "start" in this example) contains the time at which the task started (in seconds) in the video recording of each of the particpant. Since we have two video recordings (the base video and the top video), use the start time of one of these videos (preferably the top video). The function will calculate the time difference between the two recordings and adjust the start time of the other video. This adjustment is not always perfect, hence, we will have to correct for any discrepancy using the column "corr" (see below).
- The _third column_ (named as "end" in this example) contains the time at which the recording ended (again, in seconds). This can be left blank if the duration of the task is always the same for everyone (see the parameter "dur" above).
- The _fourth column_ (named as "corr" in this example, which stands for "correction") contains information that corrects for out-of-sync videos. This information can be left blank (and will be disregarded even if it is not blank) if the paramter "attempts" gets an argument of 1 (because logically, in the first attempt, we do not know how well Python syncs the two videos).
- To reiterate: the first row of these columns could have been entered as "subfolder_name", "begin_time", "end_time", and "correct_timing_difference" or anything else that makes more sense. 

> [!IMPORTANT]  
> The information entered in __the first column of the Excel file (i.e., the names of the first-level subfolders) must be a string__ (in Python terms), as shown in Image 1 above (Notice the tiny green triangle in the top left corner of each cell). To force Excel to accept numbers as strings, add an inverted comma before the number. This is very important, otherwise, Python might not be able to match the information in the Excel file with the subfolder names.

---

__(2B)__ The following code calls for the __overlay function__ exactly as shown in Example 2A above. The difference is that here, we manually enter information regarding subfolder names and video timing. 
```
from editvid import overlay
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
As should be obvious, the code above enters "None" for the parameter "excel". Instead, the information saved in the Excel file (shown earlier) is now passed as arguments to the parameters "children", "start", "end", and "corr", respectively. 
>[!TIP]
>Manual input of information is alright when we have less than five child subfolders. When the number of subfolders is huge, it becomes difficult to keep track of which timing information refers to which subfolder because these variables are not visually aligned (I'm telling from experience). In such a case, I highly recommend using an Excel file.

---

### 3. Crop videos
The following code calls for the __crop function__ to crop a video. As with Example 2 on overlaying videos, this can be done either with an Excel file or by manually entering the information. Here, I only show how the code works with an Excel file (a sample file can be found [here](./example_crop.xlsx)).
```
from editvid import crop
crop(folder = "C:/Users/user/Desktop/mc_vid",
     cam = "front",
     newname = "solo",
     dur = 183,
     amplify = 5, 
     excel = "C:/Users/user/Desktop/mc_vid/example_crop.xlsx",
     children=None, start=None, end=None, x1=None, x2=None, y1=None, y2=None)
```
In the crop function shown above, we need to give four arguments and have an Excel file ready.
- __cam__: Stands for "camera". What is the name of the video recording that needs to be cropped? In this example, Python will search for a video file that has the word "front" in the name. These videos should be stored in their respective first-level subfolders with each subfolder indicating an individual participant. The names of subfolders can either be provided in the first column of the Excel file (see below for details) or manually given to the parameter "children" (see Example 2B above for details).
- __newname__: How should Python name the new cropped video? In this example, Python will name the new cropped video as "solo" (the name of the recorded control task).
- __dur__: Stands for "duration". If the recorded task has a standard length (e.g., 3 mintues), enter the duration here in seconds (i.e., 180). If the duration of the recorded task differs between participants, leave it as "None". 
- __amplify__: How much do we want to amplify the volume of the video? The higher the number we enter here, the louder the video would be. Needless to say, an argument of 0 means that the video will be muted.
- __excel__: What is the path and name of the Excel file that contains information regarding subfolder names, video timing, and cropping details? Leave this as "None" if we want to enter this information manually.

In the __excel file__, we should have seven columns that correspond to the last few parameters of this function (i.e., "children", "start", "end", "x1", "x2", "y1", and "y2"). While these names can be changed to something else that is more intuitive (or even written in another language), the information _must_ be in entered in this order. 

<img src="https://github.com/smy1/swlab/blob/main/script/py_eg_xl_crop.png" width=auto height="280">

__Image 2__: _An example of an Excel file for the crop function._

---

### 4. Juxtapose videos
Coming soon.  
Once we have single, merged videos from each camera, we can sync and juxtapose these videos so that we see the recordings of participants from different angles. 
   - [sbr-sync-3videos.py](./sbr-sync-3videos.py) This script displays one video on the left and two (downsized) videos on the right (one on top and the other at the bottom) so that we capture parents' shared reading behaviour from three different angles. (_Note_: _SBR_ stands for shared book reading)
   - [sbr-sound.py](./sbr-sound.py) This script just replaces the audio of the juxtaposed video with another audio file (that hopefully has better quality). To sync the timing of the two audio files, I use Audacity. See [here](https://github.com/smy1/swlab/blob/main/script/audacity-sync-audio.pdf) for the instructions.

---

## Helpful resources
I relied heavily on the links below when writing these codes. Note: These links use MoviePy v1.0. 
- how to [loop multiple videos in a folder](https://stackoverflow.com/a/75788036)
- how to [concatenate multiple videos](https://www.geeksforgeeks.org/moviepy-concatenating-multiple-video-files/)
- how to [calculate time difference](https://www.geeksforgeeks.org/calculate-time-difference-in-python/)
- how to [crop a video](https://stackoverflow.com/a/74586686)
- how to [rename files](https://pynative.com/python-rename-file/)
