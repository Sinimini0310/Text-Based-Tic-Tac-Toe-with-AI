import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

# Gewinner
def check_winner(board, player):
    for i in range(3):
        # Check Reihen
        if all(cell == player for cell in board[i]):
            return True
        # Check Spalten
        if all(board[j][i] == player for j in range(3)):
            return True
    # Check Diagonalen
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# Board voll
def is_full(board):
    for row in board:
        if " " in row:
            return False
    return True

# min-max Algorithmus
def minimax(board, depth, is_maximizing):
    # Tiefe einstellen
    if check_winner(board, "X"):
        return -1
    if check_winner(board, "O"):
        return 1
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j] = " "
                    best_score = min(score, best_score)
        return best_score

# Besten Move bestimmen
def find_best_move(board):
    best_score = -float("inf")
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = " "
                if score > best_score: # Check ob move beser ist als der zuvor
                    best_score = score
                    best_move = (i, j)
    return best_move

# Zweitbesten Move bestimmen
def find_second_best_move(board):
    best_move = (-1, -1)
    best_score = -float("inf")
    second_best_move = None
    second_best_score = -float("inf")
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = " "
                if score > best_score: # Check ob move besser ist als der zuvor
                    second_best_move = best_move
                    second_best_score = best_score
                    best_move = (i, j)
                    best_score = score
                elif score > second_best_score: # Nachschieben
                    second_best_move = (i, j)
                    second_best_score = score

    return second_best_move

# Schlechtesten Move bestimmen
def find_worst_move(board):
    best_score = float("inf")
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, 0, True)
                board[i][j] = " "
                if score < best_score:  # Check ob move schlechter ist als der zuvor
                    best_score = score
                    best_move = (i, j)
    return best_move

# Entscheidung Move hard_ai
def hard_ai_move(board):
    random_number = random.randint(1, 4)
    if random_number == 1:
        return find_second_best_move(board)
    else:
        return find_best_move(board)

# Zahlen von 1-9 zu Reihe und Spalte umwandeln
def map_input_to_coordinates(input_number):
    row = (input_number - 1) // 3
    col = (input_number - 1) % 3
    return row, col

# Reihe und Spalte zu Zahlen von 1-9 umwandeln
def map_coordinates_to_input(row, col):
    return row * 3 + col + 1

# Main Loop
def tic_tac_toe():
    current_player = "X"
    while True:
        board = [[" " for _ in range(3)] for _ in range(3)
        ]
        # Spielerwahl der AI
        ai_difficulty = input("Choose AI difficulty (easy/hard/impossible): ").strip().lower()

        if ai_difficulty not in ["easy", "hard", "impossible"]:
            print("Invalid choice. Defaulting to hard AI.")
            ai_difficulty = "hard"
        # Game Loop
        while True:
            print_board(board)
            if current_player == "X":
                move = -1
                while move not in range(1, 10) or board[row][col] != " ":
                    try:
                        move = int(input("Enter a number (1-9) to make your move: "))
                        row, col = map_input_to_coordinates(move)
                    except ValueError:
                        print("Invalid input. Please try again.")
            else:
                if ai_difficulty == "easy":
                    row, col = find_worst_move(board)
                elif ai_difficulty == "hard":
                    row, col = hard_ai_move(board)
                else:
                    row, col = find_best_move(board)
                move = map_coordinates_to_input(row, col)
                print(f"AI chooses position {move}")

            board[row][col] = current_player
        
            if check_winner(board, current_player):
                print_board(board)
                if current_player == "X":
                    print("Player X wins!")
                else:
                    print("AI wins!")
                break
            elif is_full(board):
                print_board(board)
                print("It's a draw!")
                break
    
            # Spielerwechsel (noch etwas verbuggt)
            current_player = "X" if current_player == "O" else "O"
        current_player = "X" if current_player == "O" else "O"

if __name__ == "__main__":
    tic_tac_toe()
