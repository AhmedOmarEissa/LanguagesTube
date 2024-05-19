import urllib.request
import json
import urllib
import datetime
from generate_article_nos import check_articles
import os

def get_video_data(video_id):
    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % video_id}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
    return data


def add_video_intro(video_id, title):
    """
    Generates markdown text for a given YouTube video.

    Parameters:
    video_id (str): The ID of the YouTube video.
    title (str): The title of the YouTube video.

    Returns:
    str: The generated markdown text.
    """
    markdown_template = f"""
This text is automatically generated from the subtitles of NOS Nieuws van de Week. The code used is in [this repo](https://github.com/AhmedOmarEissa/LanguagesTube).

## {title}

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/{video_id}/0.jpg)](https://www.youtube.com/watch?v={video_id})
****
"""
    return markdown_template    

def get_video_content(text_file_path, text_file):
        # Open the text file and read its contents

    with open(os.path.join(text_file_path, text_file), 'r', encoding='utf-8') as f:
        content = f.read()

    return content

def add_top_words_to_content(top_words_dict, video_id,content):
    if top_words_dict is not None and video_id in top_words_dict:
        top_words = top_words_dict[video_id]
        top_words_str = ', '.join(top_words)
        content = f"\n\nNew words: {top_words_str}\n\n" + content
    return content
    

def create_markdowns(text_file_path, video_id, title, date, description, tags , top_words_dict , replace = False):
    """
    Create markdown files for videos.

    Args:
        text_file_path (str): The path to the directory containing the text file.
        video_id (str): The ID of the video.
        title (str): The title of the video.
        date (str): The date of the video.
        description (str): The description of the video.
        tags (str): The tags associated with the video.

    Returns:
        None
    """
    text_file = video_id + '.txt'
    if not os.path.exists(os.path.join(text_file_path, text_file)):
        print(f"Text file {text_file} not found.")
        return
    #check if markdown file already exists
    markdown_file = title.lower().replace(' ', '-').replace(',', '').replace('?', '') + '.md'

    if os.path.exists(os.path.join(text_file_path, markdown_file)) and not replace:
        print(f"Markdown file {markdown_file} already exists.")
        return

    content = get_video_content(text_file_path, text_file)

    content = add_top_words_to_content(top_words_dict, video_id, content)

    content = add_video_intro(video_id, title) + content

    with open(os.path.join(text_file_path, markdown_file), 'w', encoding='utf-8') as f:
        # Write the title, date, description, and tags to the markdown file
        f.write("---\n")
        f.write("layout: post\n")
        f.write(f"title: {title}\n")
        f.write(f"date: {date}\n")
        f.write(f"description: {description}\n")
        f.write(f"tags: {tags}\n")
        f.write("\n")
        f.write("---\n")
        f.write(content)
        print(f"Markdown file {markdown_file} created.")



def generate_markdowns(path, replace_if_exist = True, top_words_dict = None):
    path = './articles/'
    generated_articles = check_articles(path, create_folder_if_not_exist = False)
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' +0000'
    for article in generated_articles:
        if '.txt' not in article: 
            continue
        video = article.replace('.txt','')
        video_data = get_video_data(video)
        create_markdowns(path,
                         video,
                         video_data['title'],
                         today,
                         'NOS news for the week',
                         'NOS project',
                         top_words_dict,
                         replace = replace_if_exist)