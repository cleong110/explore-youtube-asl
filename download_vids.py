from pytube import YouTube
from pytube.exceptions import AgeRestrictedError, VideoPrivate, VideoUnavailable
from urllib.error import HTTPError
import random
from tqdm import tqdm
import json
from pathlib import Path
# https://github.com/pytube/pytube/issues/1954 stopped me. 
# had to manually edit /home/vlab/miniconda3/envs/explore-youtube-asl/lib/python3.12/site-packages/pytube/cipher.py


if __name__ == "__main__":
    youtube_ids = []
    video_count = 1000
    dataset_folder = Path("/media/vlab/storage/data/YouTube-ASL/")
    download_folder = dataset_folder / "videos"
    captions_folder = dataset_folder / "captions"
    download_results = {}
    with open("youtube_asl_video_ids.txt") as yt_ids_f:
        youtube_ids = yt_ids_f.read().splitlines()


        # for yt_id in tqdm(random.sample(youtube_ids, video_count)):
        for yt_id in tqdm(youtube_ids[:video_count]):            
        # for yt_id in tqdm(youtube_ids):            

            # download, or add to error dict
            try:
                yt = YouTube(f'http://youtube.com/watch?v={yt_id}')
                # print(yt.title)
                # print(yt.streams)
                hd = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                hd.download(output_path=str(download_folder))

                # TODO: caption tracks https://pytube.io/en/latest/user/captions.html
                # caption_file_stem = Path(hd.default_filename).stem 
                # caption_file_download_path = captions_folder / f"{caption_file_stem}.json"
                # if yt.captions:
                # with open(caption_file_download_path, "w") as captions_file:
                #     json.dump(yt.captions, captions_file)
                download_results[yt_id] = {
                    "title": hd.title,
                    "filesize_bytes": hd.filesize,
                    "includes_audio_track": hd.includes_audio_track,
                    "includes_video_track": hd.includes_video_track,
                    "bitrate": hd.bitrate,
                    "audio_codec": hd.audio_codec,
                }

            except (AgeRestrictedError, HTTPError, VideoPrivate, VideoUnavailable) as e:
                download_results[yt_id] = str(e)
    
            
    print(json.dumps(download_results, indent=4))

    save_results_path = dataset_folder / "download_results.json"
    with open(str(save_results_path), "w") as download_results_file:
        json.dump(download_results, download_results_file)