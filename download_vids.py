from pytubefix import YouTube
from pytubefix.exceptions import AgeRestrictedError, VideoPrivate, VideoUnavailable
from urllib.error import HTTPError
from http.client import IncompleteRead, RemoteDisconnected
import random
from tqdm import tqdm
import json
from pathlib import Path
import traceback
from multiprocessing.pool import ThreadPool
import timeit
import itertools

# https://github.com/pytube/pytube/issues/1954 stopped me.
# had to manually edit /home/vlab/miniconda3/envs/explore-youtube-asl/lib/python3.12/site-packages/pytube/cipher.py
# https://github.com/pytube/pytube/issues/1894#issue-2180600881 as well, 
# Tried to switch innertube.py to https://github.com/JuanBindez/pytubefix/blob/c0c07b046d8b59574552404931f6ce3c6590137d/pytubefix/innertube.py
# eventually just used pytubefix https://github.com/JuanBindez/pytubefix


def call_download(url_and_download_path: tuple) -> dict:
    yt_id, download_folder = url_and_download_path
    return download_vid(yt_id=yt_id, download_folder=download_folder)


def download_vid(yt_id: str, download_folder: Path) -> dict:

    # download, or add to error dict
    try:
        video_download_folder = download_folder / yt_id
        
        yt = YouTube(f"http://youtube.com/watch?v={yt_id}")

        # print(yt.streams)
        hd = (
            yt.streams.filter(progressive=True, file_extension="mp4")
            .order_by("resolution")
            .desc()
            .first()
        )
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
        
        # caption tracks https://pytube.io/en/latest/user/captions.html

        # print(f"downloading captions for YT ID = {yt_id}")
        # print(f"captions will go to {video_download_folder}/{caption_file_stem}")

        captions = yt.captions
        results["captions"]= {}
        # print("captions")
        # print(captions)
        # print("keys:")
        # print(captions.keys())
        for caption in captions:
            # print(caption.name)
            print(f"\tDownloading caption language: {caption.name}")
            

            caption_download_path = video_download_folder / f"{yt_id}_{caption.code}.json"
            # print(caption.code)
            with open(
                # video_download_folder / f"{caption.name} {caption.code}.json", "w"
                caption_download_path, "w" # caption name can be literally anything, including slashes
            ) as cf:
                json.dump(caption.json_captions, cf)
            
            results["captions"][caption.code] = {
                "caption_file_path": caption_download_path,
                "name": caption.name,
                }

        # results["captions"]["captions_downloaded"] = [caption.name for caption in captions]

        return yt_id, results

    except (
        AgeRestrictedError,
        HTTPError,
        VideoPrivate,
        VideoUnavailable,
        IncompleteRead,
        RemoteDisconnected,
    ) as e:        
        return yt_id, {
            "video_downloaded_successfully": False,
            "video_file_path": None,
            "video_download_error": f"{type(e)},{e}",
        }


def download_vids_multithreaded(threads_count, download_results, tuples_youtube_ids_to_process_with_download_folder):
    print("---")
    start_time = timeit.default_timer()

    thread_results = ThreadPool(threads_count).imap_unordered(
            call_download, tuples_youtube_ids_to_process_with_download_folder
        )

    for yt_id, result in thread_results:
        download_results[yt_id] = result
    download_duration = timeit.default_timer() - start_time

    print(f"Download took {download_duration:.2f} seconds")
    print("---")

def load_download_results(save_results_path):
    try:
        with open(save_results_path, "r") as srf:
            download_results = json.load(srf)
    except FileNotFoundError:
        download_results = {}
    return download_results

if __name__ == "__main__":
    youtube_ids = []
    threads_count = 8

    with open("youtube_asl_video_ids.txt") as yt_ids_f:
        youtube_ids = yt_ids_f.read().splitlines()

    dataset_folder = Path("/media/vlab/storage/data/YouTube-ASL")
    download_folder = dataset_folder / "downloads"
    download_folder.mkdir(parents=True, exist_ok=True)
    save_results_path = dataset_folder / "download_results.json"
    result_count = 0
    video_count = 50
    i = 0

    while result_count < len(youtube_ids) and i < 1000:
        i = i + 1

        print(
            "\n\n**************************************************************************************************"
        )
        print(
            f"Batch {i}: downloading {video_count} videos to {dataset_folder}, using {threads_count} threads"
        )

        
        download_results = load_download_results(save_results_path)

        successful_video_downloads = [
            key
            for key in download_results.keys()
            if download_results[key]["video_downloaded_successfully"]
        ]
        print(
            f"So far we have {len(download_results)} results, of which {len(successful_video_downloads)} were successful"
        )
        result_count = len(download_results)

        

        # make tuples so we can call the one-argument function, and filter out already-downloaded results.
        tuples_youtube_ids_to_process_with_download_folder = [
            (yt_id, download_folder)
            for yt_id in youtube_ids
            if yt_id not in download_results
        ]

        print(f"{len(tuples_youtube_ids_to_process_with_download_folder)} IDs still unprocessed")


        # error_ids.extend(tuples_youtube_ids_to_process_with_download_folder)
        # tuples_youtube_ids_to_process_with_download_folder = error_ids
        # tuples_youtube_ids_to_process_with_download_folder.extend(error_ids) # put the retries at the end

        # tuples_youtube_ids_to_process_with_download_folder = error_ids

        tuples_youtube_ids_to_process_with_download_folder = (
            tuples_youtube_ids_to_process_with_download_folder[:video_count]
        )

        if tuples_youtube_ids_to_process_with_download_folder:

            first_id = tuples_youtube_ids_to_process_with_download_folder[0][0]
            yt_id_index = youtube_ids.index(first_id)

            print(
                f"first ID in batch is {first_id}, which is id {yt_id_index} of {len(youtube_ids)}"
            )
            if first_id in download_results:
                print(download_results[first_id])
            
            download_vids_multithreaded(threads_count, download_results, tuples_youtube_ids_to_process_with_download_folder)
            

            if first_id in download_results:
                print(download_results[first_id])



            # print(json.dumps(download_results, indent=4))
            print(f"saving results to {save_results_path}")


            with open(str(save_results_path), "w") as download_results_file:
                json.dump(download_results, download_results_file)

            print(
                "**************************************************************************************************"
            )



print("Retrying videos that had http errors")
load_download_results(save_results_path)

# retry the ones with HTTPError, http.client.RemoteDisconnected, http.client.IncompleteRead
error_ids = [
    (yt_id, download_folder)
    for yt_id in youtube_ids
    if yt_id in download_results
    and "http"
    in str(
        download_results[yt_id].get("video_download_error")
    ).lower()  # get returns None if there's none
]


print(f"{len(error_ids)} of the results had an http error of some kind and can be retried")
error_slices = list(itertools.batched(error_ids, video_count))
for error_slice in tqdm(error_slices, total=len(error_slices)):
    first_id = error_slice[0][0]
    yt_id_index = youtube_ids.index(first_id)

    print(
        f"first ID in batch is {first_id}, which is id {yt_id_index} of {len(youtube_ids)}"
    )

    download_vids_multithreaded(threads_count, download_results, error_slice)

    print(f"saving results to {save_results_path}")
    with open(str(save_results_path), "w") as download_results_file:
        json.dump(download_results, download_results_file)


