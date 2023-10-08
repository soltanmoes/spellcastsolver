from time import time

from search import search_board, Move

# take time for profiling
start_time = time()

# search the board
print("Starting search for best move...")
moves = search_board(depth=12)

# remove duplicate words
unique_moves = []
for move in moves:
    if Move.extract_word(move) not in [Move.extract_word(unique_move) for unique_move in unique_moves if not unique_move.swap]:
        unique_moves.append(move)
moves = unique_moves

# sort words by score
moves.sort(key=lambda move : move.score, reverse=True)

# separate by swaps and no swaps
swap_moves = []
no_swap_moves = []

for move in moves:
    if move.swap:
        swap_moves.append(move)
    else:
        no_swap_moves.append(move)

# display top computer moves
print("MOVES WITH SWAPS")
for i, move in enumerate(swap_moves[:5]):
    print(f"{i + 1}. {move.swap_result} via swap at ({move.swapped_node.x + 1}, {move.swapped_node.y + 1}) to {move.swapped_letter} - {move.score} points")

print("\nMOVES WITHOUT SWAPS")
for i, move in enumerate(no_swap_moves[:5]):
    print(f"{i + 1}. {move.frontal_node.word()} - {move.score} points")

print("\nSearch completed!")
print(f"Words Found: {len(moves)}\nElapsed Time: {round(time() - start_time, 3)}s")