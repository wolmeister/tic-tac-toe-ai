from tic_tac_toe_ai.board_state import BoardState
from tic_tac_toe_ai.context import Context
from tic_tac_toe_ai.player import Player


class Judger:
  def __init__(self, player1: Player, player2: Player, feedback = True) -> None:
    if player1.symbol == player2.symbol:
      raise Exception('Both players have the same symbol')

    self.player1 = player1
    self.player2 = player2
    self.currentPlayer = None
    self.feedback = feedback
    self.currentState = BoardState(Context.get().size)
    self.allStates = Context.get().allBoardStates

  def play(self, show = False):
    self.reset()
    self.feedCurrentState()

    while True:
      if self.currentPlayer == self.player1:
          self.currentPlayer = self.player2
      else:
          self.currentPlayer = self.player1

      if show:
        self.currentState.debug()

      [i, j, symbol] = self.currentPlayer.takeAction()
      self.currentState = self.currentState.nextState(i, j, symbol)
      hashValue = self.currentState.getHash()

      self.currentState, finished = self.allStates[hashValue]
      self.feedCurrentState()

      if finished:
        if self.feedback:
            self.giveReward()
        return self.currentState.winner

  def giveReward(self):
    if self.currentState.winner == self.player1.symbol:
      self.player1.feedReward(1)
      self.player2.feedReward(0)
    elif self.currentState.winner == self.player2.symbol:
      self.player1.feedReward(0)
      self.player2.feedReward(1)
    else:
      self.player1.feedReward(0.1)
      self.player2.feedReward(0.5)

  def feedCurrentState(self):
    self.player1.feedState(self.currentState)
    self.player2.feedState(self.currentState)

  def reset(self):
    self.player1.reset()
    self.player2.reset()
    self.currentState = BoardState(Context.get().size)
    self.currentPlayer = None