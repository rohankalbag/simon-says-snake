import pygame, time, random
import asyncio, json
import threading
from voice_recognition import LISTENER

thread_running = True
thread_lock = threading.Lock()

# Parameters
white_color = (255,255,255)
green_color = (0,255,0)
black_color = (0,0,0)
red_color = (255,0,0)

frame_size_x = 720
frame_size_y = 480

snake_pos = [360, 240]
snake_body = [[360, 240],[360-10, 240],[360-(2*10), 240]]
snake_speed = 4
direction = 'RIGHT'
change_to = direction
directions = []

food_pos = [0,0]
food_spawn = False

score = 0


# Writing thread
def writer_thread(x):
    with thread_lock:
        directions.append(x)


# Reading thread
def reader_thread():
    with thread_lock:
        if len(directions) > 0:
            return directions.pop(0)
        else:
            return None
        

pygame.init()
pygame.display.set_caption('Snake')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
fps_controller = pygame.time.Clock()

def check_if_words_spoken():
    global thread_running
    while thread_running:
        vr = LISTENER()
        transcript = vr.listen().upper().split()
        print(transcript)
        for inst in transcript:
            if inst in ["LEFT", "RIGHT", "UP", "DOWN"]:
                writer_thread(inst)


def snake_game():
    global thread_running
    refresh_snake("RIGHT")
    update_snake()
    while thread_running:
        x = reader_thread()
        if x:
            refresh_snake(x)
            update_snake()


def refresh_snake(x):
    global directions, change_to, direction 
    if x == 'UP':
        change_to = 'UP'
    if x == 'DOWN':
        change_to = 'DOWN'
    if x == 'LEFT':
        change_to = 'LEFT'
    if x == 'RIGHT':
        change_to = 'RIGHT'

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

def update_snake():
    global snake_body,snake_pos,food_pos,score,food_spawn

    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()
        
    create_food()
    update_screen()

    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        game_over()

    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()


def create_food():
    global food_spawn,food_pos
    if(not food_spawn):
        food_pos = [random.randrange(1, int(frame_size_x/10)) * 10,random.randrange(1, int(frame_size_y/10)) * 10]
    food_spawn = True
      

def show_score(pos, color, font, size):
    score_font = pygame.font.SysFont('times new roman', size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (frame_size_x/8, frame_size_y/8)
    game_window.blit(score_surface, score_rect)

def update_screen():
    game_window.fill(black_color)
    show_score(1, white_color, 'times new roman', 20)
    for pos in snake_body:
        pygame.draw.rect(game_window, green_color,pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white_color, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    pygame.display.update()
    fps_controller.tick(snake_speed)

def game_over():
    game_window.fill(black_color)
    my_font = pygame.font.SysFont('times new roman', 100)
    smaller_font = pygame.font.SysFont('times new roman', 20)
    score_alert =  smaller_font.render("Score: "+str(score), True, red_color)
    game_end_alert = my_font.render("YOU DIED", True, red_color)
    alert_rect = game_end_alert.get_rect()
    score_rect = score_alert.get_rect()
    alert_rect.midtop = (frame_size_x/2, frame_size_y/4)
    score_rect.midtop = (frame_size_x/2, 3*frame_size_y/4)
    game_window.blit(game_end_alert, alert_rect)
    game_window.blit(score_alert,score_rect)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    quit()

if __name__ == "__main__":
    thread_1 = threading.Thread(target=check_if_words_spoken)
    thread_2 = threading.Thread(target=snake_game)

    # Start the threads
    thread_1.start()
    thread_2.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        # Terminate the threads when the user interrupts the program
        print("\nProgram interrupted. Terminating threads...")
        thread_running = False
        thread_1.join()
        thread_2.join()