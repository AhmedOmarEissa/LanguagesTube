from util import get_response_playlist, get_videos_playllist,get_subtitle
import pandas as pd
import time
import os 


def check_articles(path , create_new = False):

    if not os.path.exists(path) and create_new:
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
    



if __name__ == '__main__':

    response = get_response_playlist('PLO72qiQ-gJuFzpCgQcsdd4lkulqeeBMC3') # NOS Nieuws van de Week

    videos = get_videos_playllist(response )

    columns= ['episode','start', 'text']

    last_10_videos = videos[:10]
    path = 'articles/'
    generated_articles = check_articles(path, create_new = True)

    for video_info in last_10_videos:

        videoId = video_info['videoId'] # get video id

        response = get_subtitle(videoId)
        

        if response is not None and videoId + '.txt' not in generated_articles: 
            subtitle_text = response['text'].str.cat(sep=' ')
            generate_article(subtitle_text, videoId, path)


# The code above is a script that generates articles from the last 10 videos of the NOS Nieuws van de Week playlist.