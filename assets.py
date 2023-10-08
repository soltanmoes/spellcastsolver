alphabet = list("abcdefghijklmnopqrstuvwxyz")

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

def load_board():
    board_file = open("position.txt", "r").read().split("\n")
    board_file = [list(row) for row in board_file]

    for i in range(len(board_file)):
        board_file[i] = [tile for tile in board_file[i] if tile not in list("$+*")]

    return board_file

def load_boosts():
    board_file = open("position.txt", "r").read().split("\n")
    board_file = [list(row) for row in board_file]

    boosts = {
        "$": [],
        "+": [],
        "*": []
    }

    for y, row in enumerate(board_file):
        x_offset = 1
        for x, tile in enumerate(row):
            if tile in list("$+*"):
                boosts[tile].append([x - x_offset, y])
                x_offset += 1

    return boosts

dictionary_cache = None
def load_dictionary(letter_count = None):
    global dictionary_cache
    
    dictionary_file = None

    if dictionary_cache is None:
        dictionary_file = open("dictionary.txt", "r").read().split("\n")
        dictionary_cache = dictionary_file
    else:
        dictionary_file = [word[:letter_count] for word in dictionary_cache]
    
    return set(dictionary_file)

def load_redundant_starters(length):
    starters_file = open(f"caches/redundant-{length}.txt", "r").read().split("\n")
    return set(starters_file)