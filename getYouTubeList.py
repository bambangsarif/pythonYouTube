# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 15:55:42 2016

@author: bambangs

Modified from http://www.analyticsvidhya.com/blog/2014/09/mining-youtube-python-social-media-analysis/
There were some syntax problem with argparse. 

We are building our project from this base, use panda to get make a dataframe of 
the video list based on the search query. Get a few statistics and use NLP to 
search for keywords from the collection of titles

"""
from apiclient.discovery import build 
from apiclient.errors import HttpError 
from oauth2client.tools import argparser 
import pandas as pd 

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

import argparse
parser = argparse.ArgumentParser(description='parsing search query')
parser.add_argument("--q", help="Search term", default="Google")
parser.add_argument("--max-results", help="Max results", default=25)
parser.add_argument("--key", help="Your YouTube Developer Key")
args = parser.parse_args()
options = args

DEVELOPER_KEY = options.key

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
# Call the search.list method to retrieve results matching the specified
 # query term.
search_response = youtube.search().list(
 q=options.q,
 type="video",
 part="id,snippet",
 maxResults=options.max_results
).execute()
videos = {}
# Add each result to the appropriate list, and then display the lists of
 # matching videos.
 # Filter out channels, and playlists.
for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
        #videos.append("%s" % (search_result["id"]["videoId"]))
        videos[search_result["id"]["videoId"]] = search_result["snippet"]["title"]

#print "Videos:\n", "\n".join(videos), "\n"
s = ','.join(videos.keys())

videos_list_response = youtube.videos().list(
 id=s,
 part='id,statistics'
).execute()

res = []
for i in videos_list_response['items']:
    temp_res = dict(v_id = i['id'], v_title = videos[i['id']])
    temp_res.update(i['statistics'])
    res.append(temp_res)
 
respd = pd.DataFrame.from_dict(res)

print(respd.head(n=10))
