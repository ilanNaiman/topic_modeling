from __future__ import division

import itertools
import csv
import pandas as pd
import matplotlib.pyplot as plt
import os
from string import punctuation

male_words = {"he'", "sir", "actors", "bloke", "boyfriend", "groom", "brother", "comte", "knight", "squire", "male",
              "boyhood", "grandpa", "grandson", "gentleman", "maleness", "marquess", "margrave", "patriar", "patroniz",
              "father", "waiter", "husband", "airman", "airmen", "alderman", "aldermen", "anchorman", "anchormen",
              "assemblyman", "assemblymen", "bogeyman", "bogeymen", "bondsman", "bondsmen", "brogrammer", "bromance",
              "businessman", "businessmen", "cameraman", "cameramen", "caveman", "cavemen", "chairman", "chairmen",
              "clergyman", "clergymen", "congressman", "congressmen", "councilman", "councilmen", "countryman",
              "countrymen", "craftsman", "craftsmen", "d00dz", "daddies", "daddy", "son", "doorman", "doormen",
              "dudebro", "father", "femin", "fireman", "firemen", "fisherman", "fishermen", "foreman", "foremen",
              "freshman", "freshmen", "garbageman", "garbagemen", "godmother", "grandmother", "handyman", "handymen",
              "hangman", "hangmen", "henchman", "henchmen", "heroes", "journeyman", "journeymen", "kinsman", "kinsmen",
              "klansman", "ladiez", "laydeez", "layman", "laymen", "madman", "madmen", "mailman", "mailmen",
              "mansplain", "marksman", "marksmen", "mascul", "middleman", "middlemen", "milkman", "milkmen", "misandr",
              "misogyn", "mommies", "mommy", "nobleman", "noblemen", "ombudsman", "ombudsmen", "policeman", "policemen",
              "postman", "postmen", "repairman", "repairmen", "salesman", "salesmen", "sandman", "sandmen",
              "serviceman", "servicemen", "showman", "showmen", "snowman", "sorostitute", "spaceman", "spacemen",
              "spokesman", "spokesmen", "sportsman", "sportsmen", "statesman", "statesmen", "stepbrother", "stepmother",
              "stepsister", "superman", "supermen", "unman", "watchman", "watchmen", "weatherman", "weathermen",
              "whitemaleness", "woman", "women", "workman", "workmen", "actor", "actors", "archduke", "baron",
              "baronet", "baronets", "barons", "boy", "boyhood", "boyish", "boys", "bro", "bros", "comte", "dad",
              "dads", "deacon", "deacons", "dude", "dudelier", "dudeliest", "dudely", "dudes", "duke", "dukes", "earl",
              "earls", "emperor", "emperors", "empress", "fiance", "gal", "gentleman", "gentlemen", "god", "goddess",
              "godhead", "godhood", "godliness", "godly", "gramps", "guy", "guys", "he", "hero", "himself", "husband",
              "husbands", "king", "kings", "lord", "lords", "male", "males", "mama", "man", "manhood", "mankind",
              "manliness", "manly", "marquis", "marquise", "maternal", "maternity", "men", "menz", "mgtow", "mr", "mrs",
              "nephew", "nephews", "papa", "paternal", "paternity", "poppa", "priest", "priests", "prince", "princes",
              "queen", "queens", "radfem", "she", "sir", "son", "sons", "uncle", "uncles", "viscount", "viscounts",
              "widower"}

female_words = {"she'", "ma'am", "actresses", "gal", "girlfriend", "bride", "sister", "comtesse", "dame", "damsel",
                "female", "girlhood", "grandma", "granddaughter", "lady", "femaleness", "marchioness", "margravine",
                "matriar", "matroniz", "mother", "waitress", "wife", "airwoman", "airwomen", "alderwoman", "alderwomen",
                "anchorwoman", "anchorwomen", "assemblywoman", "assemblywomen", "bogeywoman", "bogeywomen",
                "bondswoman", "bondswomen", "sistagrammer", "lady-romance", "businesswoman", "businesswomen",
                "camerawoman", "camerawomen", "cavewoman", "cavewomen", "chairwoman", "chairwomen", "clergywoman",
                "clergywomen", "congresswoman", "congresswomen", "councilwoman", "councilwomen", "countrywoman",
                "countrywomen", "craftswoman", "craftswomen", "laydeez", "mommies", "mommy", "daughter", "doorwoman",
                "doorwomen", "galpal", "mother", "mascul", "firewoman", "firewomen", "fisherwoman", "fisherwomen",
                "forewoman", "forewomen", "freshwoman", "freshwomen", "garbagewoman", "garbagewomen", "godfather",
                "grandfather", "handywoman", "handywomen", "hangwoman", "hangwomen", "henchwoman", "henchwomen",
                "heroines", "journeywoman", "journeywomen", "kinswoman", "kinswomen", "klanswoman", "menz", "d00dz",
                "laywoman", "laywomen", "madwoman", "madwomen", "mailwoman", "mailwomen", "ladysplain", "markswoman",
                "markswomen", "femin", "middlewoman", "middlewomen", "milkwoman", "milkwomen", "misogyn", "misandr",
                "daddies", "daddy", "noblewoman", "noblewomen", "ombudswoman", "ombudswomen", "policewoman",
                "policewomen", "postwoman", "postwomen", "repairwoman", "repairwomen", "saleswoman", "saleswomen",
                "sandwoman", "sandwomen", "servicewoman", "servicewomen", "showwoman", "showwomen", "snowwoman",
                "bro-whore", "spacewoman", "spacewomen", "spokeswoman", "spokeswomen", "sportswoman", "sportswomen",
                "stateswoman", "stateswomen", "stepsister", "stepfather", "stepbrother", "superwoman", "superwomen",
                "unwoman", "watchwoman", "watchwomen", "weatherwoman", "weatherwomen", "whitefemaleness", "man", "men",
                "workwoman", "workwomen", "actress", "actresses", "archduchess", "baroness", "baronetess",
                "baronetesses", "baronesses", "girl", "girlhood", "girly", "girls", "sis", "sistas", "comtesse", "mom",
                "moms", "deaconess", "deaconesses", "lady", "womanlier", "womanliest", "womanly", "ladies", "duchess",
                "duchesses", "countess", "countesses", "empress", "empresses", "emperor", "fiancee", "fellow", "lady",
                "ladies", "goddess", "god", "goddesshead", "goddesshood", "goddessliness", "goddessly", "grandma",
                "gal", "gals", "she", "heroine", "herself", "wife", "wives", "queen", "queens", "lady", "ladies",
                "female", "females", "papa", "woman", "womanhood", "womankind", "womanliness", "womanly", "marquise",
                "marquise", "paternal", "paternity", "women", "ladiez", "wgtow", "ms", "mr", "niece", "nieces", "mama",
                "maternal", "maternity", "momma", "priestess", "priestesses", "princess", "princesses", "king", "kings",
                "radmasc", "he", "ma'am", "daughter", "daughters", "aunt", "aunts", "viscountess", "viscountesses",
                "widow"}

def gender_the_sentence(sentence_words):
    mw_length=len(male_words.intersection(sentence_words))
    fw_length=len(female_words.intersection(sentence_words))

    if mw_length>fw_length:
        gender='male'
    elif mw_length<fw_length:
        gender='female'
    else:
        gender='none'
    return gender

def is_it_proper(word):
    if word[0] == word[0].upper():
        case = 'upper'
    else:
        case = 'lower'

    word_lower = word.lower()
    try:
        proper_nouns[word_lower][case] = proper_nouns[word_lower].get(case, 0) + 1
    except Exception as e:
        # This is triggered when the word hasn't been seen yet
        proper_nouns[word_lower] = {case: 1}

def increment_gender(sentence_words,gender):
    sentence_counter[gender]+=1
    word_counter[gender]+=len(sentence_words)
    for word in sentence_words:
        word_freq[gender][word]=word_freq[gender].get(word,0)+1

sexes=['male','female','none','both']
sentence_counter={sex:0 for sex in sexes}
word_counter={sex:0 for sex in sexes}
word_freq={sex:{} for sex in sexes}
proper_nouns={}

df = pd.read_csv("tales-better.csv")
if not os.path.exists("pie charts"):
    os.mkdir("pie charts")
if not os.path.exists("gender charts"):
    os.mkdir("gender charts")
with open("gender charts/tales_genderized.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Dominant gender", "Story name", "Book name", "Country", "URL"])
    for country in df.origin.unique():
        condition = df.loc[df['origin'] == country]
        stories = condition.text.values.tolist()
        urls = condition.url.values.tolist()
        stories_names = condition.story_name.values.tolist()
        books_names = condition.book_name.values.tolist()
        # file.write("""
        # <table>
        #     <tr>
        #         <th>Dominant gender</th>
        #         <th>Story link</th>
        #     </tr>""")
        for (story, url, story_name, book_name) in zip(stories, urls, stories_names, books_names):
            # word tokenize and strip punctuation
            story_words = story.split()
            story_words = [w.strip(punctuation) for w in story_words
                              if len(w.strip(punctuation)) > 0]

            # figure out how often each word is capitalized
            [is_it_proper(word) for word in story_words[1:]]

            # lower case it
            story_words = set([w.lower() for w in story_words])

            # Figure out if there are gendered words in the sentence by computing the length of the intersection of the sets
            gender = gender_the_sentence(story_words)
            if "The Bell of" in story_name:
                writer.writerow([gender.capitalize(), "The Bell of", book_name, country, url])
            else:
                writer.writerow([gender.capitalize(), story_name, book_name, country, url])

            # Increment some counters
            increment_gender(story_words, gender)

        proper_nouns=set([word for word in proper_nouns if
                          proper_nouns[word].get('upper',0) /
                          (proper_nouns[word].get('upper',0) +
                           proper_nouns[word].get('lower',0))>.50])

        common_words=set([w for w in sorted (word_freq['female'],
                                             key=word_freq['female'].get,reverse=True)[:1000]]+[w for w in sorted (word_freq['male'],key=word_freq['male'].get,reverse=True)[:1000]])

        common_words=list(common_words-male_words-female_words-proper_nouns)
        print('country: %s' % country)
        print('%.1f%% gendered' % (100*(sentence_counter['male']+sentence_counter['female'])/
                                   (sentence_counter['male']+sentence_counter['female']+sentence_counter['none'])))
        print('%s stories are mostly about men.' % sentence_counter['male'])
        print('%s stories are mostly about women.' % sentence_counter['female'])

        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = 'Male', 'Female'
        sizes = [sentence_counter['male'], sentence_counter['female']]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=False, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.savefig("pie charts/" + country.strip().replace("/"," and ") +' gender pie chart.jpeg')
        sentence_counter = {sex: 0 for sex in sexes}
        word_counter = {sex: 0 for sex in sexes}
        word_freq = {sex: {} for sex in sexes}
        proper_nouns = {}