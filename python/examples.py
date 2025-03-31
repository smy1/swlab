#### Affiliation: SW-Lab, Dept of CFS, NTNU
#### Date: 31.03.2025
#### Author: MY Sia (with lots of help from the web, see README.md for more)
#### Example scripts to use the "editvid" function. Uses MoviePy v1.0.3

##------------------------##
##EXAMPLE 1: MERGE VIDEOS
##Concatenate short videos into a long one; batch process several cameras of several children
##Required directory: project folder -> child folder -> camera folder -> short videos (e.g., <desktop>/Peekaboo/P01/BABY/<videos>)
from editvid import merge
merge(folder="C:/Users/user/Desktop/mc_vid", ##set path to the project folder
      children=["a62_c62", "a63_c63", "a64_c64"], ##which child folder are we processing?
      camera=["BABY", "front", "SBR1", "SCREEN", "影片二"]) ##which camera folder are we processing?

##------------------------##
##EXAMPLE 2: SYNC AND OVERLAY VIDEOS
##Sync and overlay a downsized SCREEN video on a BABY video for gaze coding
##Required directory: project folder -> child folder -> videos (e.g., <desktop>/Peekaboo/P01/<videos>)
from editvid import overlay

##EXAMPLE 2a: Using info from an excel file
overlay(folder = "C:/Users/user/Desktop/mc_vid", ##set path to the project folder
        attempts = 1, ##1: correction info will be disregarded, 2 or higher: correction info will be needed
        bgcam = "baby", ##name of the background video that python should search for
        topcam = "screen", ##name of the to-be-overlaid video that python should search for
        newname = "OMI", ##name of the output video
        propsize = 0.25, ##resize the to-be-overlaid video
        dur = None,
        excel = "C:/Users/user/Desktop/mc_vid/peekbaby.xlsx",
        children=None, start=None, end=None, corr=None) ##enter info as none because they are found in the excel

##EXAMPLE 2b: Using manually entered info
overlay(folder = "C:/Users/user/Desktop/mc_vid", ##set path to the project folder
        attempts = 1, ##1: correction info will be disregarded, 2 or higher: correction info will be needed
        bgcam = "baby", ##name of the background video that python should search for
        topcam = "screen", ##name of the to-be-overlaid video that python should search for
        newname = "OMI", ##name of the output video
        propsize = 0.25, ##resize the to-be-overlaid video
        dur = None,
        excel = None, ##if not attaching an excel, enter info below
        children = ["076", "078"], ##which child folder are we processing?
        start = [20, 19], ##the seconds at which the experiment STARTED
        end = [238, 609], ##the seconds at which the experiment ENDED
        corr = [-1, 0.9]) ##manually correct out-of-sync videos

##------------------------##
##EXAMPLE 3a:
##
##Required directory:
from editvid import crop
crop(folder = "C:/Users/user/Desktop/mc_vid",
     cam = "front",
     newname = "solo",
     dur = 183,
     amplify = 5, ##do we want to mute/amplify the volume of the video?
     excel = "C:/Users/user/Desktop/mc_vid/mochibaby.xlsx",
     children=None, start=None, end=None, x1=None, x2=None, y1=None, y2=None)
##See Example 2b for manually entered info
