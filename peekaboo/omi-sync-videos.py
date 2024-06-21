#### Affiliation: SW-Lab, Dept of CFS, NTNU
#### Project: Peekaboo (aka Omi2)
#### Date: 21.06.2024 (long count: 13.0.11.12.0, 5 Ajpu')
#### Author: MY Sia (with lots of help from the web, see README for more)

#### Aim of script: Sync and overlay a downsized SCREEN video on a BABY video for gaze coding
##Input: A video showing the child's face (BABY video) and a video showing the screen that the child is watching (SCREEN video)
##Output: A single video per child with the BABY video as the main video and the SCREEN video overlaid on the top left corner
##Recommended directory: project folder -> child folder -> videos (e.g., <desktop>/Peekaboo/P01/<videos>)
##Requirement: This script was written using Python 3.12.4. Various Python modules need to be installed. See README for more.

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
#### LOOP THROUGH SEVERAL BABIES:
group = ["062", "063"] ##which child folder are we processing?
start = [7, 19] ##the seconds at which the experiment STARTED in the SCREEN video
end = [473, 637] ##the seconds at which the experiment ENDED in the SCREEN video

## To correct for out-of-sync videos:
corr = [-0.2, 0]
##This is used only in the corrective rounds (i.e., second attempt or later)
##If the baby video lags behind the screen video, give a positive number; otherwise, give a negative number
##a larger absolute number will introduce a larger time difference between the baby and screen videos
attempts = int(input(f"Please enter the attempt number in merging videos. "))

n = 0
if len(start) != len(group):
    print("The number of 'START' does not match the number of 'GROUP'.")
elif len(end) != len(group):
    print("The number of 'END' does not match the number of 'GROUP'.")
elif attempts > 1 and len(corr) != len(group):
    print("The number of 'CORR' does not match the number of 'GROUP'.")
else:
    for child in group:
        ## (a)Prepare videos:
        vid_path = Path(f"{folder}/{child}/")
        ## Baby video
        baby_list = glob.glob(f"{vid_path}/{child}_baby*.mp4")
        baby_vid = VideoFileClip(baby_list[0])
        ## Get start time of baby video
        t_baby = baby_list[0][-10:-5]
        t_baby = t_baby.replace("M", ":")
        t_baby = datetime.strptime(t_baby, "%M:%S")
        ## Screen video
        screen_list = glob.glob(f"{vid_path}/{child}_screen*.mp4")
        screen_vid = VideoFileClip(screen_list[0])
        screen_vid = screen_vid.resize(0.25).margin(5) ##downsize video to 25% and add a 5px border
        ## Get start time of screen video
        t_screen = screen_list[0][-10:-5]
        t_screen = t_screen.replace("M", ":")
        t_screen = datetime.strptime(t_screen, "%M:%S")
        ## Get time difference between videos
        diff = t_screen - t_baby
        diff = diff.total_seconds()
        ## (b)Overlay screen video on baby video at the top left corner:
        ## Sync the FIRST ROUND:
        if attempts == 1:
            if diff < 0: ##screen started recording before baby
                all_vid = CompositeVideoClip([baby_vid.subclip(start[n]-abs(diff), end[n]-abs(diff)),
                                            screen_vid.subclip(start[n], end[n]).set_position((0, 50))])
            elif diff > 0: ##screen started recording after baby
                all_vid = CompositeVideoClip([baby_vid.subclip(start[n]+diff, end[n]+diff),
                                            screen_vid.subclip(start[n], end[n]).set_position((0, 50))])
            else: ##no difference in recording time
                all_vid = CompositeVideoClip([baby_vid.subclip(start[n], end[n]),
                                        screen_vid.subclip(start[n], end[n]).set_position((0, 50))])
        ## Sync the CORRECTIVE ROUND:
        elif attempts > 1:
            if diff < 0: ##screen started recording before baby
                all_vid = CompositeVideoClip([baby_vid.subclip(start[n]-abs(diff), end[n]-abs(diff)),
                                            screen_vid.subclip(start[n]+(corr[n]*-1), end[n]+(corr[n]*-1)).set_position((0, 50))])
            elif diff > 0: ##screen started recording after baby
                all_vid = CompositeVideoClip([baby_vid.subclip(start[n]+diff+corr[n], end[n]+diff+corr[n]),
                                            screen_vid.subclip(start[n], end[n]).set_position((0, 50))])
            else: ##no difference in recording time
                all_vid = CompositeVideoClip([baby_vid.subclip(start[n]+corr[n], end[n]+corr[n]),
                                        screen_vid.subclip(start[n], end[n]).set_position((0, 50))])
        ## (c)Save composite video
        all_vid.write_videofile(f"{folder}/{child}/{child}_OMI_merged{attempts}_{start[n]}_{end[n]}_{diff}.mp4")
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        n += 1 ##now, do the next one

#### END OF SCRIPT ####
