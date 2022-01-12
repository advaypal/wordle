from collections import defaultdict
def load_words(words, hints, guesses):
    if not words:
        with open('words.txt', 'r') as f:
            words = f.readlines()
            words = [word.strip() for word in words]

    if not hints:
        return words

    greens, yellows, blacks = hints
    new_words = []
    for word in words:
        should_add = True
        for index, char in enumerate(greens):
            if char is None:
                continue
            elif word[index] != char:
                should_add = False
        for index, char_set in enumerate(yellows):
            if word[index] in char_set:
                should_add = False
            else:
                for char in char_set:
                    if char not in word:
                        should_add = False
        if word in guesses:
            should_add = False
        for char in word:
            if char in blacks:
                should_add = False
        if should_add:
            new_words.append(word)
    return new_words


def get_guess(words):
    dicts = []
    for _ in range(5):
        dicts.append(defaultdict(int))
    for word in words:
        for index, char in enumerate(word):
            dicts[index][char] += 1

    score_dict = {}
    for word in words:
        score = 1
        for index, char in enumerate(word):
            score *= dicts[index][char]
        score_dict[word] = score
    return max(score_dict, key=lambda x: score_dict[x])

def get_hints(word, answer):
    greens, yellows, blacks = [None] * 5, [], set()
    for _ in range(5):
        yellows.append(set())
    for index, char in enumerate(word):
        if char == answer[index]:
            greens[index] = char
        elif char in answer:
            yellows[index].add(char)
        else:
            blacks.add(char)
    return (greens, yellows, blacks)

def wordle(answer='favor'):
    guesses = set()
    words = load_words(None, None, None)
    first = False
    while True:
        guess = get_guess(words)
        print(guess)
        guesses.add(guess)
        if guess == answer:
            print("DONE")
            break
        hints = get_hints(guess, answer)
        words = load_words(words, hints, guesses)


wordle()
