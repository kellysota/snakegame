import time
import mysql.connector

# Database Connection
db = mysql.connector.connect(host='localhost', 
                             user='root',
                             passwd='Nibizi69..', 
                             database='test')
dbc = db.cursor()

# Ensuring leaderboard table exists
dbc.execute('CREATE TABLE IF NOT EXISTS leaderboard (Player_Name VARCHAR(20), Points INT)')
db.commit()


def main():
    print('\t\t////////////////SNAKE\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')
    print('\n1. PLAY','\n2. LEADERBOARD','\n3. EXIT')
    time.sleep(0.4) #delays the execution of following code by the specified time
    print()
    a=input('Enter the number corresponding your choice:')
    if a=='1':
        time.sleep(0.4)
        game()
    elif a=='2':
        l_board()
        main()
    elif a=='3':
        exit()
    else:
        time.sleep(0.3)
        print("Wrong Input, try again")
        print()
        time.sleep(0.4)
        main()
    


    
def game():
    import curses
    from random import randint

    l_name=input('Enter Name: ')

    print("Game Starting in 3")
    time.sleep(0.5)
    print(2)
    time.sleep(0.5)
    print(1)
    time.sleep(0.5)

    
    curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    win = curses.newwin(20,60,0,0)
    win.keypad(1)
    win.border(0)
    win.nodelay(1)

    snake = [(4,10),(4,9),(4,8)]
    food = (10,20)

    ESC = 27
    key = curses.KEY_RIGHT
    score = 0
    win.addch(food[0],food[1],"0")
    while key!= ESC:
        win.addstr(0,2,"score " + str(score) + " ")
        win.timeout(150)

        prev_key = key
        event = win.getch()
        key = event if event !=1 else prev_key

        if key not in [curses.KEY_LEFT,curses.KEY_RIGHT,curses.KEY_UP,curses.KEY_DOWN,ESC]:
            key = prev_key

    # Calculate next coordinate
        y = snake[0][0]
        x = snake[0][1]

        if key == curses.KEY_DOWN:
            y+=1
        if key == curses.KEY_UP:
            y-=1
        if key == curses.KEY_LEFT:
            x-=1
        if key == curses.KEY_RIGHT:
            x+=1
        snake.insert(0,(y,x))

    # Check border collision
        if y==0: break
        if x==0: break
        if x==59: break
        if y==19: break

        # if snake runs over itself
        if snake[0] in snake[1:]: break

        # if snake has eaten the food
        if snake[0] == food:
            score+=1
            food = ()
            while food == ():
                food = (randint(1,18), randint(1,58))
                if food in snake:
                    food()
            win.addch(food[0],food[1],"0")

        else:
            # moving the snake
            last = snake.pop()
            win.addch(last[0],last[1]," ")

        win.addch(snake[0][0],snake[0][1],"*")
        

    
    curses.endwin()
    print()
    print()
    time.sleep(0.5)
    
    # Update leaderboard
    try:
        dbc.execute('SELECT Points FROM leaderboard WHERE Player_Name = %s', (l_name,))
        res = dbc.fetchone()
        if res:
            new_score = res[0] + score
            dbc.execute('UPDATE leaderboard SET Points = %s WHERE Player_Name = %s', (new_score, l_name))
        else:
            dbc.execute('INSERT INTO leaderboard (Player_Name, Points) VALUES (%s, %s)', (l_name, score))
        db.commit()
    
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        db.rollback()

    print(f"Score = {score}")
    print("Exiting...")
    time.sleep(1)


def l_board():
    print('\t\t////////////////Leaderboard\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')

    dbc.execute('select * from leaderboard order by Points desc')
    res=dbc.fetchall()

    if len(res)==0:
        print("No player yet")
    else:
        for x in res:
            print(x)
    time.sleep(2)



# Start the program
main()