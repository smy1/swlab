#### Affiliation: SW-Lab, Dept of CFS, NTNU
#### Project: MoChi
#### Date: 04.02.2025
#### Author: MY Sia (modified from the Peekaboo project)

#### Aim of script: Concatenate short videos into a long one; batch process several cameras of several dyads
##Input: Multiple videos (each has a duration of 1 minute) stored in a folder (one folder for each camera)
##Output: A single video per camera per dyad
##Recommended directory: project folder -> dyad folder -> camera folder -> short videos
##Requirement: This script was written using Python 3.12.4. Various Python modules need to be installed. See README.md for more.

########################################
#### START HERE:
## Import everything needed to edit video clips
import glob
from pathlib import Path
from moviepy.editor import *

folder = "C:/Users/user/Desktop/mc_vid" ##set path to the project folder

########################################
dyads = ["pa5_pc5", "pa6_pc6", "pa7_pc7", "pa8_pc8"] ##which dyad folder are we processing?
camera = ["front", "side"] ##which camera folder are we processing?
problem = [] ##empty holder to store problematic IDs

#### Loop through dyad folders
for dyad in dyads:
    ## Loop through camera folders
    for cam in camera:
        video_list = [] ##empty holder to store videos
        files_path = Path(f"{folder}/{dyad}/{cam}")
        file_list = glob.glob(f"{files_path}/*.mp4")
        ## (a)Check for problematic cases:
        if len(file_list) < 2:
            x = f"Nothing to join in {dyad}'s {cam} folder."
            problem.append(x)
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

#### Were there any problematic camera folders?
if len(problem) > 0:
    for x in problem:
        print(x)
else:
    print("All the videos were concatenated successfully.")

#### END OF SCRIPT ####
