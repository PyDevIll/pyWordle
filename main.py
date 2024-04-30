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
    print("Word rating update mode activated.")
    print("Imported", len(wl), "words.")

    w_rating = load_w_ratings()
    if w_rating is None:
        return
    print("Rated", len(w_rating), "words.")
    while True:
        w = wl[randint(0, len(wl))]
        new_r = rate_word(w_rating, w)
        if new_r is None: break
        w_rating[w] = new_r


def get_number(prompt, default=None):
    # returns integer, or default otherwise
    try:
        return int(input(prompt))
    except ValueError:
        # Если значение по умолчанию не предусмотрено, значит ошибка ввода
        if default is None:
            print(" -! Ожидался ввод числа. Операция прервана !- ")
    return default


def load_words_by_level(n):
    if n == 1:
        rate_fits_level = lambda r: r == 5
    elif n == 2:
        rate_fits_level = lambda r: (r == 4) or (r == 3)
    elif n == 3:
        rate_fits_level = lambda r: (r == 2) or (r == 1)
    elif n == 4:
        rate_fits_level = lambda r: (r == 1) or (r == 0)
    else:
        rate_fits_level = lambda r: True

    wr = load_w_ratings()
    result = [w for w, r in wr.items() if rate_fits_level(r)]
    return result


def new_game(level):
    word_list = load_words_by_level(level)
    return {
        "secret_word": word_list[randint(0, len(word_list))],
        "attempt": 1
    }


max_attempt = 6
game_info = {}
terminate = False

if __name__ == "__main__":
    print("\t\t-= ВОРДЛИ =-")
    print()
    print(f"Угадайте загаданное слово за {max_attempt} попыток")
    print()
    while not terminate:
        print("Выберите сложность:")
        print("1. Нормально")
        print("2. Сложно")
        print("3. Кошмар")
        print("4. Ужас")
        print()
        if (select := get_number("Ваш выбор (1-4, ENTER - выход): ")) is None:
            break
        if select not in range(1, 5):
            rate_wordlist()
            continue

        game_info = new_game(select)
        while not terminate:
            ...

    print("До свидания!")
