# Edit videos in bulk using Python 
Most of my video-editing scripts are compiled into a module called [editvid.py](./editvid.py). This module should be downloaded and stored in the same folder as where we will be running our code.  For other video-editing scripts that have _not_ been compiled, see [here](./obsolete/). 

All my scripts use MoviePy (a Python reference tool) to edit videos in bulk, allowing the video-editing task to be automatised. Arguments can be provided to the functions in two ways, either by loading an excel file (see [examples below](#examples)) or by manually entering the arguments (see the [examples.py](./examples.py) script). 

- [Installation and requirements](#installation-and-requirements)
- [__Example 1__](#1-merge-videos): Join videos together
- [__Example 2__](#2-overlay-videos): Sync and display a smaller video on top of a bigger one
- [__Example 3__](#3-crop-videos): Crop videos
- [__Example 4__](#4-juxtapose-videos): Sync and display videos beside each other
- [Helpful resources](#helpful-resources) (I wouldn't have been able to write these scripts without them)

---

## Installation and requirements
In order to run the functions in this module, Python and the relevant packages need to be installed. I wrote these codes in Python 3.12.4.  
Download the `requirements.txt` file and run the following code: 
`pip install -r requirements.txt`

<!--Installation can be done in the command prompt (for Windows users, type "command prompt" or "cmd" in the search box):
```
python --version ## check python version
pip install --upgrade pip setuptools wheel ## check whether pip is installed
pip show <package name> ## check whether a particular package (and what version) has been install
pip install glob2 ## required to search for files in a folder
pip install openpyxl ## required if we want python to extract information from an excel file
pip install opencv-python ## required for resizing videos if using MoviePy v1.0
pip install DateTime ## required when syncing the timing of two videos
pip install pathlib ## required for Python to locate a path of a file
## The code below allows you to install either the earlier or the latest version.
pip install moviepy==1.0.3 ## this installs the older version
pip install moviepy ## this installs the latest version
```
-->
>[!NOTE]
>When I first started writing these video-editing scripts, I used [MoviePy v1.0.3](https://zulko.github.io/moviepy/v1.0.3/). As of 2025, [MoviePy v2.0](https://zulko.github.io/moviepy/) has been released. See [here](https://zulko.github.io/moviepy/getting_started/updating_to_v2.html) for details about the differences. 

### Important points
I run all my code in the terminal of [Kate](https://kate-editor.org/) (Windows PowerShell) instead of IDLE because somehow, my code doesn't run in the latter. I have never used other source code editors before, but there is no reason why my code won't run in the terminal of other editors (such as [VS Code](https://code.visualstudio.com/)).  

__1. When manually providing arguments:__
> [!IMPORTANT]  
> For parameters that expects a list (this usually means any argument that can be passed into the function by loading an excel file), even if there is only one argument that Python needs to deal with, the argument must be given within square brackets (e.g., `children = ["a62_c62"]`) so that Python treats it like a list, otherwise, the function will return an error.

> [!TIP]
> If all the arguments for a list-type parameter are the same (e.g., all 65 videos have the same start time of 0 second), a shortcut is to use `start = [0] * 65` instead of typing `0` 65 times.

__2. Before syncing videos:__
> [!IMPORTANT]
> In order for the functions to sync videos successfully, __the names of the videos must end with the time (in minutes and seconds) of the first frame__, for example, 56M09S (i.e., the first frame of this video occured at the 56th minute and 9th second of some hour). If the second video's first frame occured at 56M00S, this means that it started recording 9 seconds before the first video, hence, the function will sync the two videos by cutting the first 9 seconds of the second video.

---

## Examples
### 1. Merge videos
The following code calls for the __`merge`__ function to concatenate several videos into one long video. 
```python
from editvid import merge
merge(folder="C:/Users/user/Desktop/mc_vid", 
      children=["a62_c62", "a63_c63", "a64_c64"], 
      camera=["BABY", "front", "SBR1", "SCREEN", "影片二"])
```
In the code above:
- __`folder`__: Enter __the path of the main project folder__. 
- __`children`__: Enter __the names of first-level subfolders__. These subfolders should be stored directly within the main project folder. 
- __`camera`__: Enter __the names of second-level subfolders__. These subfolders should be stored within the first-level  subfolders. Within these subfolders should be all the short, truncated videos that we want to concatenate into one complete long video.
- In short, the storage path of the short videos should be something in the line of ___"main project folder" -> "first level (child) subfolder" -> "second level (camera) subfolder" -> "videos to be concatenated"___. By passing these subfolders into the function, all the videos in them will be processed automatically. The concatenated videos will be named after their respective second-level subfolder.

>[!TIP]
>If a subfolder or video does not exist, the function will just return a statement that there is nothing to merge for that child's camera. This means that we can list all the possible subfolders even if the combination of first and second level subfolders exist only for some but not other videos - it would not crash the function. 

---

### 2. Overlay videos
The following code calls for the __`overlay`__ function to overlay one video on top of another and create a composite video. 
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
- __`folder`__: Enter __the path of the main project folder__. 
- __`attempts`__: __The number of attempts in syncing videos__. If the number entered here is larger than 1, we need to pass arguments to the parameter `corr` (see Figure 1 below), otherwise, the function will return an error.
- __`bgcam`__: Stands for "background-camera". Enter __the name of the video that will be used as the "base"__ of the composite video. In this example, Python will search for a video file that has the word "baby" in the name. These base videos should be stored in their respective subfolders. The names of these subfolders must be passed to the parameter `children` (see Figure 1 below).
- __`topcam`__: Stands for "top-camera". Enter __the name of the video that will be overlaid on top__ of the base video. In this example, Python will search for a video file that has the word "screen" in the name. These top videos should be stored together with the base videos.
- __`newname`__: __Give the composite video a new name__. 
- __`propsize`__: Stands for "proportion-size". __How small should be top video be?__ In this example, `0.25` means 25% of its original size.
- __`dur`__: Stands for __"duration". If the recorded task has a standard length__ (e.g., 3 minutes), enter the duration here in seconds (i.e., 180). If the duration of the recorded task differs between participants, leave it as `None`. 
- __`excel`__: Enter __the path and name of the relevant Excel file__. 
- __other parameters__: Leave them as `None` here since the arguments are found in the Excel file. See the [examples.py](./examples.py) script for an example on manually passing arguments to these parameters.

&nbsp;

In the __Excel file for the `overlay` function__, we should have four columns, the first row being the names of these columns: "children", "start", "end", and "corr". These columns are essentially the last few parameters of this function.  

<img src="https://github.com/smy1/swlab/blob/main/script/py_eg_xl_overlay.png" width=auto height="250">

__Figure 1__: _An example of an Excel file for the overlay function._  

In Figure 1 above: 
- __Column A__ (or the parameter __`children`__): Contains __the names of subfolders__ in which the base video and top video are stored. 
- __Column B__ (or the parameter __`start`__): Contains __the time at which the task started__ (in seconds) in the video recording of each of the particpant. _Since we have two video recordings, use the start time of the top video._ 
- __Column C__ (or the parameter __`end`__): Contains __the time at which the task ended__ (again, in seconds). This can be left blank if the duration of the task is always the same for everyone (see the parameter `dur` above).
- __Column D__ (or the parameter __`corr`__, which stands for "correction"): Contains numbers (in seconds) to correct for out-of-sync videos. __If the base video is slower (i.e., lags behind the top video), give a positive number__. This information can be left blank if the parameter `attempts` gets an argument of `1`. 

---

### 3. Crop videos
The following code calls for the __`crop`__ function to crop a video. 
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
- __`cam`__: Stands for "camera". Enter __the name of the video that needs to be cropped__. In this example, Python will search for a video file that has the word "front" in the name. These videos should be stored in their respective subfolders. The names of these subfolders must be passed to the parameter `children` (see Figure 2 below).
- __`newname`__: __Give the cropped video a new name__. 
- __`dur`__: Stands for __"duration". If the recorded task has a standard length__ (e.g., 3 minutes), enter the duration here in seconds (i.e., 180). If the duration of the recorded task differs between participants, leave it as `None`. 
- __`amplify`__: The higher the number we enter here, the louder the video would be. An argument of `1` means that the volume is unchanged while an argument of `0` means that the video will be muted.
- __`excel`__: Enter __the path and name of the relevant Excel file__. 
- __other parameters__: Leave them as `None` here since the arguments are found in the Excel file. See the [examples.py](./examples.py) script for an example on manually passing arguments to these parameters.

&nbsp;

In the __Excel file for the `crop` function__, we should have seven columns that correspond to the last few parameters of this function (i.e., `children`, `start`, `end`, `x1`, `x2`, `y1`, and `y2`). While these names can be changed to something else that is more intuitive (or even written in another language), the information _must_ be in entered in this order.  

<img src="https://github.com/smy1/swlab/blob/main/script/py_eg_xl_crop.png" width=auto height="250">

__Figure 2__: _An example of an Excel file for the crop function._

In Figure 2 above:
- __Column A__ (or the parameter __`children`__): Contains __the names of subfolders__ in which the videos are stored. 
- __Column B__ (or the parameter __`start`__): Contains __the time at which the task started__ (in seconds) in the video recording of each of the particpant. This is assuming that we also want to clip the video in additional to cropping it.
- __Column C__ (or the parameter __`end`__): Contains __the time at which the recording ended__ (again, in seconds). This can be left blank if the duration of the task is always the same for everyone (see the parameter `dur` above).
- __Column D__ (or the parameter __`x1`__) refers to __the start of the width__ of cropping area. See [Figure 3](#figure-3) below for an illustration.
- __Column E__ (or the parameter __`x2`__) refers to __the end of the width__ of cropping area.
- __Column F__ (or the parameter __`y1`__) refers to __the start of the height__ of cropping area.
- __Column G__ (or the parameter __`y2`__) refers to __the end of the height__ of cropping area.

#
#### Figure 3 
An illustration that explains about the cropping details.

<img src="https://github.com/smy1/swlab/blob/main/script/py_eg_annotated.png" width=auto height="230">

In Figure 3 above: 
- This is a screenshot of a movie with a dimension of 640 x 480. Imagine that we want to crop the area indicated by the white border.
- To get __x1 and x2__: Given that the width of the movie is 640, we can gauge the other points along the x-axis by dividing the screenshot by halves. This gives us a value of _120 for x1_ and _480 for x2_.
- To get __y1 and y2__: Likewise, knowing that the height of the movie is 480, we can gauge the other points along the y-axis. This gives us a value of _360 for y2_. Since we do not want to cut the top, _y1 will be 0_.

>[!TIP]
>The dimension of a video can be obtained by checking its properties. We can also get this information using moviepy:
>```python
>(w, h) = vid.size ##gives the width and heigth of a video that is named "vid"
>```

---

### 4. Juxtapose videos
__(4A) Juxtapose two videos__  
The following code calls for the __`join2side`__ function to place two videos side-by-side for comparison. See [Example 4B](#4b-juxtapose-three-videos) below to join three videos. 
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
- __`folder`__: Enter __the path of the main project folder__. 
- __`attempts`__: __The number of attempts in syncing videos__. If the number entered here is larger than 1, we need to pass arguments to the parameter `corr` (see Figure 4 below), otherwise, the function will return an error.
- __`cam1`__: Stands for "camera-1". Enter __the name of the first video__. In this example, Python will search for a video file that has the word "front" in the name. These camera-1 videos should be stored in their respective subfolders. The names of these subfolders must be passed to the parameter `children` (see Figure 4 below).
- __`cam2`__: Stands for "camera-2". Enter __the name of the second video__. In this example, Python will search for a video file that has the word "side" in the name. These videos should be stored together with camera-1 videos.
- __`newname`__: __Give the new video a name__. 
- __`dur`__: Stands for __"duration". If the recorded task has a standard length__ (e.g., 3 minutes), enter the duration here in seconds (i.e., 180). If the duration of the recorded task differs between participants, leave it as `None`. 
- __`amplify_who`__: Enter __the name of the video that should be amplified__ (the name should be the same as that given for either `cam1` or `cam2`). Leave it as `no` if neither video should be amplified, and the parameter `amplify` below will be ignored.  
- __`amplify`__: The higher the number we enter here, the louder the video would be. An argument of `1` means that the volume is unchanged while an argument of `0` means that the video will be muted.
- __`mute_who`__: Enter __the name of the video that should be muted__ (the name should be the same as that given for either `cam1` or `cam2`). Leave it as `no` if neither video should be muted. 
- __`crop_who`__: Enter __the name of the video that should be cropped__ (the name should be the same as that given for either `cam1` or `cam2`). Leave it as `no` if neither video should be cropped, and the parameters `x1`, `x2`, `y1`, and `y2` below will be ignored. 
- __`match_time`__: If the start time of the two videos is different and we __need Python to calculate the time difference between the videos__, enter `yes`. The name of the videos must then end with their respective start time (e.g., 01M03S). If this is not necessary (i.e., the time of both videos is already synced), leave it as `no`.
- __`resize_yes`__: If we __want to resize the videos__, enter `yes`. The main video will then be downsized to 0.7 while the other video will be downsized to 0.4. If we enter `no`, the videos will be of equal sizes. 
- __`excel`__: Enter __the path and name of the relevant Excel file__. 
- __other parameters__: Leave them as `None` here since the arguments are found in the Excel file. See the [examples.py](./examples.py) script for an example on manually passing arguments to these parameters.  

&nbsp;

In the __Excel file for the `join2side` function__, we should have nine columns that correspond to the last few parameters of this function (i.e., `children`, `main`, `start`, `end`, `corr`, `x1`, `x2`, `y1`, and `y2`). 

<img src="https://github.com/smy1/swlab/blob/main/script/py_eg_xl_join2.png" width=auto height="250">

__Figure 4__: _An example of an Excel file for the join2side function._

In Figure 4 above: 
- __Column A__ (or the parameter __`children`__): Contains __the names of subfolders__ in which the two camera-1 and camera-2 videos are stored. 
- __Column B__ (or the parameter __`main`__): Contains __the name of the video camera that has the best angle of recording__. These names should be the same as that entered for the parameters `cam1` and `cam2`. The video identified as the main camera will be displayed larger than the other video. 
- __Column C__ (or the parameter __`start`__): Contains __the time at which the task started__ (in seconds) in the video recording of each of the particpant. _Since we have two video recordings, use the start time of camera-1._
- __Column D__ (or the parameter __`end`__): Contains __the time at which the task ended__ (again, in seconds). This can be left blank if the duration of the task is always the same for everyone (see the parameter `dur` above).
- __Column E__ (or the parameter __`corr`__, which stands for "correction"): Contains numbers (in seconds) to correct for out-of-sync videos. __If the camera-2 is slower (i.e., lags behind camera-1), give a positive number__. This parameter can be left blank if the parameter `attempts` gets an argument of `1`. 
- __Column F__ (or the parameter __`x1`__) refers to __the start of the width__ of cropping area. See [Figure 3](#figure-3) above for an illustration. This parameter (and those that follow) can be left blank if the parameter `crop_who` is `no`.
- __Column G__ (or the parameter __`x2`__) refers to __the end of the width__ of cropping area.
- __Column H__ (or the parameter __`y1`__) refers to __the start of the height__ of cropping area.
- __Column I__ (or the parameter __`y2`__) refers to __the end of the height__ of cropping area.

---

#### (4B) Juxtapose three videos
The following code calls for the __`join3side`__ function to place three videos beside each other for comparison. See [Example 4A](#4-juxtapose-videos) above to join two videos. 
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
- __`folder`__: Enter __the path of the main project folder__. 
- __`attempts`__: __The number of attempts in syncing videos__. If the number entered here is larger than 1, we need to pass arguments to the parameter `corr` (see Figure 5 below), otherwise, the function will return an error.
- __`cam1`__: Stands for "camera-1". Enter __the name of the first video__. In this example, Python will search for a video file that has the word "sbr1" in the name. These videos should be stored in their respective subfolders. The names of these subfolders must be passed to the parameter `children` (see Figure 5 below).
- __`cam2`__: Stands for "camera-2". Enter __the name of the second video__. In this example, Python will search for a video file that has the word "sbr2" in the name. These videos should be stored together with cam1 videos.
- __`cam3`__: Stands for "camera-3". Enter __the name of the third video__. In this example, Python will search for a video file that has the word "sbr3" in the name. These videos should be stored together with cam1 & cam2 videos.
- __`newname`__: __Give the new video a name__. 
- __`dur`__: Stands for __"duration". If the recorded task has a standard length__ (e.g., 3 minutes), enter the duration here in seconds (i.e., 180). If the duration of the recorded task differs between participants, leave it as `None`. 
- __`amplify_who`__: Enter __the name of the video that should be amplified__ (the name should be the same as that given for either `cam1`, `cam2`, or `cam3`). Leave it as `no` if neither video should be amplified, and the parameter `amplify` below will be ignored. In this function, the other two videos will be muted automatically.
- __`amplify`__: The higher the number we enter here, the louder the video would be. An argument of `1` means that the volume is unchanged while an argument of `0` means that the video will be muted.
- __`excel`__: Enter __the path and name of the relevant Excel file__. 
- __other parameters__: Leave them as `None` here since the arguments are found in the Excel file. See the [examples.py](./examples.py) script for an example on manually passing arguments to these parameters.

&nbsp;

In the __Excel file for the `join3side` function__, we should have six columns that correspond to the last few parameters of this function (i.e., `children`, `main`, `start`, `end`, `corr1`, `corr2`).   

<img src="https://github.com/smy1/swlab/blob/main/script/py_eg_xl_join3.png" width=auto height="250">

__Figure 5__: _An example of an Excel file for the join3side function._

In Figure 5 above: 
- __Column A__ (or the parameter __`children`__): Contains __the names of subfolders__ in which the three camera-1, camera-2, and camera-3 videos are stored. 
- __Column B__ (or the parameter __`main`__): Contains __the name of the video camera that has the best angle of recording__. These names should be the same as that entered for the parameters `cam1`, `cam2`, and `cam3`. The video identified as the main camera will be displayed larger than the other video. 
- __Column C__ (or the parameter __`start`__): Contains __the time at which the task started__ (in seconds) in the video recording of each of the particpant. _Since we have three video recordings, use the start time of camera-1._
- __Column D__ (or the parameter __`end`__): Contains __the time at which the task ended__ (again, in seconds). This can be left blank if the duration of the task is always the same for everyone (see the parameter `dur` above).
- __Column E__ (or the parameter __`corr1`__): Contains numbers (in seconds) to correct for out-of-sync camera-2. __If the camera-2 is slower (i.e., lags behind camera-1), give a positive number__. This parameter can be left blank if the parameter `attempts` gets an argument of `1`. 
- __Column F__ (or the parameter __`corr2`__): Contains numbers (in seconds) to correct for out-of-sync camera-3. __If the camera-3 is slower (i.e., lags behind camera-1), give a positive number__. 

---

## Helpful resources
I relied heavily on the links below when writing the video-editing scripts the first time. __Note__: These links use [MoviePy v1.0](https://zulko.github.io/moviepy/v1.0.3/). 
- how to [loop multiple videos in a folder](https://stackoverflow.com/a/75788036)
- how to [concatenate multiple videos](https://www.geeksforgeeks.org/moviepy-concatenating-multiple-video-files/)
- how to [crop a video](https://stackoverflow.com/a/74586686)
- how to [calculate time difference](https://www.geeksforgeeks.org/calculate-time-difference-in-python/)
- how to [rename files](https://pynative.com/python-rename-file/)
