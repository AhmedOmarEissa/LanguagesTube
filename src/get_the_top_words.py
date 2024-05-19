from sklearn.feature_extraction.text import TfidfVectorizer
import os
from nltk.corpus import stopwords
import numpy as np

path = './articles/'

# remove dutch stopwords
stop_words = set(stopwords.words('dutch'))

def create_files_map(path):
    content_dict = {}
    for file in os.listdir(path):
        if not file.endswith('.txt'):
            continue
        with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
            content = f.read()
        
        video_id = file.replace('.txt', '')
        content_dict[video_id] = content
    return content_dict


def generate_tf_idf_matrix(content_dict):
    # Initialize the TF-IDF Vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words)

    # Fit and transform the documents
    tfidf_matrix = tfidf_vectorizer.fit_transform(content_dict.values())

    # Get feature names
    feature_names = np.array(tfidf_vectorizer.get_feature_names())
    return tfidf_matrix, feature_names


def get_top_unique_words(tfidf_matrix, feature_names, content_dict, top_n=10):
    """Extracts the top unique words for each article based on TF-IDF scores."""
    top_words = {}
    for i, (video_id, article) in enumerate(zip(content_dict.keys(), tfidf_matrix)):
        # Get the indices of the top n words with the highest TF-IDF score
        top_indices = article.toarray().flatten().argsort()[-top_n:]
        top_words[video_id] = feature_names[top_indices][::-1]  # Get words and reverse to descending order
    return top_words


def top_words(path=path):
    content_dict = create_files_map(path)
    tfidf_matrix, feature_names = generate_tf_idf_matrix(content_dict)
    top_words = get_top_unique_words(tfidf_matrix, feature_names, content_dict)
    return top_words