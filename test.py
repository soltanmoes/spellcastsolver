from dictionary import load_dictionary

dictionary = load_dictionary()

alphabet = list("abcdefghijklmnopqrstuvwxyz")

redundantStarters = []

i = 0
for firstLetter in alphabet:
    for secondLetter in alphabet:
        starter = firstLetter + secondLetter

        if i % 100 == 0:
            print(f"Searching {starter}...")
            
        words = []
        for word in list(dictionary):
            if word.startswith(starter):
                words.append(word)
        if len(words) == 0:
            redundantStarters.append(starter)

        i += 1

open("redundant.txt", "w").write("\n".join(redundantStarters))