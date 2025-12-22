## Scripts that have _not_ been included in the module:

- [merge-clips.py](./merge-clips.py): This script concatenates short videos which are stored in third-level subfolders, that is, within the second-level camera subfolders. The third-level subfolders indicate the minute of the recording, e.g., a folder named "09" contains several three-second-long clips recorded at the 9th minute of the hour of experiment.
- [merge-vid2.py](./merge-vid2.py): This script concatenates videos into a long one. The difference between this and the merge function in the compiled script is that this script extracts the starting time of the videos in a different manner, due to the different way newer versions of Xiaomi security cameras name their recordings.
- [sbr-sound.py](./sbr-sound.py) This script just replaces the audio of the juxtaposed video with another audio file (that hopefully has better quality). To sync the timing of the two audio files, I use Audacity.
- [add_cover.py](./add_cover.py) This script creates a front cover for a video. The dimension of the front cover follows that of the video. The front cover shows the name of the lab (or any information regarding the video) and is personalised based on the child's name.

>[!TIP]
>Some of the video-editing scripts above call for a package that is actually unnecessary:
>```
>pip install playsound==1.2.2 ## not necessary, only for notification when video rendering is done
>```
