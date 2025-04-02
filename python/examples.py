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
      children=["a62_c62", "a63_c63", "a64_c64"], ##which 1st-level folder are we processing?
      camera=["BABY", "front", "SBR1", "SCREEN", "影片二"]) ##which 2nd-level folder are we processing?

##------------------------##
##EXAMPLE 2: SYNC AND OVERLAY VIDEOS
##Sync and overlay a downsized SCREEN video on a BABY video for gaze coding
##Required directory: project folder -> "child" subfolder -> videos
from editvid import overlay

##EXAMPLE 2a: Using info from an excel file
overlay(folder = "C:/Users/user/Desktop/mc_vid", ##set path to the project folder
        attempts = 1, ##1: correction info will be disregarded, 2 or higher: correction info will be needed
        bgcam = "baby", ##name of the base video that python should search for
        topcam = "screen", ##name of the top video that python should search for
        newname = "OMI", ##name of the output video
        propsize = 0.25, ##resize the top video
        dur = None, ##duration of the recorded task (if it is the same for everyone)
        excel = "C:/Users/user/Desktop/mc_vid/example_overlay.xlsx",
        children=None, start=None, end=None, corr=None)

##EXAMPLE 2b: Using manually entered info
overlay(folder = "C:/Users/user/Desktop/mc_vid",
        attempts = 1,
        bgcam = "baby",
        topcam = "screen",
        newname = "OMI",
        propsize = 0.25,
        dur = None,
        excel = None, ##if not attaching an excel, enter info below
        children = ["076", "078"], ##which 1st-level folder are we processing?
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
     dur = 183, ##duration of the recorded task (if it is the same for everyone)
     amplify = 5, ##do we want to amplify the volume of the video? 0=mute
     excel = None,
     children = [c63, c64],
     start = [51, 459],
     end = [],
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
        attempts = 3,
        cam1 = "front", ##name of the first video
        cam2 = "side", ##name of the second video
        newname = "sbr",
        dur = 305, ##duration of the recorded task (if it is the same for everyone)
        amplify_who = "side", ##which video should we amplify? "no" if neither
        amplify = 10, ##how much to amplify? 0 will mute the video
        mute_who = "front", ##which video should we mute? "no" if neither
        crop_who = "front", ##which video should we crop? "no" if neither
        excel = None,
        children = ["c62", "c63"],
        main = ["front", "front"], ##main is the video with the best angle
        start = [73, 334], ##the seconds at which the task STARTED, based on cam1
        end = None,
        corr = [-1.9, 0.8], ##if cam1 lags behind, give a negative number
        x1 = [644, 644], ##indicates the area of the video that we want to crop
        x2 = [2254, 2254], ##see example 3 for more
        y1 = [160, 155],
        y2 = [1092, 1092])
