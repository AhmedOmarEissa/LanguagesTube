import os

#import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd 
import secret 
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def get_response_playlist(playlist):

    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=secret.developerKey)
    request = youtube.playlistItems().list(
        playlistId=playlist,
        part = 'contentDetails',
        maxResults = 100
        )
    response = request.execute()

    return response


def get_videos_playllist(response):
    return [response['items'][i]['contentDetails']['videoId'] for i in range(len(response['items']))]



## DOWNLOAD THE VIDEO SUBTITLES
def get_subtitle(id):
    dict_sentence = YouTubeTranscriptApi.get_transcript(id,languages =['nl'])
    new_episode = pd.DataFrame(dict_sentence)
    new_episode['episode'] = 'https://www.youtube.com/watch?v=' + id 
    return new_episode
