#### Affiliation: SW-Lab, Dept of CFS, NTNU
#### Project: Peekaboo (aka Omi2)
#### Date: 23.06.2024 (long count: 13.0.11.12.2, 7 Iq')
#### Author: MY Sia (with lots of help from the web, see README.md for more)

#### Aim of script: Sync and overlay a downsized SCREEN video on a BABY video for gaze coding
##Input: A video showing the child's face (BABY video) and a video showing the screen that the child is watching (SCREEN video)
##Output: A single video per child with the BABY video as the main video and the SCREEN video overlaid on the top left corner
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
attempts = 4 ##the number of attempts in merging videos
children = ["076", "078"] ##which child folder are we processing?
start = [20, 19] ##the seconds at which the experiment STARTED in the SCREEN video
end = [238, 609] ##the seconds at which the experiment ENDED in the SCREEN video
## Manually correct out-of-sync baby videos:
corr = [-1, 0.9]
##This is used only in the corrective rounds (i.e., second attempt or later)
##if the BABY video LAGS BEHIND the screen video, give a POSITIVE number; OTHERWISE, give a NEGATIVE number
##a larger absolute number will introduce a larger time difference between the two videos

n = 0
#### Check entry of information
if len(start) != len(children):
    print("The number of 'START' does not match the number of 'GROUP'.")
elif len(end) != len(children):
    print("The number of 'END' does not match the number of 'GROUP'.")
elif attempts > 1 and len(corr) != len(children):
    print("The number of 'CORR' does not match the number of 'GROUP'.")
else:
    #### Loop through several babies
    for child in children:
        ## (a)Prepare videos:
        vid_path = Path(f"{folder}/{child}/")
        ## Baby video
        baby_list = glob.glob(f"{vid_path}/{child}_baby*.mp4")
        baby_vid = VideoFileClip(baby_list[0])
        t_baby = baby_list[0][-10:-5]
        t_baby = t_baby.replace("M", ":")
        t_baby = datetime.strptime(t_baby, "%M:%S")
        ## Screen video
        screen_list = glob.glob(f"{vid_path}/{child}_screen*.mp4")
        screen_vid = VideoFileClip(screen_list[0])
        screen_vid = screen_vid.resize(0.25).margin(5) ##downsize video to 25% and add a 5px border
        t_screen = screen_list[0][-10:-5]
        t_screen = t_screen.replace("M", ":")
        t_screen = datetime.strptime(t_screen, "%M:%S")
        ## Get time difference between videos
        diff = t_screen - t_baby
        diff = diff.total_seconds()
        ## (b)Overlay screen video on baby video at the top left corner:
        if attempts == 1: ##first round
            x = 0 ##no manual correction
            all_vid = CompositeVideoClip([baby_vid.subclip(start[n]+diff, end[n]+diff),
                                        screen_vid.subclip(start[n], end[n]).set_position((0, 50))])
        elif attempts > 1: ##corrective round
            x = corr[n]
            all_vid = CompositeVideoClip([baby_vid.subclip(start[n]+diff+corr[n], end[n]+diff+corr[n]),
                                        screen_vid.subclip(start[n], end[n]).set_position((0, 50))])
        ## (c)Save composite video:
        all_vid.write_videofile(f"{folder}/{child}/{child}_OMI_merged{attempts}_corr={x}.mp4")
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        n += 1 ##now, do the next one

#### END OF SCRIPT ####
