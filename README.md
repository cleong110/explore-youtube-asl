# explore-youtube-asl
Messing around with [YouTube-ASL](https://github.com/google-research/google-research/tree/master/youtube_asl). 

Colab notebook: https://colab.research.google.com/drive/1OBOyclRuMyjIIL15LKgRGPx3ArzpAv1F?usp=sharing

Implemented:
* randomly select and embed [Youtube-ASL](https://github.com/google-research/google-research/tree/master/youtube_asl) videos.
* Display a grid of random videos
* Download videos, and stats about them

Ideas: 
* go through the list and see which ones have audio tracks in English
* download the audio tracks and run language ID, e.g. with https://huggingface.co/speechbrain/lang-id-voxlingua107-ecapa or Open Whisper: https://huggingface.co/espnet/owsm_v3
* Load it into a `fiftyone` dataset, e.g. like in https://github.com/voxel51/fiftyone-examples/blob/master/examples/Video%20Labels.ipynb, which loads in WLASL data



Related:
* https://github.com/goatandsheep/pip does picture in picture for ASL vids
* Maybe with [YouTube API](https://developers.google.com/youtube/iframe_api_reference#seekTo)
