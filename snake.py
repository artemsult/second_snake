import pygame
import sys
import random
import time

COLOR_MAX = 255
COLOR_MIN = 0
WIDTH_MAX = 720
HEIGHT_MAX = 460
FPS = 23
TEXT_SIZE_1 = 24
TEXT_SIZE_2 = 40
TEXT_SIZE_3 = 72
SCORE_X_IN_GAME = 80
SCORE_Y_IN_GAME = 10
SCORE_X = 360
SCORE_Y = 120
GAME_OVER_X = 360
GAME_OVER_Y = 15
SNAKE_HEAD_POS_X = 100
SNAKE_HEAD_POS_Y = 50
SNAKE_BODY_POS_1_X = 100
SNAKE_BODY_POS_1_Y = 50
SNAKE_BODY_POS_2_X = 90
SNAKE_BODY_POS_2_Y = 50
SNAKE_BODY_POS_3_X = 80
SNAKE_BODY_POS_3_Y = 50
MIN_SIZE = 10

class Game():
    def __init__(self):
        self.screen_width = WIDTH_MAX
        self.screen_height = HEIGHT_MAX
        self.red = pygame.Color(COLOR_MAX, COLOR_MIN, COLOR_MIN)
        self.green = pygame.Color(COLOR_MIN, COLOR_MAX, COLOR_MIN)
        self.black = pygame.Color(COLOR_MIN, COLOR_MIN, COLOR_MIN)
        self.white = pygame.Color(COLOR_MAX, COLOR_MAX, COLOR_MAX)
        self.fps_controller = pygame.time.Clock()
        self.score = 0
        self.is_end = False
        self.KEYS = {pygame.K_RIGHT : "RIGHT", ord('d') : "RIGHT",
                    pygame.K_LEFT : "LEFT", ord('a') : "LEFT",
                    pygame.K_UP : "UP", ord('w') : "UP",
                    pygame.K_DOWN : "DOWN", ord('s') : "DOWN"}

    def init_and_check_for_errors(self):
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit(0)
        else:
            print('Ok')

    def set_surface_and_title(self):
        self.play_surface = pygame.display.set_mode((
            self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake Game')

    def event_loop(self, change_to):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                else:
                    for key in self.KEYS:
                        if event.key == key:
                            change_to = self.KEYS[key]
                            break
        return change_to

    def refresh_screen(self):
        pygame.display.flip()
        game.fps_controller.tick(FPS)
    def show_score(self, choice=1):
        s_font = pygame.font.SysFont('monaco', TEXT_SIZE_1)
        s_surf = s_font.render(
            'Score: {0}'.format(self.score), True, self.white)
        s_rect = s_surf.get_rect()
        if choice == 1:
            s_rect.midtop = (SCORE_X_IN_GAME, SCORE_Y_IN_GAME)
        else:
            s_rect.midtop = (SCORE_X, SCORE_Y)
        self.play_surface.blit(s_surf, s_rect)

    def game_over(self):
        go_font = pygame.font.SysFont('monaco', TEXT_SIZE_3)
        go_surf = go_font.render('Game over', True, self.red)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (GAME_OVER_X, GAME_OVER_Y)
        self.play_surface.blit(go_surf, go_rect)
        go_font_1 = pygame.font.SysFont('monaco', TEXT_SIZE_2)
        go_surf_1 = go_font_1.render('Tap space to rastart or esc to end game', True, self.red)
        go_rect_1 = go_surf_1.get_rect()
        go_rect_1.midtop = (GAME_OVER_X, GAME_OVER_Y * 4)
        self.play_surface.blit(go_surf_1, go_rect_1)
        self.show_score(0)
        pygame.display.flip()
        time.sleep(1)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.is_end = True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


class Snake():
    def __init__(self, snake_color):
        self.snake_head_pos = [SNAKE_HEAD_POS_X, SNAKE_HEAD_POS_Y]
        self.snake_body = [[SNAKE_BODY_POS_1_X, SNAKE_BODY_POS_1_Y], 
                            [SNAKE_BODY_POS_2_X, SNAKE_BODY_POS_2_Y],
                            [SNAKE_BODY_POS_3_X, SNAKE_BODY_POS_3_Y]]
        self.snake_color = snake_color
        self.direction = "RIGHT"
        self.change_to = self.direction

    def validate_direction_and_change(self):
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self):
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += MIN_SIZE
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= MIN_SIZE
        elif self.direction == "UP":
            self.snake_head_pos[1] -= MIN_SIZE
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += MIN_SIZE

    def snake_body_mechanism(
            self, score, food_pos, screen_width, screen_height):
        self.snake_body.insert(0, list(self.snake_head_pos))
        if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):
            food_pos = [random.randrange(1, screen_width/MIN_SIZE)*MIN_SIZE,
                        random.randrange(1, screen_height/MIN_SIZE)*MIN_SIZE]
            score += 1
        else:
            self.snake_body.pop()
        return score, food_pos

    def draw_snake(self, play_surface, surface_color):
        play_surface.fill(surface_color)
        for pos in self.snake_body:
            pygame.draw.rect(
                play_surface, self.snake_color, pygame.Rect(
                    pos[0], pos[1], MIN_SIZE, MIN_SIZE))

    def check_for_boundaries(self, game_over, screen_width, screen_height):
        if any((
            self.snake_head_pos[0] > screen_width-MIN_SIZE
            or self.snake_head_pos[0] < 0,
            self.snake_head_pos[1] > screen_height-MIN_SIZE
            or self.snake_head_pos[1] < 0
                )):
            game_over()
        for block in self.snake_body[1:]:
            if (block[0] == self.snake_head_pos[0] and
                    block[1] == self.snake_head_pos[1]):
                game_over()


class Food():
    def __init__(self, food_color, screen_width, screen_height):
        self.food_color = food_color
        self.food_size_x = MIN_SIZE
        self.food_size_y = MIN_SIZE
        self.food_pos = [random.randrange(1, screen_width/MIN_SIZE)*MIN_SIZE,
                         random.randrange(1, screen_height/MIN_SIZE)*MIN_SIZE]

    def draw_food(self, play_surface):
        pygame.draw.rect(
            play_surface, self.food_color, pygame.Rect(
                self.food_pos[0], self.food_pos[1],
                self.food_size_x, self.food_size_y))


game = Game()
snake = Snake(game.white)
food = Food(game.red, game.screen_width, game.screen_height)

game.init_and_check_for_errors()
game.set_surface_and_title()

while True:
    snake.change_to = game.event_loop(snake.change_to)

    snake.validate_direction_and_change()
    snake.change_head_position()
    game.score, food.food_pos = snake.snake_body_mechanism(
        game.score, food.food_pos, game.screen_width, game.screen_height)
    snake.draw_snake(game.play_surface, game.black)

    food.draw_food(game.play_surface)

    snake.check_for_boundaries(
        game.game_over, game.screen_width, game.screen_height)

    if game.is_end == True:
        game.score = 0
        game.is_end = False
        game.init_and_check_for_errors()
        game.set_surface_and_title()
        snake = Snake(game.white)
        snake.change_to = game.event_loop(snake.change_to)
        snake.validate_direction_and_change()

    game.show_score()
    game.refresh_screen()
