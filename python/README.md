# Python scripts for SW-Lab <img src="https://github.com/smy1/swlab/blob/main/script/swlogo.jpg" width=auto height="27"> <img src="https://github.com/smy1/swlab/blob/main/script/logo_python.png" width=auto height="27">
Most of my previous scripts (see them [here](./obsolete/)) have now been compiled into a module called [editvid.py](./editvid.py). This module should be downloaded and stored in the same folder as where we will be running our code. Briefly, the functions in this module edit videos in bulk, allowing the video-editing task to be automatised. Arguments can be provided to the functions in two ways, either by loading an excel file or manually entering the arguments. The [examples.py](./examples.py) script explains how to manually pass arguments to these functions while the [examples below](#examples) explains how these arguments can be given through an excel file.

- [General requirements](#general-requirements)
- [__Example 1__](#1-merge-videos): Join videos together
- [__Example 2__](#2-overlay-videos): Sync and display a smaller video on top of a bigger one
- [__Example 3__](#3-crop-videos): Crop videos
- [__Example 4__](#4-juxtapose-videos): Sync and display videos beside each other
- [Helpful resources](#helpful-resources) (I wouldn't have been able to write these scripts without them)

---

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

### Important points
I run all my code in the terminal of [Kate](https://kate-editor.org/) (Windows PowerShell) instead of IDLE because somehow, my code doesn't run in the latter. I have never used other source code editors before, but there is no reason why my code won't run in other editors (such as [VS Code](https://code.visualstudio.com/)).  

__1. When manually providing arguments:__
> [!IMPORTANT]  
> For parameters that expects a list (this usually means any arguments that can be passed into the function by loading an excel file), even if there is only one item that Python needs to deal with, the argument must be given within square brackets (e.g., ["a62_c62"]) so that Python treats it like a list, otherwise, the function will return an error. 

>[!TIP]
>Manual input of information is alright when we have less than five child subfolders. When the number of subfolders is huge, it becomes difficult to keep track of which timing information refers to which subfolder because these variables are not visually aligned (I'm telling from experience). In such a case, I highly recommend using an Excel file.

__2. When passing arguments by loading an Excel file:__
> [!IMPORTANT]  
> The information entered in __the first column of the Excel file (i.e., the names of subfolders; see examples below) must be a string__ (in Python terms), as shown in Figure 1 of Example 2 below (notice the tiny green triangle in the top left corner of each cell). To force Excel to accept numbers as strings, add an inverted comma before the number. This is very important, otherwise, Python might not be able to match the information in the Excel file with the subfolder names.

__3. Before syncing videos:__
> [!IMPORTANT]
> In order for the functions to sync videos successfully, __the names of the videos must end with the time (in minutes and seconds) of the first frame__, for example, 56M09S (which means that the first frame of this video occured at the 56th minute and 9th second of some hour). If the second video's first frame occured at 56M00S, this means that it started recording 9 seconds before the first video, hence, the function will sync the two videos by cutting the first 9 seconds of the second video.

---

## Examples
### 1. Merge videos
The following code calls for the __merge function__ to concatenate several videos into one long video. 
```
from editvid import merge
merge(folder="C:/Users/user/Desktop/mc_vid", 
      children=["a62_c62", "a63_c63", "a64_c64"], 
      camera=["BABY", "front", "SBR1", "SCREEN", "影片二"])
```
In the code above:
- __folder__: Where is the main project folder that stores all the videos? In this example, the main project folder is called "mc_vid", stored in the desktop by a user named "user".
- __children__: What are the names of the first-level subfolders? These subfolders should be stored directly within the main project folder. In this example, the three subfolders listed refer to our participants' ID. 
- __camera__: What are the names of the second-level subfolders? These subfolders should be stored within the first-level  subfolders. In this example, these second-level subfolders are the names of the cameras/video recorders. Within these subfolders should be all the short, truncated videos that we want to concatenate into one complete long video.
- In short, the storage path of the short videos should be something in the line of _"main project folder" -> "first level (child) subfolder" -> "second level (camera) subfolder" -> "videos to be concatenated"_. By passing these subfolders into the function, all the videos in them will be processed automatically.

>[!TIP]
>If a subfolder or video does not exist, the function will just return a statement that there is nothing to merge for that child's camera. This means that we can list all the possible subfolders even if the combination of first and second level subfolders exist only for some but not other videos - it would not crash the function. 

---

### 2. Overlay videos
The following code calls for the __overlay function__ to overlay one video on top of another and create a composite video. 
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
In the code above:
- __folder__: Where is the main project folder that stores all the videos? In this example, the main project folder is called "mc_vid", which is stored in the desktop by a user named "user".
- __attempts__: Is this the first attempt to sync and overlay videos? If yes, enter 1, and the function will ignore the argument given to the parameter "corr" (see below). If the number entered here is 2 or larger, we need to provide this argument, otherwise, the function will return an error.
- __bgcam__: Stands for "background-camera". What is the name of the video recording that will be used as the "base" of the composite video? In this example, Python will search for a video file that has the word "baby" in the name and use it as the base video. These base videos should be stored in their respective subfolders. The names of these subfolders must be provided in the first column of the Excel file (see Figure 1 below).
- __topcam__: Stands for "top-camera". What is the name of the video recording that will be overlaid on top of the base video? In this example, Python will search for a video file that has the word "screen" in the name and overlay it on top of the base video to create a composite video. These top videos should be stored together with the base videos.
- __newname__: How should Python name the composite video? In this example, the composite video that is created will be called as "OMI" (which stands for "omission task").
- __propsize__: Stands for "proportion-size". How small should be top video be? In this example, 0.25 means 25% of its original size.
- __dur__: Stands for "duration". If the recorded task has a standard length (e.g., 3 mintues), enter the duration here in seconds (i.e., 180). If the duration of the recorded task differs between participants, leave it as "None". 
- __excel__: What is the path and name of the Excel file that contains information regarding subfolder names and video timing? In this example, the Excel file is stored in the main project folder. 
- __other parameters__: Leave them as "None" here since the arguments are found in the Excel file. See the [examples.py](./examples.py) script for how to manually pass arguments to these parameters.

In the __Excel file__ (see Figure 1 below), we should have four columns, the first row being the names of these columns: "children", "start", "end", and "corr". These columns are essentially the last few parameters of this function. While these names in the Excel file can be changed to something else that is more intuitive (or even in another language), the information _must_ be in entered in this order.  

<img src="https://github.com/smy1/swlab/blob/main/script/py_eg_xl_overlay.png" width=auto height="280">

__Figure 1__: _An example of an Excel file for the overlay function._  

In Figure 1 above: 
- __Column A__ (or the parameter __"children"__): Contains the name of the subfolders in which the base video and top video are stored. In this example, the subfolders "076" and "078" refer to our participants' ID.
- __Column B__ (or the parameter __"start"__): Contains the time at which the task started (in seconds) in the video recording of each of the particpant. _Since we have two video recordings (the base and the top video), use the start time of the top video._ The function will calculate the time difference between the two videos and adjust the start time of the base video. This adjustment is not always perfect, hence, we will have to correct for any discrepancy by providing information to the column "corr" (see below).
- __Column C__ (or the parameter __"end"__): Contains the time at which the task ended (again, in seconds). This can be left blank if the duration of the task is always the same for everyone (see the parameter "dur" above).
- __Column D__ (or the parameter __"corr"__, which stands for "correction"): Contains numbers (in seconds) to correct for out-of-sync videos. _If the base video is slower (i.e., lags behind the top video), give a positive number_. This information can be left blank (and will be disregarded even if it is not blank) if the parameter "attempts" gets an argument of 1 (because logically, in the first attempt, we do not know how well Python syncs the two videos). 

---

### 3. Crop videos
The following code calls for the __crop function__ to crop a video. 
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
In the code above:
- __cam__: Stands for "camera". What is the name of the video recording that needs to be cropped? In this example, Python will search for a video file that has the word "front" in the name. These videos should be stored in their respective subfolders. The names of these subfolders must be provided in the first column of the Excel file (see Figure 2 below).
- __newname__: How should Python name the new cropped video? In this example, Python will name the new cropped video as "solo" (the name of the recorded control task).
- __dur__: Stands for "duration". If the recorded task has a standard length (e.g., 3 mintues), enter the duration here in seconds (i.e., 180). If the duration of the recorded task differs between participants, leave it as "None". 
- __amplify__: How much do we want to amplify the volume of the video? The higher the number we enter here, the louder the video would be. Needless to say, an argument of 0 means that the video will be muted.
- __excel__: What is the path and name of the Excel file that contains arguments regarding subfolder names, video timing, and cropping details?
- __other parameters__: Leave them as "None" here since the arguments are found in the Excel file. See the [examples.py](./examples.py) script for how to manually pass arguments to these parameters.

In the __Excel file__ (see Figure 2 below), we should have seven columns that correspond to the last few parameters of this function (i.e., "children", "start", "end", "x1", "x2", "y1", and "y2"). While these names can be changed to something else that is more intuitive (or even written in another language), the information _must_ be in entered in this order.  

<img src="https://github.com/smy1/swlab/blob/main/script/py_eg_xl_crop.png" width=auto height="280">

__Figure 2__: _An example of an Excel file for the crop function._

In Figure 2 above:
- __Column A__ (or the parameter __"children"__): Contains the name of the first-level subfolders in which the videos are stored. In this example, the names of subfolders correspond to our participants' ID.
- __Column B__ (or the parameter __"start"__): Contains the time at which the task started (in seconds) in the video recording of each of the particpant. This is assuming that we also want to clip the video in additional to cropping it.
- __Column C__ (or the parameter __"end"__): Contains the time at which the recording ended (again, in seconds). This can be left blank if the duration of the task is always the same for everyone (see the parameter "dur" above).
- __Column D__ (or the parameter __"x1"__) onwards requires a number to determine the area of the video that we want to crop. "x1" refers to the start of the width of cropping area.
- __Column E__ (or the parameter __"x2"__) refers to the end of the width of cropping area.
- __Column F__ (or the parameter __"y1"__) refers to the start of the height of cropping area.
- __Column G__ (or the parameter __"y2"__) refers to the end of the height of cropping area.

And if the explanation for the cropping details is unclear, Figure 3 below should be helpful.

<img src="https://github.com/smy1/swlab/blob/main/script/py_eg_annotated.png" width=auto height="230">

__Figure 3__: _An example of how to get the cropping details._

In Figure 3 above: 
- This is a screenshot of a movie with a dimension of 640 x 480. (I have decided to illustrate using a movie instead of an actual experiment recording). Imagine that we want to crop the area indicated by the white border.
- To get __x1 and x2__: Given that the width of the movie is 640, we can gauge the other points along the x-axis by dividing the screenshot by halves. This gives us a value of _120 for x1_ and _480 for x2_.
- To get __y1 and y2__: Likewise, knowing that the height of the movie is 480, we can gauge the other points along the y-axis. This gives us a value of _360 for y2_. Since we do not want to cut the top, _y1 will be 0_.

>[!TIP]
>The dimension of a video can be obtained by checking its properties. We can also get this information using moviepy:
>```
>(w, h) = vid.size ##gives the width and heigth of a video that is named "vid"
>```

---

### 4. Juxtapose videos
__(4A) Juxtapose two videos__  
The following code calls for the __join2side function__ to place two videos side-by-side for comparison. See [Example 4B](#4b-juxtapose-three-videos) below to join three videos. 
```
from editvid import join2side
join2side(folder = "C:/Users/user/Desktop/mc_vid",
        attempts = 3,
        cam1 = "front",
        cam2 = "side",
        newname = "sbr",
        dur = 305,
        amplify_who = "side",
        amplify = 10,
        mute_who = "front",
        crop_who = "front",
        excel = "C:/Users/user/Desktop/mc_vid/example_join2.xlsx",
        children=None, main=None, start=None, end=None, corr=None, x1=None, x2=None, y1=None, y2=None)
```
In the code above:
- __folder__: Where is the main project folder that stores all the videos? In this example, the main project folder is called "mc_vid", which is stored in the desktop by a user named "user".
- __attempts__: Is this the first attempt to sync and juxtapose videos? If yes, enter 1, and the function will ignore the argument given to the parameter "corr" (see below). If the number entered here is 2 or larger, we need to provide this argument, otherwise, the function will return an error.
- __cam1__: Stands for "camera-1". What is the name of the first video recording? In this example, Python will search for a video file that has the word "front" in the name. These cam1 videos should be stored in their respective subfolders. The names of these subfolders must be provided in the first column of the Excel file (see Figure 4 below).
- __cam2__: Stands for "camera-2". What is the name of the second video recording? In this example, Python will search for a video file that has the word "side" in the name. These videos should be stored together with cam1 videos.
- __newname__: How should Python name the new video? In this example, the video that is created will be called as "sbr" (which stands for "shared book reading").
- __dur__: Stands for "duration". If the recorded task has a standard length (e.g., 3 mintues), enter the duration here in seconds (i.e., 180). If the duration of the recorded task differs between participants, leave it as "None". 
- __amplify_who__: Which video should Python amplify? The argument given here should be the same as that given for either cam1 or cam2. Leave it as "no" if neither video should be amplified, and the parameter "amplify" below will be ignored. In this example, Python will amplify the volume of videos that are named "side" (i.e., cam2). 
- __amplify__: How much do we want to amplify the volume of the video? The higher the number we enter here, the louder the video would be. Needless to say, an argument of 0 means that the video will be muted.
- __mute_who__: Which video should Python mute? The argument given here should be the same as that given for either cam1 or cam2. Leave it as "no" if neither video should be muted. In this example, Python will mute videos that are named "front" (i.e., cam1). 
- __crop_who__: Which video should Python crop? The argument given here should be the same as that given for either cam1 or cam2. Leave it as "no" if neither video should be cropped, and the parameters x1, x2, y1, and y2 below will be ignored. In this example, Python will crop videos that are named "front" (i.e., cam1). 
- __excel__: What is the path and name of the Excel file that contains arguments regarding subfolder names, video timing, and cropping details?
- __other parameters__: Leave them as "None" here since the arguments are found in the Excel file. See the [examples.py](./examples.py) script for how to manually pass arguments to these parameters.

In the __Excel file__ (see Figure 4 below), we should have nine columns that correspond to the last few parameters of this function (i.e., "children", "main", "start", "end", "corr", "x1", "x2", "y1", and "y2"). While these names can be changed to something else that is more intuitive (or even written in another language), the information _must_ be in entered in this order.  

<img src="https://github.com/smy1/swlab/blob/main/script/py_eg_xl_join2.png" width=auto height="280">

__Figure 4__: _An example of an Excel file for the join2side function._

In Figure 4 above: 
- __Column A__ (or the parameter __"children"__): Contains the name of the subfolders in which the three cam1 and cam2 videos are stored. In this example, the names of subfolders correspond to our participants' ID.
- __Column B__ (or the parameter __"main"__): Contains the name of the video camera that has the best angle of recording. These names should be the same as that entered for the parameters "cam1" and "cam2". The video identified as the main camera will be displayed larger than the other video. In this example, the camera "side" has the best recording angle for participants "c47" and "c59" while the camera "front" has the best angle for participant "c61".
- __Column C__ (or the parameter __"start"__): Contains the time at which the task started (in seconds) in the video recording of each of the particpant. _Since we have two video recordings (cam1 and cam2), use the start time of cam1._
- __Column D__ (or the parameter __"end"__): Contains the time at which the task ended (again, in seconds). This can be left blank if the duration of the task is always the same for everyone (see the parameter "dur" above).
- __Column E__ (or the parameter __"corr"__, which stands for "correction"): Contains numbers (in seconds) to correct for out-of-sync videos. _If the cam2 is slower (i.e., lags behind cam1), give a positive number_. This parameter can be left blank (and will be disregarded even if it is not blank) if the parameter "attempts" gets an argument of 1 (because logically, in the first attempt, we do not know how well Python syncs the two videos). 
- __Column F__ (or the parameter __"x1"__) onwards requires a number to determine the area of the video that we want to crop. This parameter can be left blank (and will be disregarded even if it is not blank) if the parameter "crop_who" is "no". "x1" refers to the start of the width of cropping area.
- __Column G__ (or the parameter __"x2"__) refers to the end of the width of cropping area.
- __Column H__ (or the parameter __"y1"__) refers to the start of the height of cropping area.
- __Column I__ (or the parameter __"y2"__) refers to the end of the height of cropping area.

See Figure 3 above for a more helpful illustration on the cropping details.

---

#### (4B) Juxtapose three videos
The following code calls for the __join3side function__ to place three videos beside each other for comparison. See __Example 4A above__ to join two videos. 
```
from editvid import join3side
join3side(folder = "C:/Users/user/Desktop/mc_vid",
        attempts = 1,
        cam1 = "sbr1",
        cam2 = "sbr2",
        cam3 = "sbr3",
        newname = "sbr_merged",
        dur = 20,
        amplify_who = "sbr2",
        amplify = 10,
        excel = "C:/Users/user/Desktop/mc_vid/example_join2.xlsx",
        children=None, main=None, start=None, end=None, corr1=None, corr2=None)
```
In the code above:
- __folder__: Where is the main project folder that stores all the videos? In this example, the main project folder is called "mc_vid", which is stored in the desktop by a user named "user".
- __attempts__: Is this the first attempt to sync and juxtapose videos? If yes, enter 1, and the function will ignore the argument given to the parameter "corr" (see below). If the number entered here is 2 or larger, we need to provide this argument, otherwise, the function will return an error.
- __cam1__: Stands for "camera-1". What is the name of the first video recording? In this example, Python will search for a video file that has the word "sbr1" in the name. These videos should be stored in their respective subfolders.  The names of these subfolders must be provided in the first column of the Excel file (see Figure 5 below).
- __cam2__: Stands for "camera-2". What is the name of the second video recording? In this example, Python will search for a video file that has the word "sbr2" in the name. These videos should be stored together with cam1 videos.
- __cam3__: Stands for "camera-3". What is the name of the second video recording? In this example, Python will search for a video file that has the word "sbr3" in the name. These videos should be stored together with cam1 & cam2 videos.
- __newname__: How should Python name the new video? In this example, the video that is created will be called as "sbr_merged".
- __dur__: Stands for "duration". If the recorded task has a standard length (e.g., 3 mintues), enter the duration here in seconds (i.e., 180). If the duration of the recorded task differs between participants, leave it as "None". 
- __amplify_who__: Which video should Python amplify? The argument given here should be the same as that given for either cam1, cam2, or cam3. Leave it as "no" if neither video should be amplified, and the parameter "amplify" below will be ignored. In this example, Python will amplify the volume of videos that are named "sbr2" (i.e., cam2). In this function, the other two videos will be muted automatically.
- __amplify__: How much do we want to amplify the volume of the video? The higher the number we enter here, the louder the video would be. Needless to say, an argument of 0 means that the video will be muted.
- __excel__: What is the path and name of the Excel file that contains arguments regarding subfolder names, video timing and details?
- __other parameters__: Leave them as "None" here since the arguments are found in the Excel file. See the [examples.py](./examples.py) script for how to manually pass arguments to these parameters.

In the __Excel file__ (see Figure 5 below), we should have six columns that correspond to the last few parameters of this function (i.e., "children", "main", "start", "end", "corr1", "corr2"). While these names can be changed to something else that is more intuitive (or even written in another language), the information _must_ be in entered in this order.  

_Will add Figure 5 here._
<!--img src="https://github.com/smy1/swlab/blob/main/script/py_eg_xl_join3.png" width=auto height="280"-->

__Figure 5__: _An example of an Excel file for the join3side function._

In Figure 5 above: 
- __Column A__ (or the parameter __"children"__): Contains the name of the subfolders in which the three cam1, cam2, and cam3 videos are stored. In this example, the names of subfolders correspond to our participants' ID.
- __Column B__ (or the parameter __"main"__): Contains the name of the video camera that has the best angle of recording. These names should be the same as that entered for the parameters "cam1", "cam2", and "cam3". The video identified as the main camera will be displayed larger than the other video. In this example, the camera "sbr3" has the best recording angle for participant "129" while the camera "sbr2" has the best angle for participant "130".
- __Column C__ (or the parameter __"start"__): Contains the time at which the task started (in seconds) in the video recording of each of the particpant. _Since we have three video recordings (cam1, cam2, & cam3), use the start time of cam1._
- __Column D__ (or the parameter __"end"__): Contains the time at which the task ended (again, in seconds). This can be left blank if the duration of the task is always the same for everyone (see the parameter "dur" above).
- __Column E__ (or the parameter __"corr1"__, which stands for "correction-cam2"): Contains numbers (in seconds) to correct for out-of-sync cam2. _If the cam2 is slower (i.e., lags behind cam1), give a positive number_. This parameter can be left blank (and will be disregarded even if it is not blank) if the parameter "attempts" gets an argument of 1 (because logically, in the first attempt, we do not know how well Python syncs the two videos). 
- __Column F__ (or the parameter __"corr2"__, which stands for "correction-cam3"): Contains numbers (in seconds) to correct for out-of-sync cam3. _If the cam3 is slower (i.e., lags behind cam1), give a positive number_. 

---

## Helpful resources
I relied heavily on the links below when writing the video-editing scripts the first time. Note: These links use [MoviePy v1.0](https://zulko.github.io/moviepy/v1.0.3/). 
- how to [loop multiple videos in a folder](https://stackoverflow.com/a/75788036)
- how to [concatenate multiple videos](https://www.geeksforgeeks.org/moviepy-concatenating-multiple-video-files/)
- how to [calculate time difference](https://www.geeksforgeeks.org/calculate-time-difference-in-python/)
- how to [crop a video](https://stackoverflow.com/a/74586686)
- how to [rename files](https://pynative.com/python-rename-file/)
