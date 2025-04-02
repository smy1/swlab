Packages used in some of the video-editing scripts but are actually unnecessary:
```
- pip install playsound==1.2.2 ## not necessary, only for notification when video rendering is done
```

Previous scripts that are now developed into the function [editvid.py](https://github.com/smy1/swlab/blob/main/python/editvid.py).
- [merge-videos.py](./merge-videos.py): This script concatenates short videos of each video camera into a complete video.
- [rename-merge-videos.py](./rename-merge-videos.py): This script adds a chunk of "check-and-rename" code to the _merge-videos_ script so that we rename the video files before merging them. Specifically, Python will change the "00" in the file name to "60" so that the "59" recording is placed before the originally-named-as-"00" recording. 
- [omi-sync-videos.py](./omi-sync-videos.py): This script downsizes the "screen" video to 25%, then overlays it on the "baby" video at the top left corner. 
- [sbr-sync-2videos.py](./sbr-sync-2videos.py) This script syncs and juxtaposes two videos with one larger and the other smaller.
- [crop-sync-2videos.py](./crop-sync-2videos.py) This script adds an additional chunk of code to the _sbr-sync-2videos_ script to crop one of the videos before syncing both of them.
- [sbr-sync-3videos.py](./sbr-sync-3videos.py) This script displays one video on the left and two (downsized) videos on the right (one on top and the other at the bottom) so that we capture parents' shared reading behaviour from three different angles. (_Note_: _SBR_ stands for shared book reading)
