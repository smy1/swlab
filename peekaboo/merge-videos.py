#### Affiliation: SW-Lab, Dept of CFS, NTNU
#### Project: Peekaboo (aka Omi2)
#### Date: 21.06.2024 (long count: 13.0.11.12.0, 5 Ajpu')
#### Author: MY Sia (with lots of help from the web, see README.txt for more)

#### Aim of script: Concatenate short videos into a long one; batch process several cameras (BABY, SCREEN, & 3 SBRs) of several children
##Input: Multiple videos (each has a duration of 1 minute) stored in a folder (one folder for each camera)
##Output: A single video per camera per child
##Recommended directory: project folder -> child folder -> camera folder -> short videos (e.g., <desktop>/Peekaboo/P01/BABY/<videos>)
##Requirement: This script was written using Python 3.12.4. Various Python modules need to be installed. See README.txt for more.

########################################
#### START HERE:
## Import everything needed to edit video clips
## Remember to move all BABY capping videos to a sub-folder (ask the PI if you don't understand this part)
import glob
from pathlib import Path
from moviepy.editor import *
import winsound ##not necessary, just to get Python to notify me when it is done

print("Remember to MOVE CAPPING videos in the BABY folder to a sub-folder.")
folder = "C:/Users/user/Desktop/peekaboo/peekadata" ##set path to the project folder

########################################
#### LOOP THROUGH SEVERAL BABIES:
group = ["064", "065", "066", "067", "068", "069"] ##which child folder are we processing?
problem = [] ##empty holder to store problematic IDs

for child in group:
    #### CONCATENATE BABY VIDEOS
    baby_video_list = [] ##empty holder to store videos
    baby_files_path = Path(f"{folder}/{child}/BABY") ##name of camera folder is BABY
    baby_file_list = glob.glob(f"{baby_files_path}/*.mp4")
    ## (a)Check for weird cases:
    if len(baby_file_list) < 2:
        x = f"No/only one video found in {child}'s BABY folder."
        print(x) ##if the BABY folder is empty (i.e., no short videos), let us know
        problem.append(x)
    else:
        ## (b)Load mp4 files as videos:
        for i in baby_file_list:
            print(i) ##which video is being processed?
            clip = VideoFileClip(i)
            baby_video_list.append(clip)
        ## (c)Merge & save the output:
        baby = concatenate_videoclips(baby_video_list)
        new_baby = baby.set_fps(fps=30)
        first_baby_frame = baby_file_list[0][-21:-15]
        new_baby.write_videofile(f"{folder}/{child}/{child}_baby_{first_baby_frame}.mp4")
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        print(f"{child} BABY is done.")
    #### CONCATENATE SCREEN VIDEOS
    screen_video_list = [] ##empty holder to store videos
    screen_files_path = Path(f"{folder}/{child}/SCREEN") ##name of camera folder is SCREEN
    screen_file_list = glob.glob(f"{screen_files_path}/*.mp4")
    ## (a)Check for weird cases:
    if len(baby_file_list) < 2:
        x = f"No/only one video found in {child}'s SCREEN folder."
        print(x) ##if the SCREEN folder is empty, let us know
        problem.append(x)
    else:
        ## (b)Load mp4 files as videos:
        for i in screen_file_list:
            print(i) ##which video is being processed?
            clip = VideoFileClip(i)
            screen_video_list.append(clip)
        ## (c)Merge & save the output:
        screen = concatenate_videoclips(screen_video_list)
        new_screen = screen.set_fps(fps=30)#.fx(vfx.mirror_y)
        first_screen_frame = screen_file_list[0][-21:-15]
        new_screen.write_videofile(f"{folder}/{child}/{child}_screen_{first_screen_frame}.mp4")
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        print(f"{child} SCREEN is done.")
    #### CONCATENATE SBR VIDEOS
    n = 1 ##SBR camera number (we have 3)
    while n < 4:
        sbr_video_list = [] ##empty holder to store videos
        sbr_files_path = Path(f"{folder}/{child}/SBR{n}") ##name of camera folder is SBR1,2,3
        sbr_file_list = glob.glob(f"{sbr_files_path}/*.mp4")
        ## (a)Check for weird cases:
        if len(sbr_file_list) < 2:
            x = f"No/only one video found in {child}'s SBR{n}."
            print(x)
            problem.append(x)
            n += 1 ##if the SBR camera folder is empty (i.e., no short videos), move to the next one
        else:
            ## (b)Load mp4 files as videos:
            for i in sbr_file_list:
                print(i) ##which video is being processed?
                clip = VideoFileClip(i)
                sbr_video_list.append(clip)
            ## (c)Merge & save the output:
            sbr = concatenate_videoclips(sbr_video_list)
            new_sbr = sbr.set_fps(fps=30)
            first_sbr_frame = sbr_file_list[0][-21:-15]
            new_sbr.write_videofile(f"{folder}/{child}/{child}_sbr{n}_{first_sbr_frame}.mp4")
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            print(f"{child} SBR{n} is done.")
            n += 1 ##now, do the next SBR camera

#### Were there any problematic camera folders?
if len(problem) > 0:
    for x in problem:
        print(x)
else:
    print("All the videos were concatenated successfully.")

#### END OF SCRIPT ####
