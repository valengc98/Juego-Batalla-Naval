import random

#CREACIÓN DEL TABLERO
class Board:
    def __init__(self, size=10):
        self.size = size
        self.board = [["~" for _ in range(size)] for _ in range(size)]
    
    def print_board(self, hide_ships=False):
        for row in self.board:
            row_display = []
            for cell in row:
                if hide_ships and cell == "S":
                    row_display.append("~")
                else:
                    row_display.append(cell)
            print(" ".join(row_display))

    def place_ship(self, ship, col_ship, fil_ship, direction):
        positions = []
        if direction == "H":
            if col_ship + ship.size > self.size:
                return False
            for i in range(ship.size):
                positions.append((fil_ship, col_ship + i))
        elif direction == "V":
            if fil_ship + ship.size > self.size:
                return False
            for i in range(ship.size):
                positions.append((fil_ship + i, col_ship))
        else:
            return False
        
        for (fil, col) in positions:
            if self.board[fil][col] != "~":
                return False
        
        for (fil, col) in positions:
            self.board[fil][col] = "S"
        
        ship.positions = positions
        return True

#CREACIÓN DE LOS BARCOS
class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.positions = []
        self.hits = 0
    
    def hit(self):
        self.hits += 1
        return self.hits == self.size

#JUGADORES, POSICIÓN DE LOS BARCOS Y ATAQUE AL OPONENTE
class Player:
    def __init__(self, name):
        self.name = name
        self.ships = []
        self.board = Board()

    def place_ships(self):
        ships = [Ship("Destroyer", 2), Ship("Submarine", 3), Ship("Acorazado", 4)]
        for ship in ships:
            while True:
                print(f"{self.name}, coloca tu barco {ship.name} de tamaño {ship.size}")
                col_ship = int(input("Columna Inicial (0-9): "))
                fil_ship = int(input("Fila Inicial (0-9): "))
                direction = input("Dirección (H para horizontal, V para vertical): ").upper()
                if self.board.place_ship(ship, col_ship, fil_ship, direction):
                    self.ships.append(ship)
                    self.board.print_board()
                    break
                else:
                    print("Posición no válida. Inténtalo de nuevo.")

    def attack(self, opponent):
        while True:
            print(f"{self.name}, elige una posición para atacar.")
            fil = int(input("Fila (0-9): "))
            col = int(input("Columna (0-9): "))
            if 0 <= fil < self.board.size and 0 <= col < self.board.size:
                if opponent.board.board[fil][col] == '~':
                    print("Agua!")
                    opponent.board.board[fil][col] = 'A'
                    break
                elif opponent.board.board[fil][col] == 'S':
                    print("Impacto!")
                    opponent.board.board[fil][col] = 'X'
                    for ship in opponent.ships:
                        if (fil, col) in ship.positions:
                            if ship.hit():
                                print(f"¡Hundido! Has hundido el {ship.name}.")
                            break
                    break
                elif opponent.board.board[fil][col] in ['A', 'X']:
                    print("Ya has atacado esta posición. Intenta de nuevo.")
            else:
                print("Posición no válida. Intenta de nuevo.")
    
    def all_ships_sunk(self):
        return all(ship.hits == ship.size for ship in self.ships)

#JUEGO
class BattleshipGame:
    def __init__(self):
        self.player1 = Player("Jugador 1")
        self.player2 = Player("Jugador 2")

    def play(self):
        print("Bienvenido al juego de Batalla Naval!")
        print("Jugador 1 coloca sus barcos.")
        self.player1.place_ships()
        print("Jugador 2 coloca sus barcos.")
        self.player2.place_ships()

        current_player = self.player1
        opponent = self.player2

        while True:
            current_player.attack(opponent)
            if opponent.all_ships_sunk():
                print(f"¡{current_player.name} ha ganado el juego!")
                break
            current_player, opponent = opponent, current_player

#CREAR LA INSTANCIA DEL JUEGO
game = BattleshipGame()
game.play()
