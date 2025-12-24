'''
Date: 07.02.2025
Author: MY Sia
See https://github.com/smy1/edit-videos for more.

Aim of script: Mute the SBR video and replace the audio with an mp3 file
Input: A merged video showing a parent-child dyad and the corresponding recording file
Output: A single video per child with better sound quality
Recommended directory: project folder -> child folder -> videos/audios
Requirement: This script was written using Python 3.12.4. Various Python modules need to be installed.
'''

########################################
#### START HERE:
## Import everything needed to edit video clips
import glob
from pathlib import Path
from moviepy.editor import * ##v1.0.3
from playsound import playsound ##just for notification

folder = "C:/Users/user/Desktop/mc_vid" ##set path to the project folder

########################################
#### Enter information
dyads = ["a08_c08", "a10_c10"] ##which dyad folder are we looping?

#### Loop through several dyads
for dyad in dyads:
    vid_path = Path(f"{folder}/{dyad}/")
    child = dyad[4:7]
    ## Get the video and audio
    sbr_list = glob.glob(f"{vid_path}/{child}_sbr.mp4")
    sbr_vid = VideoFileClip(sbr_list[0])
    aud_list = glob.glob(f"{vid_path}/{child}_sync*.mp3")
    if len(aud_list) == 0:
        print(f"{child} has no synced audio file!")
    else:
        sbr_aud = AudioFileClip(aud_list[0])
        ## Replace the audio
        new_sbr = sbr_vid.set_audio(sbr_aud)
        new_sbr.write_videofile(f"{folder}/{dyad}/{child}_sbr_newaudio.mp4")
        ## Notify when done
        playsound("C:/Users/user/Desktop/ok.mp3")


playsound("C:/Users/user/Desktop/done.mp3")
quit()
#### END OF SCRIPT ####
