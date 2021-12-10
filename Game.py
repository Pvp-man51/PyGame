import pygame, sys, random

class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos, y_pos))

class Player(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0
    
    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()

class Ball(Block):
    def __init__(self, path, x_pos, y_pos, speed_x, speed_y, paddels):
        super().__init__(path, x_pos, y_pos)
        self.speed_x = speed_x * random.choice((1, -1))
        self.speed_y = speed_y * random.choice((1, -1))
        self.paddels = paddels
        self.active = False
        self.score_time = 0
    
    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisons()
        else:
            self.restart_counter()

    def collisons(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            pygame.mixer.Sound.play(pong_sound)
            self.speed_y *= -1
            
        if pygame.sprite.spritecollide(self, self.paddels, False):
            pygame.mixer.Sound.play(pong_sound)
            collision_paddel = pygame.sprite.spritecollide(self, self.paddels, False)[0].rect
            if abs(self.rect.right - collision_paddel.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddel.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.top - collision_paddel.bottom) < 10 and self.speed_x < 0:
                self.rect.top = collision_paddel.bottom
                self.speed_y *= -1
            if abs(self.rect.bottom - collision_paddel.top) < 10 and self.speed_x > 0:
                self.rect.bottom = collision_paddel.top
                self.speed_y *= -1
    
    def reset_ball(self):
        self.active = False
        self.speed_x *= random.choice((-1, 1))
        self.speed_y *= random.choice((-1, 1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width / 2, screen_height / 2)
        pygame.mixer.Sound.play(score_sound)

    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3
        
        if current_time - self.score_time <= 700:
            countdown_number = 3
        if 700 < current_time - self.score_time <= 1400:
            countdown_number = 2
        if 1400 < current_time - self.score_time <= 2100:
            countdown_number = 1
        if current_time - self.score_time >= 2100:
            self.active = True

        time_counter = game_font.render(str(countdown_number), True, accent_color)
        time_counter_rect = time_counter.get_rect(center = (screen_width / 2, screen_height / 2 + 50))
        pygame.draw.rect(screen, bg_color, time_counter_rect)
        screen.blit(time_counter, time_counter_rect)

class Opponent(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
    
    def update(self, ball_group):
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.y:
            self.rect.y -= self.speed
        self.constrain

    def constrain(self):
        if self.rect.top <= 0: 
            self.rect.top == 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            
class GameManager:
    def __init__(self, ball_group, paddle_group):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group
        self.startGame = False
    
    def run_game(self):
        if self.startGame == True:
            # Drawing the game objects
            self.paddle_group.draw(screen)
            self.ball_group.draw(screen)

            # Updating the game objects
            self.paddle_group.update(self.ball_group)
            self.ball_group.update()
            self.reset_ball()
            self.draw_score()
        else:
            # Titel text
            start_title = game_font.render(str("Press 'space' to Start Game"), True, accent_color)
            start_title_rect = start_title.get_rect(center = (screen_width/ 2, screen_height / 2))

            pygame.draw.rect(screen, bg_color, start_title_rect)
            screen.blit(start_title, start_title_rect)

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.reset_ball()

    def draw_score(self):
        player_score = game_font.render(str(self.player_score), True, accent_color)
        opponent_score = game_font.render(str(self.opponent_score), True, accent_color)

        player_score_rect = player_score.get_rect(midleft = (screen_width/ 2 + 40, screen_height/ 2))
        opponent_score_rect = opponent_score.get_rect(midright = (screen_width/ 2 - 40, screen_height/ 2))

        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)            

# General Setup
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# Setting up the Window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")
icon = pygame.image.load("Sprites\Ball.png")
pygame.display.set_icon(icon)

# Global Variabels
bg_color = pygame.Color("#2F373F")
accent_color = (27, 35, 43)
game_font = pygame.font.Font("freesansbold.ttf", 32)
pong_sound = pygame.mixer.Sound("Sounds\Pong.wav")
score_sound = pygame.mixer.Sound("Sounds\Score.wav")
middle_strip = pygame.Rect(screen_width/ 2 - 2, 0, 4, screen_height)

# Game objects
player = Player("Sprites\Paddle.png", screen_width - 20, screen_height/ 2, 10)
opponent = Opponent("Sprites\Paddle.png", 20, screen_height/2, 10)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

ball = Ball("Sprites\Ball.png", screen_width/ 2, screen_height/ 2, 8, 8, paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game_manager = GameManager(ball_sprite, paddle_group)

# Load and play music
pygame.mixer.music.load("Sounds\Music1.mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.1)
pygame.event.wait()

while True:

    # Handeling Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and game_manager.startGame == False:
                game_manager.startGame = True

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            #Arrow keys movement
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.movement += player.speed
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.movement -= player.speed
            
        if event.type == pygame.KEYUP:

            #Arrow keys movement
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.movement -= player.speed
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.movement += player.speed

    # Background
    screen.fill(bg_color)
    pygame.draw.rect(screen, accent_color, middle_strip)

    # Run the game
    game_manager.run_game()

    # Rendering
    pygame.display.flip()
    clock.tick(60)
