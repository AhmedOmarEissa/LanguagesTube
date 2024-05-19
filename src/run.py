from generate_article_nos import generate_articles
from get_the_top_words import top_words
from create_markdowns import generate_markdowns


if __name__ == '__main__':
    path = './articles/'
    generate_articles(path, create_folder_if_not_exist=True)
    top_words = top_words(path)
    generate_markdowns(path, replace_if_exist = False, top_words_dict = top_words)
