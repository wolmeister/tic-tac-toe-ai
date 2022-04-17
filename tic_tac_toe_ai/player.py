import pickle
from typing import Tuple

import numpy as np
from tic_tac_toe_ai.board_state import BoardState
from tic_tac_toe_ai.context import Context

class Player:
  def __init__(self, symbol: int, stepSize = 0.1, exploreRate = 0.1) -> None:
    if symbol != 1 and symbol != -1:
      raise Exception('Symbol must be 1 or -1')

    self.symbol = symbol
    self.stepSize = stepSize
    self.exploreRate = exploreRate
    self.states = []
    self.estimations = dict()

    # Init estimations
    allStates = Context.get().allBoardStates
    for hash in allStates.keys():
      (state, finished) = allStates[hash]
      if finished:
          if state.winner == self.symbol:
              self.estimations[hash] = 1.0
          else:
              self.estimations[hash] = 0
      else:
          self.estimations[hash] = 0.5

  def reset(self):
    self.states = []

  def feedState(self, state: BoardState):
    self.states.append(state)

  def feedReward(self, reward: float):
    if len(self.states) == 0:
        return

    stateHashes = [state.getHash() for state in self.states]
    target = reward
    
    for latestState in reversed(stateHashes):
        value = self.estimations[latestState] + self.stepSize * (target - self.estimations[latestState])
        self.estimations[latestState] = value
        target = value

    self.states = []

  def takeAction(self) -> Tuple[int, int, int]:
    state = self.states[-1]
    nextStates: list[int] = []
    nextPositions: list[Tuple[int, int]] = []

    for i in range(3):
      for j in range(3):
        if state.data[i, j] == 0:
          nextPositions.append([i, j])
          nextStates.append(state.nextState(i, j, self.symbol).getHash())

    if np.random.binomial(1, self.exploreRate):
      np.random.shuffle(nextPositions)
      self.states = []
      action = nextPositions[0]
      action.append(self.symbol)
      return action

    values: list[Tuple[float, int, int]] = []
    for hash, pos in zip(nextStates, nextPositions):
      values.append((self.estimations[hash], pos[0], pos[1]))

    np.random.shuffle(values)
    values.sort(key=lambda x: x[0], reverse = True)
    action = [values[0][1], values[0][2], self.symbol]

    return action

  def savePolicy(self):
    size = Context.get().size
    fw = open(f"optimal_policy_size_{size}_{self.symbol}", 'wb')
    pickle.dump(self.estimations, fw)
    fw.close()

  def loadPolicy(self):
    size = Context.get().size
    fr = open(f"optimal_policy_size_{size}_{self.symbol}", 'rb')
    self.estimations = pickle.load(fr)
    fr.close()