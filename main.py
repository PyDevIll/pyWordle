from random import randint


def load_words_by_len(fname, word_length, shuffled=False):
    def read_nearest_valid_word(f):
        while True:
            w = f.readline().strip()
            if w == '':  # end of file
                return None
            if len(w) == word_length:  # valid word found
                return w

    def make_random_offset(f):
        if not f.closed:
            f.close()
        # reset file position by reopening
        f = open(fname, 'r', encoding='utf-8')
        offset = randint(0, line_count)
        for i in range(offset):
            f.readline()
        return f

    def count_lines_in_file():
        n = 0
        with (open(fname, 'r', encoding='utf-8') as f):
            while f.readline() != '':
                n += 1
        return n

    if shuffled:
        line_count = count_lines_in_file()
        f = open(fname, 'r', encoding='utf-8')
        while True:
            f = make_random_offset(f)
            w = read_nearest_valid_word(f)
            if w is None:
                continue
            yield w
    else:
        with (open(fname, 'r', encoding='utf-8') as f):
            while True:
                w = read_nearest_valid_word(f)
                if w is None:
                    break
                yield w

    if not f.closed:
        f.close()


def load_w_ratings():
    try:
        f = open("words_rated.txt", 'r', encoding="utf-8")
    except FileNotFoundError:
        return
    w_rating = {}
    with f:
        while True:
            s = f.readline().strip()
            if s == '':
                break
            word, rate = s.split(", ")
            w_rating[word] = int(rate)
        return w_rating


def save_w_ratings(w_rating):
    with open("words_rated.txt", 'w', encoding="utf-8") as f:
        for w, r in w_rating.items():
            f.write(f'{w}, {r}\n')


def load_words_to_be_rated(rate_dict, rewise_rating=-1):
    if rewise_rating == -1:
        for w in load_words_by_len("russian_nouns.txt", word_length, shuffled=True):
            if w not in rate_dict:
                yield w
    else:
        for w, r in rate_dict.items():
            if r == rewise_rating:
                yield w


def rate_word(w_rating, w):
    max_rating = 5
    old_r = w_rating.get(w, -1)
    print(f"{w}. Rating: {old_r}. ", end='')
    new_r = get_number("Rate this word (0-5, ENTER to stop): ")
    if new_r is None:
        return None
    if new_r not in range(0, max_rating + 1):
        print("Rate hasn't been accepted!")
        return old_r
    return new_r


def rate_wordlist():
    print("Word rating mode activated.")
    print("""
        Enter word rating number (0-5) to rewise already rated words
        or press ENTER to rate new words
    """)
    rewise_rating = get_number(': ', -1)

    w_rating = load_w_ratings()
    print("Rated", len(w_rating.keys()), "words.")
    for w in load_words_to_be_rated(w_rating, rewise_rating):
        new_r = rate_word(w_rating, w)
        if new_r is None:
            break
        w_rating[w] = new_r
        save_w_ratings(w_rating)

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


def load_words_by_level(lvl):
    def rate_fits_level(r, level):
        if level == 1:
            return r == 5
        elif level == 2:
            return (r == 5) or (r == 4)
        elif level == 3:
            return (r == 4) or (r == 3)
        elif level == 4:
            return (r == 2) or (r == 1)
        else:
            return False

    wr = load_w_ratings()
    result = [w for w, r in wr.items() if rate_fits_level(r, lvl)]
    return result


def new_game(level):
    print("Началась новая игра. Вводите слова и следуйте подсказкам")
    word_list = load_words_by_level(level)
    if len(word_list) > 0:
        new_word = word_list[randint(0, len(word_list) - 1)]
        return {
            "secret_word": new_word,
            "attempt": 0
        }
    else:
        return None
    

def word_is_valid(w):
    if len(w) != word_length:
        return False

    cyr_letters = "абвгдеёзжийклмнопрстуфхцчшщъыьэюя"
    if not all(w_letter in cyr_letters for w_letter in w):
        return False

    w = w.replace("ё", "е")
    # check if w in dictionary
    for w_dict in load_words_by_len("russian_nouns.txt", word_length):
        if w_dict.replace("ё", "е") == w:
            return True
    return False


def game_show_hints(game_info):
    hint_inc = game_info.get("hint_inc", '')
    hint_exc = game_info.get("hint_exc", '')
    if (hint_inc is None) or (hint_exc is None):
        return    # нет подсказок
        
    if len(hint_inc) > 0 or len(hint_exc) > 0:
        print("Подсказка: ")
        if len(hint_inc) > 0:
            print("\tВключите в Ваше слово буквы:", ' '.join(hint_inc).strip())
        if len(hint_exc) > 0:
            print("\tЭтих букв точно нет в загаданном слове:", ' '.join(hint_exc).strip())


def game_make_attempt(game_info):
    if game_info["attempt"] + 1 > max_attempt:
        return 'noattempts'

    game_show_hints(game_info)
    user_word = input()

    if user_word == '':
        return 'quit'
    if not word_is_valid(user_word):
        print("Кажется это слово не подходит. Попробуйте еще раз")
        return 'tryagain'

    game_info["attempt"] += 1
    game_info["user_word"] = user_word.lower()
    return 'ok'


def game_check_attempt(game_info):
    def replace_char(s, pos, char):
        s = list(s)
        s[pos] = char
        return ''.join(s)

    result = [0] * word_length

    hint_include_letters = game_info.get("hint_inc", set())
    hint_exclude_letters = game_info.get("hint_exc", set())

    w = game_info["user_word"].replace('ё', 'е')
    s = game_info["secret_word"].replace('ё', 'е')

    # check for exact letter guess (letter and pos)
    w_pos = -1
    for w_letter in w:
        w_pos += 1
        if w_letter == s[w_pos]:
            result[w_pos] = 2  # 2 = letter and pos hit
            s = replace_char(s, w_pos, '_')  # replace guessed letter, so it can't be hit twice
            hint_include_letters.add(w_letter)

    # check for close letter guess (letter only)
    w_pos = -1
    for w_letter in w:
        w_pos += 1
        if result[w_pos] != 0:
            continue
        s_pos = s.find(w_letter)
        if s_pos >= 0:
            result[w_pos] = 1  # 1 = letter hit
            s = replace_char(s, s_pos, '_')  # replace guessed letter, so it can't be hit twice
            hint_include_letters.add(w_letter)
        else:
            hint_exclude_letters.add(w_letter)

    if sum(result) == word_length * 2:
        return True

    game_info["hint_exc"] = (hint_exclude_letters - hint_include_letters)
    game_info["hint_inc"] = hint_include_letters
    game_info["result"] = result
    return False


def game_draw_result(game_info):
    result = game_info.get("result", [0] * word_length)
    result_sym = '_?!'
    result_str = ''
    for i in range(word_length):
        result_str += result_sym[result[i]]

    return result_str


def end_game(game_info, event='quit'):
    if event == 'quit':
        global terminate
        terminate = True
        print("Игра окончена")
        return True     # game actually ends

    if event == 'noattempts':
        print("К сожалению Вы использовали все попытки (\n")
    if event == 'bingo':
        print("СУПЕР! Вы смогли угадать слово!\n")
        print("Использовано попыток :", game_info["attempt"])

    print(f'Было загадано слово: \"{game_info["secret_word"]}\"')

    answer = input("Хотите начать заново? (введите - \"да\")").lower()
    if answer == "да" or answer == "lf":
        return False    # game continues
    else:
        return end_game(game_info)


def main():
    print("\t\t-= ВОРДЛИ =-")
    print()
    print(f"Угадайте загаданное слово из {word_length} букв за {max_attempt} попыток")
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
        if game_info is None:
            print("Не удалось загадать слово для выбранного уровня сложности (")
            exit()
            
        while True:
            outcome_msg = game_make_attempt(game_info)
            if outcome_msg == 'tryagain':
                continue
            elif outcome_msg != 'ok':
                end_game(game_info, outcome_msg)
                break

            victory = game_check_attempt(game_info)
            if victory:
                end_game(game_info, 'bingo')
                break

            print(game_draw_result(game_info))
            print()


    print("До свидания!")


max_attempt = 6
word_length = 5
terminate = False

if __name__ == "__main__":
    main()
