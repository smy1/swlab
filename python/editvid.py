import glob
from pathlib import Path
import os ##to rename files, where necessary
from moviepy.editor import *

def merge(folder, children, camera):
    #### Loop through child folders
    for child in children:
        ## Loop through camera folders
        for cam in camera:
            video_list = [] ##empty holder to store videos
            files_path = Path(f"{folder}/{child}/{cam}")
            file_list = glob.glob(f"{files_path}/*.mp4")
            ## (a)Check for problematic cases:
            if len(file_list) < 2:
                print(f"Nothing to join in {child}'s {cam} folder.")
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
                ## add the folder back to be processed
                camera.append(cam)
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
                cam = cam.lower()
                joined.write_videofile(f"{folder}/{child}/{child}_{cam}_{first_frame}.mp4")
