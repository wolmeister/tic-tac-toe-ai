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