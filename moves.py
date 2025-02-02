class Moves:
    def is_valid_move(self, start, end, color, board_state):
        start_row, start_col = start
        end_row, end_col = end
        if end not in board_state or board_state[end] != "empty":
            return False

        if color == "black" and end_row == start_row + 1:
            return abs(end_col - start_col) == 1
        elif color == "red" and end_row == start_row - 1:
            return abs(end_col - start_col) == 1

        return False

    def is_valid_capture(self, start, end, color, board_state):
        start_row, start_col = start
        end_row, end_col = end
        if end not in board_state:
            return False
        jumped_row = (start_row + end_row) // 2
        jumped_col = (start_col + end_col) // 2
        jumped_position = (jumped_row, jumped_col)

        opponent_color = "red" if color == "black" else "black"

        if board_state.get(jumped_position) == opponent_color and board_state[end] == "empty":
            if color == "black" and end_row == start_row + 2:
                return abs(end_col - start_col) == 2
            elif color == "red" and end_row == start_row - 2:
                return abs(end_col - start_col) == 2

        return False

    def move_disk(self, start, end, player_color, board_state, disks):
        board_state[start] = "empty"
        board_state[end] = player_color
        disks[end] = disks.pop(start)
        disks[end].grid(row=end[0], column=end[1])

    def capture_disk(self, start, end, player_color, board_state, disks):
        self.move_disk(start, end, player_color, board_state, disks)

        # Remove the jumped disk
        jumped_row = (start[0] + end[0]) // 2
        jumped_col = (start[1] + end[1]) // 2
        jumped_position = (jumped_row, jumped_col)

        board_state[jumped_position] = "empty"
        disks[jumped_position].destroy()
        del disks[jumped_position]

    def check_winner(self, current_player_color, board_state):
        opponent_color = "red" if current_player_color == "black" else "black"
        count = 0

        # Step 1: Check if opponent has any pieces left
        for row in range(8):
            for col in range(8):
                if board_state[(row, col)] == opponent_color:
                    count += 1
        if count == 0:
            return current_player_color  # Opponent has no pieces, current player wins

        # Step 2: Check if opponent has any possible moves (normal or capture)
        for (row, col), color in board_state.items():
            if color == opponent_color:
                # Normal diagonal move options
                possible_moves = []
                if opponent_color == "black":
                    possible_moves = [(row + 1, col - 1), (row + 1, col + 1)]
                else:
                    possible_moves = [(row - 1, col - 1), (row - 1, col + 1)]

                # Check if at least one normal move is possible
                for move in possible_moves:
                    if board_state.get(move) == "empty":
                        return None  # Opponent still has a legal move

                # Check for possible captures (jump over an opponent's piece)
                possible_captures = []
                if opponent_color == "black":
                    possible_captures = [(row + 2, col - 2), (row + 2, col + 2)]
                else:
                    possible_captures = [(row - 2, col - 2), (row - 2, col + 2)]

                for cap in possible_captures:
                    mid_pos = ((row + cap[0]) // 2, (col + cap[1]) // 2)  # Middle square
                    if (
                            board_state.get(cap) == "empty"
                            and board_state.get(mid_pos) == current_player_color
                    ):
                        return None  # Opponent still has a valid capture

        # Step 3: If opponent has no valid moves, current player wins
        return current_player_color
