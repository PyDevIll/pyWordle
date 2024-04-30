from random import randint


def load_words_by_len(fname, max_length=5):
    def getwords():
        while (w := f.readline().strip()) != '':
            if len(w) == max_length:
                yield w

    with open(fname, 'r', encoding='utf-8') as f:
        return [word for word in getwords()]


def load_w_ratings():
    try:
        f = open("words_rated.txt", 'r', encoding="utf-8")
    except FileNotFoundError:
        return
    w_rating = {}
    with f:
        while (s := f.readline().strip()) != '':
            w_rating[s.split(", ")[0]] = int(s.split(", ")[1])
        return w_rating


def save_w_ratings(w_rating):
    with open("words_rated.txt", 'w', encoding="utf-8") as f:
        for w, r in w_rating.items():
            f.write(f'{w}, {r}\n')


def rate_word(w_rating, w):
    r = w_rating.get(w, -1)
    print(f"{w}. Rating: {r}", end='')
    try:
        new_r = int(input("Rate this word (0-5, ENTER to stop): "))
    except ValueError:
        return
    if new_r not in range(0, 6):
        print("Rate hasn't been accepted!")
        return r
    save_w_ratings(w_rating)
    return new_r


def rate_wordlist():
    wl = load_words_by_len("russian_nouns.txt")
    print("imported", len(wl), "words")

    w_rating = load_w_ratings()
    if w_rating is None:
        return
    print("Rated", len(w_rating), "words")
    while True:
        w = wl[randint(0, len(wl))]
        new_r = rate_word(w_rating, w)
        if new_r is None: break
        w_rating[w] = new_r


if __name__ == "__main__":
    ...


