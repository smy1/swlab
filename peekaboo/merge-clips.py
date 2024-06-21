#### Affiliation: SW-Lab, Dept of CFS, NTNU
#### Project: Peekaboo (aka Omi2)
#### Date: 21.06.2024 (long count: 13.0.11.12.0, 5 Ajpu')
#### Author: MY Sia (with lots of help from the web, see README.txt for more)

#### Aim of script: Concatenate second-long videos which are stored in sub-"minute"-folder; batch process several children
##Input: Multiple videos (each has a duration of a few seconds) stored in a sub-"minute"-folder (i.e., these videos add up to be about 1 minute) within a camera folder
##Output: A single video per child
##Recommended directory: project folder -> child folder -> camera folder -> minute folder -> short videos (e.g., <desktop>/Peekaboo/P01/BABY/37/<videos>)
##Requirement: This script was written using Python 3.12.4. Various Python modules need to be installed. See README.txt for more.

########################################
#### START HERE:
## Import everything needed to edit video clips
## Remember to move all BABY capping videos to a sub-folder (ask the PI if you don't understand this part)
import glob
from pathlib import Path
from moviepy.editor import *
import winsound ##not necessary, just to get Python to notify me when it is done

folder = "C:/Users/user/Desktop/peekaboo/peekadata" ##set path to the project folder

########################################
#### LOOP THROUGH SEVERAL BABIES:
group = ["002"] ##which child folder are we processing?
fold = "SBR1" ##what is the name of the camera that stores videos in sub-"minute"-folders?
r1 = [37] ##what is the number of the FIRST sub-folder that you want to merge?
r2 = [43] ##what is the number of the LAST sub-folder that you want to merge?

n = 0
for child in group:
    ## (1)Concatenate second-long videos:
    omi = range(r1[n], r2[n]+1) ##the folder numbers that we want to concatenate
    for num in omi:
        ## Need to add 0 for sub-folders 01 - 09
        if num < 10:
            num = str(0) + str(num)
        loaded_video_list = [] ##empty holder to store the videos
        video_files_path = Path(f"{folder}/{child}/{fold}/{num}")
        video_file_list = glob.glob(f"{video_files_path}/*.mp4")
        ## Load mp4 files as videos:
        for i in video_file_list:
            print(i) ##which video is being processed?
            clip = VideoFileClip(i)
            loaded_video_list.append(clip)
        ## Merge & save "minute" videos
        vid_per_min=concatenate_videoclips(loaded_video_list)
        vid_per_min.write_videofile(f"{folder}/{child}/{fold}/{child}_{fold}_{num}.mp4")
    ## (2)Concatenate the merged "minute" videos:
    video_list = [] ##empty holder to store the videos
    files_path = Path(f"{folder}/{child}/{fold}/")
    file_list = glob.glob(f"{files_path}/{child}_{fold}*.mp4")
    for i in file_list:
        print(i) ##which video is being processed?
        clip = VideoFileClip(i)
        video_list.append(clip)
    ## Add the first frame info for later use
    if r1[n] < 10:
        r1[n] = str(0) + str(r1[n])
    video_files_path = Path(f"{folder}/{child}/{fold}/{r1[n]}")
    video_file_list = glob.glob(f"{video_files_path}/*.mp4")
    first_frame = video_file_list[0][-21:-15]
    ## (3)Merge & save the final output:
    fold = fold.lower()
    wanted = concatenate_videoclips(video_list)
    new_wanted = wanted.set_fps(fps=30)
    new_wanted.write_videofile(f"{folder}/{child}/{child}_{fold}_{first_frame}.mp4")
    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    print(f"{child} {fold} is done.")
    n += 1

#### END OF SCRIPT ####
