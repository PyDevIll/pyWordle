from random import randint
from datetime import datetime


def log(agent, msg):
    with open("log.txt", 'a', encoding='utf-8') as flog:
        dt = datetime.now()
        log_str = dt.strftime('[%Y-%m-%d %H:%M:%S.%f]') + ' [INFO] ['+agent+']: '+msg
        flog.write(log_str + '\n')


def load_words_by_len(fname, word_length, shuffled=False):
    def read_nearest_valid_word(f_txt):
        while True:
            word = f_txt.readline().strip()
            if word == '':  # end of file
                return None
            if len(word) == word_length:  # valid word found
                return word

    def make_random_offset(f_txt):
        if not f_txt.closed:
            f_txt.close()
        # reset file position by reopening
        f_txt = open(fname, 'r', encoding='utf-8')
        offset = randint(0, line_count)
        for i in range(offset):
            f_txt.readline()
        return f_txt

    def count_lines_in_file():
        count = 0
        with (open(fname, 'r', encoding='utf-8') as f):
            while f.readline() != '':
                count += 1
        return count

    if shuffled:
        line_count = count_lines_in_file()
        f_nouns = open(fname, 'r', encoding='utf-8')
        while True:
            f_nouns = make_random_offset(f_nouns)
            noun = read_nearest_valid_word(f_nouns)
            if noun is None:
                continue
            yield noun
    else:
        with (open(fname, 'r', encoding='utf-8') as f_nouns):
            while True:
                noun = read_nearest_valid_word(f_nouns)
                if noun is None:
                    break
                yield noun

    if not f_nouns.closed:
        f_nouns.close()


def load_w_ratings():
    try:
        f_rates = open("words_rated.txt", 'r', encoding="utf-8")
    except FileNotFoundError:
        return
    w_rating = {}
    with f_rates:
        while True:
            line = f_rates.readline().strip()
            if line == '':
                break
            word, rate = line.split(", ")
            w_rating[word] = int(rate)
        return w_rating


def save_w_ratings(w_rating):
    with open("words_rated.txt", 'w', encoding="utf-8") as f_rates:
        for word, rate in w_rating.items():
            f_rates.write(f'{word}, {rate}\n')


def load_words_to_be_rated(rate_dict, revise_rating=-1):
    if revise_rating == -1:
        for word in load_words_by_len("russian_nouns.txt", word_length, shuffled=True):
            if word not in rate_dict:
                yield word
    else:
        for word, rate in rate_dict.items():
            if rate == revise_rating:
                yield word


def rate_word(w_rating, word):
    max_rating = 5
    old_rate = w_rating.get(word, -1)
    print(f"{word}. Rating: {old_rate}. ", end='')
    new_rate = get_number("Rate this word (0-5, ENTER to stop): ")
    if new_rate is None:
        return None
    if new_rate not in range(0, max_rating + 1):
        print("Rate hasn't been accepted!")
        return old_rate
    return new_rate


def rate_wordlist():
    print("Word rating mode activated.")
    print("""
        Enter word rating number (0-5) to revise already rated words
        or press ENTER to rate new words
    """)
    revise_rating = get_number(': ', -1)

    w_rating = load_w_ratings()
    print("Rated", len(w_rating.keys()), "words.")
    for word in load_words_to_be_rated(w_rating, revise_rating):
        new_rate = rate_word(w_rating, word)
        if new_rate is None:
            break
        w_rating[word] = new_rate
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
    def rate_fits_level(rate, level):
        if level == 1:
            return rate == 5
        elif level == 2:
            return (rate == 5) or (rate == 4)
        elif level == 3:
            return (rate == 4) or (rate == 3)
        elif level == 4:
            return (rate == 2) or (rate == 1)
        else:
            return False

    w_rating = load_w_ratings()
    result = [word for word, rate in w_rating.items() if rate_fits_level(rate, lvl)]
    return result


def new_game(level):
    print("Началась новая игра. Вводите слова и следуйте подсказкам")
    word_list = load_words_by_level(level)
    if len(word_list) > 0:
        new_word = word_list[randint(0, len(word_list) - 1)]
        log('System', 'Начата новая игра. Выбранный уровень сложности: '+str(level))
        log('System', 'Загадано слово "' + new_word + '"')
        return {
            "secret_word": new_word,
            "attempt": 0
        }
    else:
        return None
    

def word_is_valid(word):
    if len(word) != word_length:
        log('System', f'Длина слова отличается от заданной в игре ({word_length})')
        return False

    cyr_letters = "абвгдеёзжийклмнопрстуфхцчшщъыьэюя"
    if not all(word_letter in cyr_letters for word_letter in word):
        log('System', 'Слово содержит некириллические символы')
        return False

    word = word.replace("ё", "е")
    # check if w in dictionary
    for noun_from_txt in load_words_by_len("russian_nouns.txt", word_length):
        if noun_from_txt.replace("ё", "е") == word:
            return True

    log('System', 'Слово не входит в словарь russian_nouns.txt')
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
    if game_info["attempt"] >= max_attempt:
        return 'noattempts'

    log('System', f'Попытка {game_info["attempt"]+1} из {max_attempt}')
    game_show_hints(game_info)
    print()
    user_word = input()
    log('User', 'Вводит слово "' + user_word + '"')

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

    user_word = game_info["user_word"].replace('ё', 'е')
    secret_word = game_info["secret_word"].replace('ё', 'е')

    # check for exact letter guess (letter and pos)
    user_word_pos = -1
    for user_word_letter in user_word:
        user_word_pos += 1
        if user_word_letter == secret_word[user_word_pos]:
            result[user_word_pos] = 2  # 2 = letter and pos hit
            # replace guessed letter, so it can't be hit twice
            secret_word = replace_char(secret_word, user_word_pos, '_')
            hint_include_letters.add(user_word_letter)

    # check for close letter guess (letter only)
    user_word_pos = -1
    for user_word_letter in user_word:
        user_word_pos += 1
        if result[user_word_pos] != 0:
            continue
        secret_word_pos = secret_word.find(user_word_letter)
        if secret_word_pos >= 0:
            result[user_word_pos] = 1  # 1 = letter hit
            # replace guessed letter, so it can't be hit twice
            secret_word = replace_char(secret_word, secret_word_pos, '_')
            hint_include_letters.add(user_word_letter)
        else:
            hint_exclude_letters.add(user_word_letter)

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
    global terminate
    if event == 'quit':
        print("Игра окончена")
        log('System', 'Игрок пожелал покинуть игру. Завершение программы\n')
        terminate = True
        return True     # game actually ends

    if event == 'noattempts':
        print("К сожалению Вы использовали все попытки (\n")
        log('System', 'Попытки исчерпаны. Предлагаем начать заново')
    if event == 'bingo':
        print("СУПЕР! Вы смогли угадать слово!\n")
        print("Использовано попыток :", game_info["attempt"])
        log('System', 'Слово угадано.\n' +
            'Попыток: '+str(game_info["attempt"]) + '\n' +
            'Предлагаем начать заново'
        )

    print(f'Было загадано слово: \"{game_info["secret_word"]}\"')

    answer = input("Хотите начать заново? (введите - \"да\")").lower()
    log('User', 'Ответ пользователя: "'+answer+'"')
    if answer == "да" or answer == "lf":
        return False    # game continues
    else:
        return end_game(game_info)


def main():
    global game_info
    global terminate
    
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
                log('System', 'Слово отклонено. Повтор попытки ввода')
                continue
            elif outcome_msg != 'ok':
                end_game(game_info, outcome_msg)
                break

            log('System', 'Слово принято')

            victory = game_check_attempt(game_info)
            if victory:
                end_game(game_info, 'bingo')
                break

            print(game_draw_result(game_info))
            print()

    print("До свидания!")


max_attempt = 6
word_length = 5
game_info = {}
terminate = False

if __name__ == "__main__":
    main()
