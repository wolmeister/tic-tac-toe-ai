from __future__ import annotations
from itertools import product

from numpy import double

from tic_tac_toe_ai.player import AIPlayer, HumanPlayer
from tic_tac_toe_ai.context import Context
from tic_tac_toe_ai.judger import Judger

def train(epochs=20000):
  player1 = AIPlayer(1, 0.1, Context.get().player1ExploreRate)
  player2 = AIPlayer(-1, 0.1, Context.get().player2ExploreRate)
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
    shouldChangeParameters = input("Do you want to change the AI parameters? (y/n): ").lower() == 'y'
    if shouldChangeParameters == True:
      player1FeedReward = double(input("What's the player 1 feed reward for draw? (0-1): "))
      player2FeedReward = double(input("What's the player 2 feed reward for draw? (0-1): "))
      player1ExploreRate = double(input("What's the player 1 explore rate? (0-1): "))
      player2ExploreRate = double(input("What's the player 2 explore rate? (0-1): "))

      Context.get().player1FeedReward = player1FeedReward
      Context.get().player2FeedReward = player2FeedReward
      Context.get().player1ExploreRate = player1ExploreRate
      Context.get().player2ExploreRate = player2ExploreRate

    train()
  
  shouldCompete = input("Do you want to test the AI? (y/n): ").lower() == 'y'
  if shouldCompete == True:
    compete()

  shouldPlay = input("Do you want to play against the AI? (y/n): ").lower() == 'y'
  if shouldPlay == True:
    play()
