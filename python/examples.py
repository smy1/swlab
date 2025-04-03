#### Affiliation: SW-Lab, Dept of CFS, NTNU
#### Date: 02.04.2025
#### Author: MY Sia (with lots of help from the web, see README.md for more)
#### Example scripts to use the "editvid" function. Requires MoviePy v1.0.3

##------------------------##
##EXAMPLE 1: MERGE VIDEOS
##Concatenate short videos into a long one; batch process several cameras of several children
##Required directory: project folder -> "child" subfolder -> "camera" subfolder -> short videos
from editvid import merge
merge(folder="C:/Users/user/Desktop/mc_vid", ##set path to the project folder
      children=["a62_c62", "a63_c63", "a64_c64"], ##which 1st-level subfolder are we processing?
      camera=["BABY", "front", "SBR1", "SCREEN", "影片二"]) ##which 2nd-level subfolder are we processing?

##------------------------##
##EXAMPLE 2: SYNC AND OVERLAY VIDEOS
##Sync and overlay a downsized "top" video on a "base" video
##Required directory: project folder -> "child" subfolder -> videos
from editvid import overlay

##EXAMPLE 2a: Pass arguments by loading an excel file (see README.md for more)
overlay(folder = "C:/Users/user/Desktop/mc_vid", 
        attempts = 1, 
        bgcam = "baby", 
        topcam = "screen", 
        newname = "OMI", 
        propsize = 0.25, 
        dur = None, 
        excel = "C:/Users/user/Desktop/mc_vid/example_overlay.xlsx",
        children=None, start=None, end=None, corr=None)

##EXAMPLE 2b: Manually pass arguments to the parameters
overlay(folder = "C:/Users/user/Desktop/mc_vid", ##set path to the project folder
        attempts = 1, ##if 1: "corr" below will be disregarded; if 2 or larger: "corr" will be needed
        bgcam = "baby", ##name of the base video that python should search for
        topcam = "screen", ##name of the top video that python should search for
        newname = "OMI", ##name of the output video
        propsize = 0.25, ##resize the top video
        dur = None, ##standard duration of the recorded task, if "None", pass arguments to parameter "end" below
        excel = None, ##if not attaching an excel, give arguments below
        ##the following parameters must be entered as a list
        children = ["076", "078"], ##which 1st-level subfolder are we processing?
        start = [20, 19], ##the seconds at which the task STARTED, based on topcam
        end = [238, 609], ##the seconds at which the task ENDED
        corr = [-1, 0.9]) ####if topcam lags behind, give a negative number

##------------------------##
##EXAMPLE 3: CROP VIDEOS
##Crop videos
##Required directory: project folder -> "child" subfolder -> videos
from editvid import crop
crop(folder = "C:/Users/user/Desktop/mc_vid", ##set path to the project folder
     cam = "front", ##name of videos that python should crop
     newname = "solo", ##name of the output video
     dur = 183, ##standard duration of the recorded task, if "None", pass arguments to parameter "end" below
     amplify = 5, ##1=original volume, a larger number means volume amplified, 0=mute
     excel = None,
     ##the following parameters must be entered as a list
     children = [c63, c64], ##which 1st-level subfolder are we processing?
     start = [51, 459],
     end = [], ##the seconds at which the task ENDED
     x1 = [644, 644], ##start of the width that we want to crop
     x2 = [2254, 2254], ##end of the width that we want to crop
     y1 = [175, 170], ##start of the height that we want to crop
     y2 = [1092, 1092]) ##end of the height that we want to crop

##------------------------##
##EXAMPLE 4: SYNC AND JUXTAPOSE VIDEOS
##Sync the time of two videos and place them side-by-side with one video larger than the other
##Required directory: project folder -> "child" subfolder -> videos
from editvid import join2side
join2side(folder = "C:/Users/user/Desktop/mc_vid",
        attempts = 3, ##if 1: "corr" below will be disregarded; if 2 or larger: "corr" will be needed
        cam1 = "front", ##name of the first video that python should search for
        cam2 = "side", ##name of the second video that python should search for
        newname = "sbr", ##name of the output video
        dur = 305, ##standard duration of the recorded task, if "None", pass arguments to parameter "end" below
        amplify_who = "side", ##name of the video that should be amplified. "no" if neither
        amplify = 10, ##1=original volume, a larger number means volume amplified, 0=mute
        mute_who = "front", ##name of the video that should be muted. "no" if neither
        crop_who = "front", ##name of the video that should be cropped. "no" if neither
        excel = None,
        ##the following parameters must be entered as a list
        children = ["c62", "c63"], ##which 1st-level subfolder are we processing?
        main = ["front", "front"], ##name of the video with the best angle
        start = [73, 334], ##the seconds at which the task STARTED, based on cam1
        end = [], ##the seconds at which the task ENDED
        corr = [-1.9, 0.8], ##if cam1 lags behind, give a negative number
        x1 = [644, 644], ##indicates the area of the video that we want to crop
        x2 = [2254, 2254], ##see example 3 for more
        y1 = [160, 155],
        y2 = [1092, 1092])
