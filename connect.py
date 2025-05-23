"""Connect Four

Exercises
ssf
1. Change the colors.
2. Draw squares instead of circles for open spaces.
3. Add logic to detect a full col.
4. Create a random computer player.
5. How would you detect a winner?
"""

from turtle import *
from tkinter import *
from tkinter import ttk
from freegames import line
import os
import sys
import time
import random


turns = {'red': 'yellow', 'yellow': 'red'}
state = {'player': 'red', 'rows': [0] * 8}
# Инициализация 8x8 массива с None в каждой ячейке
field = [[None for _ in range(8)] for _ in range(8)]

#initialisierung
def grid():
    """Draw players move box."""
    bgcolor('green')
    
    for x in range(-150, 200, 50):
        line(x, -200, x, 200)

    for x in range(-175, 200, 50):
        for y in range(-175, 200, 50):
            up()
            goto(x, y)
            dot(40, 'pink')
    
    printPlayersMoveBox()
    printPlayersMoveText(state['player'])
    update()

def printPlayersMoveBox():
    """Draw players move box."""
    
    color(0, 79/255, 7/255)
    begin_fill()
    line(-200, 200, -200, 244)
    line(-200, 244, 200, 244)
    line(200, 244, 200, 200)
    line(200, 200, -200, 200)
    end_fill()



def check_winner(col, row, color):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dc, dr in directions:
        count = 1
        
        c_next, r_next = col + dc, row + dr
        while 0 <= c_next < 8 and 0 <= r_next < 8 and field[c_next][r_next] == color:
            count += 1
            c_next += dc
            r_next += dr
     
        c_prev, r_prev = col - dc, row - dr
        while 0 <= c_prev < 8 and 0 <= r_prev < 8 and field[c_prev][r_prev] == color:
            count += 1
            c_prev -= dc
            r_prev -= dr
        
        if count >= 4:
            return True
    return False
     
def computerMove():
    availableColumns = getAvailableColumns()
    if not availableColumns:
        return  # No available columns, game is over
    
    columnForMove = random.choice(availableColumns)
    player = state['player']
    rows = state['rows']
    row = rows[columnForMove]
    field[columnForMove][row] = player
    draw_x = columnForMove * 50 - 200 + 25
    draw_y = row * 50 - 200 + 25

    up()
    goto(draw_x, draw_y)
    dot(40, player)
    update()

    rows[columnForMove] = row + 1

    # Check for winner
    if check_winner(columnForMove, row, player):
        print(player, "wins!")
        onscreenclick(None)  # Disable clicks when game is over
        winnerPopUp(player)
        return

    # Change player after computer's move
    state['player'] = turns[player]
    printPlayersMoveText(state['player'])

def getRandomColumnForMove(list, randomNumber):
    # Проверяем, есть ли randomNumber в available
    if randomNumber in list:
        print(randomNumber)
        return randomNumber
    else:
        # Если случайный номер недоступен, можно повторить попытку
        print(randomNumber)
        return getRandomColumnForMove(list,randomNumber)  # рекурсивный вызов
            

def getAvailableColumns():
    available = []  # Список для хранения допустимых столбцов
    for col in range(8):  # Перебираем столбцы от 0 до 7
        if state['rows'][col] < 8:  # Если в столбце ещё есть свободное место           
            available.append(col)
    return available


def tap(x, y):
    """Draw red or yellow circle in tapped col."""
    player = state['player']
    
    # If it's computer's turn (yellow), ignore clicks
    if player == 'yellow':
        return

    rows = state['rows']
    col = int((x + 200) // 50)
    if not (0 <= col < 8):
        return
    row = rows[col]
    if row >= 8:
        return

    field[col][row] = player
    x_coord = ((x + 200) // 50) * 50 - 200 + 25
    y_coord = row * 50 - 200 + 25

    up()
    goto(x_coord, y_coord)
    dot(40, player)
    update()

    rows[col] = row + 1
    
    # Check for winner
    if check_winner(col, row, player):
        print(player, "wins!")
        onscreenclick(None)  # Disable clicks when game is over
        winnerPopUp(player)
        return

    # Change player and update text
    state['player'] = turns[player]
    printPlayersMoveText(state['player'])

    # If next move is computer's, run with a small delay
    if state['player'] == 'yellow':
        ontimer(computerMove, 500)


def printPlayersMoveText(player):
    
    playersMoveBoxTurtle.goto(-196, 206)
    playersMoveBoxTurtle.clear()
    playersMoveBoxTurtle.color(player)
    part1 = "'s player"
    part2 = " turn"
    insert_text = player
    new_text = insert_text.capitalize()
    formatted_text = f"{new_text}{part1}{part2}"
    print(formatted_text)

    playersMoveBoxTurtle.write(formatted_text, align="left", font=("Verdana",
                                    24, "normal"))

def winnerPopUp(player):
    insert_text = player
    new_text = insert_text.capitalize()
    win = Tk()
    win.title("Game Over")
    win.geometry("600x200")
    Label(win, text= new_text + " player won!", font=('Verdana 40 bold')).pack(pady=20)
    
    # Create a frame for buttons
    button_frame = Frame(win)
    button_frame.pack(pady=10)
    
    # New Game button
    Button(button_frame, text="New Game", command=lambda: restart_game(win), 
           font=('Verdana', 12), padx=10).pack(side=LEFT, padx=10)
    
    # Quit button that closes both the popup and the main game window
    Button(button_frame, text="Quit", command=lambda: quit_game(win), 
           font=('Verdana', 12), padx=10).pack(side=LEFT, padx=10)


def quit_game(win_window):
    win_window.destroy()  # Close the popup window
    bye()                 # Close the turtle graphics window
    sys.exit()  

def restart_game(win_window=None):
    # Close the winner popup if it exists
    if win_window:
        win_window.destroy()
    
    # Reset game state
    state['player'] = 'red'
    state['rows'] = [0] * 8
    
    # Reset field
    for i in range(8):
        for j in range(8):
            field[i][j] = None
    
    # Clear the screen and redraw
    clear()
    grid()
    
    # Re-enable clicks
    onscreenclick(tap)

setup(440, 520, 370, 0)
playersMoveBoxTurtle = Turtle()

hideturtle()
playersMoveBoxTurtle.hideturtle()
tracer(False)
grid()

print(state['player'])
onscreenclick(tap)
done()
