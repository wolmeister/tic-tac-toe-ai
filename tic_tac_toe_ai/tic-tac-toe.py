from __future__ import annotations
import numpy as np

from tic_tac_toe_ai import Player
from tic_tac_toe_ai.context import Context
from tic_tac_toe_ai.judger import Judger

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
        i = int(input("Input your top position:")) - 1
        j = int(input("Input your left position:")) - 1 
        if self.currentState.data[i, j] != 0:
            return self.takeAction()
        return (i, j, self.symbol)

def train(epochs=20000):
  player1 = Player(1)
  player2 = Player(-1)
  judger = Judger(player1, player2)
  player1Win = 0.0
  player2Win = 0.0

  for i in range(0, epochs):
    # print("Epoch", i)
    winner = judger.play()

    if winner == 1:
        player1Win += 1
    if winner == -1:
        player2Win += 1

    judger.reset()

  player1.savePolicy()
  player2.savePolicy()

  print(f"Player 1 winrate = {player1Win / epochs}")
  print(f"Player 2 winrate = {player2Win / epochs}")

def compete(turns=500):
    player1 = Player(1, exploreRate=0)
    player2 = Player(-1, exploreRate=0)
    judger = Judger(player1, player2)

    player1.loadPolicy()
    player2.loadPolicy()
    player1Win = 0.0
    player2Win = 0.0

    for i in range(0, turns):
      # print("Turn", i)
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
        player1 = Player(1, exploreRate=0)
        player2 = HumanPlayer() 
        player2.setSymbol(-1)

        judger = Judger(player1, player2)
        player1.loadPolicy()

        winner = judger.play(True)
        if winner == player2.symbol:
            print("Win!")
        elif winner == player1.symbol:
            print("Lose!")
        else:
            print("Tie!")

def start():
  Context.set(Context(size=3))

  # train()
  # compete()
  play() 
  