import turtle

wn = turtle.Screen()
wn.title("Breakout Game")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

paddle = turtle.Turtle()
paddle.speed(0)
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.penup()
paddle.goto(0, -250)

ball = turtle.Turtle()
ball.speed(1)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, -230)
ball.dx = 2
ball.dy = 2

blocks = []
block_colors = ["red", "green", "blue", "yellow"]
block_width = 60
block_height = 20
block_gap = 5
for i in range(4):
    for j in range(10):
        block = turtle.Turtle()
        block.speed(0)
        block.shape("square")
        block.color(block_colors[i % len(block_colors)])
        block.penup()
        block.goto(-350 + j * (block_width + block_gap), 250 - i * (block_height + block_gap))
        blocks.append(block)

def move_left():
    x = paddle.xcor()
    if x > -350:
        x -= 20
    paddle.setx(x)

def move_right():
    x = paddle.xcor()
    if x < 350:
        x += 20
    paddle.setx(x)

wn.listen()
wn.onkey(move_left, "Left")
wn.onkey(move_right, "Right")

def game_loop():
    global ball, blocks

    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    if ball.xcor() > 390:
        ball.setx(390)
        ball.dx *= -1

    if ball.xcor() < -390:
        ball.setx(-390)
        ball.dx *= -1

    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() < -290:
        ball.goto(0, -230)
        ball.dy *= -1

    if (ball.ycor() > paddle.ycor() - 10 and ball.ycor() < paddle.ycor() + 10) and (ball.xcor() > paddle.xcor() - 50 and ball.xcor() < paddle.xcor() + 50):
        ball.dy *= -1

    for block in blocks:
        if ball.distance(block) < 30:
            block.hideturtle()
            blocks.remove(block)
            ball.dy *= -1
            break

    wn.update()

    if not blocks:
        ball.goto(0, 0)
        paddle.goto(0, -250)
        print("¡Has ganado!")
        return 

    wn.ontimer(game_loop, 10)

game_loop()
wn.mainloop()
