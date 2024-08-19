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

**Random Video Viewer with a server**

Start up the random video viewer. Uses flask to host a simple web server, and embed a grid of YouTube videos

```bash
python youtube-asl-viewer.py
```

**Generate a .html you can just open in a browser**

Do you want to just hardcode, say, 250 videos into a .html file, and then send that to someone who doesn't have Python or Flask, and then they can just open it in their browser? You're in luck! You can! Just run the following, and it will take `youtube_asl_video_ids.txt`, pull out the number of IDs you specified, and generate a .html with them hardcoded inside. Then when someone clicks on it, it'll open in their browser and just display 6 our of those 250.

```python

# make HTML with 250 hardcoded ids, of which a few are displayed at random every time you reload the page
python create_static_html.py 250

# same thing, with 11000 videos (youtube_asl_video_ids.txt only has 11,096). Resulting html is 155 kb or so!
python create_static_html.py 11000
```

The resulting file is "yt_asl_static_demo.html"

Download videos. This script creates a folder called "downloads" and puts videos, subtitles, and audio tracks into it. 

```bash
python download_vids.py --dataset_folder "downloads"
```

### Features:

Implemented:

* Randomly select and embed [Youtube-ASL](https://github.com/google-research/google-research/tree/master/youtube_asl) videos.
* Display a grid of random videos
* Download videos, and stats about them
* Script to generate a static .html you can just click on, no Python needed.

### Ideas: 

* go through the list and see which ones have audio tracks in English
* download the audio tracks and run language ID, e.g. with https://huggingface.co/speechbrain/lang-id-voxlingua107-ecapa or Open Whisper: https://huggingface.co/espnet/owsm_v3
* Load it into a `fiftyone` dataset, e.g. like in https://github.com/voxel51/fiftyone-examples/blob/master/examples/Video%20Labels.ipynb, which loads in WLASL data
* Extend to YT-SL25

### Related

* https://github.com/goatandsheep/pip does picture in picture for ASL vids
* Maybe with [YouTube API](https://developers.google.com/youtube/iframe_api_reference#seekTo)
