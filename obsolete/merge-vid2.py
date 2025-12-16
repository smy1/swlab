#### Affiliation: SW-Lab, Dept of CFS, NTNU
#### Project: Crocodile (aka Peek2)
#### Date: 16.12.2025
#### Author: MY Sia

#### Aim of script: Concatenate a few videos; batch process several children
##Input: 2-3 videos stored in a camera folder
##Output: A single video per child
##Recommended directory: project folder -> child folder -> camera folder -> videos (e.g., <desktop>/Croc/P01/BABY/<videos>)
##Requirement: This script was written using Python 3.12.4. Various Python modules need to be installed. See README.md for more.

########################################
#### START HERE:
## Import everything needed to edit video clips
from moviepy.editor import *
from pathlib import Path
import glob
from datetime import datetime, timedelta

folder="C:/Users/user/Desktop/smy/PROJECTS/croc" ##set path to the project folder

########################################
#### LOOP THROUGH SEVERAL BABIES:
childlist=["092", "097"] ##which child folder are we processing?
camlist=["croc", "帥哥", "美女"] ##name of camera folders
for child in childlist:
    for cam in camlist:
        video_list=[]
        x=len(folder)+1+len(child)+1+len(cam)+1
        files_path = Path(f"{folder}/{child}/{cam}")
        file_list = glob.glob(f"{files_path}/*.mp4")
        end_sec = 0
        if len(file_list) < 2:
            print(f"Nothing to join in {child}'s {cam} folder.")
        else:
            for i in range(len(file_list)):
                vid=file_list[i]
                clip=VideoFileClip(file_list[i])
                video_list.append(clip)
                wanted_t=vid[-10:-5] ##extract the start time of the video
                ##for the first video
                if i==0:
                    end1=clip.duration
                    start_sec=(float(wanted_t[:2])*60)+float(wanted_t[-2:]) ##time lapsed to the wanted first frame
                    to_add=timedelta(hours=0, minutes=float(wanted_t[:2]), seconds=float(wanted_t[-2:]))
                    t_frame=f"{file_list[0][x+26:x+28]}:{file_list[0][x+28:x+30]}" ##the time of the video's first frame
                    t_frame=datetime.strptime(t_frame, "%M:%S")
                    t_start=t_frame+to_add
                    frame=t_start.strftime("%Y-%m-%d %H:%M:%S")
                ##for the other videos
                else:
                    if "前" in vid[-5:-4]: ##time lapsed till the end of the wanted recording
                        end_sec+=(float(wanted_t[:2])*60)+float(wanted_t[-2:])
                    else:
                        end_sec+=clip.duration
            joined=concatenate_videoclips(video_list)
            joined=joined.resize(height=720).set_fps(fps=30)
            final=joined.subclip(start_sec, end_sec+end1)
            final.write_videofile(f"{folder}/{child}/{child}_{cam}_{frame[-5:-3]}M{frame[-2:]}S.mp4")

#### END OF SCRIPT ####
