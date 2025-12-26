# Edit videos in bulk using Python 
This repo contains codes that I wrote to automatise video-editing tasks when I was a postdoc in CBDL-Lab (09.2023 - 12.2025). Most of my video-editing scripts are compiled into a module called [editvid.py](./editvid.py). This module should be downloaded and stored in the same folder as where we will be running our code.  

All my scripts use MoviePy (a Python reference tool) to edit videos in bulk, allowing the video-editing task to be automatised. Arguments can be provided to the functions in two ways, either by loading an excel file (see [examples below](#examples)) or by manually entering the arguments (see the [examples.py](./examples.py) script). 

For __other video-editing scripts__ that have _not_ been compiled, see [here](./obsolete/). To __transcribe audio files__, see [here](https://github.com/smy1/auto-peer/blob/main/transcribe-audio/). To __code parents' shared reading practice__ automatically, see [here](https://github.com/smy1/auto-peer/blob/main/).

- [Installation and requirements](#installation-and-requirements)
- [__Example 1__](#1-merge-videos): Join videos together into a long one
- [__Example 2__](#2-crop-videos): Crop videos
- [__Example 3__](#3-overlay-videos): Sync and display a smaller video on top of a bigger one
- [__Example 4__](#4-juxtapose-videos): Sync and display videos beside each other
- [Helpful resources](#helpful-resources) (I wouldn't have been able to write these scripts without them)

---

## Installation and requirements
1. Start with the installation of Python (see [here](https://www.python.org/downloads/release/python-31210/) for the version that I used). When installing Python, __remember to check the box that says "Add python.exe to PATH".__ 
This will enable you to run Python in the terminal of code editors such as [Kate](https://kate-editor.org/) and [VS Code](https://code.visualstudio.com/). Check whether the Python installation is successful by typing the following code
in the terminal of your editor: `python --version`  
2. Create a project folder, then download and store the [requirements.txt](./requirements.txt) file there. Open a new file in your editor, save it in that folder and type the following in the terminal: 
`pip install -r requirements.txt`
3. Once this is done, __start by checking the directory shown in the terminal__. Change it so that it leads to the project folder. You may do this by specifying the directory `cd <directory path of the folder>` or 
   setting the terminal directory to be always the same as your editor file. In Kate, it would be _settings_ -> _configure Kate_ -> _terminal_ -> select _"synchronise the terminal with the current document"_
5. Finally, you can paste whichever [example codes below](#examples) that is relevant to you in that new editor file. Then, to run the code, simply type `python <name of this editor file>.py` in the terminal.

### Some important points
> [!IMPORTANT]
> __When manually providing arguments:__  
> For parameters that expect a list (this usually means any argument that can be passed into the function by loading an excel file), even if there is only one argument that Python needs to deal with, the argument must be given within square brackets (e.g., `children = ["a62_c62"]`) so that Python treats it like a list; otherwise, the function will return an error.

>[!NOTE]
>When I first started writing these video-editing scripts, I used [MoviePy v1.0.3](https://zulko.github.io/moviepy/v1.0.3/). As of 2025, [MoviePy v2.0](https://zulko.github.io/moviepy/) has been released. See [here](https://zulko.github.io/moviepy/getting_started/updating_to_v2.html) for details about the differences, if you wish to use the latest moviepy module. 

---

## Examples
### 1. Merge videos
The following code uses the __`merge`__ function to concatenate several videos into one long video. 
```python
from editvid import merge
merge(folder="C:/Users/user/Desktop/mc_vid", 
      children=["a62_c62", "a63_c63", "a64_c64"], 
      camera=["BABY", "front", "SBR1", "SCREEN", "影片二"])
```
In the code above:
- __`folder`__: __The path to the main project folder__ that contains all subfolders.  
- __`children`__: __A list of first-level subfolders__ in the main project folder.  
- __`camera`__: __A list of second-level subfolders__ in the first-level subfolders. These should contain the video clips that you want to concatenate.  
- In short, the videos should be stored in a path like this: ___main project folder -> first-level subfolder -> second-level subfolder -> videos to be concatenated___. The final concatenated videos will be named after their respective second-level subfolder and stored in their respective first-level subfolder.

>[!TIP]
> - If a subfolder or video does not exist, the function will simply return a message saying there's nothing to merge for that particular camera. This means you can list all possible subfolders. The function won’t crash if some subfolders are missing.  
> - This `merge` function is designed specifically for certain Xiaomi Security Cameras ([2K](https://www.mi.com/global/product/mi-360-home-security-camera-2k/specs/), 
[1080p](https://www.mi.com/global/product/mi-360-camera-1080p/specs/), 
[C400](https://www.mi.com/global/product/xiaomi-smart-camera-c400/specs/)). It extracts the timestamp from the camera recording's name and adds it to the name of the concatenated video. If your video files are named differently, this function will assume the timestamp to be 00M00S.
> - To concatenate recordings from Xiaomi Security Cameras that store recordings in 10 seconds (e.g., [2K (Magnetic Mount)](https://www.mi.com/global/product/mi-camera-2k-magnetic-mount/specs/)), see this [script](./obsolete/merge-clips.py). For the newer security cameras that store recordings in longer duration (in terms of several minutes), see this [script](./obsolete/merge-vid2.py).

---

### 2. Crop videos
The following code uses the __`crop`__ function to crop a video. It will also clip the video to the desired duration.  
```python
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
- __`folder`__: __The path to the main project folder__ that contains all subfolders.   
- __`cam`__: __The name of the video that needs to be cropped__. In this example, Python will search for a video file that has the word "front" in the name. These videos should be stored in their respective subfolders, which must be passed to the parameter `children` (see Figure 1 below). In other words, the videos should be stored in a path like this: ___main project folder -> subfolder -> videos to be cropped___.
- __`newname`__: __Give the cropped video a new name__. 
- __`dur`__: __The duration (in seconds)__ of the video to be clipped. If the clipping duration differs between videos, leave this as `None` and pass information to the parameter `end` below.  
- __`amplify`__: A higher value __increases the volume of the video__. A value of `1` keeps the volume unchanged, while a value of `0` mutes the video.  
- __`excel`__: __The path to the Excel file__ that contains the cropping details of each video. 
- __other parameters__: Leave these as `None`, as the function will automatically extract the values from the Excel file. If you prefer to manually input these values, see [examples.py](./examples.py).  

#
The __Excel file used by the `crop` function__ should have seven columns, corresponding to the following parameters: `children`, `start`, `end`, `x1`, `x2`, `y1`, and `y2` (see Figure 1 below).  

__Figure 1__  
_An example of an Excel file for the crop function._  
<img src="https://github.com/smy1/swlab/blob/main/misc/py_eg_xl_crop.png" width=auto height="250">

In Figure 1 above:
- __Column A__ (`children`): __A list of subfolders__ in the main project folder. These should contain the videos that you want to crop.  
- __Column B__ (`start`): __The start time (in seconds)__ of the clipped video. This is used if you also want to clip the video in addition to cropping it.  
- __Column C__ (`end`): __The end time (in seconds)__ of the clipped video. This can be left blank if the clipping duration of all videos is the same (see the parameter `dur` above).  
- __Column D__ (`x1`): __The starting point of the cropping area’s width__. See [Figure 2](#figure-2) below for an illustration.
- __Column E__ (`x2`): __The endpoint of the cropping area’s width__.  
- __Column F__ (`y1`): __The starting point of the cropping area’s height.__
- __Column G__ (`y2`): __The endpoint of the cropping area’s height.__

#
#### Figure 2 
_An illustration that explains about the cropping details._  
<img src="https://github.com/smy1/swlab/blob/main/misc/py_eg_annotated.png" width=auto height="230">

In Figure 2 above: 
- This is a screenshot of a movie with a dimension of 640 x 480. Imagine that we want to crop the area indicated by the white border.
- To get __x1 and x2__: Given that the width of the movie is 640, we can gauge the other points along the x-axis by dividing the screenshot by halves. This gives us a value of _120 for x1_ and _480 for x2_.
- To get __y1 and y2__: Likewise, knowing that the height of the movie is 480, we can gauge the other points along the y-axis. This gives us a value of _360 for y2_. Since we do not want to cut the top, _y1 will be 0_.

>[!TIP]
>The dimension of a video can be obtained by checking its properties. We can also get this information using moviepy:
>```python
>(w, h) = vid.size ##gives the width and heigth of a video that is named "vid"
>```

---

### 3. Overlay videos
The following code uses the __`overlay`__ function to overlay one video on top of another and create a composite video. 
```python
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
- __`folder`__: __The path to the main project folder__ that contains all subfolders.  
- __`attempts`__: __The number of attempts in syncing videos__. This parameter determines whether the parameter `corr` (see Figure 3 below) is skipped or not. If `attempts` is 1, any arguments passed to the parameter `corr` is ignored, while if `attempts` is larger than 1, the function will expect a value for the parameter `corr`.
- __`bgcam`__: Stands for "background-camera". Enter __the name of the video that will be used as the "base"__ of the composite video. In this example, Python will search for a video file that has the word "baby" in the name. These base videos should be stored in their respective subfolders. The names of these subfolders must be passed to the parameter `children` (see Figure 3 below).
- __`topcam`__: Stands for "top-camera". Enter __the name of the video that will be overlaid on top__ of the base video. In this example, Python will search for a video file that has the word "screen" in the name. These top videos should be stored together with the base videos.
- __`newname`__: __Give the composite video a new name__. 
- __`propsize`__: Stands for "proportion-size". __How small should be top video be?__ In this example, `0.25` means 25% of its original size.
- __`dur`__: __The duration (in seconds)__ of the top video to be clipped. If the clipping duration differs between top videos, leave this as `None` and pass information to the parameter `end` below.   
- __`excel`__: __The path to the Excel file__ that contains the overlaying details of each video. 
- __other parameters__: Leave these as `None`, as the function will automatically extract the values from the Excel file. If you prefer to manually input these values, see [examples.py](./examples.py).  

#
The __Excel file used by the `overlay` function__ should have four columns, corresponding to the following parameters: `children`, `start`, `end`, and `corr` (see Figure 3 below).  

__Figure 3__  
_An example of an Excel file for the overlay function._  
<img src="https://github.com/smy1/swlab/blob/main/misc/py_eg_xl_overlay.png" width=auto height="250">

In Figure 3 above: 
- __Column A__ (`children`): __A list of first-level subfolders__ in the main project folder. These should contain videos that you want to work on.  
- __Column B__ (`start`): __The start time (in seconds)__ of the clipped top video.  
- __Column C__ (`end`): __The end time (in seconds)__ of the clipped top video. This can be left blank if the clipping duration of all top videos is the same (see the parameter `dur` above).
- __Column D__ (`corr`, which stands for "correction"): Contains numbers (in seconds) to correct for out-of-sync videos. __If the base video is slower (i.e., lags behind the top video), give a positive number__. If the parameter `attempts` above has a value of `1`, any argument provided here will be skipped. Likewise, if the parameter `attempts` above has a value that is larger than `1` and no argument is provided here, the function will crash.

> [!TIP]
> For this `overlay` function to work properly, __the names of the videos should end with a timestamp (in minutes and seconds)__, for example, "video_56M09S.mp4". Otherwise, the function will produce a warning message stating that "no timestamp is found and that 00:00 will be assumed". This may cause the videos to be out of sync.

---

### 4. Juxtapose videos
__(4A) Juxtapose two videos__  
The following code used the __`join2side`__ function to place two videos side-by-side for comparison. See [Example 4B](#4b-juxtapose-three-videos) below to join three videos. 
```python
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
        match_time = "yes",
        resize_yes = "yes",
        excel = "C:/Users/user/Desktop/mc_vid/example_join2.xlsx",
        children=None, main=None, start=None, end=None, corr=None, x1=None, x2=None, y1=None, y2=None)
```
In the code above:
- __`folder`__: __The path to the main project folder__ that contains all subfolders.  
- __`attempts`__: __The number of attempts in syncing videos__. This parameter determines whether the parameter `corr` (see Figure 4 below) is skipped or not. If `attempts` is 1, any arguments passed to the parameter `corr` is ignored, while if `attempts` is larger than 1, the function will expect a value for the parameter `corr`.
- __`cam1`__: Stands for "camera-1". Enter __the name of the first video__. In this example, Python will search for a video file that has the word "front" in the name. These camera-1 videos should be stored in their respective subfolders. The names of these subfolders must be passed to the parameter `children` (see Figure 4 below). In other words, the videos should be stored in a path like this: ___main project folder -> subfolder -> videos to be juxtaposed___.  
- __`cam2`__: Stands for "camera-2". Enter __the name of the second video__. In this example, Python will search for a video file that has the word "side" in the name. These videos should be stored together with camera-1 videos.
- __`newname`__: __Give the new video a name__. 
- __`dur`__: __The duration (in seconds)__ of camera-1 videos to be clipped. If the clipping duration differs between camera-1 videos, leave this as `None` and pass information to the parameter `end` below.
- __`amplify_who`__: Enter __the name of the video that should be amplified__ (the name should be the same as that given for either `cam1` or `cam2`). Leave it as `no` if neither video should be amplified, and the parameter `amplify` below will be ignored.  
- __`amplify`__: The higher the number we enter here, the louder the video would be. An argument of `1` means that the volume is unchanged while an argument of `0` means that the video will be muted.
- __`mute_who`__: Enter __the name of the video that should be muted__ (the name should be the same as that given for either `cam1` or `cam2`). Leave it as `no` if neither video should be muted. 
- __`crop_who`__: Enter __the name of the video that should be cropped__ (the name should be the same as that given for either `cam1` or `cam2`). Leave it as `no` if neither video should be cropped, and the parameters `x1`, `x2`, `y1`, and `y2` below will be ignored. 
- __`match_time`__: If the start time of the two videos is different and we __need Python to calculate the time difference between the videos__, enter `yes`. The name of the videos must end with their respective starting timestamp (e.g., "video_01M03S.mp4"). Otherwise, the function will produce a warning message stating that "no timestamp is found and that 00:00 will be assumed". This may cause the videos to be out of sync. If syncing of the videos is not necessary (e.g., the videos are already synced), leave this parameter as `no`.
- __`resize_yes`__: If we __want to resize the videos__, enter `yes`. The main video will then be downsized to 0.7 while the other video will be downsized to 0.4. If we enter `no`, the videos will be of equal sizes. 
- __`excel`__: __The path to the Excel file__ that contains the juxtaposing details of each video.  
- __other parameters__: Leave these as `None`, as the function will automatically extract the values from the Excel file. If you prefer to manually input these values, see [examples.py](./examples.py).  

#
The __Excel file used by the `join2side` function__ should have nine columns, corresponding to the following parameters: `children`, `main`, `start`, `end`, `corr`, `x1`, `x2`, `y1`, and `y2` (see Figure 4 below).  

__Figure 4__  
_An example of an Excel file for the join2side function._  
<img src="https://github.com/smy1/swlab/blob/main/misc/py_eg_xl_join2.png" width=auto height="250">

In Figure 4 above: 
- __Column A__ (`children`): __A list of first-level subfolders__ in the main project folder. These should contain the videos (i.e., camera-1 and camera-2) that you want to juxtapose.  
- __Column B__ (`main`): Contains __the name of the video camera that has the best angle of recording__. These names should be the same as that entered for the parameters `cam1` and `cam2`. The video identified as the main camera will be displayed larger than the other video. 
- __Column C__ (`start`): __The start time (in seconds)__ of the clipped camera-1 video.  
- __Column D__ (`end`): __The end time (in seconds)__ of the clipped camera-1 video. This can be left blank if the clipping duration of all camera-1 videos is the same (see the parameter `dur` above).  
- __Column E__ (`corr`, which stands for "correction"): Contains numbers (in seconds) to correct for out-of-sync videos. __If the camera-2 is slower (i.e., lags behind camera-1), give a positive number__. If the parameter `attempts` above has a value of `1`, any argument provided here will be skipped. Likewise, if the parameter `attempts` above has a value that is larger than `1` and no argument is provided here, the function will crash.
- __Column F__ (`x1`): __The starting point of the cropping area’s width__. See [Figure 2](#figure-2) above for an illustration. This parameter (and those that follow) will be ignored if the parameter `crop_who` is `no`.
- __Column G__ (`x2`): __The endpoint of the cropping area’s width__.  
- __Column H__ (`y1`): __The starting point of the cropping area’s height__.  
- __Column I__ (`y2`): __The endpoint of the cropping area’s height__.  

> [!TIP]
> For this `join2side` function to work properly, __the names of the videos should end with a timestamp (in minutes and seconds)__, for example, "video_56M09S.mp4". Otherwise, the function will produce a warning message stating that "no timestamp is found and that 00:00 will be assumed". This may cause the videos to be out of sync.

---

#### (4B) Juxtapose three videos
The following code uses the __`join3side`__ function to place three videos beside each other for comparison. See [Example 4A](#4-juxtapose-videos) above to join two videos. 
```python
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
        excel = "C:/Users/user/Desktop/mc_vid/example_join3.xlsx",
        children=None, main=None, start=None, end=None, corr1=None, corr2=None)
```
In the code above:
- __`folder`__: __The path to the main project folder__ that contains all subfolders.  
- __`attempts`__: __The number of attempts in syncing videos__. This parameter determines whether the parameters `corr1` and `corr2` (see Figure 5 below) are skipped or not. If `attempts` is 1, any argument passed to the parameters `corr1` and `corr2` is ignored, while if `attempts` is larger than 1, the function will expect a value for the parameters `corr1` and `corr2`.
- __`cam1`__: Stands for "camera-1". Enter __the name of the first video__. In this example, Python will search for a video file that has the word "sbr1" in the name. These videos should be stored in their respective subfolders. The names of these subfolders must be passed to the parameter `children` (see Figure 5 below). In other words, the videos should be stored in a path like this: ___main project folder -> subfolder -> videos to be juxtaposed___.  
- __`cam2`__: Stands for "camera-2". Enter __the name of the second video__. In this example, Python will search for a video file that has the word "sbr2" in the name. These videos should be stored together with cam1 videos.
- __`cam3`__: Stands for "camera-3". Enter __the name of the third video__. In this example, Python will search for a video file that has the word "sbr3" in the name. These videos should be stored together with cam1 & cam2 videos.
- __`newname`__: __Give the new video a name__. 
- __`dur`__: __The duration (in seconds)__ of the camera-1 video to be clipped. If the clipping duration differs between camera-1 videos, leave this as `None` and pass information to the parameter `end` below.  
- __`amplify_who`__: Enter __the name of the video that should be amplified__ (the name should be the same as that given for either `cam1`, `cam2`, or `cam3`). Leave it as `no` if neither video should be amplified, and the parameter `amplify` below will be ignored. In this function, the other two videos will be muted automatically.
- __`amplify`__: The higher the number we enter here, the louder the video would be. An argument of `1` means that the volume is unchanged while an argument of `0` means that the video will be muted.
- __`excel`__: __The path to the Excel file__ that contains the juxtaposing details of each video.  
- __other parameters__: Leave these as `None`, as the function will automatically extract the values from the Excel file. If you prefer to manually input these values, see [examples.py](./examples.py).  

#
The __Excel file used by the `join3side` function__ should have six columns, corresponding to the following parameters: `children`, `main`, `start`, `end`, `corr1`, `corr2` (see Figure 5 below).  

__Figure 5__  
_An example of an Excel file for the join3side function._  
<img src="https://github.com/smy1/swlab/blob/main/misc/py_eg_xl_join3.png" width=auto height="250">

In Figure 5 above: 
- __Column A__ (`children`): __A list of first-level subfolders__ in the main project folder. These should contain the videos (i.e., camera-1, camera-2, and camera-3) that you want to juxtapose.  
- __Column B__ (`main`): Contains __the name of the video camera that has the best angle of recording__. These names should be the same as that entered for the parameters `cam1`, `cam2`, and `cam3`. The video identified as the main camera will be displayed larger than the other video. 
- __Column C__ (`start`): __The start time (in seconds)__ of the clipped camera-1 video.  
- __Column D__ (`end`): __The end time (in seconds)__ of the clipped camera-1 video. This can be left blank if the clipping duration of all camera-1 videos is the same (see the parameter `dur` above).  
- __Column E__ (`corr1`): Contains numbers (in seconds) to correct for out-of-sync camera-2. __If the camera-2 is slower (i.e., lags behind camera-1), give a positive number__. If the parameter `attempts` above has a value of `1`, any argument provided here will be skipped. Likewise, if the parameter `attempts` above has a value that is larger than `1` and no argument is provided here, the function will crash.
- __Column F__ (`corr2`): Contains numbers (in seconds) to correct for out-of-sync camera-3. __If the camera-3 is slower (i.e., lags behind camera-1), give a positive number__. 

> [!TIP]
> For this `join3side` function to work properly, __the names of the videos should end with a timestamp (in minutes and seconds)__, for example, "video_56M09S.mp4". Otherwise, the function will produce a warning message stating that "no timestamp is found and that 00:00 will be assumed". This may cause the videos to be out of sync.

---

## Helpful resources
I relied heavily on the links below when writing the video-editing scripts the first time. __Note__: These links use [MoviePy v1.0](https://zulko.github.io/moviepy/v1.0.3/). 
- how to [loop multiple videos in a folder](https://stackoverflow.com/a/75788036)
- how to [concatenate multiple videos](https://www.geeksforgeeks.org/moviepy-concatenating-multiple-video-files/)
- how to [crop a video](https://stackoverflow.com/a/74586686)
- how to [calculate time difference](https://www.geeksforgeeks.org/calculate-time-difference-in-python/)
- how to [rename files](https://pynative.com/python-rename-file/)
