import requests

search_url = "https://www.googleapis.com/youtube/v3/search?"
api_key = "AIzaSyAnQSuacv2w4LRLw3F1jBs64WGN6KklCs0"
search_part = "snippet"
max_results = 50 #api supports up to 50
search_order = "date"
channel_id = "UCNIkB2IeJ-6AmZv7bQ1oBYg" #arXiv
channel_id = "UCsvn_Po0SmunchJYOWpOxMg" #dunkey

search_parameters = {"key": api_key,
                     "part": search_part,
                     "maxResults": max_results,
                     "order": search_order,
                     "channelId": channel_id}

search_query = requests.get(search_url, search_parameters)
search_results = search_query.json()

video_list = []
for i in range(len(search_results["items"])):
    video_list.append(search_results["items"][i]["snippet"]["title"])


while "nextPageToken" in search_results:
    search_parameters["pageToken"] = search_results["nextPageToken"]
    search_query = requests.get(search_url, search_parameters)
    search_results = search_query.json()
    for i in range(len(search_results["items"])):
        video_list.append(search_results["items"][i]["snippet"]["title"])

print(len(video_list))