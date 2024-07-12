# https://realpython.com/python-download-file-from-url/#downloading-a-file-from-a-url-in-python
# https://www.geeksforgeeks.org/how-to-download-files-from-urls-with-python/
import requests
url = r"https://storage.googleapis.com/gresearch/youtube-asl/youtube_asl_video_ids.txt"


response = requests.get(url)
file_Path = 'youtube_asl_video_ids.txt'

if response.status_code == 200:
	with open(file_Path, 'wb') as file:
		file.write(response.content)
	print('File downloaded successfully')
else:
	print('Failed to download file')

