#### Affiliation: SW-Lab, Dept of CFS, NTNU
#### Project: Peekaboo (aka Omi2)
#### Date: 23.06.2024 (long count: 13.0.11.12.2, 7 Iq')
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
dur = 334 ##duration of the SBR is fixed: 5min 34sec
problem = [] ##empty holder to store problematic IDs

#### Enter information
children = ["059", "065", "070", "071"] ##which child folder are we looping?
main = [3, 1, 3, 2] ##the number of the MAIN SBR video (1, 2, or 3)
start = [28, 48, 6, 53] ##the seconds at which SBR STARTED in the MAIN video

## Manually correct out-of-sync minor videos:
corr1 = [-2.5, -2, -1, 0] ##to correct the minor-1 video (top right corner)
corr2 = [-2.5, 0.6, -2, 0] ##to correct the minor-2 video (bottom right corner)
##these are used only in the corrective rounds (i.e., second attempt or later)
##if the MINOR video LAGS BEHIND, give a POSITIVE number; OTHERWISE, give a NEGATIVE number
##a larger absolute number given will introduce a larger time difference between the videos
attempts = int(input(f"Please enter the attempt number in merging videos. "))

n = 0
#### Check entry of information
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
            ## Identify the main video and the other two will be the minor videos
            allowed = [0, 1, 2]
            major = main[n] - 1
            allowed.remove(major)
            minor1 = allowed[0]
            minor2 = allowed[1]
            ## The main video
            major_vid = VideoFileClip(vid_list[major])
            t_major = vid_list[major][-10:-5]
            t_major = t_major.replace("M", ":")
            t_major = datetime.strptime(t_major, "%M:%S")
            ## The first minor video (top right)
            minor_vid1 = VideoFileClip(vid_list[minor1])
            t_minor1 = vid_list[minor1][-10:-5]
            t_minor1 = t_minor1.replace("M", ":")
            t_minor1 = datetime.strptime(t_minor1, "%M:%S")
            ## The second minor video (bottom right)
            minor_vid2 = VideoFileClip(vid_list[minor2])
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
            ## (c)Resize videos:
            final_min = clips_array([[minor_vid1.resize(width=480).margin(4)], ##add a border
                                     [minor_vid2.resize(width=480).margin(4)]])
            final_all = clips_array([[major_vid.resize(height=720).volumex(3).margin(5), ##increase volume
                                      final_min.resize(height=720).volumex(0).margin(4)], ])
            ## (d)Save the output:
            final_all.write_videofile(f"{folder}/{child}/{child}_allSBR{attempts}_{x}.mp4")
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            n += 1 ##now, do the next one

#### Were there any problematic camera folders?
if len(problem) > 0:
    for x in problem:
        print(x)
else:
    print("All the videos were concatenated successfully.")

#### END OF SCRIPT
