'''
Date: 21.06.2024
Author: MY Sia
See https://github.com/smy1/edit-videos for more.

Aim of script: Concatenate second-long videos which are stored in sub-"minute"-folder; batch process several children
Input: Multiple videos (each has a duration of a few seconds) stored in a sub-"minute"-folder (i.e., these videos add up to be about 1 minute) within a camera folder
Output: A single video per child
Recommended directory: project folder -> child folder -> camera folder -> minute folder -> short videos (e.g., <desktop>/Peekaboo/P01/BABY/37/<videos>)
Requirement: This script was written using Python 3.12.4. Various Python modules need to be installed.
'''

########################################
#### START HERE:
## Import everything needed to edit video clips
import glob
from pathlib import Path
from moviepy.editor import *
import winsound ##not necessary, just to get Python to notify me when it is done

folder = "C:/Users/user/Desktop/peekaboo/peekadata" ##set path to the project folder

########################################
#### LOOP THROUGH SEVERAL BABIES:
children = ["P1", "P3"] ##which child folder are we processing?
camera = "BABY" ##name of camera folder that stores videos in sub-"minute"-folders
r1 = [34, 8] ##what is the number of the FIRST sub-folder that you want to merge?
r2 = [40, 15] ##what is the number of the LAST sub-folder that you want to merge?

n = 0
for child in children:
    ## (1)Concatenate second-long videos:
    omi = range(r1[n], r2[n]+1) ##the folder numbers that we want to concatenate
    for num in omi:
        ## Need to add 0 for sub-folders 01 - 09
        if num < 10:
            num = str(0) + str(num)
        mini_video_list = [] ##empty holder to store the videos
        mini_files_path = Path(f"{folder}/{child}/{camera}/{num}")
        mini_file_list = glob.glob(f"{mini_files_path}/*.mp4")
        ## Load mp4 files as videos:
        for i in mini_file_list:
            print(i) ##which video is being processed?
            clip = VideoFileClip(i)
            mini_video_list.append(clip)
        ## Merge & save "minute" videos
        vid_per_min=concatenate_videoclips(mini_video_list)
        vid_per_min.write_videofile(f"{folder}/{child}/{camera}/{child}_{camera}_{num}.mp4")
    ## (2)Concatenate the merged "minute" videos:
    video_list = [] ##empty holder to store the videos
    files_path = Path(f"{folder}/{child}/{camera}/")
    file_list = glob.glob(f"{files_path}/{child}_{camera}*.mp4")
    for i in file_list:
        print(i) ##which video is being processed?
        clip = VideoFileClip(i)
        video_list.append(clip)
    ## Add the first frame info for later use
    if r1[n] < 10:
        r1[n] = str(0) + str(r1[n])
    mini_files_path = Path(f"{folder}/{child}/{camera}/{r1[n]}")
    mini_file_list = glob.glob(f"{mini_files_path}/*.mp4")
    first_frame = mini_file_list[0][-21:-15]
    ## (3)Merge & save the final output:
    joined = concatenate_videoclips(video_list)
    joined = joined.set_fps(fps=30) ##standardise frame per second for all videos
    cam = camera.lower()
    joined.write_videofile(f"{folder}/{child}/{child}_{cam}_{first_frame}.mp4")
    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    n += 1 ##now do the next one

#### END OF SCRIPT ####
