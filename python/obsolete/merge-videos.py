#### Affiliation: SW-Lab, Dept of CFS, NTNU
#### Project: Peekaboo (aka Omi2)
#### Date: 23.06.2024 (long count: 13.0.11.12.2, 7 Iq')
#### Author: MY Sia (with lots of help from the web, see README.md for more)

#### Aim of script: Concatenate short videos into a long one; batch process several cameras of several children
##Input: Multiple videos (each has a duration of 1 minute) stored in a folder (one folder for each camera)
##Output: A single video per camera per child
##Recommended directory: project folder -> child folder -> camera folder -> short videos (e.g., <desktop>/Peekaboo/P01/BABY/<videos>)
##Requirement: This script was written using Python 3.12.4. Various Python modules need to be installed. See README.md for more.

########################################
#### START HERE:
## Import everything needed to edit video clips
import glob
from pathlib import Path
from moviepy.editor import *
import winsound ##not necessary, just to get Python to notify me when it is done

print("Remember to MOVE CAPPING videos in the BABY folder to a sub-folder.")
folder = "C:/Users/user/Desktop/peekaboo/peekadata" ##set path to the project folder

########################################
children = ["031", "038", "042", "063", "071"] ##which child folder are we processing?
camera = ["BABY", "SCREEN", "SBR1", "SBR2", "SBR3"] ##which camera folder are we processing?
problem = [] ##empty holder to store problematic IDs

#### Loop through baby folders
for child in children:
    ## Loop through camera folders
    for cam in camera:
        video_list = [] ##empty holder to store videos
        files_path = Path(f"{folder}/{child}/{cam}")
        file_list = glob.glob(f"{files_path}/*.mp4")
        ## (a)Check for problematic cases:
        if len(file_list) < 2:
            x = f"Nothing to join in {child}'s {cam} folder."
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
            cam2 = cam.lower()
            joined.write_videofile(f"{folder}/{child}/{child}_{cam2}_{first_frame}.mp4")
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

#### Were there any problematic camera folders?
if len(problem) > 0:
    for x in problem:
        print(x)
else:
    print("All the videos were concatenated successfully.")

#### END OF SCRIPT ####
