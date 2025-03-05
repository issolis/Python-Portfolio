import turtle
import random
import math

# Set up the screen
screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Space Invaders")
screen.tracer(0)  # Turn off screen updates for smoother animation

# Create the player
player = turtle.Turtle()
player.shape("triangle")
player.color("green")
player.penup()
player.goto(0, -250)
player.setheading(90)  # Point the player upwards

playerspeed = 15

def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
        x = -280
    player.setx(x)

def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x)

screen.listen()
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")

# Create the bullet
bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("yellow")
bullet.penup()
bullet.shapesize(0.5, 0.1)
bullet.hideturtle()

bulletspeed = 20
bulletstate = "ready"  # "ready" means ready to fire, "fire" means bullet is firing

def fire_bullet():
    global bulletstate
    if bulletstate == "ready":
        bulletstate = "fire"
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

screen.onkey(fire_bullet, "space")

# Create the enemies
number_of_enemies = 5
enemies = []

for i in range(number_of_enemies):
    enemy = turtle.Turtle()
    enemy.shape("square")
    enemy.color("red")
    enemy.penup()
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.setposition(x, y)
    enemies.append(enemy)

enemyspeed = 0.1

def move_enemies():
    global enemyspeed
    for enemy in enemies:
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)
        if enemy.xcor() > 280 or enemy.xcor() < -280:
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemyspeed *= -1

def is_collision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 25:
        return True
    else:
        return False

# Main game loop
while True:
    move_enemies()

    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"

    for enemy in enemies:
        if is_collision(bullet, enemy):
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)

        if is_collision(player, enemy):
            player.hideturtle()
            bullet.hideturtle()
            for e in enemies:
                e.hideturtle()
            screen.bgcolor("red")
            break

    screen.update()
