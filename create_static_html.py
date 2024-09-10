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
        #full_list {
            display: none;
            margin-top: 20px;
            padding: 10px;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 5px;
        }

        /* Add smooth transition */
        .expanded {
            display: block;
            transition: max-height 0.3s ease-out;
        }

        /* Style the list */
        ul {
            list-style-type: none; /* Remove bullets */
            padding-left: 0;       /* Remove padding */
        }

        ul li {
            margin-bottom: 5px;    /* Space between list items */
            padding: 5px;
            background-color: #f0f0f0; /* Light background for each item */
            border-radius: 3px;    /* Rounded corners for list items */
            border: 1px solid #ddd; /* Border around each item */
        }
    </style>
    <script>
        
        function toggleFullList() {
            const fullList = document.getElementById("full_list");
            const toggleButton = document.getElementById("toggle_button");

            // Treat empty string as 'none'
            const isHidden = fullList.style.display === "none" || fullList.style.display === "";

            console.log("Current fullList display: ", fullList.style.display);

            if (isHidden) {
                console.log("Showing the list...");
                // Display the "Loading..." message first
                fullList.style.display = "block";
                toggleButton.innerHTML = "Hide Full List"; // Change button text
                fullList.innerHTML = '';  // Clear the loading message

                const ul = document.createElement('ul'); // Create an unordered list
                videoIDs.forEach(id => {
                    const li = document.createElement('li'); // Create a list item for each video ID
                    li.innerText = id; // Set the text content to the video ID
                    ul.appendChild(li); // Append the list item to the unordered list
                });
                fullList.appendChild(ul); // Append the unordered list to the 'full_list' div
            } else {
                console.log("Hiding the list...");
                // Hide the list
                fullList.style.display = "none";
                toggleButton.innerHTML = "View Full List"; // Revert button text
            }
        }
        function getQueryParam(param) {
            const urlParams = new URLSearchParams(window.location.search);
            return urlParams.get(param);
        }

        
        const videoIDs = [
"""

static_html_end = """                            
                // 'VIDEO_ID_1', 'VIDEO_ID_2', 'VIDEO_ID_3', // Add your video IDs here
                // 'VIDEO_ID_4', 'VIDEO_ID_5', 'VIDEO_ID_6',
                // Add more IDs as needed
            ];
        function displayRandomVideos() {        

            // Get the number of videos to display from the query string (default to 10 if not specified)
            let numVideos = parseInt(getQueryParam('numVideos')) || 10;
            let vid_width = parseInt(getQueryParam('vid_width')) || 420;
            let vid_height = parseInt(getQueryParam('vid_height')) || 315;

            // Randomly select video IDs
            const selectedVideos = [];
            for (let i = 0; i < numVideos; i++) {
                const randomID = videoIDs[Math.floor(Math.random() * videoIDs.length)];
                selectedVideos.push(randomID);
            }

            // Set the title
            const pageTitle = document.getElementById("page_title");
            pageTitle.innerHTML = numVideos + " Random YouTube-ASL Videos";

            // set the Heading
            const pageHeading = document.getElementById("page_heading");
            pageHeading.innerHTML = numVideos + " Random YouTube-ASL Videos";

            // set the explanation
            const explanation_text = document.getElementById("explanation");
            explanation_text.innerHTML = numVideos + " out of a set of " + videoIDs.length + " random videos sampled from the <a href='https://proceedings.neurips.cc/paper_files/paper/2023/hash/5c61452daca5f0c260e683b317d13a3f-Abstract-Datasets_and_Benchmarks.html'>YouTube-ASL Dataset</a>. Reload to view a different " + numVideos + ". Scroll down to see the sample set.";

            const query_string_explanation = document.getElementById("query_string_explanation");
            const url_example = window.location.href.split('?')[0] + "?numVideos=12"
            console.log("url example " + url_example)
            query_string_explanation.innerHTML = "If you would like to change the number of videos, please add ?numVideos=<the number you want> to the URL, e.g. <a href=" + url_example + ">" + url_example + "</a> to view 12 at once.";
            console.log("*****************")
            console.log(query_string_explanation.innerHTML)
            

            // more_explanation
            const more_explanation = document.getElementById("more_explanation");
            more_explanation.innerHTML =  "This demo selects " + numVideos + " video IDs from the following hardcoded list of " + videoIDs.length + " (sampled from <a href='https://storage.googleapis.com/gresearch/youtube-asl/youtube_asl_video_ids.txt'>the full YT-ASL list</a>):";

            // set the full list
            const full_list = document.getElementById("full_list");
            full_list.innerHTML = "[" + videoIDs + "]";

            // Build the video grid
            const videoGrid = document.getElementById("video-grid");
            videoGrid.innerHTML = '';  // Clear any existing videos

            selectedVideos.forEach(youtubeID => {
                const iframe = document.createElement('iframe');
                iframe.src = `https://www.youtube.com/embed/${youtubeID}?autoplay=1&mute=1&loop=1&playlist=${youtubeID}&cc_load_policy=1&cc_lang_pref=en&hl=en`;
                iframe.width = vid_width;
                iframe.height = vid_height;
                iframe.frameBorder = "0";
                iframe.allowFullscreen = true;
                iframe.allow = "autoplay";
                videoGrid.appendChild(iframe);
            });

        }

        // Execute the function when the page loads
        window.onload = function() {
            console.log("window.location.href");
            console.log(window.location.href);
            // Call both functions when the page loads
            displayRandomVideos(); 
                        
            // Ensure the full list is hidden when the page first loads
            const fullList = document.getElementById("full_list");
            fullList.style.display = "none"; // Explicitly set it to "none" on load
            console.log("Initial full list display set to none and the URL is " + window.location.href);
        };


    </script>
</head>

<body>
    <h1 id="page_heading">Random YouTube Video Grid</h1>    
    <p id="explanation">Hi!</p>
    <p><a href="https://github.com/cleong110/explore-youtube-asl">Source code here.</a></p>
    <p id="query_string_explanation">insert query string explanation</p>
    <div class="video-grid" id="video-grid">
        <!-- The grid of videos will be inserted here -->
    </div>
    <p id="more_explanation"></p>
    
    <!-- <p>You can change vid_width (default:420) and vid_height (default:315) the same way.</p>
    <p>So for example: ?numVideos=10&vid_width=840&vid_height=630</p> -->
    <p>Click the button below to view the full list of videos.</p>
    <!-- Button to toggle the full list visibility -->
    <button id="toggle_button" onclick="toggleFullList()">View Full List</button>

    <!-- Hidden unordered list that will show the full list -->
    <div id="full_list"></div>
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
        with open(f"yt_asl_static_demo_{video_count}_vids.html", "w") as static_f:
            static_f.write(html_string)
    else: 
        print("Couldn't load the IDs. Make sure they are downloaded to youtube_asl_video_ids.txt")
