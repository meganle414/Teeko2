# Name: Megan Le
# email: mle25@wisc.edu
# Class/Semester: CS 540 Spring 2021
# Instructor: Sharon Li
import random


class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        count = 0
        for row in state:
            for col in row:
                if col == self.my_piece:
                    count += 1

        drop_phase = True if count != 4 else False
        move = self.minimax(state, drop_phase)
        return move

    def max_value(self, state, c_depth, t_depth, drop_phase):
        """
        Recursive helper method for the minimax algorithm (max part)
        :param state: the current state of the game as saved in this Teeko2Player object
        :param c_depth: current depth
        :param t_depth: target depth
        :param drop_phase: true if in drop phase, false otherwise
        :return: a list containing (row, col) for the move
        """
        h = self.game_value(state)
        if h != 0:
            return h
        elif c_depth == t_depth:
            return h
        else:
            alpha = -2
            for s in self.succ(state, self.my_piece, drop_phase):
                alpha = max(alpha, self.min_value(s, c_depth + 1, t_depth, drop_phase))
            return alpha

    def min_value(self, state, c_depth, t_depth, drop_phase):
        """
        Recursive helper method for the minimax algorithm (min part)
        :param state: the current state of the game as saved in this Teeko2Player object
        :param c_depth: current depth
        :param t_depth: target depth
        :param drop_phase: true if in drop phase, false otherwise
        :return: a list containing (row, col) for the move
        """
        h = self.game_value(state)
        if h != 0:
            return h
        elif c_depth == t_depth:
            return h
        else:
            beta = 2
            for s in self.succ(state, self.opp, drop_phase):
                beta = min(beta, self.max_value(s, c_depth + 1, t_depth, drop_phase))
            return beta

    def minimax(self, state, drop_phase):
        """
        Minimax recursive call start
        :param state: the current state of the game as saved in this Teeko2Player object
        :param drop_phase: true if in drop phase, false otherwise
        :return: a list containing (row, col) for the move
        """
        t_depth = 4
        move = []
        best_h, best_state = -2, None
        for s in self.succ(state, self.my_piece, drop_phase):
            if self.game_value(s) != 0:  # if a winner is already declared
                best_state = s
                break
            curr_h = self.min_value(s, 1, t_depth, drop_phase)
            if curr_h > best_h:
                best_h = curr_h
                best_state = s

        for i in range(5):
            for j in range(5):
                if state[i][j] != best_state[i][j]:
                    if state[i][j] != ' ':
                        move.insert(1, (i, j))
                    else:
                        move.insert(0, (i, j))
        return move

    def succ(self, state, piece, drop_phase):
        """
        Generate a list of the legal successors
        :param state: the current state of the game as saved in this Teeko2Player object
        :param piece: current piece we generator the successors for
        :param drop_phase: true if in drop phase, false otherwise
        :return: a list of the legal successors
        """
        succ = []
        if drop_phase:
            for i in range(5):
                for j in range(5):
                    if state[i][j] == ' ':
                        temp = [x[:] for x in state]
                        temp[i][j] = self.my_piece
                        succ.append(temp)
        else:
            for i in range(5):
                for j in range(5):
                    if state[i][j] == piece:  # if the current spot has a piece on it
                        if i - 1 >= 0:  # if not first row
                            if j - 1 >= 0:  # if not in first column
                                if state[i - 1][j - 1] == ' ':  # if previous row and previous column spot is empty
                                    temp = [x[:] for x in state]
                                    temp[i - 1][j - 1], temp[i][j] = temp[i][j], temp[i - 1][j - 1]
                                    succ.append(temp)
                            if state[i - 1][j] == ' ':  # if previous row spot is empty
                                temp = [x[:] for x in state]
                                temp[i - 1][j], temp[i][j] = temp[i][j], temp[i - 1][j]
                                succ.append(temp)
                            if j + 1 < 5:  # if not last column
                                if state[i - 1][j + 1] == ' ':  # if previous row and successor column spot is empty
                                    temp = [x[:] for x in state]
                                    temp[i - 1][j + 1], temp[i][j] = temp[i][j], temp[i - 1][j + 1]
                                    succ.append(temp)
                        if i + 1 < 5:  # if not last row
                            if j - 1 >= 0:  # if not first column
                                if state[i + 1][j - 1] == ' ':
                                    temp = [x[:] for x in state]
                                    temp[i + 1][j - 1], temp[i][j] = temp[i][j], temp[i + 1][j - 1]
                                    succ.append(temp)
                            if state[i + 1][j] == ' ':  # if successor row spot is empty
                                temp = [x[:] for x in state]
                                temp[i + 1][j], temp[i][j] = temp[i][j], temp[i + 1][j]
                                succ.append(temp)
                            if j + 1 < 5:  # if not last column
                                if state[i + 1][j + 1] == ' ':  # if successor row and successor column spot is empty
                                    temp = [x[:] for x in state]
                                    temp[i + 1][j + 1], temp[i][j] = temp[i][j], temp[i + 1][j + 1]
                                    succ.append(temp)
                        if j - 1 >= 0:  # if not first column
                            if state[i][j - 1] == ' ':  # if previous column spot is empty
                                temp = [x[:] for x in state]
                                temp[i][j - 1], temp[i][j] = temp[i][j], temp[i][j - 1]
                                succ.append(temp)
                        if j + 1 < 5:  # if not last column
                            if state[i][j + 1] == ' ':  # if successor column spot is empty
                                temp = [x[:] for x in state]
                                temp[i][j + 1], temp[i][j] = temp[i][j], temp[i][j + 1]
                                succ.append(temp)
        return succ

    def heuristic_game_value(self, state):
        """
        Calculates an h value based on win conditions. 2/4 pieces towards any win condition is 0.5, and 3/4 is 0.75.
        :param state: the current state of the game as saved in this Teeko2Player object
        :return: h value based on how close the winning player is to winning.
        Negative value indicates other player is winning
        """
        h = float()
        h_values = []
        if self.game_value(state) != 0:
            return h
        # Check horizontal, vertical, and diagonal partial wins
        for i in range(5):
            for j in range(5):
                if state[i][j] != ' ':
                    # horizontal
                    if j + 2 < 5 and state[i][j] == state[i][j + 1] == state[i][j + 2]:
                        h = 0.75 if state[i][j] == self.my_piece else -0.75
                        h_values.append(h)
                    elif j + 1 < 5 and state[i][j] == state[i][j + 1]:
                        h = 0.5 if state[i][j] == self.my_piece else -0.5
                        h_values.append(h)
                    # vertical
                    if i + 2 < 5 and state[i][j] == state[i + 1][j] == state[i + 2][j]:
                        h = 0.75 if state[i][j] == self.my_piece else -0.75
                        h_values.append(h)
                    elif i + 1 < 5 and state[i][j] == state[i + 1][j]:
                        h = 0.5 if state[i][j] == self.my_piece else -0.5
                        h_values.append(h)
                    # \ wins
                    if i + 1 < 5 and j + 1 < 5:  # if not last row and not last column
                        if i + 2 < 5 and j + 2 < 5:  # if not second to last row+ and not second to last column+
                            if state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2]:
                                h = 0.75 if state[i][j] == self.my_piece else -0.75
                                h_values.append(h)
                        elif state[i][j] == state[i + 1][j + 1]:
                            h = 0.5 if state[i][j] == self.my_piece else -0.5
                            h_values.append(h)
                    # / wins
                    if i + 1 < 5 and j - 1 > 0:  # if not last row and not first column
                        if i + 2 < 5 and j - 2 > 0:  # if not second to last row+ and not 2nd column or below
                            if state[i][j] == state[i + 1][j - 1] == state[i + 2][j - 2]:
                                h = 0.75 if state[i][j] == self.my_piece else -0.75
                                h_values.append(h)
                        elif state[i][j] == state[i + 1][j - 1]:
                            h = 0.5 if state[i][j] == self.my_piece else -0.5
                            h_values.append(h)
        for i in range(1, 4):
            for j in range(1, 4):
                # four corner wins 0.5 from horizontal or vertical pair
                if state[i - 1][j - 1] != ' ' and state[i - 1][j - 1] == state[i - 1][j + 1]:  # horizontal top
                    h = 0.5 if state[i - 1][j - 1] == self.my_piece else -0.5
                    h_values.append(h)
                elif state[i - 1][j - 1] != ' ' and state[i - 1][j - 1] == state[i + 1][j - 1]:  # vertical left
                    h = 0.5 if state[i - 1][j - 1] == self.my_piece else -0.5
                    h_values.append(h)
                elif state[i - 1][j + 1] != ' ' and state[i - 1][j + 1] == state[i + 1][j + 1]:  # vertical right
                    h = 0.5 if state[i - 1][j + 1] == self.my_piece else -0.5
                    h_values.append(h)
                elif state[i + 1][j - 1] != ' ' and state[i + 1][j - 1] == state[i + 1][j + 1]:  # horizontal bottom
                    h = 0.5 if state[i + 1][j - 1] == self.my_piece else -0.5
                    h_values.append(h)
                # four corner wins 0.5 from opposite corners
                if state[i - 1][j - 1] != ' ' and state[i - 1][j - 1] == state[i + 1][j + 1]:
                    h = 0.5 if state[i + 1][j - 1] == self.my_piece else -0.5
                    h_values.append(h)
                elif state[i - 1][j + 1] != ' ' and state[i - 1][j + 1] == state[i + 1][j - 1]:
                    h = 0.5 if state[i - 1][j + 1] == self.my_piece else -0.5
                    h_values.append(h)
                # four corner wins 0.75
                    # no top right
                    if state[i - 1][j - 1] != ' ' and state[i - 1][j - 1] == state[i + 1][j - 1] == state[i + 1][j + 1]:
                        h = 0.75 if state[i - 1][j - 1] == self.my_piece else -0.75
                        h_values.append(h)
                    # no bottom left
                    elif state[i - 1][j - 1] != ' ' and state[i - 1][j - 1] == state[i - 1][j + 1] == state[i + 1][
                        j + 1]:
                        h = 0.75 if state[i - 1][j - 1] == self.my_piece else -0.75
                        h_values.append(h)
                    # no bottom right
                    elif state[i - 1][j - 1] != ' ' and state[i - 1][j - 1] == state[i - 1][j + 1] == state[i + 1][
                        j - 1]:
                        h = 0.75 if state[i - 1][j - 1] == self.my_piece else -0.75
                        h_values.append(h)
                    # no top left
                    elif state[i - 1][j + 1] != ' ' and state[i - 1][j + 1] == state[i + 1][j - 1] == state[i + 1][
                        j + 1]:
                        h = 0.75 if state[i - 1][j + 1] == self.my_piece else -0.75
                        h_values.append(h)
        h_values = sorted(h_values)
        return h_values[-1] if h_values[-1] >= abs(h_values[0]) else h_values[0]

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row is not None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and 3x3 square corners wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for j in range(5):
            for i in range(2):
                if state[i][j] != ' ' and state[i][j] == state[i + 1][j] == state[i + 2][j] == state[i + 3][j]:
                    return 1 if state[i][j] == self.my_piece else -1

        # TODO: check \ diagonal wins
        if state[1][0] != ' ' and state[1][0] == state[2][1] == state[3][2] == state[4][3]:
            return 1 if state[1][0] == self.my_piece else -1
        if state[0][0] != ' ' and state[0][0] == state[1][1] == state[2][2] == state[3][3]:
            return 1 if state[0][0] == self.my_piece else -1
        if state[1][1] != ' ' and state[1][1] == state[2][2] == state[3][3] == state[4][4]:
            return 1 if state[1][1] == self.my_piece else -1
        if state[0][1] != ' ' and state[0][1] == state[1][2] == state[2][3] == state[3][4]:
            return 1 if state[0][1] == self.my_piece else -1

        # TODO: check / diagonal wins
        if state[3][0] != ' ' and state[3][0] == state[2][1] == state[1][2] == state[0][3]:
            return 1 if state[3][0] == self.my_piece else -1
        if state[4][0] != ' ' and state[4][0] == state[3][1] == state[2][2] == state[1][3]:
            return 1 if state[4][0] == self.my_piece else -1
        if state[3][1] != ' ' and state[3][1] == state[2][2] == state[1][3] == state[0][4]:
            return 1 if state[3][1] == self.my_piece else -1
        if state[4][1] != ' ' and state[4][1] == state[3][2] == state[2][3] == state[1][4]:
            return 1 if state[4][1] == self.my_piece else -1

        # TODO: check 3x3 square corners wins
        for i in range(1, 4):
            for j in range(1, 4):
                if state[i - 1][j - 1] != ' ' and state[i - 1][j - 1] == state[i - 1][j + 1] == state[i + 1][j - 1] == \
                        state[i + 1][j + 1]:
                    return 1 if state[i - 1][j - 1] == self.my_piece else -1

        return 0  # no winner yet


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
            print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                      (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
