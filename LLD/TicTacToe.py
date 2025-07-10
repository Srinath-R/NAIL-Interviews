from typing import List, Tuple

class Player:
    def __init__(self, name, marker):
        self.name = name
        self.marker = marker

class Board:
    def __init__(self, size=3):
        self.reset(size)

    def reset(self, size: int) -> None:
        self.size = size
        self.board = [[0 for y in range(size)] for x in range(size)]
        self.rowCounts = [{} for _ in range(size)]
        self.colCounts = [{} for _ in range(size)]
        self.diagCounts = [{} for _ in range(2)]
        self.remainingSquares = size * size

    def makeMove(self, player: Player, row: int, col: int) -> Tuple[bool, str]:
        if row >= self.size or col >= self.size or row < 0 or col < 0:
            raise ValueError("Not within boundary of the board!")
        elif self.board[row][col] != 0:
            raise ValueError("Move already made on this square! ")
        else:
            marker = player.marker
            self.board[row][col] = marker
            self.remainingSquares -= 1  # Decrement remaining squares

            self.rowCounts[row][marker] = self.rowCounts[row].get(marker, 0) + 1
            if self.rowCounts[row][marker] == self.size:
                return (True, f"Player {player.name} has won the game!")

            self.colCounts[col][marker] = self.colCounts[col].get(marker, 0) + 1
            if self.colCounts[col][marker] == self.size:
                return (True, f"Player {player.name} has won the game!")

            if row == col:
                self.diagCounts[0][marker] = self.diagCounts[0].get(marker, 0) + 1
                if self.diagCounts[0][marker] == self.size:
                    return (True, f"Player {player.name} has won the game!")

            if row + col == self.size - 1:
                self.diagCounts[1][marker] = self.diagCounts[1].get(marker, 0) + 1
                if self.diagCounts[1][marker] == self.size:
                    return (True, f"Player {player.name} has won the game!")

            if self.remainingSquares == 0:
                return (True, "The game is a draw!")

            return (False, "")

class Game:
    def __init__(self, players: List[Player], board: Board):
        self.players = players
        self.board = board

    def play(self) -> None:
        gameOver = False
        currTurn = 1
        numPlayers = len(self.players)
        while not gameOver:
            currPlayer = self.players[(currTurn - 1) % numPlayers]
            row, col = map(int, input(f"{currPlayer.name}, Enter your input(Like this 'row, column'):\n").split(","))
            state = self.board.makeMove(currPlayer, row, col)
            if state[0]:
                gameOver = True
                print(state[1])
                break
            else:
                currTurn += 1

n = int(input("Enter the number of players:\n"))
players = []
for i in range(n):
    player = Player(input(f"Enter your name, player #{i+1}:\n"), i+1)
    players.append(player)
board = Board(3)
game = Game(players, board)
game.play()


