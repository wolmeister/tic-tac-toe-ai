from __future__ import annotations
import numpy as np

from tic_tac_toe_ai import Player
from tic_tac_toe_ai.context import Context
from tic_tac_toe_ai.judger import Judger

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
  