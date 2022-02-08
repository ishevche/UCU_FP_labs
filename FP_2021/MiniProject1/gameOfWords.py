game_data = [
    ("stove", ["set", "toe", "toes", "vest", "veto", "vote", "votes"], []),
    ("world", ["lor", "low", "old", "owl", "rod", "row", "lord", "word"], []),
    ("note", ["eon", "net", "not", "one", "ten", "toe", "ton", "tone"], []),
    ("acre", ["ace", "arc", "are", "car", "ear", "era", "care", "race"], []),
    ("think", ["hit", "ink", "kit", "tik", "tin", "hint", "knit", "thin"], []),
    ("learn", ["are", "ear", "era", "ran",
               "earn", "lean", "near", "real"], []),
    ("crowd", ["cod", "cow", "doc", "rod", "row", "cord", "crow", "word"], []),
    ("frame", ["are", "arm", "ear", "era", "far",
               "fame", "fare", "farm", "fear", "mare"], []),
    ("dollar", ["all", "lor", "old", "rad", "rod",
                "doll", "load", "lord", "road", "roll"], []),
    ("chart", ["act", "arc", "art", "car", "cat", "hat", "rat",
               "arch", "cart", "char", "chat"], []),
    ("career", ["ace", "arc", "are", "car", "ear", "era",
                "acre", "care", "race", "rare", "rear", "racer"], []),
    ("grace", ["ace", "age", "arc", "are", "car", "ear", "era",
               "acre", "cage", "care", "gear", "race"], []),
    ("posts", ["ops", "opt", "pot", "sos", "top",
               "post", "pots", "spot", "stop", "tops", "toss",
               "spots", "stops"], []),
    ("timed", ["die", "dim", "met", "mid", "tie",
               "diet", "dime", "edit", "item", "mite", "tide", "tied",
               "time"], []),
    ("baths", ["abs", "ash", "bat", "has", "hat", "sat", "tab",
               "bash", "bath", "bats", "hats", "stab", "tabs"], []),
    ("heard", ["are", "ear", "era", "had", "her", "rad", "red",
               "dare", "dear", "hard", "hare",
               "head", "hear", "herd", "read"], [])
]
start_message = f"""Welcome to the game of words!
This game contains {len(game_data)} levels.
At each level, you will receive a keyword.
The goal is to form as many as possible other words
out of the keyword's characters.
You have to find at least 70% of words in the level,
before you can move to the next one"""
help_string = """
There are some commands you can use:
- exit         -> you will exit the game;
- help         -> you will see this message;
- next         -> move to the next level;
- level #<num> -> move to the <num> level;
- <num>        -> the same as \"level #<num>\"
Every command should start with ->, ! or /\n
Some examples:
-> level #5
/exit
!next"""
has_i_asked_to_move_forward = False
cur_level = 0
exit_flag = False


def is_word_good(word: str, keyword: str) -> bool:
    """
    Checks if word is a valid permutation of keyword's characters.

    :param word: str
        string to check
    :param keyword: str
        string consist of characters that can be used in <word>
    :return:
        False if word's length less than 3 symbols
        False if word is equal to keyword
        False if word can not be received by rearranging some letter from keyword
        True otherwise
    """
    if len(word) < 3:
        print("Haven't I said that words must consist of at "
              "least three letters?\n"
              "I haven't forgotten, have I?")
        return False

    if word == keyword:
        print("Really? You have to be more creative!")
        return False

    keyword_array = list(keyword)
    for char in word:
        if not keyword_array.__contains__(char):
            print("Your word should contain only "
                  "keyword characters and only once!")
            return False
        keyword_array.remove(char)

    return True


def is_enough_for_level(num: int) -> bool:
    """
    Checks if enough words are found to go to the level# <num>

    :param num: int
        Number of level to go
    :return:
        True if at least 70% of words in level #<num> - 1 are found
        False otherwise
    """
    if num >= len(game_data) or num < 0:
        return False
    if num == 0:
        return True

    general_amount_of_words = len(game_data[num - 1][1]) + \
                              len(game_data[num - 1][2])
    found_words = len(game_data[num - 1][2])

    return general_amount_of_words * 0.7 <= found_words


def is_command(user_input: str) -> bool:
    return user_input[0:2] == "->" or \
           user_input[0:1] == '/' or \
           user_input[0:1] == '!'


def handle_command(cmd: str):
    """
    Executes command

    :param cmd: str
        Command string without leading / (! or ->) symbol
    :return: None
    """
    global exit_flag, cur_level, has_i_asked_to_move_forward
    if cmd == "exit":
        print("Thanks for playing. See you")
        exit_flag = True

    elif cmd == "help":
        print(help_string)

    elif cmd == "next":
        if is_enough_for_level(cur_level + 1):
            cur_level += 1
            has_i_asked_to_move_forward = False
        else:
            print("You have to find summarily at least 70% of words in "
                  "the current level, before you can move to the next")

    elif cmd[0:7] == "level #":
        try:
            goto = int(cmd[7:])
            go_to_level(goto)
        except ValueError:
            print(f"It must be a number after # symbol")

    else:
        try:
            goto = int(cmd)
            go_to_level(goto)
        except ValueError:
            print("There is no such command\n"
                  "Try using -> help command")


def go_to_level(num: int):
    """
    Changes current level to the level# <num> if it is allowed

    :param num: int
        A number of level to move to
    :return: None
    """
    global cur_level, has_i_asked_to_move_forward

    if num - 1 != cur_level:
        if num > len(game_data) or num <= 0:
            print("It must be a number less or equal "
                  f"{len(game_data)} and grater or equal 1")
        elif is_enough_for_level(num - 1):
            cur_level = num - 1
            has_i_asked_to_move_forward = False
        else:
            print("You have to find summarily at least 70% of words in "
                  f"the level #{num - 1}, "
                  f"before you can move to the level #{num}")


def move_to_uncompleted_level():
    """
    Changes current level on the first unstarted level
    If not possible, on the first uncompleted level

    :return: None
    """
    global exit_flag, cur_level, has_i_asked_to_move_forward

    not_started_level = cur_level + 1
    while not_started_level < len(game_data) and \
            len(game_data[not_started_level][2]) > 0:
        not_started_level += 1

    if is_enough_for_level(not_started_level):
        cur_level = not_started_level
        has_i_asked_to_move_forward = False
    else:
        not_completed_level = 0
        while not_completed_level < len(game_data) and \
                len(game_data[not_completed_level][1]) == 0:
            not_completed_level += 1

        if not_completed_level == len(game_data):
            print("We have an absolute winner!\n"
                  "You have found all words\n"
                  "Thank you for playing\n"
                  "See you")
            exit_flag = True
        else:
            cur_level = not_completed_level
            has_i_asked_to_move_forward = False


def play_level():
    """
    Presides player's turn

    :return: None
    """
    level_data = game_data[cur_level]
    user_input = input(">>> ").lower().strip()

    if is_command(user_input):
        handle_command(user_input[2 if user_input[0:2] == "->"
                                  else 1:].strip())
    elif is_word_good(user_input, level_data[0]):
        if level_data[2].__contains__(user_input):
            print("You have already found this word")
        elif len(level_data[1]) == 0:
            print("You have already found all words in this level\n"
                  "You can move to another one")
        elif not level_data[1].__contains__(user_input):
            print("Oh, I don't think it is a real word\n"
                  "Try another one")
        else:
            new_word_found(user_input)


def new_word_found(word: str):
    """
    Handles new valid word finding

    :param word: str
        Word that was found
    :return: None
    """
    global cur_level, has_i_asked_to_move_forward

    level_data = game_data[cur_level]

    level_data[2].append(word)
    level_data[1].remove(word)

    if len(level_data[1]) == 0:
        print("Congrats!!! You have found all the "
              "words in this level")
        move_to_uncompleted_level()

    elif cur_level < len(game_data) - 1 and \
            is_enough_for_level(cur_level + 1) and \
            not has_i_asked_to_move_forward:
        has_i_asked_to_move_forward = True
        print("Congrats!!! You can now move to the next level\n"
              "Do you want to move? [YES|no]")
        answer = input(">>> ").lower().strip()
        if answer == "yes" or answer == "y" or answer == "":
            cur_level += 1
            has_i_asked_to_move_forward = False


def print_level_info():
    """
    Prints current game state

    :return: None
    """
    level_data = game_data[cur_level]
    total_words_amount = len(level_data[1]) + len(level_data[2])
    found_words_amount = len(level_data[2])

    print(f"\nLevel #{cur_level + 1}: Keyword -> {level_data[0]} "
          f"{found_words_amount}/{total_words_amount} "
          f"({round(100 * found_words_amount / total_words_amount)}%)")

    if found_words_amount != 0:
        print("Already found:",
              ", ".join(level_data[2]))


if __name__ == '__main__':
    print(start_message)
    print(help_string)
    while not exit_flag:
        print_level_info()
        play_level()
