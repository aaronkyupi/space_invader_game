# Space Invader game using python turtle module
# Adapted from pygame to turtle to avoid external dependencies

import turtle
import random
import math
import time

# Set up the screen
screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Space Invaders - Turtle Version")
screen.tracer(0) # Turns off animation for smoother movement

# Score
score_value = 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-380, 260)
score_pen.hideturtle()
score_pen.write(f"Score: {score_value}", align="left", font=("Arial", 16, "normal"))

# Player
player = turtle.Turtle()
player.color("blue")
player.shape("triangle")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)
# Restored to original fast speed
player_speed = 20

# Enemies
num_of_enemies = 6
enemies = []

for i in range(num_of_enemies):
    enemies.append(turtle.Turtle())

for enemy in enemies:
    enemy.color("red")
    enemy.shape("circle")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-380, 380)
    y = random.randint(100, 250)
    enemy.setposition(x, y)

# Kept slow (5 times slower than original 2.0)
enemy_speed = 0.4

# Bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()
# Restored to original fast speed
bullet_speed = 40
bullet_state = "ready"

# Functions
def move_left():
    x = player.xcor()
    x -= player_speed
    if x < -380:
        x = -380
    player.setx(x)

def move_right():
    x = player.xcor()
    x += player_speed
    if x > 380:
        x = 380
    player.setx(x)

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fired"
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

def is_collision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    return distance < 20

# Keyboard bindings
screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(fire_bullet, "space")

# Main game loop
running = True
while running:
    time.sleep(0.01) # Small delay to regulate overall frame rate
    screen.update()

    # Move the bullet
    if bullet_state == "fired":
        y = bullet.ycor()
        y += bullet_speed
        bullet.sety(y)

    if bullet.ycor() > 275:
        bullet.hideturtle()
        bullet_state = "ready"

    # Move enemies (the slow obstacles)
    for enemy in enemies:
        x = enemy.xcor()
        x += enemy_speed
        enemy.setx(x)

        # Move enemy back and down
        if enemy.xcor() > 380 or enemy.xcor() < -380:
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemy_speed *= -1

        # Check for collision
        if is_collision(bullet, enemy):
            bullet.hideturtle()
            bullet_state = "ready"
            bullet.setposition(0, -400)
            # Reset enemy
            x = random.randint(-380, 380)
            y = random.randint(100, 250)
            enemy.setposition(x, y)
            # Update score
            score_value += 1
            score_pen.clear()
            score_pen.write(f"Score: {score_value}", align="left", font=("Arial", 16, "normal"))

        if enemy.ycor() < -230:
            # Game Over logic
            for e in enemies:
                e.hideturtle()
            player.hideturtle()
            score_pen.setposition(0, 0)
            score_pen.write("GAME OVER", align="center", font=("Arial", 24, "bold"))
            running = False
            break

turtle.done()
