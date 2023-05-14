import pygame, math, sys

pygame.init()
infoObject = pygame.display.Info() 
HEIGHT = infoObject.current_h
WIDTH = infoObject.current_w

FPS = 60


MAP = (
    '3333333333333333'
    '3      1       3'
    '3      22      3'
    '3      31      3'
    '3      22      3'
    '3      1       3'
    '3      2       3'
    '3      3212321 3'
    '3              3'
    '3    11111     3'
    '3    12221     3'
    '3    12321     3'
    '3    12221     3'
    '3    11111     3'
    '3              3'
    '3333333333333333'
)

MAX_HEIGHT = 3
MAP_SIZE = int(math.sqrt(len(MAP)))
TILE_SIZE = int((WIDTH / 2) / MAP_SIZE)
WALL_CONST = int(round(WIDTH / 50 * 1000, -4))

SPAWN_COL, SPAWN_ROW = 4, 10

CASTED_RAYS = 120
FOV = math.pi / 3
HALF_FOV = FOV / 2
STEP_ANGLE = FOV / CASTED_RAYS
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
SCALE = WIDTH / CASTED_RAYS

win = pygame.display.set_mode((WIDTH, HEIGHT))


pygame.display.set_caption("raycaster")
clock = pygame.time.Clock()

player_x = SPAWN_ROW * TILE_SIZE
player_y = SPAWN_COL *  TILE_SIZE
player_angle = math.pi

def check_col(dir):
    check_x, check_y = player_x, player_y

    if dir == "forward":
        check_x += -math.sin(player_angle) * speed
        check_y += math.cos(player_angle) * speed

    if dir == "back":
        check_x -= -math.sin(player_angle) * speed
        check_y -= math.cos(player_angle) * speed

    if dir == "left":
        check_y += math.sin(player_angle) * speed
        check_x += math.cos(player_angle) * speed

    if dir == "right":
        check_y -= math.sin(player_angle) * speed
        check_x -= math.cos(player_angle) * speed

    c_col, c_row = int(check_x / TILE_SIZE), int(check_y / TILE_SIZE)
    c_square = c_row * MAP_SIZE + c_col

    return MAP[c_square] == ' '

def cast_rays(check):
    start_angle = player_angle - HALF_FOV
    for ray in range(CASTED_RAYS):
        for depth in range(MAX_DEPTH):

            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth
            
            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)
            square = row * MAP_SIZE + col
            
            try:
                if MAP[square] == str(check) or check == "all":
                    if MAP[square] != ' ': 
                        colour = 255 / (1 + depth * depth * 0.0001)
                        depth *= math.cos(player_angle - start_angle)
                        wallheight = WALL_CONST / (depth + 0.0001)

                        left = ray * SCALE
                        wallchange = wallheight * int(MAP[square]) - wallheight - 100
                        top = int(((HEIGHT / 2) - wallheight / 2)) - wallchange
                        height = (wallheight * int(MAP[square])) + 50

                        pygame.draw.rect(win, (colour, colour, colour), (left, top, SCALE, height))
                        
                        break
            except IndexError:
                square = 64
        start_angle += STEP_ANGLE

get_ticks = 1

while True:
    mx, my = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    ticks = pygame.time.get_ticks()

    delta_time = (ticks - get_ticks) / 75
    get_ticks = ticks
    speed = 15 * delta_time

    col = int(player_x / TILE_SIZE)
    row = int(player_y / TILE_SIZE)
    square = row * MAP_SIZE + col

    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit(0)

    pygame.draw.rect(win, (0, 0, 0), (0, 0, WIDTH, HEIGHT))

    for height in range(MAX_HEIGHT, 1, -1):
        cast_rays(height)
    cast_rays("all")
    
    delta_mx = pygame.mouse.get_rel()[0] * delta_time / 250
    if mx < 200 or mx > WIDTH - 200 or my < 200 or my > HEIGHT - 200:
        pygame.mouse.set_pos(WIDTH / 2, HEIGHT / 2)
        delta_mx = 0

    player_angle += delta_mx
    delta_mx = pygame.mouse.get_rel()[0]
    pygame.mouse.set_visible(False)

    if keys[pygame.K_a] and check_col("left"):
        player_y += math.sin(player_angle) * speed
        player_x += math.cos(player_angle) * speed

    if keys[pygame.K_d] and check_col("right"):
        player_y -= math.sin(player_angle) * speed
        player_x -= math.cos(player_angle) * speed


    if keys[pygame.K_w] and check_col("forward"): 
        player_x += -math.sin(player_angle) * speed
        player_y += math.cos(player_angle) * speed

    if keys[pygame.K_s] and check_col("back"):
        player_x -= -math.sin(player_angle) * speed
        player_y -= math.cos(player_angle) * speed
        
    pygame.display.flip()
    pygame.display.set_caption("fps:" + str(int(clock.get_fps())))
    clock.tick(FPS)