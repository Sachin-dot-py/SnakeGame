import turtle
import random
try:
    from playsound import playsound
except:
    print("Unable to import playsound module. Please install with 'pip3 install playsound'")

CELLSIZE = 20
REFRESHTIME = 150
BACKGROUND_COLOR = "light blue"
HEAD_COLOR = "black"
BODY_COLOR = "gray"
FOOD_ICON = "banana50.gif"

SCORE = 0
DIRECTION = "none"
PAUSED = False
SETTINGS = False
COLLISION = False
CHOSEN_CATEGORY = None

BACKGROUND_COLORS = ["Light Blue", "Light Green", "Violet"]
SNAKE_COLORS = ["Black", "White", "Gray", "Red", "Green", "Light Green", "Light Blue", "Light Red", "Navy Blue"]

OPTIONS_DICT = {
    "s" : {1 : 200, 2 : 150, 3 : 75},
    "f" : {1 : "banana50.gif", 2 : "cherry42.gif", 3 : "grape50.gif", 4 : "apple42.gif"},
    "c" : {n+1 : color for n, color in enumerate(BACKGROUND_COLORS)},
    "h" : {n+1 : color for n, color in enumerate(SNAKE_COLORS)},
    "b" : {n+1 : color for n, color in enumerate(SNAKE_COLORS)},
    'd' : {}
}

DISPLAY_OPTIONS = {
    "d": ("GAME DYNAMICS", ["Connected Walls", "Self-Collisions Allowed", "Obstacles", "Swap Head and Tail", "Duplicate Food"]),
    "s" : ("SNAKE SPEED", ["0.5x", "1x", "2x"]),
    "c" : ("BACKGROUND COLOR", BACKGROUND_COLORS),
    "h" : ("SNAKE HEAD COLOR", SNAKE_COLORS),
    "b" : ("SNAKE BODY COLOR" , SNAKE_COLORS)
}

SELECTED_OPS = {
    "d" : [],
    "s" : [2],
    "c" : [1],
    "h" : [1],
    "b" : [3],
    "f" : [1]
}

def start_game():
    setup_screen()
    draw_grid()
    setup_game()
    playsound('start.wav', block=False)
    move_snake()

def clicked_option(option, play=True):
    global CHOSEN_CATEGORY, REFRESHTIME, BACKGROUND_COLOR, BODY_COLOR, HEAD_COLOR, FOOD_ICON, OPS_WRITER, SETTINGS

    for icon in FOOD_ICONS:
        icon.hideturtle()

    if option in OPTIONS_DICT.keys():
        if play: playsound("menu.wav", block=False)
        try:
            OPS_WRITER.clear()
        except:
            OPS_WRITER = turtle.Turtle()

        OPS_WRITER.penup()
        OPS_WRITER.hideturtle()
        CHOSEN_CATEGORY = option
        if option != "f":
            OPS_WRITER.goto(0, 40)
            OPS_WRITER.color("navy blue")
            OPS_WRITER.write(DISPLAY_OPTIONS[option][0], align="center", font=("Futura", 30, "bold"))
            OPS_WRITER.color("black")
            OPS_WRITER.goto(0, 25)

            for n, opt in enumerate(DISPLAY_OPTIONS[option][1]):
                if n + 1 in SELECTED_OPS[option]:
                    opt += " ☑️"
                OPS_WRITER.write(f"({n+1}) {opt}", align="center", font=("Futura", 20, "bold"))
                OPS_WRITER.sety(OPS_WRITER.ycor() - 20)
        else:
            OPS_WRITER.goto(0, 25)
            OPS_WRITER.color("navy blue")
            OPS_WRITER.write("FOOD ICON", align="center", font=("Futura", 30, "bold"))
            OPS_WRITER.color("black")
            OPS_WRITER.goto(-15, 0)

            for n, icon in enumerate(FOOD_ICONS):
                if n + 1 in SELECTED_OPS[option]:
                    ext = " ☑️"
                else:
                    ext = ""

                OPS_WRITER.write(f"({n+1}) {ext}", align="center", font=("Futura", 20, "bold"))
                icon.goto(30, OPS_WRITER.ycor() + 7)
                icon.showturtle()
                OPS_WRITER.sety(OPS_WRITER.ycor() - 20)

    elif option == "Enter":
        # Get rid of listeners, close screen, start game
        for char in OPTIONS_DICT.keys():
            turtle.onkey(None, char)
        for num in range(1,10):
            turtle.onkey(None, num)
        turtle.onkey(None, "Return")
        if SETTINGS:
            global head, body, food, obstacle
            OPS_WRITER.clear()
            turtle.clear()
            head.showturtle()
            SETTINGS = False
            head.color(HEAD_COLOR)
            if 3 in SELECTED_OPS["d"]: # Obstacles
                obstacle.showturtle()
            for part in body:
                part.color(BODY_COLOR)
                part.showturtle()
            if "." in FOOD_ICON:
                for f in food:
                    f.shape(FOOD_ICON)
            else:
                for f in food:
                    f.shape("square")
                    f.color(FOOD_ICON)
            turtle.getscreen().bgcolor(BACKGROUND_COLOR)
            turtle.onkey(lambda: change_direction("up"), "w")
            turtle.onkey(lambda: change_direction("left"), "a")
            turtle.onkey(lambda: change_direction("down"), "s")
            turtle.onkey(lambda: change_direction("right"), "d")
            turtle.listen()
            turtle.tracer(0,0)
            click(400,200)
        else:
            turtle.resetscreen()
            for t in turtle.turtles():
                t.hideturtle()
            start_game()

    else:
        playsound("menu.mov", block=False)
        if CHOSEN_CATEGORY != "d":
            SELECTED_OPS[CHOSEN_CATEGORY] = [option]
        if CHOSEN_CATEGORY == "s":
            REFRESHTIME = OPTIONS_DICT["s"][option]
        elif CHOSEN_CATEGORY == "c":
            BACKGROUND_COLOR = OPTIONS_DICT["c"][option]
        elif CHOSEN_CATEGORY == "b":
            BODY_COLOR = OPTIONS_DICT["b"][option]
        elif CHOSEN_CATEGORY == "h":
            HEAD_COLOR = OPTIONS_DICT["h"][option]
        elif CHOSEN_CATEGORY == "f":
            FOOD_ICON = OPTIONS_DICT["f"][option]
        elif CHOSEN_CATEGORY == "d":
            if option not in SELECTED_OPS[CHOSEN_CATEGORY]:
                SELECTED_OPS[CHOSEN_CATEGORY] = SELECTED_OPS[CHOSEN_CATEGORY] + [option]
            else:
                SELECTED_OPS[CHOSEN_CATEGORY] = [n for n in SELECTED_OPS[CHOSEN_CATEGORY] if n != option]
        clicked_option(CHOSEN_CATEGORY, play=False)


def options_screen():
    global opts_scrn, FOOD_ICONS
    opts_scrn = turtle.Screen()
    opts_scrn.setup(800, 800)
    opts_scrn.setworldcoordinates(-200, -200, 200, 200)
    opts_scrn.title("Snake Game ++ - Options Menu")
    opts_scrn.bgcolor("light blue")
    turtle.hideturtle()
    turtle.tracer(0, 0)

    turtle.penup()
    turtle.goto(0, 160)
    turtle.color("navy blue")
    turtle.write("OPTIONS", align="center", font=("Futura", 30, "bold"))
    turtle.goto(-150,125)
    turtle.color("lime green")
    for option in ["Dynamics (D)", "Speed (S)", "Food (F)", "Background (C)"]:
        turtle.write(option, align="center", font=("Futura", 20, "bold"))
        turtle.setx(turtle.xcor() + 100)
    turtle.goto(-75,100)
    for option in ["Snake Head Color (H)", "Snake Body Color (B)"]:
        turtle.write(option, align="center", font=("Futura", 20, "bold"))
        turtle.setx(turtle.xcor() + 150)
    turtle.goto(0,-175)
    turtle.color("red")
    turtle.write("START GAME (Enter)", align="center", font=("Futura", 40, "bold"))
    turtle.color("black")

    FOOD_ICONS = []
    for file in OPTIONS_DICT["f"].values():
        turtle.register_shape(file)
        icon = create_square(file)
        icon.hideturtle()
        FOOD_ICONS.append(icon)

    for char in OPTIONS_DICT.keys():
        turtle.onkey(lambda char=char: clicked_option(char), char)
    for num in range(1,10):
        turtle.onkey(lambda num=num: clicked_option(num), num)
    turtle.onkey(lambda: clicked_option("Enter"), "Return")
    turtle.listen()
    turtle.tracer(1,1)
    clicked_option("d") # Default to be dynamics options

def setup_screen():
    screen = turtle.getscreen()
    screen.setup(800, 800)
    screen.setworldcoordinates(-200, -200, 200, 200)
    screen.title("Snake Game ++")
    screen.bgcolor(BACKGROUND_COLOR)
    turtle.hideturtle()
    screen.tracer(0, 0)

def setup_game():
    global head, body, food, settings, obstacle

    turtle.register_shape("settings42.gif")
    settings = turtle.Turtle()
    settings.penup()
    settings.shape("settings42.gif")
    settings.goto(188, 192)
    turtle.register_shape("pause42.gif")
    settings = turtle.Turtle()
    settings.penup()
    settings.shape("pause42.gif")
    settings.goto(-188, 192)

    food = [create_square(FOOD_ICON)]
    if 5 in SELECTED_OPS["d"]: # Duplicate Food
        food.append(create_square(FOOD_ICON))
    head = create_square(HEAD_COLOR)
    head.goto(10, 10)
    body = []

    for i in range(3):
        part = create_square(BODY_COLOR)
        part.goto(-CELLSIZE*(i+1)+10, 10)
        body.append(part)

    if 3 in SELECTED_OPS["d"]: # Obstacles
        obstacle = create_square("maroon")
        obstacle.goto(400,400) # Out of frame

    for f in food:
        f.goto(get_random_cell())
    update_score()

    turtle.onkey(lambda: change_direction("up"), "w")
    turtle.onkey(lambda: change_direction("left"), "a")
    turtle.onkey(lambda: change_direction("down"), "s")
    turtle.onkey(lambda: change_direction("right"), "d")
    turtle.onscreenclick(click)
    turtle.listen()

def change_direction(direction):
    global DIRECTION, PAUSED
    if PAUSED: return

    if DIRECTION == "none":
        if direction != "left":
            DIRECTION = direction
    elif direction == "up":
        if DIRECTION != "down":
            DIRECTION = "up"
    elif direction == "down":
        if DIRECTION != "up":
            DIRECTION = "down"
    elif direction == "left":
        if DIRECTION != "right":
            DIRECTION = "left"
    elif direction == "right":
        if DIRECTION != "left":
            DIRECTION = "right"

def move_snake():
    global DIRECTION, COLLISION, SCORE, head, body, obstacle, PAUSED

    if PAUSED:
        turtle.ontimer(move_snake, REFRESHTIME)
        return

    head_coord = head.pos()
    if DIRECTION == "right":
        head.setx(head.xcor() + CELLSIZE)
    elif DIRECTION == "left":
        head.setx(head.xcor() - CELLSIZE)
    elif DIRECTION == "up":
        head.sety(head.ycor() + CELLSIZE)
    elif DIRECTION == "down":
        head.sety(head.ycor() - CELLSIZE)

    for f in food:
        if head.distance(f) < CELLSIZE:
            playsound('crunch.mov', block=False)
            part = create_square(BODY_COLOR) # Will be relocated to the position of the previous tail when every part is moved forward
            body.append(part)

    if head.ycor() > 180 or head.ycor() < -200 or abs(head.xcor()) > 200:
        if 1 in SELECTED_OPS["d"]: # Connected Walls
            if head.xcor() > 200:
                head.setx(-200 + CELLSIZE/2)
            elif head.xcor() < -200:
                head.setx(200 - CELLSIZE/2)
            elif head.ycor() < -200:
                head.sety(180 - CELLSIZE/2)
            elif head.ycor() > 180:
                head.sety(-200 + CELLSIZE/2)
        else:
            COLLISION = True

    if head_coord != head.pos(): # Only move body if head has moved
        playsound('bubble.wav', block=False)
        for n, part in reversed(list(enumerate(body))):
            if n == 0:
                part.goto(*head_coord)
            else:
                part.goto(body[n-1].pos())

    if 3 in SELECTED_OPS["d"]: # Obstacles
        if head.distance(obstacle) < CELLSIZE:
            COLLISION = True

    for f in food:
        if head.distance(f) < CELLSIZE:
            SCORE += 10
            update_score()

            if 4 in SELECTED_OPS["d"]: # Swap head and tail
                head_pos = head.pos()
                head.goto(body[-1].pos())
                body[-1].goto(*head_pos)
                body.insert(0,body.pop()) # Put tail at first position
                body = list(reversed(body)) # Reverse positions because direction of snake is reversed

                xdirection = head.xcor() - body[0].xcor()
                ydirection = head.ycor() - body[0].ycor()

                if xdirection > 0:
                    DIRECTION = "right"
                elif xdirection < 0:
                    DIRECTION = "left"
                elif ydirection > 0:
                    DIRECTION = "up"
                elif ydirection < 0:
                    DIRECTION = "down"

            if 3 in SELECTED_OPS["d"]: # Obstacles
                obstacle.goto(get_random_cell())
                while head.distance(obstacle) < 2*CELLSIZE or f.distance(obstacle) < CELLSIZE:
                    obstacle.goto(get_random_cell())
            f.goto(get_random_cell())

    turtle.update()

    if 2 not in SELECTED_OPS["d"]: # Self-Collisions Allowed
        for part in body:
                if head.distance(part) < CELLSIZE:
                    COLLISION = True

    if COLLISION:
        game_over()
    else:
        turtle.ontimer(move_snake, REFRESHTIME)

def ingame_options():
    global FOOD_ICONS, opts_scrn, head, body, obstacle
    opts_scrn = turtle.getscreen()
    opts_scrn.title("Snake Game ++ - Options Menu")
    turtle.hideturtle()
    turtle.tracer(0, 0)

    turtle.penup()
    turtle.goto(0, 160)
    turtle.color("navy blue")
    turtle.write("OPTIONS", align="center", font=("Futura", 30, "bold"))
    turtle.goto(-75,125)
    turtle.color("lime green")
    for option in ["Background (C)", "Food (F)"]:
        turtle.write(option, align="center", font=("Futura", 20, "bold"))
        turtle.setx(turtle.xcor() + 150)
    turtle.goto(-75,100)
    for option in ["Snake Head Color (H)", "Snake Body Color (B)"]:
        turtle.write(option, align="center", font=("Futura", 20, "bold"))
        turtle.setx(turtle.xcor() + 150)
    turtle.goto(0,-175)
    turtle.color("red")
    turtle.write("RETURN TO GAME (Enter)", align="center", font=("Futura", 40, "bold"))
    turtle.color("black")

    FOOD_ICONS = []
    for file in OPTIONS_DICT["f"].values():
        icon = create_square(file)
        icon.hideturtle()
        FOOD_ICONS.append(icon)
    head.hideturtle()
    for part in body:
        part.hideturtle()
    if 3 in SELECTED_OPS["d"]: # Obstacles
        obstacle.hideturtle()

    for char in ["f","c","h","b"]:
        turtle.onkey(lambda char=char: clicked_option(char), char)
    for num in range(1,10):
        turtle.onkey(lambda num=num: clicked_option(num), num)
    turtle.onkey(lambda: clicked_option("Enter"), "Return")
    turtle.listen()
    turtle.tracer(1,1)
    turtle.update()
    clicked_option("c")


def click(x, y):

    global PAUSED, PAUSEDRAW, SETTINGS
    if x == 400:
        PAUSED = True
        SETTINGS = False

    if y >= 180 and abs(x) > 178 and not SETTINGS and x != 400:
        if x <= -185 or not PAUSED: PAUSED = not PAUSED
        if x >= 185 and x <= 200: SETTINGS = True

        if PAUSED:
            PAUSEDRAW = turtle.Turtle()
            PAUSEDRAW.hideturtle()
            PAUSEDRAW.penup()
            PAUSEDRAW.goto(-200, 200)
            PAUSEDRAW.color("gray")
            PAUSEDRAW.begin_fill()
            for _ in range(4):
                PAUSEDRAW.forward(410)
                PAUSEDRAW.right(90)
            PAUSEDRAW.end_fill()
            if not SETTINGS:
                PAUSEDRAW.color("black")
                PAUSEDRAW.goto(0,0)
                PAUSEDRAW.write("GAME PAUSED", align="center", font=("Futura", 40, "bold"))
                PAUSEDRAW.goto(0,-40)
                PAUSEDRAW.write("Click anywhere to resume.", align="center", font=("Futura", 20, "normal"))
        else:
            try:
                PAUSEDRAW.clear()
                PAUSED = False
            except:
                pass

        if SETTINGS:
            ingame_options()
    elif PAUSED and not SETTINGS:
        PAUSEDRAW.clear()
        PAUSED = False

def play_again():
    global SCORE, DIRECTION, COLLISION
    turtle.clear()
    SCORE = 0
    DIRECTION = "none"
    COLLISION = False
    turtle.onkeypress(None)
    start_game()

def game_over():
    turtle.clear()
    gridpen.clear()
    scorepen.clear()
    head.hideturtle()
    for f in food: f.hideturtle()
    if 3 in SELECTED_OPS["d"]: # Obstacles
        obstacle.hideturtle()
    for part in body:
        part.hideturtle()
    turtle.update()
    playsound('gameover.wav', block=False)
    if save_high_score():
        turtle.penup()
        turtle.goto(0, 90)
        turtle.write("Game Over", align="center", font=("Verdana", 60, "bold"))
        turtle.goto(0, 40)
        turtle.write("New High Score!", align="center", font=("Verdana", 40, "bold"))
        turtle.goto(0, 0)
    else:
        turtle.goto(0, 50)
        turtle.write("Game Over", align="center", font=("Verdana", 60, "bold"))
        turtle.goto(0, 0)
    turtle.write(f"Score: {SCORE}", align="center", font=("Verdana", 60, "bold"))
    turtle.goto(0,-40)
    turtle.write(f"Press any key to play again with your saved settings.", align="center", font=("Verdana", 25, "normal"))
    turtle.onkeypress(play_again)

def update_score():
    high_score = get_high_score()
    if SCORE > high_score:
        high_score = SCORE

    global scorepen
    try:
        scorepen.clear()
    except:
        scorepen = turtle.Turtle()
        scorepen.hideturtle()
        scorepen.penup()

    scorepen.goto(0, 181)
    scorepen.write(f"Score: {SCORE}   High Score: {high_score}", align="center", font=("Verdana", 40, "bold"))
    turtle.update()

def create_square(color):
    square = turtle.Turtle()
    if "." in color: # Custom file
        square.shape(color)
    else:
        square.shape("square")
        square.color(color)
    square.penup()
    square.shapesize(1.9, 1.9, 1)
    return square

def get_random_cell():
    global obstacle
    while True:
        row = random.randint(-9,9)
        column = random.randint(-9,10)
        x = (column*CELLSIZE + (column-1)*CELLSIZE)/2
        y = (row*CELLSIZE + (row-1)*CELLSIZE)/2
        if 3 in SELECTED_OPS["d"]: # Obstacles
            if obstacle.distance(x, y) < CELLSIZE:
                continue
        for object in body + [head]:
            if object.distance(x, y) < CELLSIZE:
                break
        else:
            return x, y

def draw_vertical_line(x):
    gridpen.penup()
    gridpen.goto(x, -200)
    gridpen.pendown()
    gridpen.goto(x, 180)

def draw_horizontal_line(y):
    gridpen.penup()
    gridpen.goto(-200, y)
    gridpen.pendown()
    gridpen.goto(200, y)

def draw_grid():
    global gridpen
    gridpen = turtle.Turtle()
    gridpen.hideturtle()
    gridpen.color("navy blue")
    for i in range(11):
        draw_vertical_line(i*CELLSIZE)
        draw_vertical_line(-i*CELLSIZE)
        if i != 10: draw_horizontal_line(i*CELLSIZE)
        draw_horizontal_line(-i*CELLSIZE)

def get_high_score():
    try:
        with open("score.txt", "r") as f:
            score = int(f.read())
    except:
        score = 0
    return score

def save_high_score():
    score = get_high_score()
    if SCORE > score:
        with open("score.txt", "w") as f:
            f.write(str(SCORE))
        return True
    return False

if __name__ == '__main__':
    options_screen()
    turtle.mainloop()
