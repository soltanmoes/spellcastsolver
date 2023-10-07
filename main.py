from time import time

from search import search_board

# take time for profiling
start_time = time()

# search the board
words = search_board(depth=12)

# remove duplicate words
unique_words = []
for node in words:
    if node.word() not in [unique_node.word() for unique_node in unique_words]:
        unique_words.append(node)
words = unique_words

# sort words by score
words.sort(key=lambda node : node.score(), reverse=True)

# display top computer moves
for i, node in enumerate(words[:10]):
    print(f"{i + 1}. {node.word()} - {node.score()} points")

print(f"Search complete (elapsed time: {round(time() - start_time, 3)}s)")
print(f"Found {len(words)} words.")