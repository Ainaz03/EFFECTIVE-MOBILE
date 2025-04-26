import random

class Cell:
    def __init__(self, around_mines=0, mine=False):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False


class GamePole:
    def __init__(self, N, M):
        self.N = N  # размер поля
        self.M = M  # количество мин
        self.pole = [[Cell() for c in range(N)] for c in range(N)]
        self.init()

    def init(self):
        # Сброс поля
        for row in self.pole:
            for cell in row:
                cell.mine = False
                cell.around_mines = 0
                cell.fl_open = False

        # Установка M мин
        all_coords = [(i, j) for i in range(self.N) for j in range(self.N)]
        mine_coords = random.sample(all_coords, self.M)

        for i, j in mine_coords:
            self.pole[i][j].mine = True

        # Подсчёт мин вокруг каждой клетки
        for i in range(self.N):
            for j in range(self.N):
                if self.pole[i][j].mine:
                    continue
                count = 0
                for x in range(max(0, i-1), min(self.N, i+2)):
                    for y in range(max(0, j-1), min(self.N, j+2)):
                        if self.pole[x][y].mine:
                            count += 1
                self.pole[i][j].around_mines = count

    def show(self):
        for i in range(self.N):
            row_repr = []
            for j in range(self.N):
                cell = self.pole[i][j]
                if not cell.fl_open:
                    row_repr.append('#')
                elif cell.mine:
                    row_repr.append('*')
                else:
                    row_repr.append(str(cell.around_mines))
            print(' '.join(row_repr))

pole_game = GamePole(10, 12)
pole_game.show()
print(" ")
pole_game.pole[3][6].fl_open = True
pole_game.show()
print(" ")
pole_game.pole[6][4].fl_open = True
pole_game.show()