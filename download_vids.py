from pytube import YouTube
from pytube.exceptions import AgeRestrictedError, VideoPrivate, VideoUnavailable
from urllib.error import HTTPError
import random
from tqdm import tqdm
import json
from pathlib import Path
import traceback
# https://github.com/pytube/pytube/issues/1954 stopped me. 
# had to manually edit /home/vlab/miniconda3/envs/explore-youtube-asl/lib/python3.12/site-packages/pytube/cipher.py

def download_vid(yt_id:str, download_folder:Path) -> dict:

    # download, or add to error dict
    try:
        video_download_folder = download_folder/ yt_id
        yt = YouTube(f'http://youtube.com/watch?v={yt_id}')
        # print(yt.title)
        # print(yt.streams)
        hd = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        out = hd.download(output_path=str(video_download_folder))


        # print(f"Downloaded {hd.default_filename} to {out}")

        

        results = {
            "video_downloaded_successfully": True,
            "video_file_path": out,
            "title": hd.title,
            "filesize_bytes": hd.filesize,
            "includes_audio_track": hd.includes_audio_track,
            "includes_video_track": hd.includes_video_track,
            "bitrate": hd.bitrate,
            "audio_codec": hd.audio_codec,
        }

        
        # try:
        # caption tracks https://pytube.io/en/latest/user/captions.html
        caption_file_stem = Path(hd.default_filename).stem 

        # print(f"downloading captions for YT ID = {yt_id}")
        # print(f"captions will go to {video_download_folder}/{caption_file_stem}")



        captions = yt.captions

        # print("captions")
        # print(captions)
        # print("keys:")
        # print(captions.keys())
        for caption in captions: 
            # print(caption.name)
            # print(caption.code)
            with open(video_download_folder / f"{caption.name} {caption.code}.json", "w") as cf:
                json.dump(caption.json_captions, cf)


        results["captions_downloaded"] = [caption.name for caption in captions]

        return results

    except (AgeRestrictedError, HTTPError, VideoPrivate, VideoUnavailable) as e:
        return {
            "video_downloaded_successfully": False,
            "video_file_path": None,
            "video_download_error": f"{type(e)},{e}",
        }

if __name__ == "__main__":
    youtube_ids = []
    video_count = 30
    dataset_folder = Path("/media/vlab/storage/data/YouTube-ASL")
    download_folder = dataset_folder / "downloads"
    download_folder.mkdir(parents=True, exist_ok=True)


    save_results_path = dataset_folder / "download_results.json"
    try:
        with open(save_results_path, "r") as srf:
            download_results = json.load(srf)
    except FileNotFoundError:
        download_results = {}


    with open("youtube_asl_video_ids.txt") as yt_ids_f:
        youtube_ids = yt_ids_f.read().splitlines()

        # TODO: parallelize with https://www.markhneedham.com/blog/2018/07/15/python-parallel-download-files-requests/


        # for yt_id in tqdm(random.sample(youtube_ids, video_count)):
        for yt_id in tqdm(youtube_ids[:video_count]):
            if yt_id not in download_results:
            # for yt_id in tqdm(youtube_ids):   
                download_results[yt_id] = download_vid(yt_id=yt_id, 
                                                    download_folder=download_folder)

    
            
    # print(json.dumps(download_results, indent=4))

    with open(str(save_results_path), "w") as download_results_file:
        json.dump(download_results, download_results_file)