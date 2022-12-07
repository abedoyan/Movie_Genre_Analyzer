## CS410 - Text Information Systems
## Course Project
## Arda Bedoyan
## Fall 20222

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from collections import defaultdict
from gensim import corpora
from gensim import models
from gensim import similarities
from pathlib import Path

# Create a training set of movies and their main genre
# Genre selection was subjective
movie_graph = {'The Terminator': 'action',
               'Die Hard': 'action',
               'The Dark Knight': 'action',
               'Dumb and Dumber': 'comedy',
               'Bean': 'comedy',
               'Bridesmaids': 'comedy',
               'Forrest Gump': 'drama',
               'Good Will Hunting': 'drama',
               'The Godfather': 'drama',
               'Titanic': 'romance',
               'Pretty Woman': 'romance',
               'Notting Hill': 'romance',
               'Get Out': 'horror',
               'The Conjuring': 'horror',
               'The Shining': 'horror'}

# Create a blank dictionary to store results in
genre_results = {}

# Initialize a starter variable to tell the program to run or stop
start = 'y'

# Function to run the genre analysis using similarity queries #
def genre_analysis():
    documents = []
    key_count = 0

    # read in the movie scripts
    # the names of the txt files of the scripts should match the names in movie_graph
    while (key_count < len(keys)):
        movie = Path(keys[key_count] + '.txt').read_text()
        documents.append(movie)
        key_count += 1

    # remove common words and tokenize
    stoplist = set(line.strip() for line in open('stop_words.txt'))

    texts = [
        [word for word in document.lower().split() if word not in stoplist]
        for document in documents
    ]

    # remove words that appear only once
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [
        [token for token in text if frequency[token] > 1]
        for text in texts
    ]

    # create a corpus of all of the documents
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    # create an LSI model
    # LSI = Latent Semantic Indexing
    # Transforms documents from either bag-of-words or TfIdf-weighted space
    # into a latent space of a lower dimensionality.
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=300)

    # read in the movie script to run genre analysis on
    doc = Path(new_movie + '.txt').read_text()
    doc = [word for word in doc.lower().split() if word not in stoplist]

    # convert the query to LSI space
    vec_bow = dictionary.doc2bow(doc)
    vec_lsi = lsi[vec_bow]  
    #print(vec_lsi)

    # transform corpus to LSI space and index it
    index = similarities.MatrixSimilarity(lsi[corpus])

    # perform a similarity query against the corpus
    sims = index[vec_lsi]

    # sort the results
    sims = sorted(enumerate(sims), key=lambda item: -item[1])

    # get the top three movies based on similarity
    top_choice = sims[0]
    second_choice = sims[1]
    third_choice = sims[2]

    # get the top three genres based on top three movies
    for doc_position, doc_score in sims:
        print(doc_score, "Movie:", list(movie_graph.keys())[doc_position])
        if doc_position == top_choice[0]:
            genre1 = list(movie_graph.values())[doc_position]
        elif doc_position == second_choice[0]:
            genre2 = list(movie_graph.values())[doc_position]
        elif doc_position == third_choice[0]:
            genre3 = list(movie_graph.values())[doc_position]


    # print out the results and remove duplicate genres
    print("\nGenres: ", end="")

    count = 1
    while(count < 4):
        if (count == 1):
            print(genre1 + " ", end="")
        if (count == 2 and genre2 != genre1):
            print(genre2 + " ", end="")
        if (count == 3 and genre3 != genre1 and genre3 != genre2):
            print (genre3)
        count +=1

    print()

    temp_list = []
    genres = [genre1, genre2, genre3]

    for genre in genres:
        if genre not in temp_list:
            temp_list.append(genre)


    # add results to the genre_results directory
    genre_results[new_movie] = set(temp_list)
    movie_graph[new_movie] = genre1

    # check with user if the resulting genres are a good match for the movie
    # if not, manually enter genres to improve system
    human_input = input('Are these genres correct? (y/n) \n')
    if (human_input == 'n'):
        human_genre = input("What is the main genre? \n")
        movie_graph[new_movie] = human_genre
        human_genre2 = input("What is the second genre the movie falls under? \n")
        genre_results[new_movie] = set([human_genre2, human_genre])

#############end of function definition#######################


# Loop to run the program in
while (start == 'y' or start == 'Y' or start == 'yes' or start == 'Yes' or start == 'YES'):

    # user to input movie to check
    # user must save text file of movie script
    # and name it the same name as inputted into the program
    new_movie = input('Enter the title of a movie \n')
    keys = list(movie_graph.keys())

    # check if the movie already exists in our directory
    if (new_movie in keys or new_movie in list(genre_results.keys())):
        print('Movie already exists in directory \n')
        if (new_movie in list(genre_results.keys())):
            print('Genres: ' + str(genre_results[new_movie]) + '\n')
        else:
            print('Genre: ' + str(movie_graph[new_movie]) + '\n')

        # allows user to rerun the program for existing movies
        # in case the addition of some movies affected its genres
        rerun = input('Do you want to run the movie through the system again? \n')

        if (rerun == 'y' or rerun == 'Y' or rerun == 'yes' or rerun == 'Yes' or rerun == 'YES'):
            genre_analysis()
            start = input('Do you want to continue? \n')
        else:
            start = input('Do you want to continue? \n')

    # movie does not exist in directory, run the program
    else:
        genre_analysis()
        start = input('Do you want to continue? \n')






