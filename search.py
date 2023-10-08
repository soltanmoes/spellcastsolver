from collections import deque
from copy import deepcopy

from assets import load_board, load_boosts, load_dictionary, letter_values, alphabet

# load in dictionary and redundant starters cache
dictionary = load_dictionary()
dictionary_caches = []

board = load_board()
board_boosts = load_boosts()

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
    
    def score(self):
        score = 0
        curr = self

        doubleWordScore = False
        while True:
            letter_multiplier = 1
            for doubleLetterBoost in board_boosts["+"]:
                if doubleLetterBoost[0] == curr.x and doubleLetterBoost[1] == curr.y:
                    letter_multiplier = 2
                    break
            for tripleLetterBoost in board_boosts["*"]:
                if tripleLetterBoost[0] == curr.x and tripleLetterBoost[1] == curr.y:
                    letter_multiplier = 3
                    break
            if not doubleWordScore:
                for doubleWordBoost in board_boosts["$"]:
                    if doubleWordBoost[0] == curr.x and doubleWordBoost[1] == curr.y:
                        doubleWordScore = True
                        break

            score += letter_values[curr.letter()] * letter_multiplier

            if curr.parent is None:
                break
            else:
                curr = curr.parent

        if doubleWordScore:
            score *= 2
        
        if len(self.word()) >= 6:
            score += 10

        return score
    
    def chain(self):
        nodes = deque()
        curr = self
        while True:
            nodes.appendleft(curr)
            if curr.parent is None:
                break
            else:
                curr = curr.parent
        return list(nodes)
    
    def chain_contains(self, target_node):
        for node in self.chain():
            if node.x == target_node.x and node.y == target_node.y:
                return True
        return False

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
            if node.x >= 0 and node.x < 5 and node.y >= 0 and node.y < 5:
                valid_adjacent.append(node)

        return valid_adjacent
    

class Move:
    swap = False
    swapped_node: SearchNode = None
    swapped_letter: str = None
    swap_result: str = None

    score = 0

    def __init__(self, frontal_node: SearchNode, score: int):
        self.frontal_node = frontal_node
        self.score = score

    def extract_word(move):
        if move.swap:
            return move.swap_result
        else:
            return move.frontal_node.word()


def search_from_node(root_node, depth):
    global board

    moves = deque()

    frontier = deque()
    frontier.appendleft(root_node)

    while len(frontier) > 0:
        curr = frontier.pop()

        # if current branch is a word log its frontal node
        candidate_word = curr.word()
        if candidate_word in dictionary:
            moves.appendleft(Move(curr, curr.score()))

        # check all possible swaps in chain
        candidate_chain: list[SearchNode] = curr.chain()
        for swap_focus_index in range(len(candidate_word)):
            for letter in alphabet:
                # get resulting word of the swap
                candidate_swap_result = list(candidate_word)
                candidate_swap_result[swap_focus_index] = letter
                candidate_swap_result = "".join(candidate_swap_result)

                # if resulting word is in the dictionary
                if candidate_swap_result in dictionary:
                    # create virtual board and apply swap to it
                    board_copy = deepcopy(board)
                    board[candidate_chain[swap_focus_index].y][candidate_chain[swap_focus_index].x] = letter

                    # generate move object
                    candidate_swap_move = Move(curr, curr.score())
                    candidate_swap_move.swap = True
                    candidate_swap_move.swap_result = candidate_swap_result
                    candidate_swap_move.swapped_letter = letter
                    candidate_swap_move.swapped_node = candidate_chain[swap_focus_index]

                    # add the swap move to the found moves list
                    moves.appendleft(candidate_swap_move)

                    board = board_copy

        # if maximum search depth reached, terminate search
        if len(candidate_word) > depth:
            break

        # queue adjacent nodes that are not in current's parent chain
        usefulBranch = True
        for i in range(2, depth):
            if len(candidate_word) < i:
                break
            if candidate_word[:i] not in dictionary_caches[i - 2]:
                usefulBranch = False
                break

        if usefulBranch:
            for adjacent_node in curr.adjacent_nodes():
                if not curr.chain_contains(adjacent_node):
                    frontier.appendleft(adjacent_node)

    return list(moves)

def search_board(depth) -> list[Move]:
    global dictionary_caches
    dictionary_caches = [load_dictionary(x) for x in range(2, depth)]

    words = []
    for y in range(5):
        for x in range(5):
            words += search_from_node(SearchNode(None, x, y), depth)

    return words