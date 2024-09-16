# https://realpython.com/python-download-file-from-url/#downloading-a-file-from-a-url-in-python
# https://www.geeksforgeeks.org/how-to-download-files-from-urls-with-python/
import requests
yt_asl_url = r"https://storage.googleapis.com/gresearch/youtube-asl/youtube_asl_video_ids.txt"
yt_sl_25_url = r"https://storage.googleapis.com/gresearch/youtube-sl-25/youtube-sl-25-metadata.csv" # TODO: download this one too

response = requests.get(yt_asl_url)
file_Path = 'youtube_asl_video_ids.txt'

if response.status_code == 200:
	with open(file_Path, 'wb') as file:
		file.write(response.content)
	print('File downloaded successfully')
else:
	print('Failed to download file')

