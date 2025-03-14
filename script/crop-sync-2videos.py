#### Affiliation: SW-Lab, Dept of CFS, NTNU
#### Project: MoChi
#### Date: 18.02.2025
#### Author: MY Sia (modified from the Peekaboo project)

#### Aim of script: (1) Extract solo reading and (2) sync and combine two videos for SBR
##Input: Two video recordings (front and side) showing a parent-child dyad
##Output: A single video per child with one angle as the main video and the other as the minor
##Recommended directory: project folder -> child folder -> videos
##Requirement: This script was written using Python 3.12.4. Various Python modules need to be installed. See README.md for more.

########################################
#### START HERE:
## Import everything needed to edit video clips
import glob
from pathlib import Path
from moviepy.editor import * ##v1.0.3
from datetime import datetime ##to calculate time difference between videos
import cv2 ##so that videos can be resized properly
import os ##to delete unwanted files
from playsound import playsound ##just for notification

folder = "C:/Users/user/Desktop/mc_vid" ##set path to the project folder

########################################
#### Set default values
dur_solo = 183 ##duration of the solo condition + 3sec
dur_sbr = 305 ##duration of the SBR condition + 5sec
x1, y1, x2, y2 = 450, 100, 2300, 1450 ##crop the front camera
## - if the position of the dyad is not within this range, give a new dimension below
vol_front, vol_side = 0, 10 ##amplify the side camera, mute the other
col_front, col_side = (0, 0, 0), (0, 0, 225) ##amplified video gets a blue border

#### Enter information
attempts = 1 ##the number of attempts in merging videos
dyads = ["a26_c26", "a28_c28", "a29_c29"] ##which dyad folder are we looping?
main = ["front", "side", "front"] ##does the front or the side video have a better recording angle?
solo_done = "no" ##if yes, the script will not render the solo videos
strt_solo = [448, 438, 62] ##the seconds at which the FRONT video STARTED recording the SOLO condition
strt_sbr = [11, 25, 378] ##the seconds at which the FRONT video STARTED recording the SBR condition
## Manually correct out-of-sync side video for SBR:
corr = [-0.9, -0.7, -0.6]
## - this is used only in the corrective rounds (i.e., second attempt or later)
## - if the SIDE video LAGS BEHIND, give a POSITIVE number; OTHERWISE, give a NEGATIVE number
## - a larger absolute number given will introduce a larger time difference between the videos

#### Check entry of information
n = 0 ##to loop the information entered above
if len(main) != len(dyads):
    print("The number of 'MAIN' does not match the number of 'DYADS'.")
elif len(strt_sbr) != len(dyads):
    print("The number of 'START' does not match the number of 'DYADS'.")
elif attempts > 1 and len(corr) != len(dyads):
    print("The number of 'CORR' does not match the number of 'DYADS'.")
else:
    #### Loop through several dyads
    for dyad in dyads:
        ## (a)Prepare videos:
        vid_path = Path(f"{folder}/{dyad}/")
        child = dyad[4:7]
        ## For different cropping dimensions
        if child == "c13":
            x1, y1, x2, y2 = 350, 90, 1800, 1400
        elif child == "c14":
            x1, y1, x2, y2 = 250, 100, 1700, 1370
        ## The front video
        front_list = glob.glob(f"{vid_path}/front*.mp4")
        front_vid = VideoFileClip(front_list[0])
        #(x, y) = front_vid.size ##check width and height of the video (2576x1456)
        front_vid = front_vid.crop(x1=x1, y1=y1, x2=x2, y2=y2)
        front_vid = front_vid.margin(10, color=col_front)
        ## The side video
        side_list = glob.glob(f"{vid_path}/side_*.mp4")
        side_vid = VideoFileClip(side_list[0])
        side_vid = side_vid.volumex(vol_side).margin(10, color=col_side)
        ## (b)Extract and render solo video:
        if solo_done == "no":
            final_solo = front_vid.volumex(5)
            ##in case of any error, don't stop; just move on
            try:
                final_solo = final_solo.subclip(strt_solo[n], strt_solo[n]+dur_solo)
                final_solo.write_videofile(f"{folder}/{dyad}/{child}_solo{attempts}_{x1}_{y1}_{x2}_{y2}.mp4")
                playsound("C:/Users/user/Desktop/ok.mp3")
            except: ##create a text file so that we know why the video was not rendered
                prob = open(f"{folder}/{dyad}/{child}_solo.txt", "w")
                prob.write("The solo video is problematic.")
                prob.close()
                playsound("C:/Users/user/Desktop/no.mp3")
        ## (c)Extract and render SBR video:
        ## Get time difference
        t_front = front_list[0][-10:-5]
        t_front = t_front.replace("M", ":")
        t_front = datetime.strptime(t_front, "%M:%S")
        t_side = side_list[0][-10:-5]
        t_side = t_side.replace("M", ":")
        t_side = datetime.strptime(t_side, "%M:%S")
        diff = t_front - t_side
        diff = diff.total_seconds()
        ## Sync the videos
        ##in case of any error, don't stop; just move on
        try:
            sbr_front = front_vid.subclip(strt_sbr[n], strt_sbr[n]+dur_sbr)
            if attempts == 1: ##first round
                x = 0 ##no manual correction
                ##save a copy of the front audio to aid correction of out-of-sync videos
                audio_front = sbr_front.audio
                audio_front.write_audiofile(f"{folder}/{dyad}/{child}_front.mp3")
                side_vid = side_vid.subclip(strt_sbr[n]+diff, strt_sbr[n]+diff+dur_sbr)
            elif attempts > 1: ##corrective round
                x = corr[n]
                side_vid = side_vid.subclip(strt_sbr[n]+diff+corr[n], strt_sbr[n]+diff+dur_sbr+corr[n])
                ##remove the front audio since it has done its job
                if os.path.exists(f"{folder}/{dyad}/{child}_front.mp3"):
                    os.remove(f"{folder}/{dyad}/{child}_front.mp3")
            ## Extract audio (for processing later)
            audio_sbr = side_vid.audio
            audio_sbr.write_audiofile(f"{folder}/{dyad}/{child}_sbr.mp3")
            sbr_front = sbr_front.volumex(vol_front) ##mute the video
            playsound("C:/Users/user/Desktop/ok.mp3")
            ## Position and resize the videos
            if main[n] == "front":
                major, minor = sbr_front, side_vid
            else:
                major, minor = side_vid, sbr_front
            major_vid = major.resize(0.7)
            minor_vid =  minor.resize(0.4)
            final_sbr = clips_array([[major_vid, minor_vid], ])
            ## Save the output
            final_sbr.write_videofile(f"{folder}/{dyad}/{child}_sbr{attempts}_{strt_sbr[n]}_corr={x}.mp4")
            n += 1 ##now, do the next one
            playsound("C:/Users/user/Desktop/done.mp3")
        except: ##create a text file so that we know why the video was not rendered
            prob = open(f"{folder}/{dyad}/{child}_sbr.txt", "w")
            prob.write("The sbr video is problematic:")
            prob.write(f"\nfront video = {t_front}\nside video = {t_side}\ndiff = {diff}\nstart time = {strt_sbr[n]}")
            prob.close()
            n += 1 ##move on to the next one
            playsound("C:/Users/user/Desktop/no.mp3")

#### END OF SCRIPT ####
