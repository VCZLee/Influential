import requests
import pandas as pd


def get_playlist_id(channel_id, api_key):
    playlist_url = "https://www.googleapis.com/youtube/v3/channels?"
    playlist_part = "contentDetails"
    playlist_parameters = {"key": api_key,
                           "part": playlist_part,
                           "id": channel_id}

    playlist_query = requests.get(playlist_url, playlist_parameters)
    playlist_results = playlist_query.json()
    playlist_id = playlist_results["items"][0][playlist_part]["relatedPlaylists"]["uploads"]
    return playlist_id


def get_videos(playlist_id, columns, api_key):
    video_url = "https://www.googleapis.com/youtube/v3/playlistItems?"
    video_part = "snippet"
    max_results = 50  # api supports up to 50
    video_parameters = {"key": api_key,
                        "part": video_part,
                        "playlistId": playlist_id,
                        "maxResults": max_results,
                        "pageToken": ""}

    video_query = requests.get(video_url, video_parameters)
    video_results = video_query.json()
    video_data = []
    for i in range(len(video_results["items"])):
        video_data.append([video_results["items"][i]["snippet"][column] for column in columns])

    while "nextPageToken" in video_results:
        video_parameters["pageToken"] = video_results["nextPageToken"]
        video_query = requests.get(video_url, video_parameters)
        video_results = video_query.json()
        for i in range(len(video_results["items"])):
            video_data.append([video_results["items"][i]["snippet"][column] for column in columns])

    return video_data



arxiv = "UCNIkB2IeJ-6AmZv7bQ1oBYg" #arXiv
dunkey = "UCsvn_Po0SmunchJYOWpOxMg" #dunkey
video_columns = ["title", "description"]

uploads = get_playlist_id(arxiv, api_key)
video_dataframe = pd.DataFrame(get_videos(uploads, video_columns, api_key), columns=video_columns)