# MATLAB scripts for SW-Lab <img src="https://github.com/smy1/swlab/blob/main/script/swlogo.jpg" width=auto height="27"> <img src="https://github.com/smy1/swlab/blob/main/script/logo_matlab.png" width=auto height="27">
   - [remove_stim.m](./remove_stim.m) This script rejects stimuli in snirf data files based on gaze data stored as an excel file (e.g., whether the child was looking at the screen). (_Note_: I didn't write this from scratch) The script was originally written by Chi-Chuan Chen to toggle off stimuli. However, her script is for .nirs files, which works slightly differently from .snirf files. Furthermore, her script requires a .mat file for gaze data and I prefer loading the raw excel file instead.
   - [copy_files.m](./copy_files.m) This script first checks an excel file to see whether a data file/folder is to be copied or not. The script then copies specified files from the wanted subfolders and pastes the files in a new folder. (_Note_: I didn't write this from scratch) The script was originally written by Prof Chia-Feng Lu to copy a list of .snirf files to another folder.

## General requirements
- Download and install MATLAB (probably with an institution account). According to online tutorials, Homer3 is only compatible with MATLAB R2017b.
- Download and add [Homer3](https://github.com/BUNPC/Homer3/wiki/Download-and-Installation) to the MATLAB path.

## Helpful resources
- Introduction to MATLAB: [youtube link](https://www.youtube.com/watch?v=MYRkBoojh_Y&list=PLx_IWc-RN82tw_J9nYqIc0tjvaMjowRVi&pp=iAQB)
- SNIRF: [documentation](https://github.com/fNIRS/snirf/blob/master/snirf_specification.md)
- Homer3: [documentation](https://github.com/BUNPC/Homer3/wiki/), video tutorials by [NIRx](https://www.youtube.com/watch?v=I_eH0_ed8I4),
  [Prof. CF Lu](https://www.youtube.com/watch?v=bHhn2vBXF0Y) (slides in English, explanation in Mandarin)
