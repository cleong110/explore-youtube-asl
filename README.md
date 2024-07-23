# Explore YouTube ASL

![A screenshot of a web page with several random YouTube videos autoplaying and embedded, all of which have people signing](random_asl_videos.png)

Messing around with [YouTube-ASL](https://github.com/google-research/google-research/tree/master/youtube_asl).

[Colab notebook](https://colab.research.google.com/drive/1OBOyclRuMyjIIL15LKgRGPx3ArzpAv1F?usp=sharing)

## Quickstart

Install requirements with [conda](https://docs.anaconda.com/miniconda/)

```bash
conda create -n explore-youtube-asl pip
conda activate explore-youtube-asl
python -m pip --version # should show the pip inside your env
pip install -r requirements.txt
```

Download the list of YouTube video IDs released by [YouTube-ASL](https://proceedings.neurips.cc/paper_files/paper/2023/hash/5c61452daca5f0c260e683b317d13a3f-Abstract-Datasets_and_Benchmarks.html)

```bash
python download_ids.py # should create a file called 'youtube_asl_video_ids.txt'
```

Start up the random video viewer. Uses flask to host a simple web server, and embed a grid of YouTube videos

```bash
python youtube-asl-viewer.py
```

Download videos. This script creates a folder called "downloads" and puts videos, subtitles, and audio tracks into it. 

```bash
python download_vids.py --download_folder "downloads"
```

### Features:

Implemented:

* Randomly select and embed [Youtube-ASL](https://github.com/google-research/google-research/tree/master/youtube_asl) videos.
* Display a grid of random videos
* Download videos, and stats about them

### Ideas: 

* go through the list and see which ones have audio tracks in English
* download the audio tracks and run language ID, e.g. with https://huggingface.co/speechbrain/lang-id-voxlingua107-ecapa or Open Whisper: https://huggingface.co/espnet/owsm_v3
* Load it into a `fiftyone` dataset, e.g. like in https://github.com/voxel51/fiftyone-examples/blob/master/examples/Video%20Labels.ipynb, which loads in WLASL data
* Extend to YT-SL25

### Related

* https://github.com/goatandsheep/pip does picture in picture for ASL vids
* Maybe with [YouTube API](https://developers.google.com/youtube/iframe_api_reference#seekTo)
