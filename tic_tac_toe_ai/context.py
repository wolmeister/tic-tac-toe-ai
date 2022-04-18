from __future__ import annotations
from tic_tac_toe_ai.board_state import BoardState

class Context:
  _instance: Context

  def __init__(self, size: int, player1FeedReward = 0.1, player2FeedReward = 0.5, player1ExploreRate = 0.1, player2ExploreRate = 0.1) -> None:
    if size < 3:
      raise Exception('Size must be at least 3')
    if size % 2 == 0:
      raise Exception('Size must be odd')
      
    self.size = size
    self.player1FeedReward = player1FeedReward
    self.player2FeedReward = player2FeedReward
    self.player1ExploreRate = player1ExploreRate
    self.player2ExploreRate = player2ExploreRate
    self.allBoardStates = BoardState.getAllStates(size=size)

  @staticmethod
  def get() -> Context:
    return Context._instance;

  @staticmethod
  def set(context: Context):
    Context._instance = context