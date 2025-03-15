import math

class Board:
    def __init__(self, position) -> None:
        self.position: list[list[str]] = position

    def __str__(self):
        position = ""
        for row in self.position:
            position += "|"
            for cell in row:
                position += f"{cell}|"
            position += "\n"
        return position

    @classmethod
    def new(cls):
        return cls(position=[
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]])

    @property
    def empty_cells(self) -> list[tuple[int, int]]:
        return [
            (y, x)
            for (y, row) in enumerate(iterable=self.position)
            for (x, cell) in enumerate(iterable=row)
            if cell == " "]

    def is_won(self, player) -> bool:
        # SIZE = 3 puis remplacer tous les 3 par la variable
        # Vérification des lignes et des colonnes
        for row in range(3):
            if all(self.position[row][col] == player for col in range(3)):  # Lignes
                return True
            if all(self.position[col][row] == player for col in range(3)):  # Colonnes
                return True
        # Vérification des diagonales
        if all(self.position[i][i] == player for i in range(3)):  # Diagonale principale
            return True
        if all(self.position[i][2 - i] == player for i in range(3)):  # Diagonale secondaire
            return True
        return False

        # Si vous avez besoin d'un commentaire c'est que le code n'est pas assez "humain":
        row_win = all(self.position[row][col] == player for col in range(3))
        col_win = all(self.position[col][row] == player for col in range(3))
        principal_diagonal_win = all(self.position[i][i] == player for i in range(3))
        secondary_diagonal_win = all(self.position[i][2 - i] == player for i in range(3))

        return any(row_win, col_win, principal_diagonal_win, secondary_diagonal_win)

        # Etant donné que la fonction any() retournera True dès qu'une des conditions est validée,
        # on peut avoir envie d'en faire des fonctions afin de ne pas recalculer les 4 à chaque fois
        def row_win():
            return all(self.position[row][col] == player for col in range(3))
        ...
        return any(row_win(), col_win(), principal_diagonal_win(), secondary_diagonal_win())
        """Ici si row_win() return True, python ne cherchera pas à savoir si col_win() etc valent True ou pas,
        étant donné que any() aura déjà 1 element de True il ne regardera pas la valeur des autres. Encore une
        fois la performance ne devrait pas être un problème surtout pour si peu, le but est surtout d'éviter le
        commentaire en le remplacant par du code plus "humain" qui permet de comprendre sans se poser de question."""


    def play_turn(self, player, pos_y, pos_x):
        if self.position[pos_y][pos_x] != " ":
            raise ValueError("Already taken")
        self.position[pos_y][pos_x] = player
        print(self)
        if self.is_won(player=player):
            print(f"{player} won!")
            return True
        if not self.empty_cells:
            print("Draw!")
            return True
        return False

    def get_score(self, is_maximizing) -> int:
        if self.is_won("O"):
            return 1
        if self.is_won("X"):
            return -1
        if not self.empty_cells:
            return 0

        if is_maximizing:
            best_score = -math.inf
            for (y, x) in self.empty_cells:
                self.position[y][x] = "O"
                score = self.get_score(is_maximizing=False)
                self.position[y][x] = " "
                best_score = max(score, best_score)
            return best_score

        best_score = math.inf
        for (y, x) in self.empty_cells:
            self.position[y][x] = "X"
            score = self.get_score(is_maximizing=True)
            self.position[y][x] = " "
            best_score = min(score, best_score)
        return best_score

    def best_move(self) -> tuple[int, int]:
        best_score = -math.inf
        move = None
        for y, x in self.empty_cells:
            self.position[y][x] = "O"
            score = self.get_score(is_maximizing=False)
            self.position[y][x] = " "
            if score > best_score:
                best_score = score
                move = (y, x)
        return move
