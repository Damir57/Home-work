import random
from random import randint


class BoardException(Exception):    # родительский класс исключений
    pass


class BoardOutException(BoardException):    # класс исключения - выстрел за пределы доски
    def __str__(self):
        return "Выстрел за пределы доски!"


class BoardUsedException(BoardException):    # класс исключения - повторный выстрел в клетку
    def __str__(self):
        return "В эту клетку уже стреляли!"


class WrongShipPlacementException(BoardException):    # класс исключения - неправильная установка корабля
    pass


class Dot:    # класс точек для сравнения координат
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):    # метод для проверки точек
        return self.x == other.x and self.y == other.y


class Ship:    # класс корабль. Параметры класса: начало корабля, длина корабля, направление корабля и жизни корабля
    def __init__(self, bow, length, orientation):
        self.bow = bow
        self.length = length
        self.orientation = orientation
        self.ship_lives = length

    @property
    def dots(self):    # метод для возвращения списка всех точек корабля
        ship_dots = []
        for i in range(self.length):
            cur_x = self.bow.x
            cur_y = self.bow.y
            if self.orientation == 0:
                cur_x += i
            else:
                cur_y += i
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots


class Board:    # класс игровой доски. Параметры: размер игрового поля, параметр скрытия игрового поля оппонента,
    def __init__(self, hid=False, size=6):                      # список состояния каждой точки, список кораблей
        self.size = size
        self.hid = hid
        self.count = 0
        self.field = [["O"] * size for _ in range(size)]
        self.busy = []
        self.ships = []

    def add_ship(self, ship):    # метод для установки кораблей на доску
        for dot in ship.dots:
            if self.out(dot) or dot in self.busy:
                raise WrongShipPlacementException()
        for dot in ship.dots:
            self.field[dot.x][dot.y] = "□"
            self.busy.append(dot)
        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):    # метод который обводит корабль по контуру
        near_ship = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dot in ship.dots:
            for dot_x, dot_y in near_ship:
                cur = Dot(dot.x + dot_x, dot.y + dot_y)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def out(self, dot):    # метод для определения выходит ли точка за пределы доски
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def shot(self, dot):    # метод для выстрела по доске
        if self.out(dot):
            raise BoardOutException()
        if dot in self.busy:
            raise BoardUsedException()
        self.busy.append(dot)

        for ship in self.ships:    # блок кода показывающий результат выстрела с изменением статуса точки на доске
            if dot in ship.dots:
                ship.ship_lives -= 1
                self.field[dot.x][dot.y] = "X"
                if ship.ship_lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    self.ships.remove(ship)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль подбит!")
                    return True
        self.field[dot.x][dot.y] = "T"
        print("Промах")
        return False

    def begin(self):    # очистка списка точек
        self.busy = []

    def __str__(self):    # метод для отображения игровой доски
        res = "  | " + " | ".join(str(i + 1) for i in range(self.size)) + " |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"
        if self.hid:
            res = res.replace("□", "O")
        return res

class Player:    # родительский класс игрока. Параметры: доска игрока (пользователя), доска оппонента
    def __init__(self, board, board_opponent):
        self.board = board
        self.board_opponent = board_opponent

    def ask(self):    # пустой метод для запроса в какую точку делать выстрел
        raise NotImplementedError()

    def move(self):    # метод отвечающий за ход игры
        while True:
            try:
                target = self.ask()
                repeat = self.board_opponent.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class User(Player):    # класс пользователь с методом запроса в какую точку делать выстрел
    def ask(self):
        while True:
            coordinates = input("Ход игрока: ").split()
            if len(coordinates) != 2:
                print("Введите 2 координаты через пробел")
                continue
            x, y = coordinates
            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа")
                continue
            x = int(x)
            y = int(y)
            return Dot(x - 1, y - 1)


class AI(Player):    # класс оппонента (в данном случае компьютера) с методом выстрела в случайную точку
    def ask(self):
        x = random.randint(0, self.board.size - 1)
        y = random.randint(0, self.board.size - 1)
        print(f"Ход оппонента: {x + 1}, {y + 1}")
        return Dot(x, y)


class Game:    # класс Игра. Параметры: доска пользователя, объект класса User (пользователь),
    def __init__(self, size=6):              # доска компьютера, объект класса AI (компьютер)
        self.size = size
        user_board = self.random_board()
        ai_board = self.random_board()
        ai_board.hid = True
        self.user = User(user_board, ai_board)
        self.ai = AI(ai_board, user_board)

    def random_board(self):    # метод генерации доски
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):    # метод для расстановки кораблей на доске
        ship_points = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for point in ship_points:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), point, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except WrongShipPlacementException:
                    pass
        board.begin()
        return board

    def greet(self):    # метод приветствия игрока
        print("Добро пожаловать в игру Морской бой")
        print("Для игры требуется вводить через пробел номер строки и номер столбца")

    def loop(self):    # метод с игровым циклом. Показ игровых полей, вызов метода хода игры,
        num = 0                 # проверка количсетва живых кораблей и объявление победителя
        while True:
            print("")
            print("Поле игрока:")
            print(self.user.board)
            print("")
            print("Поле оппонента:")
            print(self.ai.board)
            if num % 2 == 0:
                print("")
                repeat = self.user.move()
            else:
                print("Ход оппонента")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            if self.user.board.count == 7:
                print("Поле игрока:")
                print(self.user.board)
                print("Оппонент выиграл!")
                break
            if self.ai.board.count == 7:
                print("Поле оппонента:")
                print(self.ai.board)
                print("Игрок выиграл!")
                break
            num += 1

    def start(self):    # метод запуска игры
        self.greet()
        self.loop()


g = Game()    # создание экземпляра класса Game
g.start()    # вызов метода start для запуска игры
