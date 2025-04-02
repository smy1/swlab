#### Affiliation: SW-Lab, Dept of CFS, NTNU
#### Date: 31.03.2025
#### Author: MY Sia (with lots of help from the web, see README.md for more)
#### Functions: (1) concatenate, (2) sync and overlay, (3) crop, (4) juxtapose

#### Import necessary modules
import glob
from pathlib import Path
import os ##to rename files, where necessary
from moviepy.editor import * ##MoviePy v1.0.3
##for syncing videos
from datetime import datetime ##to calculate time difference between videos
import cv2 ##so that videos can be resized properly
from openpyxl import load_workbook ##if we extract info from an excel file

#### FUNCTION 1: CONCATENATE short videos into a long one
##Date: first written on 23.06.2024, further editing on 12.02.2025
##Input: Multiple videos stored in a folder (one folder for each camera)
##Output: A single video per camera per child
##Required directory: project folder -> "child" subfolder -> "camera" subfolder -> short videos
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


#### END OF FUNCTION 1 ####

#### FUNCTION 2: SYNC AND OVERLAY a downsized "top" video on a "bg" video
##Date: first written on 23.06.2024
##Input: A video showing the child's face (BABY video) and a video showing the screen that the child is watching (SCREEN video)
##Output: A single video per child with the BABY video as the main video and the SCREEN video overlaid on the top left corner
##Required directory: project folder -> "child" subfolder -> videos (e.g., <desktop>/Peekaboo/P01/<videos>)
def overlay(folder, attempts, bgcam, topcam, newname, propsize, dur,
            excel, children, start, end, corr):
    ### Extract information if we load an excel file
    if excel != None:
        wb = load_workbook(excel)
        sheet = wb["Sheet1"]
        ##Extract information from excel
        children=[] ##which child folder are we processing?
        list_children = sheet["a"]
        for i in list_children[1:]:
            children.append(i.value)
        #
        start=[] ##the seconds at which the experiment STARTED in the SCREEN video
        list_start =  sheet["b"]
        for i in list_start[1:]:
            start.append(i.value)
        #
        end=[] ##the seconds at which the experiment ENDED in the SCREEN video
        list_end =  sheet["c"]
        for i in list_end[1:]:
            end.append(i.value)
        #
        corr=[] ## Manually correct out-of-sync baby videos:
        list_corr =  sheet["d"]
        for i in list_corr[1:]:
            corr.append(i.value)
        #
    ##If all videos are of the same length, use it to calculate the end time
    if dur != None:
        end = []
        for i in start:
            end.append(i + dur)
    ### Start overlaying videos
    n = 0
    for child in children:
        ## (a)Prepare videos:
        vid_path = Path(f"{folder}/{child}/")
        ## Baby video
        baby_list = glob.glob(f"{vid_path}/*{bgcam}*.mp4")
        if len(baby_list) < 1: ##check for problem
            print(f"Can't find {child}'s {bgcam}. Please check the path and folder names.")
        else:
            baby_vid = VideoFileClip(baby_list[0])
            t_baby = baby_list[0][-10:-5]
            t_baby = t_baby.replace("M", ":")
            t_baby = datetime.strptime(t_baby, "%M:%S")
            ## Screen video
            screen_list = glob.glob(f"{vid_path}/*{topcam}*.mp4")
            if len(screen_list) < 1: ##check for problem
                print(f"Can't find {child}'s {topcam}. Please check the path and folder names.")
            else:
                screen_vid = VideoFileClip(screen_list[0])
                screen_vid = screen_vid.resize(propsize).margin(5) ##downsize video and add a 5px border
                t_screen = screen_list[0][-10:-5]
                t_screen = t_screen.replace("M", ":")
                t_screen = datetime.strptime(t_screen, "%M:%S")
                ## Get time difference between videos
                diff = t_screen - t_baby
                diff = diff.total_seconds()
                ## (b)Overlay screen video on baby video at the top left corner:
                if attempts == 1: ##first round
                    x = 0 ##no manual correction
                    all_vid = CompositeVideoClip([baby_vid.subclip(start[n]+diff, end[n]+diff),
                                                screen_vid.subclip(start[n], end[n]).set_position((0, 50))])
                elif attempts > 1: ##corrective round
                    x = corr[n]
                    all_vid = CompositeVideoClip([baby_vid.subclip(start[n]+diff+corr[n], end[n]+diff+corr[n]),
                                                screen_vid.subclip(start[n], end[n]).set_position((0, 50))])
                ## (c)Save composite video:
                all_vid.write_videofile(f"{folder}/{child}/{child}_{newname}_merged{attempts}_corr={x}.mp4")
                n += 1 ##now, do the next one


#### END OF FUNCTION 2 ####

#### FUNCTION 3: CROP a video
##Date: first written on 18.02.2025
##Input:
##Output:
##Required directory: project folder -> "child" subfolder -> videos
def crop(folder, cam, newname, dur, amplify,
         excel, children, start, end, x1, x2, y1, y2):
    if excel != None:
        wb = load_workbook(excel)
        sheet = wb["Sheet1"]
        ##Extract information from excel
        children=[] ##which child folder are we processing?
        list_children = sheet["a"]
        for i in list_children[1:]:
            children.append(i.value)
        #
        start=[] ##the seconds at which the experiment STARTED
        list_start =  sheet["b"]
        for i in list_start[1:]:
            start.append(i.value)
        #
        end=[] ##the seconds at which the experiment ENDED
        list_end =  sheet["c"]
        for i in list_end[1:]:
            end.append(i.value)
        #
        x1=[]
        list_x1 =  sheet["d"]
        for i in list_x1[1:]:
            x1.append(i.value)
        #
        x2=[]
        list_x2 =  sheet["e"]
        for i in list_x2[1:]:
            x2.append(i.value)
        #
        y1=[]
        list_y1 =  sheet["f"]
        for i in list_y1[1:]:
            y1.append(i.value)
        #
        y2=[]
        list_y2 =  sheet["g"]
        for i in list_y2[1:]:
            y2.append(i.value)
        #
    ##If all videos are of the same length, use it to calculate the end time
    if dur != None:
        end = []
        for i in start:
            end.append(i + dur)
        #
    ##Start overlaying videos
    n = 0
    for child in children:
        ## Prepare video:
        vid_path = Path(f"{folder}/{child}/")
        vid_list = glob.glob(f"{vid_path}/*{cam}*.mp4")
        if len(vid_list) < 1: ##check for problem
            print(f"Can't find {child}'s {cam}. Please check the path and folder names.")
        else:
            thevid = VideoFileClip(vid_list[0])
            if thevid.duration > end[n]:
                thevid = thevid.subclip(start[n], end[n])
            else:
                thevid = thevid.subclip(start[n], thevid.duration)
            ## Crop it:
            cropped = thevid.crop(x1=x1[n], x2=x2[n], y1=y1[n], y2=y2[n])
            cropped = cropped.volumex(amplify)
            ## Extract and render:
            cropped.write_videofile(f"{folder}/{child}/{child}_{newname}.mp4")
            n += 1 ##now, do the next one


#### END OF FUNCTION 3 ####

#### FUNCTION 4: JUXTAPOSE videos
##Date: first written on 08.07.2024, further editing on 18.02.2025
##Input: Two video recordings (from different angles) that record the participant performing a task
##Output: A single video per participant with one of the recordings (the one with the best angle) as the main video and the other as the minor
##Required directory: project folder -> "child" subfolder -> videos
def join2side(folder, attempts, cam1, cam2, newname, dur, amplify_who, amplify, mute_who, crop_who,
              excel, children, main, start, end, corr, x1, x2, y1, y2):
    if excel != None:
        wb = load_workbook(excel)
        sheet = wb["Sheet1"]
        ##Extract information from excel
        children=[] ##which child folder are we processing?
        list_children = sheet["a"]
        for i in list_children[1:]:
            children.append(i.value)
        #
        main=[] ##the video with the best angle
        list_main = sheet["b"]
        for i in list_main[1:]:
            main.append(i.value)
        #
        start=[] ##the seconds at which the experiment STARTED
        list_start = sheet["c"]
        for i in list_start[1:]:
            start.append(i.value)
        #
        end=[] ##the seconds at which the experiment ENDED
        list_end = sheet["d"]
        for i in list_end[1:]:
            end.append(i.value)
        #
        corr=[] ##the seconds at which the experiment ENDED
        list_corr = sheet["e"]
        for i in list_corr[1:]:
            corr.append(i.value)
        #
        x1=[]
        list_x1 = sheet["f"]
        for i in list_x1[1:]:
            x1.append(i.value)
        #
        x2=[]
        list_x2 = sheet["g"]
        for i in list_x2[1:]:
            x2.append(i.value)
        #
        y1=[]
        list_y1 = sheet["h"]
        for i in list_y1[1:]:
            y1.append(i.value)
        #
        y2=[]
        list_y2 = sheet["i"]
        for i in list_y2[1:]:
            y2.append(i.value)
        #
    ##If all videos are of the same length, use it to calculate the end time
    if dur != None:
        end = []
        for i in start:
            end.append(i + dur)
        #
    ##Start juxtaposing videos
    n = 0
    for child in children:
        ### (a)Prepare videos (crop if necessary):
        vid_path = Path(f"{folder}/{child}/")
        ## The first camera
        vid1_list = glob.glob(f"{vid_path}/*{cam1}*.mp4")
        if len(vid1_list) < 1: ##check for problem
            print(f"Can't find {child}'s {cam1}. Please check the path and folder names.")
        else:
            vid1 = VideoFileClip(vid1_list[0])
            if crop_who == cam1:
                vid1 = vid1.crop(x1=x1[n], x2=x2[n], y1=y1[n], y2=y2[n])
            ## The second camera
            vid2_list = glob.glob(f"{vid_path}/*{cam2}*.mp4")
            if len(vid2_list) < 1: ##check for problem
                print(f"Can't find {child}'s {cam2}. Please check the path and folder names.")
            else:
                vid2 = VideoFileClip(vid2_list[0])
                if crop_who == cam2:
                    vid2 = vid2.crop(x1=x1[n], x2=x2[n], y1=y1[n], y2=y2[n])
                ### (b)Sync the videos:
                t_vid1 = vid1_list[0][-10:-5]
                t_vid1 = t_vid1.replace("M", ":")
                t_vid1 = datetime.strptime(t_vid1, "%M:%S")
                t_vid2 = vid2_list[0][-10:-5]
                t_vid2 = t_vid2.replace("M", ":")
                t_vid2 = datetime.strptime(t_vid2, "%M:%S")
                diff = t_vid1 - t_vid2
                diff = diff.total_seconds()
                ## cam1
                if vid1.duration > end[n]:
                    vid1 = vid1.subclip(start[n], end[n])
                else:
                    vid1 = vid1.subclip(start[n], vid1.duration)
                ## cam2
                if attempts == 1: ##first round
                    x = 0 ##no manual correction
                    if vid2.duration > end[n]+diff:
                        vid2 = vid2.subclip(start[n], end[n]+diff)
                    else:
                        vid2 = vid2.subclip(start[n], vid2.duration)
                    ##save audio files to aid correction of out-of-sync videos:
                    audio_vid1 = vid1.audio
                    audio_vid1.write_audiofile(f"{folder}/{child}/{child}_{cam1}_audio.mp3")
                    audio_vid2 = vid2.audio
                    audio_vid2.write_audiofile(f"{folder}/{child}/{child}_{cam2}_audio.mp3")
                elif attempts > 1: ##corrective round
                    x = corr[n]
                    if vid2.duration > end[n]+diff+corr[n]:
                        vid2 = vid2.subclip(start[n]+corr[n], end[n]+diff+corr[n])
                    else:
                        vid2 = vid2.subclip(start[n]+corr[n], vid2.duration)
                ### (c) Deal with the volume/audio extraction:
                ##amplify if necessary and add a blue border
                if amplify_who == cam1:
                    vid1 = vid1.volumex(amplify).margin(10, color=(0, 0, 225))
                    vid2 = vid2.margin(10)
                elif amplify_who == cam2:
                    vid2 = vid2.volumex(amplify).margin(10, color=(0, 0, 225))
                    vid1 = vid1.margin(10)
                ##mute if necessary
                if mute_who == cam1:
                    vid1 = vid1.volumex(0)
                elif mute_who == cam2:
                    vid2 = vid2.volumex(0)
                ### (d) Position videos and save them:
                if main[n] == cam1:
                    major, minor = vid1, vid2
                else:
                    major, minor = vid2, vid1
                ##resize videos
                major_vid = major.resize(0.7)
                minor_vid =  minor.resize(0.4)
                final_vid = clips_array([[major_vid, minor_vid], ])
                ##save the output
                final_vid.write_videofile(f"{folder}/{child}/{child}_{newname}_{attempts}_corr={x}.mp4")
                n += 1 ##now, do the next one
