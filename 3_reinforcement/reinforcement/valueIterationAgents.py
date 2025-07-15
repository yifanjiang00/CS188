# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp: mdp.MarkovDecisionProcess, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        """
          Run the value iteration algorithm. Note that in standard
          value iteration, V_k+1(...) depends on V_k(...)'s.
        """
        "*** YOUR CODE HERE ***"

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

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        QValue=0
        for next,prob in self.mdp.getTransitionStatesAndProbs(state,action):
            reward=self.mdp.getReward(state,action,next)
            QValue+=prob*(reward+self.discount*self.getValue(next))
        
        return QValue
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        #如果当前状态(x,y)下一个动作为空，则返回None	

        if len(self.mdp.getPossibleActions(state)) == 0:	
            return None	
        	
        #新建一个动作的计数器	
        valuesForActions = util.Counter()	
        #遍历当前状态（x,y）的可能的动作集	
        for action in self.mdp.getPossibleActions(state):	
            valuesForActions[action]=self.computeQValueFromValues(state,action)	
        #返回最大值maxQ*（s,a）	
        return valuesForActions.argMax()	

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
