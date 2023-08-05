# what do we need to do here?

# step 1: get words from text
# step 2: make a graph using those words
# step 3: get the next word for x number of words (defined by user)
# step 4: show the user!
import os
import re
import string
import random
from graph import Graph, Vertex

def get_words_from_text(text_path):
    with open(text_path, 'rb') as file:
        text = file.read().decode("utf-8")  

        # remove [verse 1: artist]
        # include the following line if you are doing song lyrics
        text = re.sub(r'\[(.+)\]', ' ', text)

        text = ' '.join(text.split())  # this is saying turn whitespace into just spaces
        text = text.lower() # make everything lowercase to compare stuff
        # now we could be complex and deal with punctuation... but there are cases where
        # you might add a period such as (Mr. Brightside), but that's not really
        # punctuation... so we just remove all the punctuation
        # hello! it's me. --> hello its me
        text = text.translate(str.maketrans('', '', string.punctuation))

    words = text.split() # split on spaces again

    # words = words[:1000]

    return words


def make_graph(words):
    g = Graph()
    prev_word = None
    # for each word
    for word in words:
        # check that word is in graph, and if not then add it
        word_vertex = g.get_vertex(word)

        # if there was a previous word, then add an edge if it does not already exist
        # if exists, increment weight by 1
        if prev_word:  # prev word should be a Vertex
            # check if edge exists from previous word to current word
            prev_word.increment_edge(word_vertex)

        prev_word = word_vertex

    g.generate_probability_mappings()
    
    return g

def compose(g, words, length=50):
    composition = []
    word = g.get_vertex(random.choice(words)) # pick a random word to start!
    for _ in range(length):
        composition.append(word.value)
        word = g.get_next_word(word)

    return composition


def main(artist):
    # step 1: get words from text
    # words = get_words_from_text('texts/hp_sorcerer_stone.txt')
    # for song lyrics
    words = []     
    for song_file in os.listdir(f'songs/{artist}'):
        if song_file == '.DS_Store':
            continue
        song_words = get_words_from_text(f'songs/{artist}/{song_file}')
        words.extend(song_words)
    # step 2: make a graph using those words     
    g = make_graph(words)

    # step 3: get the next word for x number of words (defined by user)
    # step 4: show the user! 
    composition = compose(g, words, 100)
    return ' '.join(composition) # returns a string, where all the words are separated by a space!!


if __name__ == '__main__':
    print(main('taylor_swift')) 