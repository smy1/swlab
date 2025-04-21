## Obsolete Python scripts

Packages used in some of the video-editing scripts below but are actually unnecessary:
```
pip install playsound==1.2.2 ## not necessary, only for notification when video rendering is done
```

__Previous scripts that have _not_ been included in the module:__
- [merge-clips.py](./merge-clips.py): This script concatenates short videos which are stored in third-level subfolders, that is, within the second-level camera subfolders. The third-level subfolders indicate the minute of the recording, e.g., a folder named "09" contains several three-second-long clips recorded at the 9th minute of the hour of experiment.
- [sbr-sound.py](./sbr-sound.py) This script just replaces the audio of the juxtaposed video with another audio file (that hopefully has better quality). To sync the timing of the two audio files, I use Audacity. See [here](https://github.com/smy1/swlab/blob/main/script/audacity-sync-audio.pdf) for the instructions.
- [add_cover.py](./add_cover.py) This script creates a front cover for a video. The dimension of the front cover follows that of the video. The front cover shows the name of the lab (or any information regarding the video) and is personalised based on the child's name.

__Previous scripts that are now developed into the [editvid.py](https://github.com/smy1/swlab/blob/main/python/editvid.py) module:__
- [merge-videos.py](./merge-videos.py): This script concatenates short videos of each video camera into a complete video.
- [rename-merge-videos.py](./rename-merge-videos.py): This script adds a chunk of "check-and-rename" code to the _merge-videos_ script so that we rename the video files before merging them. Specifically, Python will change the "00" in the file name to "60" so that the "59" recording is placed before the originally-named-as-"00" recording. 
- [omi-sync-videos.py](./omi-sync-videos.py): This script downsizes the "screen" video to 25%, then overlays it on the "baby" video at the top left corner. 
- [sbr-sync-2videos.py](./sbr-sync-2videos.py) This script syncs and juxtaposes two videos with one larger and the other smaller.
- [crop-sync-2videos.py](./crop-sync-2videos.py) This script adds an additional chunk of code to the _sbr-sync-2videos_ script to crop one of the videos before syncing both of them.
- [sbr-sync-3videos.py](./sbr-sync-3videos.py) This script displays one video on the left and two (downsized) videos on the right (one on top and the other at the bottom).
