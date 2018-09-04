from game.BoardState import BoardState
from game.Direction import Direction
import random
import numpy as np
import webbrowser

class Pseudo_ML:
    # given a set of weights, returns the top weight [0] and top score [1]
    def get_direction_recommendation(self, weights):
        #print scores and get max value
        retVal = Direction.Down
        top_score = -100
        for direction in Direction:
            this_score = weights[direction]
            # print(str(direction) + ": " + str(this_score))
            if this_score > top_score:
                top_score = this_score
                retVal = direction
        
        #return the top-scoring direction
        return [retVal, top_score]

    # given a board state, returns scores corresponding to each possible move
    def get_direction_weights(self, board_state: BoardState):
        statesAfterMove = []
        direction_scores = { d:0 for d in Direction }

        # get a list of the board state after making all legal moves
        for direction in Direction:
            dir_move = board_state.move(direction, False, False)
            if dir_move.changed_board(): # ignore moves that do not change the board
                possible_states = self.enumerate_possible_outcomes(dir_move.end_state, board_state.FOUR_CHANCE)
                for state in possible_states:#move  state      prob             score
                    score = self.score_board_state(BoardState.state_to_2d_state(state[0], board_state.BOARD_SIZE))
                    #                    0:dir     1:state   2:prob   3:score
                    state_assessment = [direction, state[0], state[1], score]
                    direction_scores[direction] += state[1] * score
                    # print(state_assessment)
                    statesAfterMove.append(state_assessment)
            else:
                direction_scores[direction] -= 100 # never pick a direction that will have no impact
        
        return direction_scores
    
    def enumerate_possible_outcomes(self, squares_array, four_chance):
        retVal = []
        empty_indexes = [idx for idx, val in enumerate(squares_array) \
                              if val == 0]
        for idx in empty_indexes:
            new_outcome_1 = squares_array[:]
            new_outcome_1[idx] = 1
            retVal.append([new_outcome_1, 1 - four_chance])
            new_outcome_2 = squares_array[:]
            new_outcome_2[idx] = 2
            retVal.append([new_outcome_2, four_chance])
        
        return retVal
    
    def score_board_state(self, board_2d_state):
        # get orientation of the board (where highest values are); this
        # makes it so we only need to score in one direction rather than in four
        board_size = len(board_2d_state[0])
        index_count = int(board_size / 2) # half the board, rounded down
        direction_scores = { d:0 for d in Direction }

        for x in range(board_size): # for each row
            if x < index_count:
                direction_scores[Direction.Up] += sum(board_2d_state[x])
            elif x >= (board_size - index_count):
                direction_scores[Direction.Down] += sum(board_2d_state[x])
            direction_scores[Direction.Left] += sum(board_2d_state[x][:index_count])
            direction_scores[Direction.Right] += sum(board_2d_state[x][board_size - index_count:])
        
        # get the orientation based on score
        orientation = Direction.Down
        orientation_score = 0
        for direction in Direction:
            this_score = direction_scores[direction]
            if this_score > orientation_score:
                orientation = direction
                orientation_score = this_score

        # tranform the array so the orientation is left
        working_board = []
        if orientation == Direction.Left:
            working_board = board_2d_state
        if orientation == Direction.Right:
            for row in board_2d_state:
                working_board.append(row[::-1])
        if orientation == Direction.Down:
            working_board = np.rot90(board_2d_state, 3)
        if (orientation == Direction.Up):
            working_board = np.rot90(board_2d_state, 1)

        score = 0
        #for every row, score value pairs by whether they are in ascending order
        for x in range(board_size):
            #for every value pair
            values = [val for val in working_board[x] if val > 0]
            value_count = len(values)
            if value_count > 2: # there have to be at least 2 values to score the row
                for idx in range(len(values) - 1): # for every value except the last
                    fst_val = values[idx]
                    sec_val = values[idx + 1]
                    if sec_val >= fst_val:
                        score += 1
                    else:
                        score -= 1

        return score
                    