import argparse
import random
import sys

static_html_start="""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title id="page_title">Random YouTube Video Grid</title>
    <style>
        .video-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
            gap: 20px;
            padding: 20px;
        }
    </style>
    <script>
        function displayRandomVideos() {
            const videoIDs = [
"""
static_html_end = """                            
                // 'VIDEO_ID_1', 'VIDEO_ID_2', 'VIDEO_ID_3', // Add your video IDs here
                // 'VIDEO_ID_4', 'VIDEO_ID_5', 'VIDEO_ID_6',
                // Add more IDs as needed
            ];

            const numVideos = 6; // Number of videos to display

            // Randomly select video IDs
            const selectedVideos = [];
            for (let i = 0; i < numVideos; i++) {
                const randomID = videoIDs[Math.floor(Math.random() * videoIDs.length)];
                selectedVideos.push(randomID);
            }

            // Set the title
            const pageTitle = document.getElementById("page_title")
            pageTitle.innerHTML = numVideos + " Random YouTube-ASL Videos"

            // set the Heading
            const pageHeading = document.getElementById("page_heading")
            pageHeading.innerHTML = numVideos + " Random YouTube-ASL Videos"

            // set the explanation
            const explanation_text = document.getElementById("explanation")
            explanation_text.innerHTML = numVideos + " out of a set of " + videoIDs.length + " random videos sampled from the <a href='https://proceedings.neurips.cc/paper_files/paper/2023/hash/5c61452daca5f0c260e683b317d13a3f-Abstract-Datasets_and_Benchmarks.html'>YouTube-ASL Dataset</a>. Reload to view a different " + numVideos + ". Scroll down to see the sample set."

            
            // more_explanation
            const more_explanation = document.getElementById("more_explanation")
            more_explanation.innerHTML =  "This demo selects " + numVideos + " video IDs from the following hardcoded list of " + videoIDs.length + " (sampled from <a href='https://storage.googleapis.com/gresearch/youtube-asl/youtube_asl_video_ids.txt'>the full YT-ASL list</a>):"

            // set the full list
            // explain_2
            // videoIDs
            // full_list


            const full_list = document.getElementById("full_list")
            full_list.innerHTML ="[" + videoIDs + "]"
            

            // Build the video grid
            const videoGrid = document.getElementById("video-grid");
            videoGrid.innerHTML = '';  // Clear any existing videos

            selectedVideos.forEach(youtubeID => {
                const iframe = document.createElement('iframe');
                iframe.src = `https://www.youtube.com/embed/${youtubeID}?autoplay=1&mute=1&loop=1&playlist=${youtubeID}&cc_load_policy=1&cc_lang_pref=en&hl=en`;
                iframe.width = "420";
                iframe.height = "315";
                iframe.frameBorder = "0";
                iframe.allowFullscreen = true;
                iframe.allow = "autoplay";
                videoGrid.appendChild(iframe);
            });
        }

        // Execute the function when the page loads
        window.onload = displayRandomVideos;
    </script>
</head>

<body>
    <h1 id="page_heading">Random YouTube Video Grid</h1>    
    <p id="explanation">Hi!</p>
    <p><a href="https://github.com/cleong110/explore-youtube-asl">Source code here.</a></p>
    <div class="video-grid" id="video-grid">
        <!-- The grid of videos will be inserted here -->
    </div>
    <p id="more_explanation"></p>
    <p id="full_list"></p>
</body>

</html>"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="YouTube ASL Explorer Static HTML generator",
        description="Makes an HTML file you can just open by hardcoding in a bunch of IDs from the YouTube ASL list",
    )

    parser.add_argument(
        "video_count", type=int, default=100
    )

    args = parser.parse_args()
    youtube_ids = []
    video_count = args.video_count

    with open("youtube_asl_video_ids.txt") as yt_ids_f:
        youtube_ids = yt_ids_f.read().splitlines()

    if youtube_ids:
        sample_vid_ids = [f"'{yt_id}'," for yt_id in random.sample(youtube_ids, video_count)]
        print(sample_vid_ids)
        html_string = f"{static_html_start}{"".join(sample_vid_ids)}{static_html_end}"
        with open("yt_asl_static_demo.html", "w") as static_f:
            
            static_f.write(html_string)


    else: 
        print("Couldn't load the IDs. Make sure they are downloaded to youtube_asl_video_ids.txt")
