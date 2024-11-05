import argparse
from pathlib import Path
import json
from typing import List

# 4eNt91uV02o {'video_downloaded_successfully': True, 'video_file_path': '/media/vlab/storage/data/YouTube-ASL/downloads/4eNt91uV02o/Harry Potter The Dream Team (Sign Language).mp4', 'title': 'Harry Potter: The Dream Team (Sign Language)', 'filesize_bytes': 2438029, 'includes_audio_track': True, 'includes_video_track': True, 'bitrate': 351712, 'audio_codec': 'mp4a.40.2', 'captions_downloaded': ['English', 'English (auto-generated)']}
def get_successfully_downloaded_keys(json_results) -> List[str]:
    successes = [key for key in json_results.keys() if json_results[key]["video_downloaded_successfully"]]
    return successes

def write_out_unique(unique_list, original_results_dict, stem):
    out_path = Path.cwd()/f"unique_to_{stem}.json"
    with out_path.open("w") as out_f:
        unique_to_dict = {}
        for id in unique_list:
            unique_to_dict[id] = original_results_dict[id]
        json.dump(unique_to_dict, out_f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="YouTube ASL download JSON comparison",
        description="Given two jsons, checks which files are in one and which are in the other and such.",
    )

    parser.add_argument(
        "first_json", type=Path
    )
    parser.add_argument("second_json", type=Path)

    args = parser.parse_args()

    with args.first_json.open() as fjf:
        first_download_results = json.load(fjf)
        print(f"JSON 1: {args.first_json}")
    
    with args.second_json.open() as sjf:
        second_download_results = json.load(sjf)
        print(f"JSON 2: {args.second_json}")


    
    if first_download_results and second_download_results:
        result_dicts = [first_download_results, second_download_results]
        success_sets = []
        for i, result_dict in enumerate(result_dicts):
            n = i+1


                
            print(f"loaded {len(result_dict.keys())} from {n} json")
            successes = get_successfully_downloaded_keys(result_dict)
            
            print(f"JSON {n} had this many successes: {len(successes)}")

            print(successes[:20])
            success_sets.append(set(successes))
        
        intersection = success_sets[0].intersection(success_sets[1])
        unique_to_first = success_sets[0].difference(success_sets[1])
        unique_to_second = success_sets[1].difference(success_sets[0])
        print(f"Intersection size: {len(intersection)}")
        print(f"Only in 1st: {len(unique_to_first)}")
        write_out_unique(unique_to_first, first_download_results, args.first_json.stem)
        

        print(f"Only in 2nd: {len(unique_to_second)}")

        write_out_unique(unique_to_second, second_download_results, args.second_json.stem)

        

