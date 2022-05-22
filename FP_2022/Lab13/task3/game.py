from task3.board import Board

if __name__ == '__main__':
    board = Board()
    while board.get_status() == 'continue':
        print(board)
        while True:
            try:
                x, y = map(int,
                           input("Your move in format 1, 0\n>>> ").split(','))
                board.make_move((x, y), 'x')
                break
            except IndexError as e:
                print(e)
        if board.get_status() != 'continue':
            break
        board.make_computer_move()
    print(board)
    print()
    winner = board.get_status()
    if len(winner) == 1:
        print(f'{winner} won!')
    else:
        print(winner)
