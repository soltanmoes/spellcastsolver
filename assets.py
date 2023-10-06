letter_values = {
    "a": 1,
    "b": 4,
    "c": 5,
    "d": 3,
    "e": 1,
    "f": 5,
    "g": 3,
    "h": 4,
    "i": 1,
    "j": 7,
    "k": 6,
    "l": 3,
    "m": 4,
    "n": 2,
    "o": 1,
    "p": 4,
    "q": 8,
    "r": 2,
    "s": 2,
    "t": 2,
    "u": 4,
    "v": 5,
    "w": 5,
    "x": 7,
    "y": 4,
    "z": 8
}

def word_score(word):
    score = 0
    for letter in list(word):
        score += letter_values[letter]

    if len(word) >= 6:
        score += 10
    
    return score

def load_board():
    board_file = open("position.txt", "r").read().split("\n")
    board_file = [list(row) for row in board_file]
    return board_file

def load_dictionary():
    dictionary_file = open("dictionary.txt", "r").read().split("\n")
    dictionary_file = [word.lower() for word in dictionary_file]
    return set(dictionary_file)

def load_redundant_starters(length):
    starters_file = open(f"redundant-{length}.txt", "r").read().split("\n")
    return set(starters_file)