from __future__ import annotations
from typing import Tuple
import numpy as np

class BoardState:
  def __init__(self, size: int) -> None:
    self.size = size
    self.data = np.zeros((self.size, self.size))
    self.winner = None
    self.hashValue = None
    self.finished = None
    
  def getHash(self) -> int:
    if self.hashValue is None:
      self.hashValue = 0;

      for i in self.data.reshape(self.size * self.size):
        if i == -1:
            i = 2
        self.hashValue = self.hashValue * self.size + i

    return int(self.hashValue)
  
  def hasFinished(self) -> bool:
    if self.finished is not None:
      return self.finished

    for i in range(self.size):
      # Column
      columnSum = sum(self.data[:, i])
      if columnSum == self.size:
        self.finished = True
        self.winner = 1
        return self.finished
      elif columnSum == -self.size:
        self.finished = True
        self.winner = -1
        return self.finished

      # Row
      rowSum = sum(self.data[i, :])
      if rowSum == self.size:
        self.finished = True
        self.winner = 1
        return self.finished
      elif rowSum == -self.size:
        self.finished = True
        self.winner = -1
        return self.finished

      # Diagonal
      boardArray = np.asarray(self.data)
      diagonalSum = np.trace(boardArray)
      antiDiagonalSum = np.trace(np.fliplr(boardArray))

      if max(abs(diagonalSum), abs(antiDiagonalSum)) == 3:
        if diagonalSum == 3 or antiDiagonalSum == 3:
          self.winner = 1
        else:
          self.winner = -1
        
        self.finished = True
        return self.finished

      # Draw
      if np.sum(np.abs(self.data)) == self.size * self.size:
        self.finished = True
        self.winner = 0
        return self.finished

    self.finished = False
    return self.finished

  def nextState(self, i: int, j: int, playerSymbol: int) -> BoardState:
    newState = BoardState(size=self.size)
    newState.data = np.copy(self.data)
    newState.data[i, j] = playerSymbol
    return newState
  
  def debug(self):
    for i in range(0, self.size):
        print('-------------')
        out = '| '
        for j in range(0, self.size):
            if self.data[i, j] == 1:
                token = '*'
            if self.data[i, j] == -1:
                token = 'x'
            if self.data[i, j] == 0:
                token = ' '
            out += token + ' | '
        print(out)
    print('-------------')

  @staticmethod
  def getAllStates(size: int) -> dict[int, Tuple[BoardState, bool]]:
    currentSymbol = 1
    currentState = BoardState(size=size)
    allStates = dict()
    allStates[currentState.getHash()] = (currentState, currentState.hasFinished())
    BoardState._getAllStatesRecursive(size, currentState, currentSymbol, allStates)
    return allStates

  @staticmethod
  def _getAllStatesRecursive(size: int, currentState: BoardState, currentSymbol: int, allStates: dict):
    for i in range(0, size):
      for j in range(0, size):
        if currentState.data[i][j] == 0:
          newState = currentState.nextState(i, j, currentSymbol)
          newHash = newState.getHash()

          if newHash not in allStates.keys():
            finished = newState.hasFinished()
            allStates[newHash] = (newState, finished)

            if not finished:
              BoardState._getAllStatesRecursive(size, newState, -currentSymbol, allStates)