## Project2:Multi-Agent Search
Project2要求实现多智能体对抗的Minimax算法(包含α-β剪枝),Expectimax算法,并尝试设计Evaluation Functions

### Q1：Reflex Agent
这一问我是做的有点懵逼，怎么写evaluationFunction的表达式基本上靠蒙，感觉跟运气关系比较大。evaluationFunction的设计原则就是：离food近/离ghost远/离scared ghost近-->高score<br>
在这个想法下慢慢试，也借鉴了网上一些前辈的想法。<br>
最终我的evaluationFunction如下：
```python
    def evaluationFunction(self, currentGameState: GameState, action):
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()
        foodPos = newFood.asList()
        for food in foodPos:
            score += 1 / (manhattanDistance(newPos, food) + 1)  # Encourage eating food

        for i, ghostState in enumerate(newGhostStates):
            ghostPos = ghostState.getPosition()
            ghost_distance = util.manhattanDistance(newPos, ghostPos)
            if newScaredTimes[i] > 0:
                # Ghost is scared, it's good to be close
                score += 1 / (ghost_distance + 1) # Encourage being close to scared ghosts
            else:
                if ghost_distance < 2: # min_distance
                    score -= 100  # Big penalty for being too close
                else:
                    score -= 1 / (ghost_distance + 1) # Encourage staying away from ghosts
        return score
```
运行结果也是非常好，Q1十次测试中最第一次分数是1094.

### Q2：Minimax
代码如下：
```python
class MinimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState: GameState):
        "*** YOUR CODE HERE ***"
        def terminate(state, depth):
            # Check if the game is over or if we have reached the maximum depth.
            return state.isWin() or state.isLose() or depth == self.depth   
        
        def min_value(state, depth, agentIndex):
            if terminate(state, depth):
                return self.evaluationFunction(state)
            min_val = float('inf')
            for action in state.getLegalActions(agentIndex):
                successor = state.generateSuccessor(agentIndex, action)
                if agentIndex == gameState.getNumAgents() - 1:
                    # If it's the last ghost, we go to the next depth level
                    min_val = min(min_val, max_value(successor, depth + 1))
                else:
                    # If it's not the last ghost, we stay at the same depth
                    min_val = min(min_val, min_value(successor, depth, agentIndex + 1)) 
            return min_val
        
        def max_value(state, depth):
            if terminate(state, depth):
                return self.evaluationFunction(state)
            max_val = float('-inf')
            for action in state.getLegalActions(0):
                successor = state.generateSuccessor(0, action)
                max_val = max(max_val, min_value(successor, depth, 1))
            return max_val
        
        def minimax(state):
            maxi = -float('inf')
            best_action = None
            for action in state.getLegalActions(0):
                successor = state.generateSuccessor(0, action)
                value = min_value(successor, 0, 1)
                if value > maxi:
                    maxi = value
                    best_action = action
            return best_action
        
        return minimax(gameState)
        util.raiseNotDefined()
```

### Q3:Alpha-Beta Pruning
在minmax的基础上进行修改：
```python
class AlphaBetaAgent(MultiAgentSearchAgent):
    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def terminate(state, depth):
            # Check if the game is over or if we have reached the maximum depth.
            return state.isWin() or state.isLose() or depth == self.depth   
        
        def min_value(state, depth, agentIndex, A, B):
            if terminate(state, depth):
                return self.evaluationFunction(state)
            min_val = float('inf')
            for action in state.getLegalActions(agentIndex):
                successor = state.generateSuccessor(agentIndex, action)
                if agentIndex == gameState.getNumAgents() - 1:
                    # If it's the last ghost, we go to the next depth level
                    min_val = min(min_val, max_value(successor, depth + 1, A , B))
                else:
                    # If it's not the last ghost, we stay at the same depth
                    min_val = min(min_val, min_value(successor, depth, agentIndex + 1, A , B))
                if min_val < A:
                    return min_val
                B = min(B, min_val)
            return min_val
        
        def max_value(state, depth,A, B):
            if terminate(state, depth):
                return self.evaluationFunction(state)
            max_val = float('-inf')
            for action in state.getLegalActions(0):
                successor = state.generateSuccessor(0, action)
                max_val = max(max_val, min_value(successor, depth, 1, A, B))
                if max_val > B:
                    return max_val
                A = max(A, max_val)
            return max_val
        
        def alpha_beta_search(state):
            best_action = None
            A = float('-inf')
            B = float('inf')
            for action in state.getLegalActions(0):
                successor = state.generateSuccessor(0, action)
                value = min_value(successor, 0, 1, A, B)
                if value > A:
                    A = value
                    best_action = action
            return best_action
        return alpha_beta_search(gameState)
        util.raiseNotDefined()
```

### Q4:Expectimax
仍然是在minimax的基础上进行修改，只要把min_vlaue改成exp_value就可以了。<br>
代码如下：
```python
class ExpectimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState: GameState):
        "*** YOUR CODE HERE ***"
        def terminate(state, depth):
            # Check if the game is over or if we have reached the maximum depth.
            return state.isWin() or state.isLose() or depth == self.depth   
        
        def exp_value(state, depth, agentIndex):
            if terminate(state, depth):
                return self.evaluationFunction(state)
            min_val = 0
            for action in state.getLegalActions(agentIndex):
                successor = state.generateSuccessor(agentIndex, action)
                if agentIndex == gameState.getNumAgents() - 1:
                    # If it's the last ghost, we go to the next depth level
                    min_val += max_value(successor, depth + 1) / len(state.getLegalActions(agentIndex))
                else:
                    # If it's not the last ghost, we stay at the same depth
                    min_val += exp_value(successor, depth, agentIndex + 1) / len(state.getLegalActions(agentIndex))

            return min_val
        
        def max_value(state, depth):
            if terminate(state, depth):
                return self.evaluationFunction(state)
            max_val = float('-inf')
            for action in state.getLegalActions(0):
                successor = state.generateSuccessor(0, action)
                max_val = max(max_val, exp_value(successor, depth, 1))
            return max_val
        
        def expectimax(state):
            maxi = -float('inf')
            best_action = None
            for action in state.getLegalActions(0):
                successor = state.generateSuccessor(0, action)
                value = exp_value(successor, 0, 1)
                if value > maxi:
                    maxi = value
                    best_action = action
            return best_action
        
        return expectimax(gameState)
        util.raiseNotDefined()
```

### Q5:Evaluation Function
发现直接用Q1里面写的Evaluation Function就能拿满Q6的分，只要改成评估currentGameState就行了：
```python
def betterEvaluationFunction(currentGameState: GameState):
    "*** YOUR CODE HERE ***"
    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]

    score = currentGameState.getScore()
    foodPos = Food.asList()
    for food in foodPos:
        score += 1 / (manhattanDistance(Pos, food) + 1)  # Encourage eating food

    for i, ghostState in enumerate(GhostStates):
        ghostPos = ghostState.getPosition()
        ghost_distance = util.manhattanDistance(Pos, ghostPos)
        if ScaredTimes[i] > 0:
            # Ghost is scared, it's good to be close
            score += 1 / (ghost_distance + 1) # Encourage being close to scared ghosts
        else:
            if ghost_distance < 2: # min_distance
                score -= 100  # Big penalty for being too close
            else:
                score -= 1 / (ghost_distance + 1) # Encourage staying away from ghosts
    return score
    util.raiseNotDefined()