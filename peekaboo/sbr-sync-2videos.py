#### Affiliation: SW-Lab, Dept of CFS, NTNU
#### Project: Peekaboo (aka Omi2)
#### Date: 23.06.2024 (long count: 13.0.11.12.2, 7 Iq')
#### Author: MY Sia (with lots of help from the web, see README.md for more)

#### Aim of script: Sync and combine two SBR (shared book reading) videos for PEER coding
##Input: Two video recordings (from different angles) showing a parent-child dyad during SBR
##Output: A single video per child with one of the recordings as the main video and the other as the minor video
##Recommended directory: project folder -> child folder -> videos (e.g., <desktop>/Peekaboo/P01/<videos>)
##Requirement: This script was written using Python 3.12.4. Various Python modules need to be installed. See README.md for more.

########################################
#### START HERE:
## Import everything needed to edit video clips
import glob
from pathlib import Path
from moviepy.editor import *
from datetime import datetime ##to calculate time difference between videos
import cv2 ##so that videos can be resized properly
import winsound ##not necessary, just to get Python to notify me when it is done

folder = "C:/Users/user/Desktop/peekaboo/peekadata" ##set path to the project folder

########################################
#### Enter information
dur = 334 ##duration of the SBR is fixed: 5min 34sec
children = ["035", "038", "051", "066"] ##which child folder are we looping?
major = [1, 2, 3, 2] ##the camera number that has the best view of the parent-child dyad
minor = [2, 1, 1, 1] ##the other camera number
start = [20, 60, 25, 5] ##the seconds at which SBR STARTED in the MAIN video

## Manually correct out-of-sync minor videos:
corr = [2, 1]
##this is used only in the corrective rounds (i.e., second attempt or later)
##if the MINOR video LAGS BEHIND, give a POSITIVE number; OTHERWISE, give a NEGATIVE number
##a larger absolute number given will introduce a larger time difference between the videos
attempts = int(input(f"Please enter the attempt number in merging videos. "))

n = 0
#### Check entry of information
if len(major) != len(children):
    print("The number of 'MAJOR' does not match the number of 'CHILDREN'.")
elif len(minor) != len(children):
    print("The number of 'MINOR' does not match the number of 'CHILDREN'.")
elif len(start) != len(children):
    print("The number of 'START' does not match the number of 'CHILDREN'.")
elif attempts > 1 and len(corr) != len(children):
    print("The number of 'CORR' does not match the number of 'CHILDREN'.")
else:
    #### Loop through several babies
    for child in children:
        ## (a)Prepare videos:
        vid_path = Path(f"{folder}/{child}/")
        ## The main video
        major_list = glob.glob(f"{vid_path}/{child}_sbr{major[n]}*.mp4")
        major_vid = VideoFileClip(major_list[0])
        t_major = major_list[0][-10:-5]
        t_major = t_major.replace("M", ":")
        t_major = datetime.strptime(t_major, "%M:%S")
        ## The minor video
        minor_list = glob.glob(f"{vid_path}/{child}_sbr{minor[n]}*.mp4")
        minor_vid = VideoFileClip(minor_list[0], audio=False)
        t_minor = minor_list[0][-10:-5]
        t_minor = t_minor.replace("M", ":")
        t_minor = datetime.strptime(t_minor, "%M:%S")
        ## Get time difference between videos
        diff = t_major - t_minor
        diff = diff.total_seconds()
        ## (b)Sync the videos:
        end = start[n] + dur ##the seconds at which SBR should have ended in the main video
        ## But some videos may not be long enough to be clipped off
        if end > major_vid.duration:
            major_vid = major_vid.subclip(start[n], major_vid.duration)
        else:
            major_vid = major_vid.subclip(start[n], end)
        major_vid = major_vid.resize(0.7).volumex(3).margin(5) ##increase volume and add a border
        if attempts == 1: ##first round
            x = 0 ##no manual correction
            if end+diff > minor_vid.duration:
                minor_vid = minor_vid.subclip(start[n]+diff, minor_vid.duration)
            else:
                minor_vid = minor_vid.subclip(start[n]+diff, end+diff)
        elif attempts > 1: ##corrective round
            x = corr[n]
            if end+diff+corr[n] > minor_vid.duration:
                minor_vid = minor_vid.subclip(start[n]+diff+corr[n], minor_vid.duration)
            else:
                minor_vid = minor_vid.subclip(start[n]+diff+corr[n], end+diff+corr[n])
        minor_vid = minor_vid.resize(0.4).margin(8)
        final_sbr = clips_array([[major_vid, minor_vid], ])
        ## (c)Save the output:
        final_sbr.write_videofile(f"{folder}/{child}/{child}_allSBR{attempts}_corr={x}.mp4")
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        n += 1 ##now, do the next one

#### END OF SCRIPT ####
