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
import multiprocessing
import timeit
import itertools
import argparse

# https://github.com/pytube/pytube/issues/1954 stopped me.
# had to manually edit /home/vlab/miniconda3/envs/explore-youtube-asl/lib/python3.12/site-packages/pytube/cipher.py
# https://github.com/pytube/pytube/issues/1894#issue-2180600881 as well,
# Tried to switch innertube.py to https://github.com/JuanBindez/pytubefix/blob/c0c07b046d8b59574552404931f6ce3c6590137d/pytubefix/innertube.py
# eventually just used pytubefix https://github.com/JuanBindez/pytubefix


def call_download_with_one_arg(args_tuple: tuple) -> dict:
    yt_id, download_folder, download_audio, download_captions = args_tuple
    return download_vid(yt_id=yt_id, download_folder=download_folder)


def download_vid(
    yt_id: str, download_folder: Path, download_audio=True, download_captions=True
) -> dict:

    # download, or add error info
    try:
        video_download_folder = download_folder / yt_id
        # filename = f"{yt_id}.mp4"

        yt = YouTube(f"http://youtube.com/watch?v={yt_id}")

        # print(yt.streams)
        hd = (
            yt.streams.filter(progressive=True, file_extension="mp4")
            .order_by("resolution")
            .desc()
            .first()
        )
        vid_out_path = hd.download(
            output_path=str(video_download_folder),
            filename=f"{yt_id}.mp4",  # default name is OS-safe and more human-readable, but still a pain
        )
        vid_out_path = Path(vid_out_path)

        results = {
            "video_downloaded_successfully": True,
            "video_file_path": vid_out_path,
            "title": hd.title,
            "filesize_bytes": hd.filesize,
            "includes_audio_track": hd.includes_audio_track,
            "includes_multiple_audio_tracks": hd.includes_multiple_audio_tracks,
            "includes_video_track": hd.includes_video_track,
            "bitrate": hd.bitrate,
            "audio_codec": hd.audio_codec,
        }

        if download_audio:
            ###############
            # Audio
            # https://pytubefix.readthedocs.io/en/latest/user/mp3.html
            ys = yt.streams.get_audio_only()
            audio_file_path = ys.download(
                output_path=str(video_download_folder), filename=yt_id, mp3=True
            )
            audio_file_path = Path(audio_file_path)
            #   print(f"\tDownloaded {yt_id} audio: {audio_file_path.name}")
            results["audio"] = {
                "audio_file_path": str(audio_file_path.absolute()),
                "audio_codec": ys.audio_codec,
                "bitrate": ys.bitrate,
                "filesize": ys.filesize,
                "audio_track_name": ys.audio_track_name,
            }

        if download_captions:
            ##################
            # captions
            # caption tracks https://pytube.io/en/latest/user/captions.html

            captions = yt.captions
            results["captions"] = {}

            for caption in captions:
                # print(caption.name)
                #   print(f"\tDownloading {yt_id} caption: language: {caption.name}, code {caption.code}")

                # caption name can be literally anything, including slashes.
                # but the caption code is unique, uses vssid internally I believe.
                caption_json_path = (
                    video_download_folder / f"{yt_id} ({caption.code}).json"
                )
                caption_json_path = Path(caption_json_path)
                with open(caption_json_path, "w") as cf:
                    json.dump(caption.json_captions, cf)

                caption_srt_path = caption.download(
                    output_path=video_download_folder, title=f"{yt_id}.srt", srt=True
                )
                caption_srt_path = Path(caption_srt_path)
                #   print(f"")
                #   print(f"\tDownloaded {yt_id} caption: language: {caption.name}, code {caption.code}\n\t\tJSON: {caption_json_path.name}, \n\t\tSRT: {caption_srt_path.name}")

                results["captions"][caption.code] = {
                    "caption_json_path": str(caption_json_path),
                    "caption_srt_path": str(caption_srt_path),
                    "name": caption.name,
                }

        
        

        # caption_results = [f"\n\tCaption ({caption_code}), aka '{result['name']}' downloaded to \n\t\tSRT: {Path(result['caption_srt_path']).name}\n\t\t{Path(result['caption_json_path']).name}" for caption_code, result in results.get("captions").items()]
        caption_results = [f"\n\tCaption downloaded:\t{caption_code:<10}\taka\t{result['name']:<15}" for caption_code, result in results.get("captions").items()]
        results_str = "".join(caption_results)

        audio_results = results.get("audio")
        if audio_results:
            # results_str = f"{results_str}\n\tAudio downloaded to: {Path(audio_results['audio_file_path']).name}"
            results_str = f"{results_str}\n\tAudio downloaded"

        
            
        print(
            f"\n{yt_id}:\n\tTitle: '{yt.title}'",
            f"\n\tDownload folder: '{video_download_folder.absolute()}'",
            f"\n\tVideo downloaded to {vid_out_path.name}",
            f"\n\t\tSize: {hd.filesize_mb} mb",
            results_str,
        )
        return yt_id, results

    except (
        AgeRestrictedError,
        HTTPError,
        VideoPrivate,
        VideoUnavailable,
        IncompleteRead,
        RemoteDisconnected,
    ) as e:
        print(f"{yt_id}:\t{str(e)}")
        return yt_id, {
            "video_downloaded_successfully": False,
            "video_file_path": None,
            "video_download_error": f"{type(e)},{e}",
        }


def download_vids_multithreaded(
    threads_count,
    download_results,
    yt_ids_to_process,
    download_folder,
    download_audio=True,
    download_captions=True,
):
    print("---")
    start_time = timeit.default_timer()

    # get it into the right format to call multithreaded.
    arg_tuples_list = [
        (yt_id, download_folder, download_audio, download_captions)
        for yt_id in yt_ids_to_process
    ]

    thread_results = ThreadPool(threads_count).imap_unordered(
        call_download_with_one_arg, arg_tuples_list
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
    except json.decoder.JSONDecodeError:
        print(
            f"JSONDecodeError loading JSON at {save_results_path.absolute()}, it might be corrupted. Try removing it and re-running this!"
        )
        raise

    return download_results


if __name__ == "__main__":

    default_thread_count = multiprocessing.cpu_count() - 1

    parser = argparse.ArgumentParser(
        prog="YouTube ASL downloader",
        description="Downloads vids from YouTube ASL dataset in batches, saving results as it goes and continuing where it left off if interrupted.",
    )

    parser.add_argument(
        "--dataset_folder", type=Path, default="/media/vlab/storage/data/YouTube-ASL"
    )
    parser.add_argument("--thread_count", type=int, default=default_thread_count)
    parser.add_argument(
        "--id_file_path", type=Path, default="youtube_asl_video_ids.txt"
    )
    parser.add_argument(
        "--batch_video_count", type=int, default=default_thread_count * 2
    )
    parser.add_argument("--download_captions", action="store_true")
    parser.add_argument("--download_audio", action="store_true")

    args = parser.parse_args()

    youtube_ids = []

    threads_count = args.thread_count

    with open(args.id_file_path) as yt_ids_f:
        youtube_ids = yt_ids_f.read().splitlines()

    dataset_folder = args.dataset_folder
    download_folder = dataset_folder / "downloads"
    download_folder.mkdir(parents=True, exist_ok=True)
    save_results_path = dataset_folder / "download_results.json"
    result_count = 0
    batch_video_count = args.batch_video_count

    print(
        f"Dataset folder set to: {dataset_folder}, which works out to {dataset_folder.absolute()}"
    )
    print(
        f"Download results, details, and stats will be saved at {save_results_path.absolute()}"
    )

    # basically if we've tried twice the required number batches we should give up
    iteration_limit = len(youtube_ids) / batch_video_count * 2
    i = 0
    while result_count < len(youtube_ids) and i < iteration_limit:
        i = i + 1

        print(
            "\n\n**************************************************************************************************"
        )
        print(
            f"Batch {i}: downloading {batch_video_count} videos to {dataset_folder.absolute()}, using {threads_count} threads"
        )

        print(f"Loading results from {save_results_path.absolute()}")
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
        yt_ids_to_process = [
            yt_id for yt_id in youtube_ids if yt_id not in download_results
        ]

        print(f"{len(yt_ids_to_process)} IDs still unprocessed")

        # error_ids.extend(tuples_youtube_ids_to_process_with_download_folder)
        # tuples_youtube_ids_to_process_with_download_folder = error_ids
        # tuples_youtube_ids_to_process_with_download_folder.extend(error_ids) # put the retries at the end

        # tuples_youtube_ids_to_process_with_download_folder = error_ids

        yt_ids_to_process = yt_ids_to_process[:batch_video_count]

        if yt_ids_to_process:

            first_id = yt_ids_to_process[0]
            yt_id_index = youtube_ids.index(first_id)

            print(
                f"first ID in batch is {first_id}, which is id {yt_id_index} of {len(youtube_ids)}"
            )
            if first_id in download_results:
                print(download_results[first_id])

            download_vids_multithreaded(
                threads_count,
                download_results,
                yt_ids_to_process,
                download_folder,
                download_audio=args.download_audio,
                download_captions=args.download_captions,
            )

            if first_id in download_results:
                print(download_results[first_id])

            # print(json.dumps(download_results, indent=4))
            print(f"saving results to {save_results_path.absolute()}")

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


print(
    f"{len(error_ids)} of the results had an http error of some kind and can be retried"
)
error_slices = list(itertools.batched(error_ids, batch_video_count))
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
