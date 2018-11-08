import requests
import numpy as np
import pandas as pd
import re
import datetime
import string

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
        output = [video_results["items"][i]["snippet"]["resourceId"]["videoId"]]
        output.extend([video_results["items"][i]["snippet"][column] for column in columns])
        video_data.append(output)

    while "nextPageToken" in video_results:
        video_parameters["pageToken"] = video_results["nextPageToken"]
        video_query = requests.get(video_url, video_parameters)
        video_results = video_query.json()
        for i in range(len(video_results["items"])):
            output = [video_results["items"][i]["snippet"]["resourceId"]["videoId"]]
            output.extend([video_results["items"][i]["snippet"][column] for column in columns])
            video_data.append(output)
    return video_data


publishedAt_parser = np.vectorize(lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ"))


arxiv = "UCNIkB2IeJ-6AmZv7bQ1oBYg" #arXiv
dunkey = "UCsvn_Po0SmunchJYOWpOxMg" #dunkey
video_columns = ["title", "description", "publishedAt"]
dataframe_columns = ["id"] + video_columns


uploads = get_playlist_id(dunkey, api_key)
video_dataframe = pd.DataFrame(get_videos(uploads, video_columns, api_key), columns=dataframe_columns)
video_dataframe["publishedAt"]= publishedAt_parser(video_dataframe["publishedAt"])