import requests
import math

base_url = "https://www.googleapis.com/youtube/v3/search?"

part = "snippet"
channel_id = "UCNIkB2IeJ-6AmZv7bQ1oBYg" #arXiv
channel_id = "UCsvn_Po0SmunchJYOWpOxMg" #dunkey
order_by = "date"
max_results = 50

parameters = {"key": api_key,
              "part": part,
              "channelId": channel_id,
              "order": order_by,
              "maxResults": max_results}

query = requests.get(base_url, parameters)
results = query.json()
num_videos = results["pageInfo"]["totalResults"]
if num_videos > max_results:
    num_loops = math.ceil(num_videos/max_results) - 1
    print("Need to fetch " + str(num_loops) + " more pages")