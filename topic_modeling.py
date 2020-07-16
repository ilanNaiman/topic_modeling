import re
import json
import numpy as np
import pandas as pd
from pprint import pprint
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import scipy.misc
from gensim.test.utils import datapath
import pickle


# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy for lemmatization
import spacy

# Plotting tools
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt

# Enable logging for gensim - optional
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

from nltk.corpus import stopwords

stop_words = stopwords.words('english')


# Import Dataset
df = pd.read_csv("tales-csv.csv")
unique_origins = df["origin"].unique()

# Convert to list
data = df.text.values.tolist()

# Remove new line characters
data = [re.sub('\s+', ' ', sent) for sent in data]

# Remove distracting single quotes
data = [re.sub("\'", "", sent) for sent in data]


def sent_to_words(sentences):
    for sentence in sentences:
        yield gensim.utils.simple_preprocess(str(sentence), deacc=True)


data_words = list(sent_to_words(data))


# Build the bigram and trigram models
bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
trigram = gensim.models.Phrases(bigram[data_words], threshold=100)

bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)



# Define functions for stopwords, bigrams, trigrams and lemmatization
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]


def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]


def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]


def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out


# Remove Stop Words
data_words_nostops = remove_stopwords(data_words)


# Form Bigrams
data_words_bigrams = make_bigrams(data_words_nostops)


# Initialize spacy 'en' model, keeping only tagger component (for efficiency)
# python3 -m spacy download en
nlp = spacy.load('en', disable=['parser', 'ner'])


# Do lemmatization keeping only noun, adj, vb, adv
data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])


# MUST run this analysis only for EACH origin only
# thus, running the whole process of pre-processing the csv
# filtered per origin and save the results here.
# CHANGES IN CODE NEEDED TO RUN THIS METHOD ACCORDING TO DESCRIPTION
def analyze_animals():
    animals_hash = {}
    with open('animals.json') as json_file:
        animals = json.load(json_file)
        for animal in animals:
            animal = animal.lower()
            animals_hash[animal] = 0
    for data_l in data_lemmatized:
        for word in data_l:
            if word in animals_hash:
                animals_hash[word] += 1


# Create Dictionary
id2word = corpora.Dictionary(data_lemmatized)

# Create Corpus
texts = data_lemmatized

# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]

# Creat tuples of (origin, corpus)
country_corpus = [(df.loc[i]['origin'], corpus[i]) for i in range(len(df['origin']))]

# save the mapping into a file, s.t it could be possible
# to work with this file from other py files.
with open('country_corpus', 'wb') as fp:
    pickle.dump(country_corpus, fp)


# here we use mallet LDA to generate better results than
# we got using regular gensim LDA
mallet_path = 'mallet-2.0.8/bin/mallet'
ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=14, id2word=id2word)

# this method converts the mallet LDA model to gensim LDA model object
# so we could use it for visualization via pyLDAvis
mallet_lda_model = gensim.models.wrappers.ldamallet.malletmodel2ldamodel(ldamallet)

# using sort_topics=False will help us to synchronize the results by this visualization
# and the word clouds results
vis = pyLDAvis.gensim.prepare(mallet_lda_model, corpus, id2word, sort_topics=False)
pyLDAvis.save_html(vis, 'LDA_Mallet_' + str(len(mallet_lda_model.get_topics())) + '_topics.html')

# tool to save the model to some file and then use it in other python files
temp_file = datapath("mallet_lda_model")
mallet_lda_model.save(temp_file)


# This LDA model is regular gensim, produced worse results then mallet
# Build LDA model
# lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
#                                            id2word=id2word,
#                                            num_topics=14,
#                                            random_state=100,
#                                            update_every=1,
#                                            chunksize=100,
#                                            passes=10,
#                                            alpha='auto',
#                                            minimum_probability=0.0,
#                                            per_word_topics=True)


def generate_distribution_among_country(country_corpus, unique_origins, lda_model):
    """
    :param country_corpus: list of tuples: (origin, corpus)
    :param unique_origins: list of the origins inside the csv
    :param lda_model: gensim LDA model
    :return: the function returns list of tuples (origin, vector(x_1,...,x_n)) where each entry of the vector
             x_i is the probability of topic i among the origin.
    """
    vec = []
    for i in range(len(country_corpus)):
        vec_mid, vec_prob = [], []
        topic_nums = []
        for tup in lda_model[country_corpus[i][1]]:
            vec_mid.append(tup)
            topic_nums.append(tup[0])
        for j in range(0, 14):
            if j not in topic_nums:
                vec_mid.append((j, 0))
        sorted(vec_mid, key=lambda x: x[0])
        for tup in vec_mid:
            vec_prob.append(tup[1])
        vec.append(vec_prob)
    all_means = []
    for origin in unique_origins:
        mean_vector = [vec[i] for i in range(len(country_corpus))
                       if origin == country_corpus[i][0]]
        all_means.append([origin, np.mean(mean_vector, axis=0)])
    return all_means


# generate words cloud per topic from lda model
def generate_word_clouds(lda_model):
    pprint(lda_model.print_topics())
    wc = WordCloud(background_color="white", width=1000, height=1000, max_words=100, relative_scaling=0.5,
                   normalize_plurals=False)
    topics = lda_model.show_topics(num_topics=14, num_words=30, formatted=False)
    for tup in topics:
        topic_words = dict(tup[1])
        wc.generate_from_frequencies(topic_words, max_font_size=300)
        plt.figure(dpi=1200)
        plt.gca().imshow(wc)
        plt.gca().set_title('Topic ' + str(tup[0] + 1), fontdict=dict(size=16))
        plt.gca().axis('off')
        plt.savefig('Topic ' + str(tup[0] + 1) + '.jpeg')


def generate_animals_analysis(unique_origins, hash_animals):
    for origin in unique_origins:
        f = open("../AnimalsByCountry/" + origin + ".txt", "w")
        f.write(str(hash_animals))
        f.close()
        wc = WordCloud(background_color="white",width=1000,height=1000, max_words=100,relative_scaling=0.5,
                       normalize_plurals=False).generate_from_frequencies(hash_animals)
        wc.to_file(origin + '.png')
        plt.imshow(wc)
        plt.title(origin)
        plt.show()


# generate topics distribution among countries
print(generate_distribution_among_country(country_corpus, unique_origins, mallet_lda_model))
generate_word_clouds(mallet_lda_model)
generate_animals_analysis(unique_origins, [])
