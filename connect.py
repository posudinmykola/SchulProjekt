"""Connect Four

Exercises
ssf
1. Change the colors.
2. Draw squares instead of circles for open spaces.
3. Add logic to detect a full row.
4. Create a random computer player.
5. How would you detect a winner?
"""

from turtle import *

from freegames import line

turns = {'red': 'yellow', 'yellow': 'red'}
state = {'player': 'red', 'rows': [0] * 8}
# Инициализация 8x8 массива с None в каждой ячейке
field = [[None for _ in range(8)] for _ in range(8)]
#grid1 = [[None for _ in range(state['rows'])] for _ in range(state['rows'])]


def grid():
    """Draw Connect Four grid."""
    bgcolor('blue')

    for x in range(-150, 200, 50):
        line(x, -200, x, 200)

    for x in range(-175, 200, 50):
        for y in range(-175, 200, 50):
            up()
            goto(x, y)
            dot(40, 'pink')

    update()


def tap(x, y):
    """Draw red or yellow circle in tapped row."""
    
    player = state['player']
    print(player)
    
    rows = state['rows']
    
    row = int((x + 200) // 50)
    print(row)
    count = rows[row]
    print(count)
    field[count][row] = player
    x = ((x + 200) // 50) * 50 - 200 + 25
    y = count * 50 - 200 + 25

    up()
    goto(x, y)
    dot(40, player)
    update()
    
    rows[row] = count + 1
    state['player'] = turns[player]
    for rowOnField in field:
        for elementOnField in rowOnField:
            print(element, end='')
        print()
 


setup(420, 420, 370, 0)
hideturtle()
tracer(False)
grid()
onscreenclick(tap)
done()
