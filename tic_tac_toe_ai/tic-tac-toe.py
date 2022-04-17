import numpy as np

class Player:
  def __init__(self, symbol: int) -> None:
    if symbol != 1 or symbol != -1:
      raise Exception('Symbol must be 1 or -1')

    self.symbol = symbol

class Board:
  def __init__(self, size: int) -> None:
    if size < 3:
      raise Exception('Size must be at least 3')
    if size % 2 == 0:
      raise Exception('Size must be odd')

    self.size = size;
    self.board = np.zeros((size, size))
    self.ended = False

  def winner(self) -> int:
    for i in range(self.size):
      # Column
      columnSum = sum(self.board[:, i])
      if columnSum == self.size:
        self.ended = True
        return 1
      elif columnSum == -self.size:
        self.ended = True
        return -1
      # Row
      rowSum = sum(self.board[i, :])
      if rowSum == self.size:
        self.ended = True
        return 1
      elif rowSum == -self.size:
        self.ended = True
        return -1

    # Diagonal
    boardArray = np.asarray(self.board)
    diagonalSum = np.trace(boardArray)
    antiDiagonalSum = np.trace(np.fliplr(boardArray))

    if max(abs(diagonalSum), abs(antiDiagonalSum)):
      self.ended = True
      if diagonalSum == 3 or antiDiagonalSum == 3:
        return 1
      return -1;

    # Draw
    if self.countAvailablePositions() == 0:
      self.ended = True
      return 0

    return None

  def countAvailablePositions(self) -> int:
    count = 0

    for i in range(self.size):
      for j in range(self.size):
        if self.board[i, j] == 0:
          count += 1

    return count

def start() -> None:
  board = Board(3)

class HumanPlayer:
    def __init__(self, stepSize = 0.1, exploreRate=0.1):
        self.symbol = None
        self.currentState = None
        return
    def reset(self):
        return
    def setSymbol(self, symbol):
        self.symbol = symbol
        return
    def feedState(self, state):
        self.currentState = state
        return
    def feedReward(self, reward):
        return
    def takeAction(self):
        data = int(input("Input your position:"))
        data -= 1
        i = data
        j = data
        if self.currentState.data[i, j] != 0:
            return self.takeAction()
        return (i, j, self.symbol)

def train(epochs=20000):
    player1 = Player()
    player2 = Player()
    judger = Judger(player1, player2)
    player1Win = 0.0
    player2Win = 0.0
    for i in range(0, epochs):
        print("Epoch", i)
        winner = judger.play()
        if winner == 1:
            player1Win += 1
        if winner == -1:
            player2Win += 1
        judger.reset()
    print(player1Win / epochs)
    print(player2Win / epochs)
    player1.savePolicy()
    player2.savePolicy()

def compete(turns=500):
    player1 = Player(exploreRate=0)
    player2 = Player(exploreRate=0)
    judger = Judger(player1, player2, False)
    player1.loadPolicy()
    player2.loadPolicy()
    player1Win = 0.0
    player2Win = 0.0
    for i in range(0, turns):
        print("Epoch", i)
        winner = judger.play()
        if winner == 1:
            player1Win += 1
        if winner == -1:
            player2Win += 1
        judger.reset()
    print(player1Win / turns)
    print(player2Win / turns)

def play():
    while True:
        player1 = Player(exploreRate=0)
        player2 = HumanPlayer()
        judger = Judger(player1, player2, False)
        player1.loadPolicy()
        winner = judger.play(True)
        if winner == player2.symbol:
            print("Win!")
        elif winner == player1.symbol:
            print("Lose!")
        else:
            print("Tie!")

# train()
# compete()
# play() 