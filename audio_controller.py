import pygame, time, random
import sounddevice as sd
from deepgram import Deepgram
import asyncio, json
import soundfile as sf
import os

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

pygame.init()
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
fps_controller = pygame.time.Clock()

def check_for_events():
    print("Speak Now:")
    fs = 44100
    duration = 4
    myrecording = sd.rec(duration * fs, samplerate=fs, channels=2,dtype='float64')
    sd.wait()
    print("Don't Speak Now:")
    sf.write("dummy.wav", myrecording, fs)
    #Enter your API KEY
    DEEPGRAM_API_KEY = 'ENTER YOUR API KEY HERE'
    PATH_TO_FILE = os.getcwd() + '\dummy.wav'

    async def main():
        global directions
        # Initialize the Deepgram SDK
        dg_client = Deepgram(DEEPGRAM_API_KEY)
        # Open the audio file
        with open(PATH_TO_FILE, 'rb') as audio:
            # Replace mimetype as appropriate
            source = {'buffer': audio, 'mimetype': 'audio/wav'}
            response = await dg_client.transcription.prerecorded(source, {'punctuate': False})
            x = json.loads(json.dumps(response, indent=4))
            x = str(x["results"]["channels"][0]["alternatives"][0]["transcript"]).upper().split()
            for i in x:
                if(i in ['LEFT','RIGHT','UP','DOWN']):
                    directions.append(i)

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

def refresh_snake():
    global directions, change_to, direction
    x = directions.pop(0)
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
    
    #print(directions)

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


while True:
    check_for_events()
    while(len(directions)>0):
        refresh_snake()
        update_snake()
    else:
        directions += [direction]