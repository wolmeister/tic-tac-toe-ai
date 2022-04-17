from __future__ import annotations

from tic_tac_toe_ai.player import AIPlayer, HumanPlayer
from tic_tac_toe_ai.context import Context
from tic_tac_toe_ai.judger import Judger

def train(epochs=20000):
  player1 = AIPlayer(1)
  player2 = AIPlayer(-1)
  judger = Judger(player1, player2)
  player1Wins = 0.0
  player2Wins = 0.0

  print("Training...")

  for i in range(0, epochs):
    winner = judger.play()

    if winner == 1:
        player1Wins += 1
    if winner == -1:
        player2Wins += 1

    judger.reset()

  player1.savePolicy()
  player2.savePolicy()

  print(f"Player 1 winrate = {player1Wins / epochs}")
  print(f"Player 2 winrate = {player2Wins / epochs}")

def compete(turns=500):
    player1 = AIPlayer(1, exploreRate=0)
    player2 = AIPlayer(-1, exploreRate=0)
    judger = Judger(player1, player2)

    player1.loadPolicy()
    player2.loadPolicy()
    player1Wins = 0.0
    player2Wins = 0.0

    print("Competing...")

    for i in range(0, turns):
      winner = judger.play()
      if winner == 1:
          player1Wins += 1
      if winner == -1:
          player2Wins += 1
      judger.reset()

    print(f"Player 1 winrate = {player1Wins / turns}")
    print(f"Player 2 winrate = {player2Wins / turns}")

def play():
    while True:
        player1 = AIPlayer(1, exploreRate=0)
        player2 = HumanPlayer(-1) 

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
  size = int(input("What's the board size? (minimum 3): "))
  Context.set(Context(size=size))

  shouldTrain = input("Do you want to train the AI? (y/n): ").lower() == 'y'
  if shouldTrain == True:
    train()
  
  shouldCompete = input("Do you want to test the AI? (y/n): ").lower() == 'y'
  if shouldCompete == True:
    compete()

  shouldPlay = input("Do you want to play against the AI? (y/n): ").lower() == 'y'
  if shouldPlay == True:
    play()
