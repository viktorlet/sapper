from random import randint
from emoji import emojize


class Cell:
    error = ValueError("недопустимое значение атрибута")

    def __init__(self):
        self.is_mine = False
        self.number = 0
        self.is_open = False
        self.flag = False

    @classmethod
    def __check_bool(cls, value):
        if not isinstance(value, bool):
            raise cls.error

    @property
    def is_mine(self):
        return self.__is_mine

    @is_mine.setter
    def is_mine(self, value):
        self.__check_bool(value)
        self.__is_mine = value

    @property
    def is_open(self):
        return self.__is_open

    @is_open.setter
    def is_open(self, value):
        self.__check_bool(value)
        self.__is_open = value

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, value):
        if not isinstance(value, int) or not 0 <= value <= 8:
            raise self.error
        self.__number = value

    def __bool__(self):
        return not self.is_open


class GamePole:
    def __new__(cls, *args):
        if not hasattr(cls, 'instance'):
            cls.n = args[0]
            cls.m = args[1]
            cls.total_mines = args[2]
            cls.instance = super(GamePole, cls).__new__(cls)
        return cls.instance

    def __init__(self, *args):
        self.__pole_cells = tuple(tuple(Cell() for _ in range(self.m)) for _ in range(self.n))

    @property
    def pole(self):
        return self.__pole_cells

    def init_pole(self):
        """Создает поле для игры"""
        self.__init__()
        self.__place_manes()
        self.__count_mines()

    def __place_manes(self):
        """Расставляет бомбы на поле"""
        mines = self.total_mines
        while mines:
            i, j = randint(0, self.n - 1), randint(0, self.m - 1)
            cell = self.pole[i][j]
            if not cell.is_mine:
                cell.is_mine = True
                mines -= 1
            else:
                continue

    def __count_mines(self):
        """Расставляет цифры на поле"""
        for i in range(self.n):
            for j in range(self.m):
                self.pole[i][j].number = self.__check_mines(i, j)

    def __check_mines(self, i, j):
        """Считает число мин вокруг одной клетки"""
        around_mines = 0
        for n in range(i - 1, i + 2):
            for m in range(j - 1, j + 2):
                if (n != i or m != j) and n >= 0 and m >= 0:
                    try:
                        around_mines += self.pole[n][m].is_mine
                    except IndexError:
                        continue
        return around_mines

    def open_cell(self, i, j):
        """Открывает клетку  на поле"""
        if not 0 <= i <= self.n - 1 or not 0 <= j <= self.m - 1:
            raise IndexError('некорректные индексы i, j клетки игрового поля')
        self.pole[i][j].is_open = True
        if self.pole[i][j].number == 0:
            self.__check_number(i, j)

    def __check_number(self, i, j):
        """Проверяет число в клетке.
        Если '0', то открывает все соседние клетки"""
        for n in range(i - 1, i + 2):
            for m in range(j - 1, j + 2):
                if (n != i or m != j) and n >= 0 and m >= 0:
                    try:
                        if not self.pole[n][m].is_open:
                            self.pole[n][m].is_open = True
                            if self.pole[n][m].number == 0:
                                self.__check_number(n, m)
                    except IndexError:
                        continue

    def show_pole(self):
        """Выводит поле в терминал"""
        for i in range(self.n):
            for j in range(self.m):
                cell = self.pole[i][j]
                if cell.flag:
                    point = emojize(':triangular_flag:')
                elif not cell.is_open:
                    point = emojize(':brown_square:')
                elif cell.is_mine:
                    point = emojize(':bomb:')
                else:
                    nums = {0: ':keycap_0:', 1: ':keycap_1:', 2: ':keycap_2:', 3: ':keycap_3:', 4: ':keycap_4:',
                            5: ':keycap_5:', 6: ':keycap_6:', 7: ':keycap_7:', 8: ':keycap_8:', 9: ':keycap_9:'}
                    point = emojize(nums[cell.number])
                print(point, end=' ')
            print()
        print()


s = GamePole(9, 9, 10)
s.init_pole()


def enter_coordinates():
    """Запрашивает координаты клетки у пользователя"""
    try:
        i, *j = input('Введите координаты клетки: ').split()
        if not all(1 <= x <= 9 for x in (int(i), int(j[0]))):
            raise TypeError('Некорректные координаты клетки')
        if len(j) == 2:  # Отмечает клетку флагом
            if j[1] == 'o':
                s.pole[int(i) - 1][int(j[0]) - 1].flag = True
            else:
                raise TypeError('Некорректный ввод')
        return int(i), int(j[0])
    except Exception as e:
        print(e)
        return enter_coordinates()


def game():
    """Запускает игру"""
    counter = 0
    while True:
        s.show_pole()
        i, j = enter_coordinates()
        cell = s.pole[i - 1][j - 1]
        if cell.flag:
            continue
        if not cell.is_open and not cell.flag:
            s.open_cell(i - 1, j - 1)
            counter += 1
        if cell.is_mine and not cell.flag:
            s.show_pole()
            print('Вы проиграли')
            break
        if counter == 71:
            print('Вы победили')
            s.show_pole()
            break


game()
