from util import manhattanDistance

from game import Directions
import random, util

from game import Agent
from heapq import *

INF = 10 ** 9


## Example Agent
class ReflexAgent(Agent):

    def Action(self, gameState):
        move_candidate = gameState.getLegalActions()

        scores = [self.reflex_agent_evaluationFunc(gameState, action) for action in move_candidate]
        bestScore = max(scores)
        Index = [index for index in range(len(scores)) if scores[index] == bestScore]
        get_index = random.choice(Index)

        return move_candidate[get_index]

    def reflex_agent_evaluationFunc(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        return successorGameState.getScore()


def scoreEvalFunc(currentGameState):
    return currentGameState.getScore()


class AdversialSearchAgent(Agent):

    def __init__(self, getFunc='scoreEvalFunc', depth='2'):
        self.index = 0
        self.evaluationFunction = util.lookup(getFunc, globals())

        self.depth = int(depth)


class MinimaxAgent(AdversialSearchAgent):
    """
      [문제 01] MiniMax의 Action을 구현하시오. (20점)
      (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
    """

    def Action(self, gameState):
        ####################### Write Your Code Here ################################
        def minimax_handler(state, agent_idx, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            if agent_idx == 0:  # pacman
                return max_player(state, agent_idx, depth)
            else:  # ghost
                return min_player(state, agent_idx, depth)

        def max_player(state, agent_idx, depth):
            mxv = - INF
            for action in state.getLegalActions(agent_idx):
                nxt_state = state.generateSuccessor(agent_idx, action)
                mxv = max(mxv, minimax_handler(nxt_state, agent_idx + 1, depth))
            return mxv

        def min_player(state, agent_idx, depth):
            """
            if next agent is pacman, reset depth and agent
            else agent to next ghost
            """
            if agent_idx == self.numAgents - 1:  # ghost 끝남 -> 다시 pacman
                nxt_agent = 0
                depth += 1
            else:  # next ghost
                nxt_agent = agent_idx + 1

            mnv = INF
            for action in state.getLegalActions(agent_idx):
                nxt_state = state.generateSuccessor(agent_idx, action)
                mnv = min(mnv, minimax_handler(nxt_state, nxt_agent, depth))
            return mnv

        self.agent_idx = self.index
        self.numAgents = gameState.getNumAgents()
        self.legalMoves = gameState.getLegalActions(self.index)

        self.agent_idx += 1

        pq = list()
        init_depth = 0
        for idx, action in enumerate(self.legalMoves):
            nxt_state = gameState.generateSuccessor(self.index, action)
            cur_value = minimax_handler(nxt_state, self.agent_idx, init_depth)
            heappush(pq, (-cur_value, idx))

        _, action_idx = heappop(pq)
        return self.legalMoves[action_idx]

        ############################################################################


class AlphaBetaAgent(AdversialSearchAgent):
    """
      [문제 02] AlphaBeta의 Action을 구현하시오. (25점)
      (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
    """

    def Action(self, gameState):
        ####################### Write Your Code Here ################################
        def alphabeta_handler(state, depth, agent_index, alpha=-INF, beta=INF):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            if agent_index == 0:  # pacman
                return max_player(state, depth, agent_index, alpha, beta)
            else:
                return min_player(state, depth, agent_index, alpha, beta)

        def max_player(state, depth, agent_index, alpha=-INF, beta=INF):
            mxv = - INF
            for action in state.getLegalActions(agent_index):
                nxt_state = state.generateSuccessor(agent_index, action)
                mxv = max(mxv, alphabeta_handler(nxt_state, depth, agent_index + 1, alpha, beta))
                if mxv > beta:
                    return mxv
                alpha = max(alpha, mxv)
            return mxv

        def min_player(state, depth, agent_index, alpha=-INF, beta=INF):
            if agent_index == self.numAgents - 1:
                nxt_agent = 0
                depth += 1
            else:
                nxt_agent = agent_index + 1

            mnv = INF
            for action in state.getLegalActions(agent_index):
                nxt_state = state.generateSuccessor(agent_index, action)
                mnv = min(mnv, alphabeta_handler(nxt_state, depth, nxt_agent, alpha, beta))
                if mnv < alpha:
                    return mnv
                beta = min(beta, mnv)
            return mnv


        self.agent_idx = self.index
        self.numAgents = gameState.getNumAgents()
        self.legalMoves = gameState.getLegalActions(self.index)

        self.alpha = -INF
        self.beta = INF
        self.agent_idx += 1

        pq = list()
        cur_value = - INF
        for idx, action in enumerate(self.legalMoves):
            nxt_state = gameState.generateSuccessor(self.index, action)
            nxt_value = alphabeta_handler(nxt_state, 0, 1, self.alpha, self.beta)
            if nxt_value > cur_value:
                cur_value = nxt_value
            self.alpha = max(self.alpha, cur_value)
            heappush(pq, (-cur_value, idx))
        _, action_idx = heappop(pq)

        return self.legalMoves[action_idx]

        ############################################################################


class ExpectimaxAgent(AdversialSearchAgent):
    """
      [문제 03] Expectimax의 Action을 구현하시오. (25점)
      (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
    """


    def Action(self, gameState):
        ####################### Write Your Code Here ################################

        def expectimax_handler(state, agent, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            if agent == 0:  # pacman
                return max_player(state, agent, depth)
            else:
                return exp_player(state, agent, depth)

        def max_player(state, agent, depth):
            maxVal = - INF
            for action in state.getLegalActions(agent):
                nxt_state = state.generateSuccessor(agent, action)
                maxVal = max(maxVal, expectimax_handler(nxt_state, agent + 1, depth))
            return maxVal

        def exp_player(state, agent, depth):
            if agent == self.numAgents - 1:  # ghost 끝남 -> 다시 pacman
                nxt_agent = 0
                depth += 1
            else:  # next ghost
                nxt_agent = agent + 1

            exp_val = 0
            for action in state.getLegalActions(agent):
                nxt_state = state.generateSuccessor(agent, action)
                p = 1 / len(state.getLegalActions(agent))
                exp_val += p * expectimax_handler(nxt_state, nxt_agent, depth)
            return exp_val

        # set self.agent to refer to ghost
        self.agent = self.index
        self.depthCount = 0
        self.numAgents = gameState.getNumAgents()
        self.legalMoves = gameState.getLegalActions(self.index)

        self.agent += 1
        pq = list()
        for idx, action in enumerate(self.legalMoves):
            nxt_state = gameState.generateSuccessor(self.index, action)
            cur_value = expectimax_handler(nxt_state, self.agent, self.depthCount)
            heappush(pq, (-cur_value, idx))

        action_idx = heappop(pq)
        return self.legalMoves[action_idx]

        # raise Exception("Not implemented yet")

        ############################################################################
