game_board = [
    ["-", "-", "-"],
    ["-", "-", "-"],
    ["-", "-", "-"]
]                               # игровое поле

def view_board(board):    # функция для отображения игрового поля
    for row in board:
        for element in row:
            print(element, end=" ")
        print()


def win(board, player):    # функция для проверки победной комбинации
    for row in board:
        if row.count(player) == 3:
            return True
    if board[0][0] == player and board[1][0] == player and board[2][0] == player:
        return True
    if board[0][1] == player and board[1][1] == player and board[2][1] == player:
        return True
    if board[0][2] == player and board[1][2] == player and board[2][2] == player:
        return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True


current_player = "X"    # первый игрок ставит X

while True:    # Блок кода в котором прописано принятие и сохранение хода игрока
    view_board(game_board)
    print("Сейчас ходит игрок", current_player)
    row = int(input("Выберите строку: ")) - 1
    col = int(input("Выберите столбец: ")) - 1
    if game_board[row][col] != "-":
        print("Поле занято")
        continue
    game_board[row][col] = current_player
    if win(game_board, current_player):
        view_board(game_board)
        print(f"Игрок {current_player} выиграл")
        break
    if all([element != "-" for row in game_board for element in row]):
        print("Ничья")
        view_board(game_board)
        break

    current_player = "O" if current_player == "X" else "X"    # Смена игрока на O
