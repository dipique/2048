from abc import abstractmethod, ABCMeta

# NOTE: This is currently in conflict with the "RewardMethod" class. Where does the scoring mechanism belong?

# Because methods of scoring a given state are dependent on the
# implementation details of that state, a state and its respective
# scoring methods are built into the same class. These classes
# should inherit from State and implement the score_state method.

class State:
    __metaclass__ = ABCMeta # prevents classes from inheriting unless the abstract methods have been overloaded

    # states are represented by [][] of integers ("fields")
    def __init__(self, state_old: list, state_new: list):
        self.state_old = state_old
        self.state_new = state_new

    @abstractmethod
    def score_state(self): # this scores the change from the old state to the new
        pass