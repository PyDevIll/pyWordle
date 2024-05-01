from random import randint


def load_words_by_len(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        while (w := f.readline().strip()) != '':
            if len(w) == word_length:
                yield w


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
    max_rating = 6
    r = w_rating.get(w, -1)
    print(f"{w}. Rating: {r}. ", end='')
    try:
        new_r = int(input("Rate this word (0-5, ENTER to stop): "))
    except ValueError:
        return
    if new_r not in range(0, max_rating + 1):
        print("Rate hasn't been accepted!")
        return r
    save_w_ratings(w_rating)
    return new_r


def rate_wordlist(rewise_rating=-1):
    print("Word rating update mode activated.")

    w_rating = load_w_ratings()
    if w_rating is None:
        return
    print("Rated", len(w_rating), "words.")
    ok = False
    for w in load_words_by_len("russian_nouns.txt", 5):
        if rewise_rating == -1:
            ok = (w not in w_rating.keys())
        else:
            ok = (w_rating[w] == rewise_rating)
        if ok:
            new_r = rate_word(w_rating, w)
            if new_r is None: break
            w_rating[w] = new_r
    print()


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
    print("Началась новая игра. Вводите слова и следуйте подсказкам")
    word_list = load_words_by_level(level)
    return {
        "secret_word": word_list[randint(0, len(word_list)-1)],
        "attempt": 0
    }


def word_is_valid(w):
    if len(w) != word_length:
        return False

    cyr_letters = "абвгдеёзжийклмнопрстуфхцчшщъыьэюя"
    if not all(w_letter in cyr_letters for w_letter in w):
        return False

    w = w.replace("ё", "е")
    # check if w in dictionary
    for w_dict in load_words_by_len("russian_nouns.txt"):
        if w_dict.replace("ё", "е") == w:
            return True
    return False


def game_make_attempt(game_info):
    if game_info["attempt"] >= max_attempt:
        return end_game(game_info)
    game_info["attempt"] += 1
    while True:
        user_word = input()
        if user_word == '':
            return end_game(game_info)
        if word_is_valid(user_word):
            break
        print("Кажется это слово не подходит. Попробуйте еще раз")
    game_info["user_word"] = user_word
    return True


def game_check_attempt(game_info):
    result = [0] * word_length

    hint_include_letters = game_info.get("hint_inc", [])
    hint_exclude_letters = game_info.get("hint_exc", [])
    w = game_info["user_word"]
    s = game_info["secret_word"]
    w_pos = 0
    for w_letter in w:
        s_pos = s.find(w_letter)
        if s_pos >= 0:
            result[w_pos] += 1       # 1 = letter hit
            hint_include_letters.append(w_letter)
            s = s.replace(w_letter, '_', 1)   # replace guessed letter, so it can't be hit twice
            if s_pos == w_pos:
                result[w_pos] += 1   # 2 = letter and pos hit
        else:
            hint_exclude_letters.append(w_letter)
        w_pos += 1

    if sum(result) == word_length * 2:
        return end_game(game_info, can_repeat=True)

    game_info["hint_exc"] = hint_exclude_letters
    game_info["hint_inc"] = hint_include_letters
    game_info["result"] = result
    return True


def game_draw_result(game_info):
    result = game_info.get("result", [0] * word_length)
    result_sym = '_?!'
    result_str = ''
    for i in range(word_length):
        result_str += result_sym[result[i]]

    print(result_str)
    print()


def end_game(game_info, can_repeat=False):
    if not can_repeat:
        global terminate
        terminate = True
        print("Игра окончена")
        return False

    print("Использовано попыток :", game_info["attempt"])
    print(f"Было загадано слово: \"{game_info["secret_word"]}\"")
    answer = input("Хотите начать заново? (введите - \"да\")")
    if answer == "да" or answer == "lf":
        return False
    else:
        end_game(game_info)


max_attempt = 6
word_length = 5

global terminate

if __name__ == "__main__":
    print("\t\t-= ВОРДЛИ =-")
    print()
    print(f"Угадайте загаданное слово из {word_length} букв за {max_attempt} попыток")
    print()
    terminate = False
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
            if not game_make_attempt(game_info):
                break
            if not game_check_attempt(game_info):
                break
            game_draw_result(game_info)


    print("До свидания!")
