from Boards import Board

def get_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value not in [0, 1, 2]:
                raise ValueError
            return value
        except ValueError:
            print("Please enter a valid number between 0 and 2.")

def play():
    board = Board.new()
    while True:
        # Tour du joueur X
        print("Player X's turn")
        row = get_input("Enter the row (0, 1, 2): ")
        col = get_input("Enter the column (0, 1, 2): ")
        try:
            if board.play_turn("X", row, col):
                play_again = input("Do you want to play again? (yes/no): ")
                if play_again.lower() == "yes":
                    board = Board.new()  # Créer un nouveau plateau
                    continue
                else:
                    quit()
        except ValueError:
            continue

        # Tour du joueur O (IA)
        print("Player O's turn (AI)")
        row, col = board.best_move()
        if board.play_turn("O", row, col):
            play_again = input("Do you want to play again? (yes/no): ")
            if play_again.lower() == "yes":
                board = Board.new()  # Créer un nouveau plateau
                # On se doute bien que Board.new() retourne un nouveau plateau
                continue
            else:
                quit()

play()
