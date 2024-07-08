#### Affiliation: SW-Lab, Dept of CFS, NTNU
#### Project: Peekaboo (aka Omi2)
#### Date: 08.07.2024 (long count: 13.0.11.12.17, 9 No'j)
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
#### Set default values
dur = 334 ##duration of the SBR is fixed: 5min 34sec
problem = [] ##empty holder to store problematic IDs

#### Enter information
attempts = 2 ##the number of attempts in merging videos
children = ["074", "075"] ##which child folder are we looping?
major = [2, 1] ##the camera (1, 2, or 3) that has the best view of the parent-child dyad
start = [29, 32] ##the seconds at which SBR STARTED in the MAIN video
## Manually correct out-of-sync minor videos:
corr = [1, -0.7]
## - this is used only in the corrective rounds (i.e., second attempt or later)
## - if the MINOR video LAGS BEHIND, give a POSITIVE number; OTHERWISE, give a NEGATIVE number
## - a larger absolute number given will introduce a larger time difference between the videos

#### Check entry of information
n = 0 ##to loop the information entered above
if len(major) != len(children):
    print("The number of 'MAJOR' does not match the number of 'CHILDREN'.")
elif len(start) != len(children):
    print("The number of 'START' does not match the number of 'CHILDREN'.")
elif attempts > 1 and len(corr) != len(children):
    print("The number of 'CORR' does not match the number of 'CHILDREN'.")
else:
    #### Loop through several babies
    for child in children:
        ## (a)Prepare videos:
        vid_path = Path(f"{folder}/{child}/")
        vid_list = glob.glob(f"{vid_path}/{child}_sbr*.mp4")
        ## Check for problematic cases
        if len(vid_list) != 2:
            x = f"There should only be 2 SBR videos in {child}'s folder."
            problem.append(x)
            n += 1 ##skip this problematic case
        else:
            ## Identify main and minor videos
            if vid_list[0][-15:-11] == f"sbr{major[n]}":
                maj_n, min_n = 0, 1
            else:
                maj_n, min_n = 1, 0
            ## The main video
            major_vid = VideoFileClip(vid_list[maj_n])
            t_major = vid_list[maj_n][-10:-5]
            t_major = t_major.replace("M", ":")
            t_major = datetime.strptime(t_major, "%M:%S")
            ## The minor video
            minor_vid = VideoFileClip(vid_list[min_n])
            t_minor = vid_list[min_n][-10:-5]
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
            ## Resize, set volumes, & border colour
            if vid_list[maj_n][-15:-11] == f"sbr2":
                vol_maj, vol_min = 6, 0
                col_maj, col_min = (0, 0, 255), (0, 0, 0)
            elif vid_list[min_n][-15:-11] == f"sbr2":
                vol_maj, vol_min = 0, 6
                col_maj, col_min = (0, 0, 0), (0, 0, 255)
            else:
                vol_maj, vol_min = 10, 0
                col_maj, col_min = (0, 0, 255), (0, 0, 0)
            major_vid = major_vid.resize(0.7).volumex(vol_maj).margin(8, color=col_maj)
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
            minor_vid = minor_vid.resize(0.4).volumex(vol_min).margin(8, color=col_min)
            final_sbr = clips_array([[major_vid, minor_vid], ])
            ## (c)Save the output:
            final_sbr.write_videofile(f"{folder}/{child}/{child}_allSBR{attempts}_{start[n]}_corr={x}.mp4")
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            n += 1 ##now, do the next one

#### Were there any problematic camera folders?
if len(problem) > 0:
    for i in problem:
        print(i)
else:
    print("All the videos were concatenated successfully.")

#### END OF SCRIPT ####
