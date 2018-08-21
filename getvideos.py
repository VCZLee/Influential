import requests

playlist_url = "https://www.googleapis.com/youtube/v3/channels?"

playlist_part = "contentDetails"
channel_id = "UCNIkB2IeJ-6AmZv7bQ1oBYg" #arXiv
channel_id = "UCsvn_Po0SmunchJYOWpOxMg" #dunkey

playlist_parameters = {"key": api_key,
                       "part": playlist_part,
                       "id": channel_id}

playlist_query = requests.get(playlist_url, playlist_parameters)
playlist_results = playlist_query.json()
playlist_id = playlist_results["items"][0][playlist_part]["relatedPlaylists"]["uploads"]
print(playlist_id)

video_url = "https://www.googleapis.com/youtube/v3/playlistItems?"
video_part = "snippet"
max_results = 50
video_parameters = {"key": api_key,
                    "part": video_part,
                    "playlistId": playlist_id,
                    "maxResults": max_results,
                    "pageToken": ""}


video_query = requests.get(video_url, video_parameters)
video_results = video_query.json()
print(video_query.url)
while "nextPageToken" in video_results:
    video_parameters["pageToken"] = video_results["nextPageToken"]
    video_query = requests.get(video_url, video_parameters)
    video_results = video_query.json()
    print(video_query.url)