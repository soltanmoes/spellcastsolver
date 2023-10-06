from time import time

from assets import load_board, load_dictionary, load_redundant_starters, word_score

# load in dictionary and redundant starters cache
dictionary = load_dictionary()
redundant_starters_two = load_redundant_starters(2)
redundant_starters_three = load_redundant_starters(3)

board = load_board()

depth = 8

class SearchNode:
    def __init__(self, parent, x, y):
        self.parent = parent
        self.x = x
        self.y = y

    def letter(self):
        return board[self.y][self.x]

    def word(self):
        word = ""
        curr = self
        while True:
            word = curr.letter() + word
            if curr.parent is None:
                break
            else:
                curr = curr.parent
        return word

    def adjacent_nodes(self):
        adjacent = []
        adjacent.append(SearchNode(self, self.x, self.y - 1))
        adjacent.append(SearchNode(self, self.x + 1, self.y - 1))
        adjacent.append(SearchNode(self, self.x + 1, self.y))
        adjacent.append(SearchNode(self, self.x + 1, self.y + 1))
        adjacent.append(SearchNode(self, self.x, self.y + 1))
        adjacent.append(SearchNode(self, self.x - 1, self.y + 1))
        adjacent.append(SearchNode(self, self.x - 1, self.y))
        adjacent.append(SearchNode(self, self.x - 1, self.y - 1))

        valid_adjacent = []
        for node in adjacent:
            if node.x > 0 and node.x <= 4 and node.y > 0 and node.y <= 4:
                valid_adjacent.append(node)

        return valid_adjacent

    def chain_contains(self, target_node):
        curr = self
        while True:
            if curr.x == target_node.x and curr.y == target_node.y:
                return True
            elif curr.parent is None:
                return False
            else:
                curr = curr.parent


def search(root_node):
    words = []
    frontier = [root_node]

    while len(frontier) > 0:
        curr = frontier.pop(0)

        # if current branch is a word log it
        candidate_word = curr.word()
        if candidate_word in dictionary:
            words.append(candidate_word)

        # if maximum search depth reached, terminate search
        if len(candidate_word) > depth:
            break

        # queue adjacent nodes that are not in current's parent chain
        pruneChecks = [
            candidate_word[:2] in redundant_starters_two, candidate_word[:3]
            in redundant_starters_three
        ]

        if True not in pruneChecks:
            for adjacent_node in curr.adjacent_nodes():
                if not curr.chain_contains(adjacent_node):
                    frontier.append(adjacent_node)

    return words


start_time = time()

words = []
for y in range(5):
    for x in range(5):
        print(f"Searching from root node at ({x}, {y})...")
        words += search(SearchNode(None, x, y))

# dont touch i got from medium.com
resultsSet = set()
for word in words:
    resultsSet.add(word)
words = list(resultsSet)

# sort words by score
words.sort(key=word_score, reverse=True)

# display top computer moves
for i, word in enumerate(words[:10]):
    print(f"{i + 1}. {word} - {word_score(word)} points")

print(f"Search complete (elapsed time: {time() - start_time}s)")
