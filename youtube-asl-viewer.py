# http://www.compjour.org/lessons/flask-single-page/simple-youtube-viewing-flask-app/
# https://www.w3schools.com/html/html_youtube.asp
from flask import Flask
import random
app = Flask(__name__)

@app.route('/')
def homepage():
    youtube_ids = []
    with open("youtube_asl_video_ids.txt") as yt_ids_f:
        youtube_ids = yt_ids_f.readlines()


    htmlstring = """
    <h1>Random Youtube-ASL Videos</h1>
    """

    if youtube_ids:
        for youtube_id in random.sample(youtube_ids, 12):
            # embed = f"<iframe src=\"https://www.youtube.com/embed/{youtube_id}\" width=\"853\" height=\"480\" frameborder=\"0\" allowfullscreen></iframe>"
            
            # autoplay, muted, looped
            embed = f"<iframe src=\"https://www.youtube.com/embed/{youtube_id}?autoplay=1&mute=1&loop=1\"  width=\"420\" height=\"315\" frameborder=\"0\" allowfullscreen></iframe>"
            
            htmlstring = f"{htmlstring}\n{embed}"



    return htmlstring

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True )