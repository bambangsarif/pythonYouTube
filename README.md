# pythonYouTube

This is a practice project to extract and analyze information from YouTube videos. 
We will use YouTube's Python API, Panda, NLTK.

In this project, we will:
1. List youtube videos based on certain search query.
2. Extract keywords from the video's closed caption
3. Perform sentiment analysis on the video

The main goal of this project is to provide information for 
user who want to upload a video to youtube. if the video match 
a certain query term, we can see the lists of videos that are 
currently available. Perform some keywords extraction from the 
videos that have closed caption and perform sentiment analysis 
from these videos.


Currently, we have two main files
1. getYouTubeList
   This will list the video based on search query
   To do: put the option to search for videos with closed caption only
2. getKeywordsFromCC
   This will extract keywords from video's CC using NLTK

Note:
To run the code, we need to first import NLTK library. Both Python 
scripts have default parameters included in them, it can run without 
passing any argument. For more info regarding the argument, you need 
to put '-h' to run the script.
