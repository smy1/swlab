#### Affiliation: SW-Lab, Dept of CFS, NTNU
#### Project: MoChi
#### Date: 17.04.2025
#### Author: MY Sia (with lots of help from the following websites)
## https://zulko.github.io/moviepy/v1.0.3/examples/moving_letters.html
## https://imagemagick.org/script/download.php#windows
## https://stackoverflow.com/a/74701556

#### Aim of script: Add a frontcover to the main video, personalised with the child's name
##Recommended directory: project folder -> "child" subfolder -> videos
##Requirement: a blank background picture and a small lab logo picture (both stored in the project folder)

#### Load packages and set parameters
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})
import glob
from pathlib import Path
from moviepy.editor import * ##MoviePy v1.0.3
from openpyxl import load_workbook ##if we pass arguments from an excel file

folder = "C:/Users/user/Desktop/mc_vid"
outsub = "to_send" ##subfolder within the main folder to store the outputs
targ = "brain_activation"
newname = "大腦動畫"

#### Read arguments from excel
wb = load_workbook(f"{folder}/mc_name.xlsx")
sheet = wb["Sheet5"]

children=[] ##which subfolder are we processing
list_children = sheet["c"]
for i in list_children[1:]:
    children.append(i.value)

name=[] ##name of the child (to personalise the videos)
list_name =  sheet["b"]
for i in list_name[1:]:
    name.append(i.value)

#### Prepare material clips
##prepare the frontpage
proj = "\n".join([
"親子共讀的大腦同步性研究",
"2025",
"親子大腦動畫"
])
lab = "\n".join([
"臺師大嬰幼兒大腦發展與學習實驗室",
"Child Brain Development and Learning Lab"
])
bg = ImageClip(f"{folder}/blank.jpg") ##blank white canvas
p1 = TextClip(proj, color="black", font="DengXian-Bold", fontsize=35)
logo = ImageClip(f"{folder}/logo.jpg") ##lab logo (make sure it's small!!)
p2 = TextClip(lab, color="black", font="DengXian-Bold", fontsize=25)
##prepare the brain tags
p_clip = TextClip("家長", color="black", font="DengXian", fontsize=20)
c_clip = TextClip("小孩", color="black", font="DengXian", fontsize=20)

#### Start looping videos
n = 0
for child in children:
    ## the brain activation video
    vid_path = Path(f"{folder}/brain/{child}/")
    vid_list = glob.glob(f"{vid_path}/*{targ}*.mp4")
    if len(vid_list) == 1:
        ##Create a front page based on the dimension of the main video
        vid1 = VideoFileClip(vid_list[0])
        (x, y) = screensize = vid1.size
        ##stitch the material clips together
        front = CompositeVideoClip([bg, ##each chinese character has a width of 30-35 px
                                p1.set_pos(((x/2)-(6*35), y/8)),
                                logo.set_pos(((x/2)-54, (y/2)-54)), ##depends on the px of the picture
                                p2.set_pos(((x/2)-(8*30), y*5/8))],
                                size=screensize).set_duration(2).set_fps(fps=15)
        ##personalise with child's name
        chi_name = TextClip(name[n]+"小朋友", color="black", font="DengXian", fontsize=35)
        front = CompositeVideoClip([front,
                                    chi_name.set_pos(((x/2)-(3*35), y*7/8))]).set_duration(2).set_fps(fps=15)
        ##add brain tags to the main video
        main = CompositeVideoClip([vid1,
                                   p_clip.set_pos(((x/4)-20, (y*7/8)+15)),
                                   c_clip.set_pos(((x*3/4)-20, (y*7/8)+15))]).set_duration(vid1.duration).set_fps(fps=15)
        ## compose and render
        full = concatenate_videoclips([front, main])
        full.write_videofile(f"{folder}/{outsub}/{name[n]}_{newname}.mp4") ##to send to parents
        # if child[0] == "p":
        #     full.write_videofile(f"{folder}/new/{child}_brain.mp4")
        # elif child < 10:
        #     full.write_videofile(f"{folder}/new/c0{child}_brain.mp4")
        # else:
        #     full.write_videofile(f"{folder}/new/c{child}_brain.mp4")
        n += 1
    else:
        n += 1
