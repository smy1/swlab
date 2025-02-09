#### Affiliation: SW-Lab, Dept of CFS, NTNU
#### Project: MoChi
#### Date: 09.02.2025
#### Author: MY Sia (modified from the Peekaboo project)

#### Aim of script: Concatenate short videos into a long one; batch process several cameras of several dyads
##Input: Multiple videos (each has a duration of 1 minute) stored in a folder (one folder for each camera)
##Output: A single video per camera per dyad
##Recommended directory: project folder -> dyad folder -> camera folder -> short videos
##Requirement: This script was written using Python 3.12.4. Various Python modules need to be installed. See README.md for more.

########################################
#### START HERE:
## Import everything needed to edit video clips
import os ##to rename files, where necessary
import glob
from pathlib import Path
from moviepy.editor import *
from playsound import playsound ##just for notification

folder = "C:/Users/user/Desktop/mc_vid" ##set path to the project folder

########################################
dyads = ["a08_c08", "a09_c09", "a10_c10"] ##which dyad folder are we processing?
camera = ["front", "side"] ##which camera folder are we processing?

#### Loop through dyad folders
for dyad in dyads:
    ## Loop through camera folders
    for cam in camera:
        video_list = [] ##empty holder to store videos
        files_path = Path(f"{folder}/{dyad}/{cam}")
        file_list = glob.glob(f"{files_path}/*.mp4")
        ## (a)Check for problematic cases:
        if len(file_list) < 2:
            print(f"Nothing to join in {dyad}'s {cam} folder.")
        ## if the recording passed the hour (e.g., 10:59 to 11:00)
        elif  file_list[0][-22:-20] == "\\0" and file_list[-1][-22:-20] == "\\5":
            for f_name in file_list:
                p1 = f_name[0:-22]
                xx = f_name[-22:-20]
                p2 = f_name[-20:]
                ## rename 0 to 6 and 1 to 7
                if xx == "\\0":
                    new_fname = f"{p1}\\6{p2}"
                    os.rename(f_name, new_fname)
                elif xx == "\\1":
                    new_fname = f"{p1}\\7{p2}"
                    os.rename(f_name, new_fname)
            ## after renaming videos in both camera folders
            if cam == "side":
                dyads.append(dyad) ##add the dyad back to the loop for merging
                playsound("C:/Users/user/Desktop/ok.mp3")
        else:
            ## (b)Load mp4 files as videos:
            for i in file_list:
                print(i) ##which video is being processed?
                clip = VideoFileClip(i)
                video_list.append(clip)
            ## (c)Merge & save the output:
            joined = concatenate_videoclips(video_list)
            joined = joined.set_fps(fps=30) ##standardise frame per second for all videos
            first_frame = file_list[0][-21:-15]
            child = dyad[4:7]
            joined.write_videofile(f"{folder}/{dyad}/{cam}_{child}_{first_frame}.mp4")


playsound("C:/Users/user/Desktop/done.mp3")
quit()
#### END OF SCRIPT ####
