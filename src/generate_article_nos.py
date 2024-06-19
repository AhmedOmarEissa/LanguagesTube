from util import get_response_playlist, get_videos_playllist,get_subtitle
import pandas as pd
import os 
import json


# def create_files_map(path,json_file):
#     with open(path +'data.json', 'w') as f:
#         json.dump(json_file, f)
#         print('File created')


def check_articles_folder(path , create_folder_if_not_exist = False):

    if not os.path.exists(path) and create_folder_if_not_exist:
        os.makedirs(path)
        return  []
    else:
        return os.listdir(path)

def generate_article(subtitle_text, videoId, path):

    subtitle_text = subtitle_text.replace('\n', ' ')
    subtitle_text = subtitle_text.replace('\r,', ' ')
    with open(path + videoId + '.txt', "w") as f:
        f.write(subtitle_text)
        print(f'Article {videoId} generated')
    

def generate_articles(path, create_folder_if_not_exist = False):
    response = get_response_playlist('PLO72qiQ-gJuFzpCgQcsdd4lkulqeeBMC3') # NOS Nieuws van de Week

    videos = get_videos_playllist(response )

    columns= ['episode','start', 'text']

    # create_files_map('articles/',{str(i['videoId']): str(i['videoPublishedAt']) for i in videos})

    last_10_videos = videos[:10]
    generated_articles = check_articles_folder(path, create_folder_if_not_exist = create_folder_if_not_exist)
    video_metadata = {}
    for video_info in last_10_videos:

        videoId = video_info['videoId'] # get video id

        response = get_subtitle(videoId)
        
        if response is not None and videoId + '.txt' not in generated_articles:
            subtitle_text = response['text'].str.cat(sep=' ')
            generate_article(subtitle_text, videoId, path)
            video_metadata[videoId] = video_info['videoPublishedAt']
    json.dump(video_metadata, open(path + 'metadata.json', 'w'))


# The code above is a script that generates articles from the last 10 videos of the NOS Nieuws van de Week playlist.