import turtle
import random
import pickle
import os

SQUARE_SIZE = 100
BOARD_SIZE = SQUARE_SIZE * 3
LINE_WIDTH = 5
SYMBOL_SIZE = 35
SAVE_FILE = "savegame.dat"
HISTORY_FILE = "game_history.txt"
game_board = [
    [None, None, None, None],
    [None, ' ', ' ', ' '],
    [None, ' ', ' ', ' '],
    [None, ' ', ' ', ' ']
]


def setup_board():
    screen = turtle.Screen()
    screen.setup(width=BOARD_SIZE + 50, height=BOARD_SIZE + 50)
    screen.title("Tic-Tac-Toe")
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.pensize(LINE_WIDTH)
    t.penup()
    t.goto(-BOARD_SIZE / 2, -BOARD_SIZE / 2)
    t.pendown()
    return t


def draw_grid(t):
    for i in range(1, 3):
        t.penup()
        t.goto(-BOARD_SIZE / 2 + (SQUARE_SIZE * i), -BOARD_SIZE / 2)
        t.pendown()
        t.setheading(90)
        t.forward(BOARD_SIZE)
    for j in range(1, 3):
        t.penup()
        t.goto(-BOARD_SIZE / 2, -BOARD_SIZE / 2 + (SQUARE_SIZE * j))
        t.pendown()
        t.setheading(0)
        t.forward(BOARD_SIZE)


def get_turtle_coords(row, col):
    x = -BOARD_SIZE / 2 + (col - 1) * SQUARE_SIZE + SQUARE_SIZE / 2
    y = -BOARD_SIZE / 2 + (row - 1) * SQUARE_SIZE + SQUARE_SIZE / 2
    return x, y


def draw_x(t, cx, cy):
    t.color("red")
    t.penup()
    t.goto(cx - SYMBOL_SIZE, cy - SYMBOL_SIZE)
    t.pendown()
    t.goto(cx + SYMBOL_SIZE, cy + SYMBOL_SIZE)
    t.penup()
    t.goto(cx - SYMBOL_SIZE, cy + SYMBOL_SIZE)
    t.pendown()
    t.goto(cx + SYMBOL_SIZE, cy - SYMBOL_SIZE)
    t.color("black")


def draw_o(t, cx, cy):
    t.color("blue")
    t.penup()
    t.goto(cx, cy - SYMBOL_SIZE)
    t.pendown()
    t.circle(SYMBOL_SIZE)
    t.color("black")


def draw_symbol(t, row, col, symbol):
    x, y = get_turtle_coords(row, col)
    if symbol == 'X':
        draw_x(t, x, y)
    elif symbol == 'O':
        draw_o(t, x, y)


def highlight_win(t, coords):
    start_x, start_y = get_turtle_coords(coords[0][0], coords[0][1])
    end_x, end_y = get_turtle_coords(coords[2][0], coords[2][1])
    t.pensize(LINE_WIDTH + 5)
    t.color("green")
    t.penup()
    t.goto(start_x, start_y)
    t.pendown()
    t.goto(end_x, end_y)


def check_win(board, p):
    for r in range(1, 4):
        if board[r][1] == board[r][2] == board[r][3] == p:
            return True, ((r, 1), (r, 2), (r, 3))
    for c in range(1, 4):
        if board[1][c] == board[2][c] == board[3][c] == p:
            return True, ((1, c), (2, c), (3, c))
    if board[1][1] == board[2][2] == board[3][3] == p:
        return True, ((1, 1), (2, 2), (3, 3))
    if board[1][3] == board[2][2] == board[3][1] == p:
        return True, ((1, 3), (2, 2), (3, 1))
    return False, None
def log_game_results(p1,p2,winner):
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{p1},{p2},{winner}\n")

def print_history():
    print("\n--- Game History ---")
    if not os.path.exists(HISTORY_FILE):
        print("no history found")
        return
    with open(HISTORY_FILE, "r") as f:
        for line in f:
            p1,p2,win=line.strip().split(",")
            print(f"Player 1: {p1} | Player 2: {p2} | Winner: {win}")
            print("--------------------\n")

def save_game(board):
    with open(SAVE_FILE, "wb") as f:
        pickle.dump(board, f)


def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "rb") as f:
            return pickle.load(f)
    return None


def redraw_board(t, board):
    for r in range(1, 4):
        for c in range(1, 4):
            if board[r][c] in ['X', 'O']:
                draw_symbol(t, r, c, board[r][c])


def get_player_move(p):
    while True:
        r = turtle.numinput(f"Turn: {p}", "Row (1-3):", minval=1, maxval=3)
        c = turtle.numinput(f"Turn: {p}", "Col (1-3):", minval=1, maxval=3)
        if r is None or c is None: return None, None
        if game_board[int(r)][int(c)] == ' ': return int(r), int(c)
        turtle.textinput("Error", "Cell taken!")


def get_computer_move():
    cells = [(r, c) for r in range(1, 4) for c in range(1, 4) if game_board[r][c] == ' ']
    return random.choice(cells) if cells else (None, None)


def main_game_loop():
    global game_board
    t = setup_board()
    draw_grid(t)

    mode = turtle.textinput("Mode", "Play against Computer? (y/n)")
    vs_computer = (mode and mode.lower() == 'y')

    if os.path.exists(SAVE_FILE):
        load = turtle.textinput("Load", "Load saved game? (y/n)")
        if load and load.lower() == 'y':
            game_board = load_game()
            redraw_board(t, game_board)

    x_count = sum(row.count('X') for row in game_board if isinstance(row, list))
    o_count = sum(row.count('O') for row in game_board if isinstance(row, list))
    curr = 'O' if x_count > o_count else 'X'
    moves = x_count + o_count
    hist_check = turtle.textinput("History", "Print game history to console? (y/n)")
    if hist_check and hist_check.lower() == 'y':
        print_history()

    if os.path.exists(SAVE_FILE):
        load = turtle.textinput("Load", "Load saved game? (y/n)")
        if load and load.lower() == 'y':
            with open(SAVE_FILE, "rb") as f:
                game_board = pickle.load(f)
            for r in range(1, 4):
                for c in range(1, 4):
                    if game_board[r][c] in ['X', 'O']:
                        draw_symbol(t, r, c, game_board[r][c])

    while moves < 9:
        if vs_computer and curr == 'O':
            row, col = get_computer_move()
        else:
            row, col = get_player_move(curr)

        if row is None:
            save = turtle.textinput("Exit", "Save game? (y/n)")
            if save and save.lower() == 'y': save_game(game_board)
            return

        game_board[row][col] = curr
        draw_symbol(t, row, col, curr)
        moves += 1

        win, coords = check_win(game_board, curr)
        if win:
            highlight_win(t, coords)
            turtle.textinput("Over", f"{curr} Wins!")
            if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
            break

        if moves == 9:
            turtle.textinput("Over", "Draw!")
            if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
            break

        curr = 'O' if curr == 'X' else 'X'
    turtle.done()

def print_history():

    print("\n--- Game History ---")
    if not os.path.exists(HISTORY_FILE):
        print("no history found")
        return
    with open(HISTORY_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 3:
                print(f"Skipping malformed history line: {line}")
                continue
            p1, p2, win = parts
            print(f"Player 1: {p1} | Player 2: {p2} | Winner: {win}")
            print("--------------------\n")

def get_player_move(p):
    while True:
        r = turtle.numinput(f"Turn: {p}", "Row (1-3):", minval=1, maxval=3)
        c = turtle.numinput(f"Turn: {p}", "Col (1-3):", minval=1, maxval=3)
        if r is None or c is None:
            return None, None
        r_i, c_i = int(r), int(c)
        if game_board[r_i][c_i] == ' ':
            return r_i, c_i
        turtle.textinput("Error", "Cell taken! Press OK to choose again.")

def main_game_loop():
    global game_board
    t = setup_board()
    draw_grid(t)
    mode = turtle.textinput("Mode", "Play against Computer? (y/n)")
    vs_computer = (mode and mode.lower() == 'y')
    if os.path.exists(SAVE_FILE):
        load = turtle.textinput("Load", "Load saved game? (y/n)")
        if load and load.lower() == 'y':
            try:
                loaded = load_game()
                if loaded:
                    game_board = loaded
                    redraw_board(t, game_board)
            except Exception as e:
                turtle.textinput("Load Error", f"Unable to load saved game: {e}")
    x_count = sum(row.count('X') for row in game_board if isinstance(row, list))
    o_count = sum(row.count('O') for row in game_board if isinstance(row, list))
    curr = 'O' if x_count > o_count else 'X'
    moves = x_count + o_count
    hist_check = turtle.textinput("History", "Print game history to console? (y/n)")
    if hist_check and hist_check.lower() == 'y':
        print_history()
    while moves < 9:
        if vs_computer and curr == 'O':
            row, col = get_computer_move()
        else:
            row, col = get_player_move(curr)
        if row is None:
            save = turtle.textinput("Exit", "Save game? (y/n)")
            if save and save.lower() == 'y':
                try:
                    save_game(game_board)
                except Exception as e:
                    turtle.textinput("Save Error", f"Unable to save game: {e}")
            try:
                turtle.bye()
            except Exception:
                pass
            return
        game_board[row][col] = curr
        draw_symbol(t, row, col, curr)
        moves += 1
        win, coords = check_win(game_board, curr)
        if win:
            highlight_win(t, coords)
            turtle.textinput("Over", f"{curr} Wins!")
            if os.path.exists(SAVE_FILE):
                try:
                    os.remove(SAVE_FILE)
                except Exception:
                    pass
            break
        if moves == 9:
            turtle.textinput("Over", "Draw!")
            if os.path.exists(SAVE_FILE):
                try:
                    os.remove(SAVE_FILE)
                except Exception:
                    pass
            break
        curr = 'O' if curr == 'X' else 'X'
    turtle.done()
if __name__ == "__main__":
    main_game_loop()