# topic_modeling

As a part of a Digital Humanities course for computer science students from Ben Gurion University, taught by Dr. Yael Netzer,
we collected data about folk tales from different countries. We had many questions about those tales, for instance, What are their main topics?
Which topic is more dominant in each country? What can we learn about a country’s culture and environment from their stories, and how they affect the stories?
We try to explain some of the results we obtained from our point of view, of course the reader is encouraged to think about the different
reasons for the diversity among the origins.

Our Goal:

The goal of our project is to analyse the differences in folk tales from different countries around the world. Using this analysis, 
we want to learn about the different aspects of each culture.
Using Topic Modeling tools, we generate Topics distribution among countries.
By checking the gender representation in each country’s stories we check the dominance of each gender in the culture. Through the references to animals
in the tales, we learn about the environment of each country and their communication with their surroundings. 
In addition, our goal is to get experience in the process of getting the data, cleaning the data and adjusting it to our needs.
Also, using NLP tools to process the data, such as LDA (topic modeling algorithm).

This project is mainly about topic modeling. A topic model takes a collection of texts as input.
It discovers a set of “topics” — recurring themes that are discussed in the collection — and the degree to which each document exhibits those topics.



Process:
 
Data mining and organizing:
While searching for data we came across World of Tales that contains semi structured data about folktales and stories from across the world.
By going over the source code, we noticed that the whole website is organized in a way that makes it easy to get the information (as we learned in class).
In order to get the data in a comfortable form for working on it, we had to create a crawler.
To make sure it is allowed, we checked the robots.txt file and checked what stories we should avoid.
By using the Scrapy library, we created a crawler that pulled the stories into a csv file including all the metadata about which includes: 
  URL
  Story’s name
  Book’s name
  Publisher
  Author
  Editor
  Publish year 
  Notes about the book
  Country
 After creating the csv file we used actions from Openrefine as we learned in class to organize the stories and all their metadata and delete any errors
 that were made in the crawler or the way the data was in the website, such as unnecessary spaces, differences in country names, etc.
 In the process we arranged the metadata in a unified structure that made the work with it much easier. We used tools such as Cluster & Edit, Facet and Transform.
 As part of organizing the data, we had to manually fix several collisions and problems in the text, and even delete a few records that were not in
 the standard structure.
 
Preprocessing:
Before running the LDA algorithm, we first had to do some extra preprocess work on the text we got.
As we learnt during the course of Digital Humanities, in computing, stop words are words which are filtered out before or after processing of
natural language data (text). Though "stop words" usually refers to the most common words in a language, there is no single universal list of
stop words used by all natural language processing tools, and indeed not all tools even use such a list. 

Specifically we used stopwords from NLTK and Spacy’s “en” model.
Using regular expressions we get rid of extra spaces, new line characters and distracting single quotes.
Next we break down the text of each document into a list of words through tokenization, while clearing up all the messy text in the process.
(using gensim’s tool simple_preprocess)

We also learnt about n-grams:
 “In the fields of computational linguistics and probability, an n-gram is a contiguous sequence of n items from a given sample of text or speech.
 The items can be phonemes, syllables, letters, words or base pairs according to the application.
 The n-grams typically are collected from a text or speech corpus.”
(from wikipedia)

We also created Bigram and Trigram Models (using the gensim library Phrases model we were able to build and implement the bigrams, trigrams, quadgrams and more)


Lemmatisation (or lemmatization) in linguistics is the process of grouping together the inflected forms of a word so they can be analysed as a single item,
identified by the word's lemma, or dictionary form. (from wikipedia)
For grammatical reasons, documents are going to use different forms of a word, such as organize, organizes, and organizing.
For simplicity, lemmatization is nothing but converting a word to its root word. For example: the lemma of the word ‘fans’ is ‘fan’.
As we know, the quality of text preprocessing is a key factor in the results we will get, thus this is very important to let the model “recognize”
those words as the same words as they have the same meaning.

Running LDA:

Finally we give the LDA model all its arguments and run the algorithm. But how do we choose the number of topics? Well, this one is rather experimental.
We try and run the algorithm each time with different numbers of topics, ranging from 2 up to 20.
Each time we go over the topics we received by the algorithm and decide whether the results are good enough.
We add words to stopwords such as “say”, “go”, “come”, “see”, where we observe we get the same topics containing those words and also we feel that
those words do not contribute to the analysis of general topic of some country.

Calculating Topics distribution among countries:
First, the LDA model we got in the previous stage holds for each document a vector with the distribution of topics among this document.
(e.g. (p1, p2, ... , pn) if we have n topics s.t that p1 + p2 +...+ pn = 1)
For each entry in the corpus we created a mapping between an entry and its origin (i.e. its country).
In the end we were able to filter for each origin its documents and to calculate the mean.

Another Analysis:

Generating “popular” animals among each country:
This is a different approach from before. Here we don't have to use some new tools. 
We took a list that contains different kinds of animals and we just hold a hash table where the keys are the animals and the values are their count in each tale.
For each word in the document (after the preprocessing) check whether it has a key in the table.
We filter the documents by the different countries to obtain the value for a specific country.

Finding the dominant gender among each country:
Using a list of female nouns and a list of male nouns that we got from the application Jailbreak-the-Patriarchy
we analysed each story and counted the amount of uses of female or male nouns. 
Each story we categorized as “Male dominant” or “Female dominant” by comparing the amounts of gendered nouns.
For each country we checked the percentage of each gender dominant document using a pie chart that was created by the tools of Matplotlib.



Tools:

  Gensim
  Mallet
  Wix
  WordCloud
  Pandas
  pyLDAvis
  Matplotlib
  Spacy
  Numpy
  NLTK
  Matplotlib
  
 Gensim provides a wrapper to implement Mallet’s LDA from within Gensim itself. You only need to download the zipfile,
 http://mallet.cs.umass.edu/dist/mallet-2.0.8.zip
 unzip it and provide the path to mallet in the unzipped directory to gensim.models.wrappers.LdaMallet
