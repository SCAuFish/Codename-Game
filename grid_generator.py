import random
import os
from collections import defaultdict
try:
    import nltk
except:
    os.system("pip3 install nltk")

try:
    from nltk.corpus import brown, wordnet
    brown.categories()
    wordnet.words()
except:
    nltk.download('brown')
    nltk.download('wordnet')

WORDNET_WORDS = set(wordnet.words())
BROWN_WORDS = defaultdict(set)
for i, category in enumerate(brown.categories()):
    BROWN_WORDS[i + 1] = set(brown.words(categories=category)).intersection(WORDNET_WORDS)
    BROWN_WORDS[0] = BROWN_WORDS[0].union(BROWN_WORDS[i+1])

def get_words():
    categories = brown.categories()
    choices = '\n'.join([f'{i+1}: {category}' for i, category in enumerate(categories)])
    index = input(f"Choose category from below (0 if covering all)\n{choices}\n")
    index = int(index or '0')

    candidate_words = BROWN_WORDS[index]

    words = random.sample(candidate_words, 20)

    return words


def get_layout():
    idx = [i for i in range(20)]

    team_A = random.sample(idx, 8)

    for chosen in team_A:
        idx.remove(chosen)

    team_B = random.sample(idx, 7)

    for chosen in team_B:
        idx.remove(chosen)

    death = random.sample(idx, 1)

    grid = [['O' for i in range(5)] for j in range(4)]

    for a in team_A:
        row = a // 5
        col = a % 5
        grid[row][col] = 'A'

    for b in team_B:
        row = b // 5
        col = b % 5
        grid[row][col] = 'B'

    grid[death[0] // 5][death[0] % 5] = 'X'

    return grid


def get_explanation(word):
    if word not in WORDNET_WORDS:
        print(f"Not a word with explanation: {word}, check your spelling")
        return False
    synsets = wordnet.synsets(word)
    defs = [f"{i+1}: {synset.definition()} ({', '.join(synset.lemma_names(lang='cmn'))})" for i, synset in enumerate(synsets)]
    definitions = '\n'.join(defs)
    print(f"definitions include:\n{definitions}\n")
    return True


def print_words(words):
    template = "{0:20}|{1:20}|{2:20}|{3:20}|{4:20}" # column widths: 8, 10, 15, 7, 10
    grid = [['' for i in range(5)] for j in range(4)]
    for i in range(4):
        for j in range(5):
            grid[i][j] = words[i * 5 + j]

    for i in range(4):
        print(template.format(*grid[i]))


def print_grid(layout):
    template = "{0:20}|{1:20}|{2:20}|{3:20}|{4:20}" # column widths: 8, 10, 15, 7, 10
    for i in range(4):
        print(template.format(*layout[i]))

print()
print()

resume = True
while resume:
    candidate_words = get_words()
    print("-" * 100)
    print_words(candidate_words)
    print("-" * 100)

    query = input("Any word that needs explanation? Press ENTER to skip.\n")
    while len(query.strip()) > 0:
        get_explanation(query.strip())
        
        query = input("Any word that needs explanation? Press ENTER to skip.\n")

    layout = get_layout()
    print("*" * 100)
    print_grid(layout)
    print("*" * 100)

    resume = input("Another game? [Y/n]")
    if resume.lower() != 'n':
        resume = True
    else:
        resume = False