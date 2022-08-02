import pygame
from random import randint

pygame.init()

black = (0, 0, 0)
red = (150, 0, 0)
white = (225, 225, 225)
pygame.mixer.music.load('atari.mp3')
pygame.mixer.music.play(-1)

# SCREEN ATTRIBUTES
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
background = white

# BALL SPEED
speed = [1, -2]


class InfoText:
    def __init__(self):
        self.colour = red
        self.x = width // 2
        self.y = height - 220
        self.size = 20
        self.text = "PRESS 'S' TO START AND THEN 'SPACE' TO THROW THE BALL"

    def write_info_text(self):
        text = pygame.font.SysFont("timesnewroman", self.size, True, True)
        label = text.render(self.text, True, self.colour)
        screen.blit(label, (self.x - label.get_width() // 2, self.y))


class ScoreText:
    def __init__(self):
        self.colour = red
        self.x = width - 50
        self.y = 20
        self.size = 30
        self.text = "SCORE: "

    def write_score_text(self):
        text = pygame.font.SysFont("timesnewroman", self.size, True, True)
        label = text.render(self.text + str(game_ball.move_ball()), True, self.colour)
        screen.blit(label, (self.x - label.get_width(), self.y))


class LifeText:
    def __init__(self):
        self.colour = red
        self.x = 50
        self.y = 20
        self.size = 30
        self.text = "LIVES: "

    def write_life_text(self):
        text = pygame.font.SysFont("timesnewroman", self.size, True, True)
        label = text.render(self.text + str(game_ball.lives), True, self.colour)
        screen.blit(label, (self.x, self.y))


class Ball:
    def __init__(self):
        self.ball = pygame.image.load("ball.png")
        self.rect = self.ball.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.score = 0
        self.lives = 5
        self.state = "passive"

    def draw_ball(self):
        pygame.draw.rect(screen, background, self.rect)

    def move_ball(self):
        paddle = game_paddle.paddle
        self.rect.x += speed[0]
        self.rect.y += speed[1]
        # GAME SCREEN COLLISION
        # GAME SCREEN LEFT AND RIGHT
        if self.rect.left < 0:
            self.rect.x = 0
            if speed[0] == -2:
                speed[0] = -speed[0]
            else:
                speed[0] = 1
        if self.rect.right > width:
            self.rect.left = width - self.rect.width
            if speed[0] == 2:
                speed[0] = -speed[0]
            else:
                speed[0] = -1
        # GAME SCREEN TOP
        if self.rect.top < 0:
            speed[1] = -speed[1]
        # PADDLE COLLISION
        # PADDLE TOP
        if self.rect.bottom > paddle.bottom:
            speed[1] = speed[1]
        else:
            if self.rect.bottom > paddle.top and paddle.topleft < self.rect.midbottom < paddle.topright:
                speed[1] = -speed[1]
        # PADDLE TOP RIGHT
        if self.rect.collidepoint(paddle.topright):
            speed[0] = 2
            speed[1] = -1
        # PADDLE TOP LEFT
        if self.rect.collidepoint(paddle.topleft):
            speed[0] = -2
            speed[1] = -1
        # BRICK COLLISION
        for i in brick_list:
            # BRICK TOP AND BOTTOM
            if i.brick.top < self.rect.top < i.brick.bottom \
                    and i.brick.topleft < self.rect.midtop < i.brick.topright \
                    or i.brick.top < self.rect.bottom < i.brick.bottom \
                    and i.brick.bottomleft < self.rect.midbottom < i.brick.bottomright:
                if i.colour != white:
                    i.colour = white
                    speed[1] = -speed[1]
                    self.score += 1
                else:
                    speed[1] = speed[1]
            # BRICK TOP LEFT CORNER
            if self.rect.collidepoint(i.brick.topleft):
                if speed[0] == -1 or speed[0] == -2:
                    if i.colour != white:
                        i.colour = white
                        speed[1] = -speed[1]
                        self.score += 1
                    else:
                        speed[1] = speed[1]
                if speed[0] == 1 or speed[0] == 2:
                    if speed[1] == -1 or speed[1] == -2:
                        if i.colour != white:
                            i.colour = white
                            speed[0] = -speed[0]
                            self.score += 1
                        else:
                            speed[1] = speed[1]
                    if speed[1] == 1 or speed[1] == 2:
                        if i.colour != white:
                            i.colour = white
                            speed[0] = -speed[0]
                            speed[1] = -speed[1]
                            self.score += 1
                        else:
                            speed[1] = speed[1]
            # BRICK TOP RIGHT CORNER
            if self.rect.collidepoint(i.brick.topright):
                if speed[0] == -1 or speed[0] == -2:
                    if speed[1] == -1 or speed[1] == -2:
                        if i.colour != white:
                            i.colour = white
                            speed[0] = -speed[0]
                            self.score += 1
                        else:
                            speed[1] = speed[1]
                    if speed[1] == 1 or speed[1] == 2:
                        if i.colour != white:
                            i.colour = white
                            speed[0] = -speed[0]
                            speed[1] = -speed[1]
                            self.score += 1
                        else:
                            speed[1] = speed[1]
                if speed[0] == 1 or speed[0] == 2:
                    if i.colour != white:
                        i.colour = white
                        speed[1] = -speed[1]
                        self.score += 1
                    else:
                        speed[1] = speed[1]
            # BRICK BOTTOM LEFT CORNER
            if self.rect.collidepoint(i.brick.bottomleft):
                if speed[0] == -1 or speed[0] == -2:
                    if i.colour != white:
                        i.colour = white
                        speed[1] = -speed[1]
                        self.score += 1
                    else:
                        speed[1] = speed[1]
                if speed[0] == 1 or speed[0] == 2:
                    if speed[1] == -1 or speed[1] == -2:
                        if i.colour != white:
                            i.colour = white
                            speed[0] = -speed[0]
                            speed[1] = -speed[1]
                            self.score += 1
                        else:
                            speed[1] = speed[1]
                    if speed[1] == 1 or speed[1] == 2:
                        if i.colour != white:
                            i.colour = white
                            speed[0] = -speed[0]
                            self.score += 1
                        else:
                            speed[1] = speed[1]
            # BRICK BOTTOM RIGHT CORNER
            if self.rect.collidepoint(i.brick.bottomright):
                if speed[0] == -1 or speed[0] == -2:
                    if speed[1] == -1 or speed[1] == -2:
                        if i.colour != white:
                            i.colour = white
                            speed[0] = -speed[0]
                            speed[1] = -speed[1]
                            self.score += 1
                        else:
                            speed[1] = speed[1]
                    if speed[1] == 1 or speed[1] == 2:
                        if i.colour != white:
                            i.colour = white
                            speed[0] = -speed[0]
                            self.score += 1
                        else:
                            speed[1] = speed[1]
                if speed[0] == 1 or speed[0] == 2:
                    if i.colour != white:
                        i.colour = white
                        speed[1] = -speed[1]
                        self.score += 1
                    else:
                        speed[1] = speed[1]

            # BRICK LEFT AND RIGHT
            if self.rect.collidepoint(i.brick.left, i.brick.top + i.brick.height // 2) \
                    or self.rect.collidepoint(i.brick.right, i.brick.top + i.brick.height // 2):
                if i.colour != white:
                    i.colour = white
                    speed[0] = -speed[0]
                    self.score += 1
                else:
                    speed[0] = speed[0]
        return self.score


class Brick:
    def __init__(self, x, y, colour):
        self.brick = pygame.Rect(x, y, 100, 30)
        self.colour = colour

    def draw_brick(self):
        pygame.draw.rect(screen, self.colour, self.brick)
        pygame.draw.rect(screen, white, self.brick, 2)


class Paddle:
    def __init__(self):
        self.paddle = pygame.Rect(width // 2 - 150 // 2, height - 100, 150, 10)

    def draw_paddle(self):
        pygame.draw.rect(screen, red, self.paddle)

    def move_paddle(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.paddle.left > 0:
            self.paddle.x -= 5
        if key[pygame.K_RIGHT] and self.paddle.right < width:
            self.paddle.x += 5


# CLASS INSTANCE CREATIONS
game_ball = Ball()
game_paddle = Paddle()
game_info_text = InfoText()
game_score_text = ScoreText()
game_life_text = LifeText()

# CREATING THE BRICK WALL
brick_list = []
brick_x = 0
brick_y = 70
for j in range(8):
    for k in range(width // 100):
        game_brick = Brick(brick_x, brick_y, black)
        brick_x += 100
        brick_list.append(game_brick)
    brick_x = 0
    brick_y += 30

# SCREEN LOOP
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # INITIAL START OR RESTART CONDITION
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                if game_info_text.colour != white:
                    game_info_text.colour = white
                    game_ball.lives = 5
                    game_ball.score = 0
                    game_paddle.paddle.x = width // 2 - 75
                    game_paddle.paddle.y = height - 100
                    speed = [1, -2]
                    for b in brick_list:
                        b.colour = (randint(0, 200), randint(0, 200), randint(0, 200))
            # THROWING THE BALL CONDITION
            if event.key == pygame.K_SPACE:
                if game_info_text.colour != red:
                    game_ball.state = "active"
            # QUIT THE GAME WITH 'ESC'
            if event.key == pygame.K_ESCAPE:
                run = False
    # CONDITION TO LOSE A LIFE
    if game_ball.rect.bottom >= height:
        game_ball.state = "passive"
        game_ball.lives -= 1
        speed = [1, -2]
    # CONDITION TO LOSE THE GAME
    if game_ball.lives == 0:
        game_ball.state = "passive"
        game_info_text.text = "GAME OVER! PRESS 'S' TO RESTART OR 'ESC' TO QUIT"
        game_info_text.colour = red
    # CONDITION TO WIN THE GAME
    if game_ball.score == len(brick_list):
        game_ball.state = "passive"
        game_ball.score = 0
        game_ball.lives = 5
        game_info_text.text = "CONGRATULATIONS! YOU WIN! PRESS 'S' TO RESTART OR 'ESC' TO QUIT"
        game_info_text.colour = red

    # SCREEN AND TEXT
    screen.fill(background)
    game_info_text.write_info_text()
    game_score_text.write_score_text()
    game_life_text.write_life_text()

    # CREATING THE BRICKS IN THE GAME WINDOW
    for b in brick_list:
        b.draw_brick()

    game_ball.draw_ball()

    # GAME BALL STATE
    if game_ball.state == "active":
        game_ball.move_ball()
    if game_ball.state == "passive":
        # CONNECTING THE GAME BALL AND THE GAME PADDLE
        game_ball.rect.x = game_paddle.paddle.x + 67
        game_ball.rect.y = height - 116

    # PADDLE
    game_paddle.draw_paddle()
    game_paddle.move_paddle()

    # SCREEN UPDATE
    screen.blit(game_ball.ball, game_ball.rect)
    pygame.display.update()
