while True:
    game_round = input()
    if not game_round:
        break
    if game_round[0] == game_round[1]:
        print('False | False')
        continue
    if game_round[0] == 'S':
        if game_round[1] == 'P':
            print('True')
        else:
            print('False')
    elif game_round[0] == 'P':
        if game_round[1] == 'R':
            print('True')
        else:
            print('False')
    else:
        if game_round[1] == 'S':
            print('True')
        else:
            print('False')
