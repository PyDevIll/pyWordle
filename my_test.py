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
    "кольцевание",
    "ручей",
    "идеал",
    "хряст",
    "кино",
    "ворог",
    "фьорд",
    "жатва",
    "носач",
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
    # rate_word returns new rating after user input
    main.input = lambda _: input_case['value']

    input_cases = [
        {'value': '-1', 'changed': False},      # rate_word should return unchanged rate
        {'value': '-2', 'changed': False},
        {'value': '0', 'changed': True, 'result': 0},   # rate_word should return new rate
        {'value': '1', 'changed': True, 'result': 1},
        {'value': '5', 'changed': True, 'result': 5},
        {'value': '6', 'changed': False},
        {'value': '100', 'changed': False},
        {'value': '', 'changed': True, 'result': None},     # rate_word should return None
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
        {"rating_to_load": '0', "rating_to_set": '1'},
        {"rating_to_load": '1', "rating_to_set": '2'},
        {"rating_to_load": '2', "rating_to_set": '3'},
        {"rating_to_load": '3', "rating_to_set": '4'},
        {"rating_to_load": '4', "rating_to_set": '5'},
        {"rating_to_load": '5', "rating_to_set": ''},
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
        "шпала": 5,
        "покой": 5,
        "скетч": 5,
        "десна": 5,
        "бухта": 5,
        "обрыв": 5,
        "олово": 5
    }
    main.input = input


def test_get_number():
    main.input = lambda _: input_case["num"]

    input_cases = [
        {"num": "", "will_succeed": False},
        {"num": "-1", "will_succeed": True},
        {"num": "-0", "will_succeed": True},
        {"num": "000_000", "will_succeed": True},
        {"num": "0_0", "will_succeed": True},
        {"num": "-1_", "will_succeed": False},
        {"num": "0", "will_succeed": True},
        {"num": "$1", "will_succeed": False},
        {"num": "\n", "will_succeed": False},
        {"num": "1", "will_succeed": True},
        {"num": "1.0", "will_succeed": False},
        {"num": "1.0.0", "will_succeed": False}        
    ]

    for input_case in input_cases:
        assert (type(main.get_number("")) == int) == input_case["will_succeed"]
        assert type(main.get_number("", 0)) == int

    main.input = input
    

def test_load_words_by_level():
    global words_rated_txt
    words_rated_txt = {
        "шпала": 0,
        "хряст": 1,
        "ворог": 2,
        "фьорд": 3,
        "жатва": 4,
        "носач": 3,
        "олово": 5
    }
    level_normal = 1
    level_hard = 2
    level_nightmare = 3
    level_horror = 4

    words_returned = main.load_words_by_level(level_normal)
    assert set(words_returned) == {"олово"}                      # normal: ratings 5
    
    words_returned = main.load_words_by_level(level_hard)
    assert set(words_returned) == {"олово", "жатва"}             # hard  : ratings 5 & 4
    
    words_returned = main.load_words_by_level(level_nightmare) 
    assert set(words_returned) == {"фьорд", "жатва", "носач"}    # nightmare: ratings 4 & 3
    
    words_returned = main.load_words_by_level(level_horror)
    assert set(words_returned) == {"хряст", "ворог"}             # horror: ratings 2 & 1

    words_returned = main.load_words_by_level(0)
    assert len(words_returned) == 0

    words_returned = main.load_words_by_level(-1)
    assert len(words_returned) == 0

    words_returned = main.load_words_by_level(5)
    assert len(words_returned) == 0

    words_returned = main.load_words_by_level(999)
    assert len(words_returned) == 0


def test_new_game():
    test_levels_success = [4, 3, 2, 1]
    for level in test_levels_success:
        game_info = main.new_game(level)
        assert game_info["attempt"] == 0
        assert len(game_info["secret_word"]) == main.word_length
        assert game_info["secret_word"] in words_rated_txt
        assert game_info["secret_word"] in main.load_words_by_level(level)

    test_levels_fail = [0, 5, -1, 999]
    for level in test_levels_fail:
        game_info = main.new_game(level)
        assert game_info is None


def test_word_is_valid():
    main.word_length = 5
    assert not main.word_is_valid("округлость")
    assert not main.word_is_valid("")
    assert not main.word_is_valid("кино")
    assert not main.word_is_valid("сампридумал")
    assert not main.word_is_valid("абвгд")
    assert not main.word_is_valid("ол0во")
    assert not main.word_is_valid("false")
    
    assert main.word_is_valid("бухта")
    assert main.word_is_valid("шпала")
    assert main.word_is_valid("ручей")
    assert main.word_is_valid("идеал")
    assert main.word_is_valid("прием")    # е <=> ё


def test_game_show_hints():
    game_info = {
        "hint_inc": {"й", "щ"},
        "hint_exc": {"ь", "э"}
    }
    main.game_show_hints(game_info)
    assert True    # no crash
    
    game_info = {
        "hint_inc": {},
        "hint_exc": None
    }
    main.game_show_hints(game_info)
    assert True    # no crash
    

def test_game_make_attempt():
    main.input = lambda _='': input_case["user_input"]

    input_cases = [
        {"user_input": '', "outcome_msg": 'quit'},
        {"user_input": 'скетч', "outcome_msg": 'ok'},           # word that is in dictionary
        {"user_input": 'абоба', "outcome_msg": 'tryagain'},     # is not in dictionary
        {"user_input": 'бухта', "outcome_msg": 'ok'},
        {"user_input": 'десна', "outcome_msg": 'noattempts'}
    ]

    game_info = {
        "attempt": 4,
    }
    main.max_attempt = 6

    for input_case in input_cases:
        game_info["user_word"] = ''         # previously unset
        outcome_msg = main.game_make_attempt(game_info)
        assert outcome_msg == input_case["outcome_msg"]
        if outcome_msg == 'ok':
            assert game_info["user_word"] == input_case["user_input"]   # becomes set
        else:
            assert game_info["user_word"] == ''     # stays unset

    main.input = input


def test_game_check_attempt():
    game_info = {
        "user_word": "ручей",
        "secret_word": "скетч"
    }
    victory = main.game_check_attempt(game_info)
    assert not victory
    assert game_info["result"] == [0, 0, 1, 1, 0]
    assert game_info["hint_inc"] == {'е', 'ч'}
    assert game_info["hint_exc"] == {'р', 'у', 'й'}

    game_info["user_word"] = "отчёт"
    victory = main.game_check_attempt(game_info)
    assert not victory
    assert game_info["result"] == [0, 1, 1, 1, 0]
    assert game_info["hint_inc"] == {'е', 'ч', 'т'}
    assert game_info["hint_exc"] == {'р', 'у', 'й', 'о'}

    game_info = {
        "user_word": "прием",
        "secret_word": "приём"
    }
    victory = main.game_check_attempt(game_info)
    assert victory


def test_game_draw_result():
    main.word_length = 5
    game_info = {
        "result": [1, 0, 0, 2, 0]
    }
    assert main.game_draw_result(game_info) == '?__!_'

    game_info = {}
    assert main.game_draw_result(game_info) == '_____'

    game_info = {
        "result": [2, 2, 2, 2, 2]
    }
    assert main.game_draw_result(game_info) == '!!!!!'


def test_end_game():
    game_info = {
        "attempt": 0,
        "secret_word": ""
    }
    main.terminate = False
    assert main.end_game(game_info)     # True - game ends
    assert main.terminate

    assert main.end_game(game_info, 'quit')
    assert main.terminate

    main.input = lambda _: input_case["user_input"]
    input_cases = [
        {"user_input": "lf", "result": False},   # False - game continues
        {"user_input": "да", "result": False},
        {"user_input": "ДА", "result": False},
        {"user_input": "", "result": True},
        {"user_input": "нет", "result": True}
    ]
    for input_case in input_cases:
        main.terminate = False
        assert main.end_game(game_info, 'bingo') == input_case["result"]
        assert main.terminate == input_case["result"]

    for input_case in input_cases:
        main.terminate = False
        assert main.end_game(game_info, 'noattempts') == input_case["result"]
        assert main.terminate == input_case["result"]

    main.input = input


"""
    scenario_step = -1
    
                        # !!! couldn't implement !!! 
    def test_main():
        def fake_input(prompt=''):
            global scenario_step
            scenario_step += 1
            return scenario[scenario_step][prompt]
    
        main.input = fake_input
        main.randint = lambda a, b: 1       # no random during tests
    
        global words_rated_txt
        words_rated_txt = {
            "шпала": 0,
            "хряст": 1,
            "ворог": 2,
            "фьорд": 3,
            "жатва": 4,
            "носач": 3,
            "олово": 5
        }
        global scenario_step
    
        scenario = [
            {"Ваш выбор (1-4, ENTER - выход): ": "5"},       # go into rate mode
            {": ": "0"},                                     # select words with rating 0
            {"Rate this word (0-5, ENTER to stop): ": "5"},  # change rate to 5
            {"Ваш выбор (1-4, ENTER - выход): ": ""},        # exit
        ]
        scenario_step = -1
        main.main()
        assert words_rated_txt["шпала"] == 5        # !!!  fails to change value !!!
    
        scenario = [
            {"Ваш выбор (1-4, ENTER - выход): ": "2"},
            {"Ваше слово: ": "жатва"},
            {"Хотите начать заново? (введите - \"да\")": ""}
        ]
        scenario_step = -1
        main.main()
        assert main.game_info == {
            "user_word": "жатва",
            "secret_word": "жатва",
            "attempt": 1,
        }
    
        main.input = input
"""

