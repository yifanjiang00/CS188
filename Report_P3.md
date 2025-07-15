## Project3:Reinforcement Learning

### Q1:Value Iteration
就是要完成以下过程：
\[ V_{k+1}(s) = \max_a \sum_{s'} T(s,a,s') [R(s,a,s') + \gamma V_k(s')] \]
代码如下：
```python
    def runValueIteration(self):
        for i in range(self.iterations):	
            #新建一个用于状态的计数器	
            valueForState = util.Counter()	
            #遍历获取马尔科夫链的所有状态(x,y)，“#”墙不包括。	
            for state in self.mdp.getStates():	
                #在当前状态（x，y），新建一个用于动作的计数器	
                valuesForActions = util.Counter()	
                #获取这个状态（x，y）可能的动作'north','west','south','east'，'exit'	
                for action in self.mdp.getPossibleActions(state):	
                    #在动作计数器中记录计算状态（x，y）执行下一个动作的Q-values	
                    valuesForActions[action]=self.computeQValueFromValues(state,action)	
                #在状态（x,y）所有动作中取得最大的动作值，作为状态计数器的值。	
                valueForState[state] = valuesForActions[valuesForActions.argMax()]	
            #遍历马尔科夫链的状态集,给values赋值	
            for state in self.mdp.getStates():	
                self.values[state] = valueForState[state]
```
参考了https://blog.csdn.net/duan_zhihua/article/details/90625916
```python
    def computeQValueFromValues(self, state, action):
        QValue=0
        for next,prob in self.mdp.getTransitionStatesAndProbs(state,action):
            reward=self.mdp.getReward(state,action,next)
            QValue+=prob*(reward+self.discount*self.getValue(next)) #值迭代的状态更新公式
        return QValue
        util.raiseNotDefined()
```
计算各个QValue

```python
    def computeActionFromValues(self, state):
        #如果当前状态(x,y)下一个动作为空，则返回None	
        if len(self.mdp.getPossibleActions(state)) == 0:	
            return None	
        #新建一个动作的计数器	
        valuesForActions = util.Counter()	
        #遍历当前状态（x,y）的可能的动作集	
        for action in self.mdp.getPossibleActions(state):	
            valuesForActions[action]=self.computeQValueFromValues(state,action)	
        return valuesForActions.argMax()	
```
返回maxQ(s,a)对应的action

### Q2:Policies
这一问重要的是理解题目、各个parameter的含义。
根据每一个例子的要求，确定对应的parameter来达成相应的策略。
几个参数的作用：
answerDiscount：折扣因子，范围通常在 0~1。越大表示越重视未来奖励，越小表示更看重即时奖励。
answerNoise：行动的随机性。0 表示完全确定性（每次都按预期方向走），越大表示行动越不确定（有概率走错方向）。
answerLivingReward：每走一步获得的奖励。为负值时鼓励尽快结束（走到出口），为正值时鼓励一直走下去（不结束）。

**调参思路**
鼓励走近路/远路：
想让智能体选择近的出口，livingReward 设为负值（每走一步都扣分，早点结束更好）。
想让智能体选择远的出口，可以适当提高 discount（重视未来大奖励），并让 livingReward 不是太负。

冒险/保守：
想让智能体冒险（愿意冒着掉下悬崖的风险），noise 设低（如 0），livingReward 设负。
想让智能体保守（避免掉下悬崖），noise 设高（如 0.2~0.5），livingReward 设为 0 或较小负值。

避免所有出口：
discount 设为 0（不关心未来），noise 设高（如 1），livingReward 设为正（每走一步都有奖励，智能体不想结束）。

了解几个参数的作用之后，就慢慢调试，利用python gridworld.py -g DiscountGrid -a value --discount [YOUR_DISCOUNT] --noise [YOUR_NOISE] --livingReward [YOUR_LIVING_REWARD] 来观察策略情况，一步步地调整各个例子的参数，直至通过Q2.
最终我调出来的参数如下：
```python
def question2a():
    """
      Prefer the close exit (+1), risking the cliff (-10).
    """
    answerDiscount = 0.2
    answerNoise = 0
    answerLivingReward = -0.5
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question2b():
    """
      Prefer the close exit (+1), but avoiding the cliff (-10).
    """
    answerDiscount = 0.5
    answerNoise = 0.2
    answerLivingReward = -2
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question2c():
    """
      Prefer the distant exit (+10), risking the cliff (-10).
    """
    answerDiscount = 1
    answerNoise = 0.1
    answerLivingReward = -1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question2d():
    """
      Prefer the distant exit (+10), avoiding the cliff (-10).
    """
    answerDiscount = 1
    answerNoise = 0.4
    answerLivingReward = -1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question2e():
    """
      Avoid both exits and the cliff (so an episode should never terminate).
    """
    answerDiscount = 0
    answerNoise = 0.5
    answerLivingReward = 10
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'
```

### Q3:Q-Learning
关键公式：\[ Q(s,a) \gets Q(s,a) + \alpha \left[ r + \gamma \max_{a'} Q(s',a') - Q(s,a) \right] = (1-\alpha)Q(s,a) + \alpha[r + \gamma \max_{a'} Q(s',a')]\]
```python
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)
        self.qValues=util.Counter()

    def getQValue(self, state, action):
        return self.qValues[(state,action)]

    def computeValueFromQValues(self, state):
        q_values = [self.getQValue(state, action) for action in self.getLegalActions(state)]
        if len(q_values):
          return max(q_values)
        return 0

    def computeActionFromQValues(self, state):
        actions = self.getLegalActions(state)
        if not actions:
          return None
        max_q = self.computeValueFromQValues(state)
        best_actions = [action for action in actions if self.getQValue(state, action) == max_q]
        return random.choice(best_actions)

    def update(self, state, action, nextState, reward: float):
        NewQvalue=0
        Qvalue=self.getQValue(state,action)
        NewQvalue=(1-self.alpha)*Qvalue+self.alpha*(reward+self.discount*self.computeValueFromQValues(nextState))
        self.qValues[(state,action)]=NewQvalue
```

### Q4:Epsilon Greedy
有 $\epsilon$ 的概率从所有legal actions里面随机选一个执行，另外1 - $\epsilon$ 的概率执行greedy action (所以实际上执行greedy action的概率是1 - $\epsilon$ + $\epsilon$/|A|,其中|A|表示legal actions的数量)
```python
    def getAction(self, state):
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        if util.flipCoin(self.epsilon):
          action = random.choice(legalActions)
        else:
          action = self.computeActionFromQValues(state)
        return action
```

### Q5:Q-Learning and Pacman
啥也不用动，直接过了

### Q6:Approximate Q-Learning
Approximate Q-Learning的梯度更新规则为：
\[
\theta \leftarrow \theta + \alpha \left( r + \gamma \max_{a'} Q(s', a'; \theta) - Q(s, a; \theta) \right) \nabla_\theta Q(s, a; \theta)
\]
```python
class ApproximateQAgent(PacmanQAgent):
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        features=self.featExtractor.getFeatures(state,action)
        qValue=0

        for feature,value in features.items():
            qValue+=self.weights[feature]*value
        
        return qValue

    def update(self, state, action, nextState, reward: float):
        features=self.featExtractor.getFeatures(state,action)
        difference=(reward+self.discount*self.computeValueFromQValues(nextState))-self.getQValue(state,action)
        for feature,value in features.items():
         self.weights[feature]+=self.alpha*difference*value

    def final(self, state):
        """Called at the end of each game."""
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
```
