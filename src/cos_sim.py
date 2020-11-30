import configparser
import string
import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

from nltk.corpus import stopwords
from pymystem3 import Mystem

import nltk
nltk.download('stopwords')


config = configparser.ConfigParser()
config.read('config.ini')
SHORT_WORD = int(config['tables']['SHORT_WORD'])
EXTRA_STOPWORDS = config['tables']['EXTRA_STOPWORDS'].split(',')

stopwords_list = stopwords.words('russian') + EXTRA_STOPWORDS

m = Mystem()


def preprocess(sentence):
    sentence = sentence.lower()
    sentence = ''.join([symbol for symbol in sentence if symbol not in string.punctuation and not symbol.isdigit()])
    sentence = ' '.join([word for word in sentence.split() if word not in stopwords_list and len(word) > SHORT_WORD])
    sentence = ''.join(m.lemmatize(sentence)).strip()
    return sentence


def compare_names(parsed_names_df, keywords, threshold):
    parsed_names = list(parsed_names_df['name'])
    sentences = keywords + parsed_names
    preprocessed_sentences = list(map(preprocess, sentences))
    vectorizer = CountVectorizer().fit_transform(preprocessed_sentences)
    vectors = vectorizer.toarray()
    cos_sim = cosine_similarity(vectors)
    
    keywords_num = len(keywords)
    indices = [
        list(parsed_names_df['graph_id']),
        list(parsed_names_df['path']),
        list(parsed_names_df['name']),
    ]
    
    cos_sim_df = pd.DataFrame(data=cos_sim[keywords_num:, :keywords_num],
                              columns=keywords,
                              index=indices)
    cos_sim_df = cos_sim_df.reset_index()
    cos_sim_df = cos_sim_df.rename(columns={'level_0': 'graph_id',
                                            'level_1': 'path',
                                            'level_2': 'table_name'})
    
    linear_df = cos_sim_df.melt(id_vars=['graph_id', 'path', 'table_name'],
                        var_name='keyword',
                        value_name='cos_sim')
    linear_df = linear_df[linear_df['cos_sim'] >= threshold]
    linear_df = linear_df.sort_values(by=['keyword', 'cos_sim'])
    linear_df.reset_index(drop=True, inplace=True)
    
    return linear_df