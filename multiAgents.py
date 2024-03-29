# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        bigNum = 999999999999999999999
        "*** YOUR CODE HERE ***"
        if successorGameState.isWin():
          return bigNum

        # powerup = currentGameState.getCapsules()

        ghostList = currentGameState.getGhostPositions()
        closestGhostDist = 200
        closestGhost = (-99,-99)
        # print newGhostStates[0]
        for ghost in ghostList:
          spookDist = util.manhattanDistance(ghost,newPos)
          if spookDist < closestGhostDist:
            closestGhostDist = spookDist
            closestGhost = ghost

        # print newScaredTimes
        if(newScaredTimes[0]==0):
          score = successorGameState.getScore() + max(util.manhattanDistance(closestGhost,newPos),2)
        else:
          score = successorGameState.getScore()


        for ghost in successorGameState.getGhostPositions():
          # print ghost
          if successorGameState.getPacmanPosition() == ghost:
             score-=8000


        powerup = currentGameState.getCapsules()
        # print(powerup)
        closestCapDist = 200
        closestCap = (-99,-99)
        for cap in powerup:
          capDist = util.manhattanDistance(cap,newPos)
          if capDist < closestCapDist:
            closestCap = cap

        if successorGameState.getPacmanPosition() in powerup:
           score+=400
        if(len(currentGameState.getCapsules()) > len(successorGameState.getCapsules())):
          score+=400


        dotList = newFood.asList()
        closestDot = 200
        for dot in dotList:
          dotDist = util.manhattanDistance(dot,newPos)
          if dotDist < closestDot:
            closestDot = dot

        if(currentGameState.getNumFood() > successorGameState.getNumFood()):
          score+=200
        if action == Directions.STOP:
          score-=2

        if len(powerup)<1:
          score -= 2*util.manhattanDistance(closestDot,newPos)
        else:
          score -= 2*util.manhattanDistance(closestDot,newPos) + 3*util.manhattanDistance(closestCap,newPos)
        
        return score


        # return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
#_________________________________________________________________________________________________________________________
        def minimize(player, ghosts, currentState, depth):
          mini = float("inf")

          if currentState.isLose() or currentState.isWin() or depth ==0:
            return self.evaluationFunction(currentState)

          for choice in currentState.getLegalActions(player):
            if player < ghosts:
                mini = min(mini, minimize(player+1, ghosts, currentState.generateSuccessor(player,choice),depth))
            else:
                mini = min(mini, maximize(0,ghosts,currentState.generateSuccessor(player,choice),depth-1 ))

          return mini
#_________________________________________________________________________________________________________________________
        def maximize(player, ghosts, currentState, depth):
          maxi = -(float("inf"))

          if currentState.isLose() or currentState.isWin() or depth ==0:
            return self.evaluationFunction(currentState)

          for choice in currentState.getLegalActions(player):
            maxi = max(maxi, minimize(1,ghosts,currentState.generateSuccessor(player,choice),depth))

          return maxi
#_________________________________________________________________________________________________________________________
        
        currentEffort = -(float("inf"))
        chosenDirection = Directions.LEFT

        for choice in gameState.getLegalActions():
          destination = gameState.generateSuccessor(0,choice)
          oldEffort = currentEffort
          currentEffort = max(currentEffort, minimize(1,gameState.getNumAgents()-1,destination,self.depth))
          if currentEffort > oldEffort:
            chosenDirection = choice
          
        return chosenDirection
#_________________________________________________________________________________________________________________________
        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
#_________________________________________________________________________________________________________________________
        def minimize(player, ghosts, currentState, depth,alpha,beta):
          mini = float("inf")

          if currentState.isLose() or currentState.isWin() or depth ==0:
            return self.evaluationFunction(currentState)

          for choice in currentState.getLegalActions(player):
            if player < ghosts:
                mini = min(mini, minimize(player+1, ghosts, currentState.generateSuccessor(player,choice),depth,alpha,beta))
            else:
                mini = min(mini, maximize(0,ghosts,currentState.generateSuccessor(player,choice),depth-1,alpha,beta))
           
            if mini < alpha:
              return mini
            beta = min(beta,mini)
          return mini
#_________________________________________________________________________________________________________________________
        def maximize(player, ghosts, currentState, depth,alpha,beta):
          maxi = -(float("inf"))

          if currentState.isLose() or currentState.isWin() or depth ==0:
            return self.evaluationFunction(currentState)

          for choice in currentState.getLegalActions(player):
            maxi = max(maxi, minimize(1,ghosts,currentState.generateSuccessor(player,choice),depth,alpha,beta))
            if maxi > beta:
              return maxi
            alpha = max(alpha, maxi)
          return maxi
#_________________________________________________________________________________________________________________________
        
        currentEffort =       -(float("inf"))
        alpha =               -(float("inf"))
        beta =                 (float("inf"))
        chosenDirection = Directions.LEFT

        for choice in gameState.getLegalActions():
          destination = gameState.generateSuccessor(0,choice)
          oldEffort = currentEffort
          currentEffort = max(currentEffort, minimize(1,gameState.getNumAgents()-1,destination,self.depth,alpha,beta))
          if currentEffort > oldEffort:
            chosenDirection = choice
          if currentEffort >= beta:
            return chosenDirection
          alpha = max(alpha,currentEffort)
        return chosenDirection
#_________________________________________________________________________________________________________________________
 
        # util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
#_________________________________________________________________________________________________________________________
        def expectimize(player, ghosts, currentState, depth):
          expect = 0

          if currentState.isLose() or currentState.isWin() or depth ==0:
            return self.evaluationFunction(currentState)

          for choice in currentState.getLegalActions(player):
            if player < ghosts:
                expect += expectimize(player+1, ghosts, currentState.generateSuccessor(player,choice),depth)
            else:
                expect += maximize(0,ghosts,currentState.generateSuccessor(player,choice),depth-1 )

          return (expect / len(currentState.getLegalActions(player)))
#_________________________________________________________________________________________________________________________
        def maximize(player, ghosts, currentState, depth):
          maxi = -(float("inf"))

          if currentState.isLose() or currentState.isWin() or depth ==0:
            return self.evaluationFunction(currentState)

          for choice in currentState.getLegalActions(player):
            maxi = max(maxi, expectimize(1,ghosts,currentState.generateSuccessor(player,choice),depth))

          return maxi
#_________________________________________________________________________________________________________________________
        
        currentEffort = -(float("inf"))
        chosenDirection = Directions.LEFT

        for choice in gameState.getLegalActions():
          destination = gameState.generateSuccessor(0,choice)
          oldEffort = currentEffort
          currentEffort = max(currentEffort, expectimize(1,gameState.getNumAgents()-1,destination,self.depth))
          if currentEffort > oldEffort:
            chosenDirection = choice
          
        return chosenDirection
#_________________________________________________________________________________________________________________________
        # util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: My previous evaluation function didn't seem to work.  Pacman makes some very studid choices, I think because we
      now lack the chosen "action" that we had in the previous evaluation function.  I made sure to give points for winning and losing. 
      I also wanted to award points for being away from the ghosts, eating food, and eating powerups. 
    """

    # Useful information you can extract from a GameState (pacman.py)
    # successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    bigNum = 999999999999999999999
    
    if currentGameState.isWin():
      return bigNum
    if currentGameState.isLose():
      return -bigNum

    score = scoreEvaluationFunction(currentGameState)

    ghostList = currentGameState.getGhostPositions()
    closestGhostDist = 200
    closestGhost = (-99,-99)

    for ghost in ghostList:
      spookDist = util.manhattanDistance(ghost,newPos)
      if spookDist < closestGhostDist:
        closestGhostDist = spookDist
        closestGhost = ghost

    if(newScaredTimes[0]==0):
      score += max(util.manhattanDistance(closestGhost,newPos),4)

    powerup = currentGameState.getCapsules()
    dotList = newFood.asList()

    score-= len(dotList)
    score-= len(powerup)

    
    return score
    # util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

