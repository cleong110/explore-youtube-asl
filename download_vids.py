from pytube import YouTube
from pytube.exceptions import AgeRestrictedError, VideoPrivate, VideoUnavailable
from urllib.error import HTTPError
from http.client import IncompleteRead, RemoteDisconnected
import random
from tqdm import tqdm
import json
from pathlib import Path
import traceback
from multiprocessing.pool import ThreadPool
import timeit
# https://github.com/pytube/pytube/issues/1954 stopped me. 
# had to manually edit /home/vlab/miniconda3/envs/explore-youtube-asl/lib/python3.12/site-packages/pytube/cipher.py

def call_download(url_and_download_path:tuple)->dict:
    yt_id, download_folder = url_and_download_path
    return download_vid(yt_id=yt_id, download_folder=download_folder)

def download_vid(yt_id:str, download_folder:Path) -> dict:

    # download, or add to error dict
    try:
        video_download_folder = download_folder/ yt_id
        yt = YouTube(f'http://youtube.com/watch?v={yt_id}')
        
        # print(yt.streams)
        hd = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        out = hd.download(output_path=str(video_download_folder))

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

        print(f"{yt.title}: {hd.filesize_mb} mb downloaded")

        
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

        return yt_id, results

    except (AgeRestrictedError, HTTPError, VideoPrivate, VideoUnavailable, IncompleteRead, RemoteDisconnected) as e:
        return yt_id, {
            "video_downloaded_successfully": False,
            "video_file_path": None,
            "video_download_error": f"{type(e)},{e}",
        }

if __name__ == "__main__":
    youtube_ids = []
    threads_count = 8

    for i in range(20000):
        
        video_count = 40
        
        dataset_folder = Path("/media/vlab/storage/data/YouTube-ASL")

        print("\n\n**************************************************************************************************")
        print(f"Iteration {i}: downloading {video_count} videos to {dataset_folder}, using {threads_count} threads")
        download_folder = dataset_folder / "downloads"
        download_folder.mkdir(parents=True, exist_ok=True)


        save_results_path = dataset_folder / "download_results.json"
        try:
            with open(save_results_path, "r") as srf:
                download_results = json.load(srf)
        except FileNotFoundError:
            download_results = {}

        print(f"So far we have {len(download_results)} results")


        with open("youtube_asl_video_ids.txt") as yt_ids_f:
            youtube_ids = yt_ids_f.read().splitlines()


            #TODO: retry the ones with HTTPError, RemoteDisconnected, IncompleteRead

            # make tuples so we can call the one-argument function
            tuples_youtube_ids_to_process_with_download_folder = [(yt_id,download_folder) for yt_id in youtube_ids if yt_id not in download_results]
            tuples_youtube_ids_to_process_with_download_folder = tuples_youtube_ids_to_process_with_download_folder[:video_count]
            first_id = tuples_youtube_ids_to_process_with_download_folder[0][0]
            yt_id_index = youtube_ids.index(first_id)

            print(f"first ID in batch is {first_id}, which is id {yt_id_index} of {len(youtube_ids)}")
            start_time = timeit.default_timer()
            
            thread_results = ThreadPool(threads_count).imap_unordered(call_download, tuples_youtube_ids_to_process_with_download_folder)
            
            for yt_id, result in thread_results: 
                download_results[yt_id] = result
            # for yt_id_and_folder in tqdm(tuples_youtube_ids_to_process_with_download_folder):
            #         # download_results[yt_id] = download_vid(yt_id=yt_id, 
            #         #                                     download_folder=download_folder)
            #         yt_id, result = call_download(yt_id_and_folder)
            #         download_results[yt_id] = result
            download_duration = timeit.default_timer() - start_time
            print(f"Download took {download_duration:.2f} seconds")

        
                
        # print(json.dumps(download_results, indent=4))
        print(f"saving results to {save_results_path}")
        with open(str(save_results_path), "w") as download_results_file:
            json.dump(download_results, download_results_file)

        print("**************************************************************************************************")