import main

russian_nouns_txt = [
    "шпала",
    "округлость",
    "покой",
    "скетч",
    "столяр",
    "десна",
    "бухта",
    "визави",
    "обрыв",
    "колхозница",
    "олово",
    "приём",
    "отдых",
    "кольцевание"
    "ручей",
    "идеал"
]

words_rated_txt = {
    "шпала": 0,
    "покой": 1,
    "скетч": 2,
    "десна": 3,
    "бухта": 4,
    "обрыв": 5,
    "олово": 0
}

def fake__load_words_by_len(fname, word_length, shuffled=False):
    # generator
    for w in russian_nouns_txt:
        if len(w) == word_length:
            yield w


def fake__load_w_ratings():
    return words_rated_txt


def fake__save_w_ratings(w_rating):
    global words_rated_txt
    words_rated_txt = w_rating


# stubs for functions using file IO
main.load_words_by_len = fake__load_words_by_len
main.load_w_ratings = fake__load_w_ratings
main.save_w_ratings = fake__save_w_ratings


def test_load_words_to_be_rated():
    w_rating = fake__load_w_ratings()

    # when we want to re-rate previously rated words
    # if returned words are rated as specified by rewise_rating?
    for rewise_rating in range(0, 6):
        for w in main.load_words_to_be_rated(w_rating, rewise_rating):
            assert w_rating[w] == rewise_rating
            assert len(w) == main.word_length
            
    # when we want to rate never rated words
    # if returned words are indeed unrated before?
    for w in main.load_words_to_be_rated(w_rating, -1):
        assert w not in w_rating
        assert len(w) == main.word_length

    # test unexisted rating numbers
    not_entered = True
    for rewise_rating in [-2, 6, 7, 10, 100, 999_999_999]:
        for w in main.load_words_to_be_rated(w_rating, rewise_rating):
            not_entered = False        # cycle should not be entered
            
    assert not_entered


def test_rate_word():
    #rate_word returns new rating after user input
    main.input = lambda _: input_case['value']

    input_cases = [
        {'value': '-1', 'changed': False}, # rate_word should return unchanged rate
        {'value': '-2', 'changed': False},
        {'value': '0', 'changed': True, 'result': 0}, # rate_word should return new rate
        {'value': '1', 'changed': True, 'result': 1},
        {'value': '5', 'changed': True, 'result': 5},
        {'value': '6', 'changed': False},
        {'value': '100', 'changed': False},
        {'value': '', 'changed': True, 'result': None}, # rate_word should return None
        {'value': 'one', 'changed': True, 'result': None}
    ]

    # when we want to modify rating
    # does rating change to a new value or stays unchanged as expected?
    w_rating = fake__load_w_ratings()
    for w, r in w_rating.items():
        for input_case in input_cases:
            returned_value = main.rate_word(w_rating, w)
            if input_case['changed']:
                assert returned_value == input_case['result']
            else:
                assert returned_value == r    # if returned rate is unchanged?
    
    main.input = input
    

def test_rate_wordlist():
    def fake_input(prompt):
        if prompt == ': ':
            return input_case["rating_to_load"]
        if prompt == 'Rate this word (0-5, ENTER to stop): ':
            return input_case["rating_to_set"]
            
    main.input = fake_input

    input_cases = [
        {"rating_to_load": 0, "rating_to_set": 1},
        {"rating_to_load": 1, "rating_to_set": 2},
        {"rating_to_load": 2, "rating_to_set": 3},
        {"rating_to_load": 3, "rating_to_set": 4},
        {"rating_to_load": 4, "rating_to_set": 5},
        {"rating_to_load": 5, "rating_to_set": 0},
    ]

    input_case = input_cases[0]
    main.rate_wordlist()
    assert words_rated_txt == {
        "шпала": 1,
        "покой": 1,
        "скетч": 2,
        "десна": 3,
        "бухта": 4,
        "обрыв": 5,
        "олово": 1
    }
    
    input_case = input_cases[1]
    main.rate_wordlist()
    assert words_rated_txt == {
        "шпала": 2,
        "покой": 2,
        "скетч": 2,
        "десна": 3,
        "бухта": 4,
        "обрыв": 5,
        "олово": 2
    }
    
    input_case = input_cases[2]
    main.rate_wordlist()
    assert words_rated_txt == {
        "шпала": 3,
        "покой": 3,
        "скетч": 3,
        "десна": 3,
        "бухта": 4,
        "обрыв": 5,
        "олово": 3
    }
    
    input_case = input_cases[3]
    main.rate_wordlist()
    assert words_rated_txt == {
        "шпала": 4,
        "покой": 4,
        "скетч": 4,
        "десна": 4,
        "бухта": 4,
        "обрыв": 5,
        "олово": 4
    }
    
    input_case = input_cases[4]
    main.rate_wordlist()
    assert words_rated_txt == {
        "шпала": 5,
        "покой": 5,
        "скетч": 5,
        "десна": 5,
        "бухта": 5,
        "обрыв": 5,
        "олово": 5
    }
    
    input_case = input_cases[5]
    main.rate_wordlist()
    assert words_rated_txt == {
        "шпала": 0,
        "покой": 0,
        "скетч": 0,
        "десна": 0,
        "бухта": 0,
        "обрыв": 0,
        "олово": 0
    }

    main.input = input

#     print("Word rating mode activated.")
#     print("""
#         Enter word rating number (0-5) to rewise already rated words
#         or press ENTER to rate new words
#     """)
#     rewise_rating = get_number(': ', -1)

#     w_rating = load_w_ratings()
#     if w_rating is None:
#         return
#     print("Rated", len(w_rating.keys()), "words.")
#     for w in load_words_to_be_rated(w_rating, rewise_rating):
#         new_r = rate_word(w_rating, w)
#         if new_r is None:
#             break
#         w_rating[w] = new_r
#         save_w_ratings(w_rating)

#     print()


# def get_number(prompt, default=None):
#     # returns integer, or default otherwise
#     try:
#         return int(input(prompt))
#     except ValueError:
#         # Если значение по умолчанию не предусмотрено, значит ошибка ввода
#         if default is None:
#             print(" -! Ожидался ввод числа. Операция прервана !- ")
#     return default


# def load_words_by_level(lvl):
#     def rate_fits_level(r, level):
#         if level == 1:
#             return r == 5
#         elif level == 2:
#             return (r == 5) or (r == 4)
#         elif level == 3:
#             return (r == 4) or (r == 3)
#         elif level == 4:
#             return (r == 2) or (r == 1)
#         else:
#             return True

#     wr = load_w_ratings()
#     result = [w for w, r in wr.items() if rate_fits_level(r, lvl)]
#     return result


# def new_game(level):
#     print("Началась новая игра. Вводите слова и следуйте подсказкам")
#     word_list = load_words_by_level(level)
#     return {
#         "secret_word": word_list[randint(0, len(word_list)-1)],
#         "attempt": 0
#     }


# def word_is_valid(w):
#     if len(w) != word_length:
#         return False

#     cyr_letters = "абвгдеёзжийклмнопрстуфхцчшщъыьэюя"
#     if not all(w_letter in cyr_letters for w_letter in w):
#         return False

#     w = w.replace("ё", "е")
#     # check if w in dictionary
#     for w_dict in load_words_by_len("russian_nouns.txt", word_length):
#         if w_dict.replace("ё", "е") == w:
#             return True
#     return False


# def game_show_hints(game_info):
#     hint_inc = game_info.get("hint_inc", '')
#     hint_exc = game_info.get("hint_exc", '')
#     if len(hint_inc) > 0 or len(hint_exc) > 0:
#         print("Подсказка: ")
#         if len(hint_inc) > 0:
#             print("\tВключите в Ваше слово буквы:", ' '.join(hint_inc).strip())
#         if len(hint_exc) > 0:
#             print("\tЭтих букв точно нет в загаданном слове:", ' '.join(hint_exc).strip())


# def game_make_attempt(game_info):
#     if game_info["attempt"] >= max_attempt:
#         return end_game(game_info, event='noattempts')
#     game_info["attempt"] += 1

#     game_show_hints(game_info)
#     while True:
#         user_word = input()
#         if user_word == '':
#             return end_game(game_info)
#         if word_is_valid(user_word):
#             break
#         print("Кажется это слово не подходит. Попробуйте еще раз")
#     game_info["user_word"] = user_word.lower()
#     return True


# def game_check_attempt(game_info):
#     def replace_char(s, pos, char):
#         s = list(s)
#         s[pos] = char
#         return ''.join(s)

#     result = [0] * word_length

#     hint_include_letters = game_info.get("hint_inc", set())
#     hint_exclude_letters = game_info.get("hint_exc", set())

#     w = game_info["user_word"]
#     s = game_info["secret_word"]

#     # check for exact letter guess (letter and pos)
#     w_pos = -1
#     for w_letter in w:
#         w_pos += 1
#         if w_letter == s[w_pos]:
#             result[w_pos] = 2       # 2 = letter and pos hit
#             s = replace_char(s, w_pos, '_')      # replace guessed letter, so it can't be hit twice
#             hint_include_letters.add(w_letter)

#     # check for close letter guess (letter only)
#     w_pos = -1
#     for w_letter in w:
#         w_pos += 1
#         if result[w_pos] != 0:
#             continue
#         s_pos = s.find(w_letter)
#         if s_pos >= 0:
#             result[w_pos] = 1       # 1 = letter hit
#             s = replace_char(s, s_pos, '_')      # replace guessed letter, so it can't be hit twice
#             hint_include_letters.add(w_letter)
#         else:
#             hint_exclude_letters.add(w_letter)

#     if sum(result) == word_length * 2:
#         return end_game(game_info, event='bingo')

#     game_info["hint_exc"] = (hint_exclude_letters - hint_include_letters)
#     game_info["hint_inc"] = hint_include_letters
#     game_info["result"] = result
#     return True


# def game_draw_result(game_info):
#     result = game_info.get("result", [0] * word_length)
#     result_sym = '_?!'
#     result_str = ''
#     for i in range(word_length):
#         result_str += result_sym[result[i]]

#     print(result_str)
#     print()


# def end_game(game_info, event=''):

#     if event == '':
#         global terminate
#         terminate = True
#         print("Игра окончена")
#         return False

#     if event == 'noattempts':
#         print("К сожалению Вы использовали все попытки (\n")
#     if event == 'bingo':
#         print("СУПЕР! Вы смогли угадать слово!\n")
#         print("Использовано попыток :", game_info["attempt"])

#     print(f"Было загадано слово: \"{game_info["secret_word"]}\"")

#     answer = input("Хотите начать заново? (введите - \"да\")").lower()
#     if answer == "да" or answer == "lf":
#         return False
#     else:
#         end_game(game_info)

