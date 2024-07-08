#### Affiliation: SW-Lab, Dept of CFS, NTNU
#### Project: Peekaboo (aka Omi2)
#### Date: 08.07.2024 (long count: 13.0.11.12.17, 9 No'j)
#### Author: MY Sia (with lots of help from the web, see README.md for more)

#### Aim of script: Sync and combine three SBR (shared book reading) videos for PEER coding
##Input: Three video recordings (from different angles) showing a parent-child dyad during SBR
##Output: A single video per child with one of the recordings as the main video and two others as the minor video
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
dur = 334 ##duration of the SBR: 5min 34sec
problem = [] ##empty holder to store problematic IDs

#### Enter information
attempts = 2 ##the number of attempts in merging videos
children = ["079", "080", "081", "082", "083", "084", "085", "086"] ##which child folder are we looping?
main = [3, 3, 1, 3, 3, 3, 3, 2] ##the camera number (1, 2, or 3) that has the best view of the parent-child dyad
start = [34.5, 22, 55, 51.5, 19, 60, 35, 31] ##the seconds at which SBR STARTED in the MAIN video
## Manually correct out-of-sync minor videos:
corr1 = [1, 0.8, -0.8, 2, 1, 1, 2, 0] ##to correct the minor-1 video (top right corner)
corr2 = [-1, -0.8, 0.8, 1, 2, 1, 1, -1] ##to correct the minor-2 video (bottom right corner)
## - these are used only in the corrective rounds (i.e., second attempt or later)
## - if the MINOR video LAGS BEHIND, give a POSITIVE number; OTHERWISE, give a NEGATIVE number
## - a larger absolute number given will introduce a larger time difference between the videos

#### Check entry of information
n = 0 ##to loop the information entered above
if len(main) != len(children):
    print("The number of 'MAIN' does not match the number of 'CHILDREN'.")
elif len(start) != len(children):
    print("The number of 'START' does not match the number of 'CHILDREN'.")
elif attempts > 1 and (len(corr1) != len(children) or len(corr2) != len(children)):
    print("The number of 'CORR1' or 'CORR2' does not match the number of 'CHILDREN'.")
else:
    #### Loop through several babies
    for child in children:
        vid_path = Path(f"{folder}/{child}/")
        vid_list = glob.glob(f"{vid_path}/{child}_sbr*.mp4")
        ## Check for problematic cases
        if len(vid_list) != 3:
            x = f"There should only be 3 SBR videos in {child}'s folder."
            problem.append(x)
            n += 1 ##skip this problematic case
        else:
            ## (a)Prepare videos:
            ## Initial video settings: muted + black borders
            vol_mj = vol_mn1 = vol_mn2 = 0
            col_mj = col_mn1 = col_mn2 = (0, 0, 0)
            ## Identify the main video and the other two will be the minor videos
            allowed = [0, 1, 2]
            major = main[n] - 1
            allowed.remove(major)
            minor1, minor2 = allowed[0], allowed[1]
            ## Search for SBR2-camera, which happened to have the clearest audio
            ## - retain only SBR2's audio, & add a blue border to SBR2-camera
            ## The main video
            major_vid = VideoFileClip(vid_list[major])
            if vid_list[major][-15:-11] == "sbr2":
                vol_mj = 6
                col_mj = (0, 0, 255)
            t_major = vid_list[major][-10:-5]
            t_major = t_major.replace("M", ":")
            t_major = datetime.strptime(t_major, "%M:%S")
            ## The first minor video (top right)
            minor_vid1 = VideoFileClip(vid_list[minor1])
            if vid_list[minor1][-15:-11] == "sbr2":
                vol_mn1 = 6
                col_mn1 = (0, 0, 255)
            t_minor1 = vid_list[minor1][-10:-5]
            t_minor1 = t_minor1.replace("M", ":")
            t_minor1 = datetime.strptime(t_minor1, "%M:%S")
            ## The second minor video (bottom right)
            minor_vid2 = VideoFileClip(vid_list[minor2])
            if vid_list[minor2][-15:-11] == "sbr2":
                vol_mn2 = 6
                col_mn2 = (0, 0, 255)
            t_minor2 = vid_list[minor2][-10:-5]
            t_minor2 = t_minor2.replace("M", ":")
            t_minor2 = datetime.strptime(t_minor2, "%M:%S")
            ## Get time difference between videos
            diff1 = t_major - t_minor1
            diff1 = diff1.total_seconds() ##between major and minor-1
            diff2 = t_major - t_minor2
            diff2 = diff2.total_seconds() ##between major and minor-2
            ## (b)Sync videos:
            end = start[n] + dur ##the seconds at which SBR should have ended in the main video
            ## But some videos may not be long enough to be clipped off
            if end > major_vid.duration:
                major_vid = major_vid.subclip(start[n], major_vid.duration)
            else:
                major_vid = major_vid.subclip(start[n], end)
            if attempts == 1: ##first round
                x = "corr=0" ##no manual correction
                if end+diff1 > minor_vid1.duration:
                    minor_vid1 = minor_vid1.subclip(start[n]+diff1, minor_vid1.duration)
                else:
                    minor_vid1 = minor_vid1.subclip(start[n]+diff1, end+diff1)
                if end+diff2 > minor_vid2.duration:
                    minor_vid2 = minor_vid2.subclip(start[n]+diff2, minor_vid2.duration)
                else:
                    minor_vid2 = minor_vid2.subclip(start[n]+diff2, end+diff2)
            elif attempts > 1: ##corrective round
                x = f"corr1={corr1[n]}_corr2={corr2[n]}"
                if end+diff1+corr1[n] > minor_vid1.duration:
                    minor_vid1 = minor_vid1.subclip(start[n]+diff1+corr1[n], minor_vid1.duration)
                else:
                    minor_vid1 = minor_vid1.subclip(start[n]+diff1+corr1[n], end+diff1+corr1[n])
                if end+diff2+corr2[n] > minor_vid2.duration:
                    minor_vid2 = minor_vid2.subclip(start[n]+diff2+corr2[n], minor_vid2.duration)
                else:
                    minor_vid2 = minor_vid2.subclip(start[n]+diff2+corr2[n], end+diff2+corr2[n])
            ## (c)Resize videos, change volume, add borders:
            final_min = clips_array([[minor_vid1.resize(width=480).volumex(vol_mn1).margin(8, color=col_mn1)],
                                     [minor_vid2.resize(width=480).volumex(vol_mn2).margin(8, color=col_mn2)]])
            final_all = clips_array([[major_vid.resize(height=720).volumex(vol_mj).margin(8, color=col_mj),
                                      final_min.resize(height=720)], ])
            ## (d)Save the output:
            final_all.write_videofile(f"{folder}/{child}/{child}_allSBR{attempts}_{start[n]}_{x}.mp4")
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            n += 1 ##now, do the next one

#### Were there any problematic camera folders?
if len(problem) > 0:
    for i in problem:
        print(i)
else:
    print("All the videos were concatenated successfully.")

#### END OF SCRIPT
