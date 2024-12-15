from tkinter import *
from random import randrange

# Initialize global variables
players = []  # Store players' snakes and their directions
scores = []  # Store scores for each player
current_player = 0  # Index of the current player
game_over = False

# Settings
arena_size = 500
snake_size = 10
food_size = 10
directions = {'haut': (0, -snake_size), 'bas': (0, snake_size), 'gauche': (-snake_size, 0), 'droite': (snake_size, 0)}

# Initialize the game arena
fen = Tk()
fen.title("Snake Game")
can = Canvas(fen, width=arena_size, height=arena_size, bg='black')
can.pack(side=TOP, padx=5, pady=5)

# Initialize food position
food_x = randrange(0, arena_size - food_size, food_size)
food_y = randrange(0, arena_size - food_size, food_size)

# Draw the food
food = can.create_rectangle(food_x, food_y, food_x + food_size, food_y + food_size, outline='green', fill='red')

def create_snake(x, y):
    return [[x, y], [x - snake_size, y], [x - 2 * snake_size, y]]

def reset_game():
    global players, scores, current_player, game_over, food_x, food_y
    players = [
        {'snake': create_snake(100, 100), 'direction': 'droite', 'alive': True},
        {'snake': create_snake(300, 300), 'direction': 'gauche', 'alive': True}
    ]
    scores[:] = [0] * len(players)
    current_player = 0
    game_over = False
    food_x = randrange(0, arena_size - food_size, food_size)
    food_y = randrange(0, arena_size - food_size, food_size)
    can.coords(food, food_x, food_y, food_x + food_size, food_y + food_size)
    redraw_arena()
    fen.after(300, move_snake)

def redraw_arena():
    can.delete('all')
    can.create_rectangle(food_x, food_y, food_x + food_size, food_y + food_size, outline='green', fill='red')
    for i, player in enumerate(players):
        for segment in player['snake']:
            color = 'blue' if i == 0 else 'yellow'
            can.create_oval(segment[0], segment[1], segment[0] + snake_size, segment[1] + snake_size, outline='green', fill=color)

def move_snake():
    global current_player, game_over, food_x, food_y
    if game_over:
        return

    player = players[current_player]
    if not player['alive']:
        switch_turn()
        return

    head = player['snake'][0]
    dx, dy = directions[player['direction']]
    new_head = [head[0] + dx, head[1] + dy]

    # Check for collisions
    if (
        new_head[0] < 0 or new_head[1] < 0 or
        new_head[0] >= arena_size or new_head[1] >= arena_size or
        any(new_head == segment for other in players for segment in other['snake'])
    ):
        player['alive'] = False
        switch_turn()
        return

    # Check for food collision
    if food_x <= new_head[0] < food_x + food_size and food_y <= new_head[1] < food_y + food_size:
        player['snake'].insert(0, new_head)  # Grow snake
        scores[current_player] += 1
        food_x = randrange(0, arena_size - food_size, food_size)
        food_y = randrange(0, arena_size - food_size, food_size)
        can.coords(food, food_x, food_y, food_x + food_size, food_y + food_size)
    else:
        player['snake'].insert(0, new_head)
        player['snake'].pop()

    redraw_arena()
    switch_turn()

def switch_turn():
    global current_player, game_over
    current_player = (current_player + 1) % len(players)
    print(f"Switching to Player {current_player + 1}")
    if all(not player['alive'] for player in players):
        game_over = True
        display_game_over()
    else:
        fen.after(300, move_snake)

def display_game_over():
    can.create_text(arena_size // 2, arena_size // 2, text="Game Over", fill='white', font=('Helvetica', 24))
    for i, score in enumerate(scores):
        can.create_text(
            arena_size // 2, arena_size // 2 + (i + 1) * 30,
            text=f"Player {i + 1} Score: {score}", fill='white', font=('Helvetica', 18)
        )

def change_direction(event):
    global players
    key_to_direction = {'z': 'haut', 's': 'bas', 'q': 'gauche', 'd': 'droite'}
    new_direction = key_to_direction.get(event.keysym)
    if new_direction:
        player = players[current_player]
        current_direction = player['direction']
        
        if (directions[new_direction][0] + directions[current_direction][0] != 0 or
                directions[new_direction][1] + directions[current_direction][1] != 0):
            player['direction'] = new_direction

# Reset and start the game
reset_game()

# Buttons and bindings
b1 = Button(fen, text='Nouvelle Partie', command=reset_game, bg='black', fg='green')
b1.pack(side=LEFT, padx=5, pady=5)

b2 = Button(fen, text='Quitter', command=fen.destroy, bg='black', fg='green')
b2.pack(side=RIGHT, padx=5, pady=5)

fen.bind('<KeyPress>', change_direction)
fen.after(300, move_snake)
fen.mainloop()
