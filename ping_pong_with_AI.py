import pygame
import sys
import random
import math
import time
import numpy as np
import pickle
import glob
import os

table_path = "tables/"

def load_q_table_and_params(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    print(f"Данные загружены из файла {filename}")
    return data['Q'], data['alpha'], data['gamma'], data['epsilon'], data['epsilon_decay'], data['epsilon_min'], data['counter']

def get_proper_file(directory, level):
    files = glob.glob(os.path.join(directory, "*"))
    if level == "easy":
        return None
    if level == "medium":
        _file = "tables/gen_1_q_table_and_params_4901.pkl"
    if level == "hard":
        _file = "tables/gen_2_q_table_and_params_4901.pkl"
    return _file

pygame.mixer.init()
pygame.init()

sound_effect = pygame.mixer.Sound('sound/click.wav')
sound_effect2 = pygame.mixer.Sound('sound/pass_win.wav')
sound_effect3 = pygame.mixer.Sound('sound/pass_loose.wav')

WIDTH, HEIGHT = 600, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Понг с двумя игроками")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

background = pygame.image.load('img/background.jpg')
paddle = pygame.image.load('img/paddle.png')
ball = pygame.image.load('img/ball.png')

# Функция для отображения меню выбора уровня
def show_menu():
    menu_running = True
    selected_level = None
    hovered_level = None

    # Загружаем фон для меню
    menu_bg = pygame.Surface((WIDTH, HEIGHT))
    menu_bg.blit(background, (0, 0))

    # Создаем затемнение
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    menu_bg.blit(overlay, (0, 0))

    # Шрифты
    title_font = pygame.font.Font(None, 70)
    level_font = pygame.font.Font(None, 64)
    description_font = pygame.font.Font(None, 36)

    # Текст заголовка
    title_text = title_font.render("ВЫБЕРИТЕ УРОВЕНЬ", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH//2, 200))

    # Текст для уровней с описанием
    levels = [
        {"name": "ЛЕГКИЙ", "description": "Простой алгоритм", "level": "easy", "color": GREEN, "rect": None, "desc_rect": None},
        {"name": "СРЕДНИЙ", "description": "ИИ первого поколения", "level": "medium", "color": YELLOW, "rect": None, "desc_rect": None},
        {"name": "ТЯЖЕЛЫЙ", "description": "ИИ второго поколения", "level": "hard", "color": RED, "rect": None, "desc_rect": None}
    ]

    # Позиции для уровней
    y_positions = [350, 475, 600]

    # Текст инструкции
    instruction_text = description_font.render("Нажмите на выбранный уровень", True, GRAY)
    instruction_rect = instruction_text.get_rect(center=(WIDTH//2, 750))

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                # Проверяем наведение мыши
                mouse_pos = pygame.mouse.get_pos()
                hovered_level = None
                for i, level_info in enumerate(levels):
                    if level_info["rect"] and level_info["rect"].collidepoint(mouse_pos):
                        hovered_level = i
                        break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Проверяем клик по уровню
                mouse_pos = pygame.mouse.get_pos()
                for level_info in levels:
                    if level_info["rect"] and level_info["rect"].collidepoint(mouse_pos):
                        selected_level = level_info["level"]
                        # Подсветка выбранного уровня
                        screen.blit(menu_bg, (0, 0))

                        # Рисуем подсветку
                        highlight_rect = level_info["rect"].inflate(20, 20)
                        pygame.draw.rect(screen, level_info["color"], highlight_rect, 3)

                        # Обновляем текст
                        screen.blit(title_text, title_rect)
                        for i, lvl in enumerate(levels):
                            color = lvl["color"]
                            # Основной текст уровня
                            text = level_font.render(lvl["name"], True, color)
                            text_rect = text.get_rect(center=(WIDTH//2, y_positions[i]))
                            levels[i]["rect"] = text_rect
                            screen.blit(text, text_rect)

                            # Описание уровня
                            desc_text = description_font.render(lvl["description"], True, GRAY)
                            desc_rect = desc_text.get_rect(center=(WIDTH//2, y_positions[i] + 30))
                            levels[i]["desc_rect"] = desc_rect
                            screen.blit(desc_text, desc_rect)

                        screen.blit(instruction_text, instruction_rect)
                        pygame.display.flip()
                        sound_effect.play()

                        # Пауза на 0.5 секунды
                        pygame.time.wait(500)

                        menu_running = False
                        break

        if menu_running:
            # Отрисовка меню
            screen.blit(menu_bg, (0, 0))

            # Рисуем заголовок
            screen.blit(title_text, title_rect)

            # Рисуем уровни
            for i, level_info in enumerate(levels):
                # Определяем цвет для основного текста
                if hovered_level == i:
                    main_color = WHITE
                else:
                    main_color = level_info["color"]

                # Основной текст уровня
                text = level_font.render(level_info["name"], True, main_color)
                text_rect = text.get_rect(center=(WIDTH//2, y_positions[i]))
                levels[i]["rect"] = text_rect

                # Описание уровня (всегда серым цветом)
                desc_text = description_font.render(level_info["description"], True, GRAY)
                desc_rect = desc_text.get_rect(center=(WIDTH//2, y_positions[i] + 30))
                levels[i]["desc_rect"] = desc_rect

                # Добавляем эффект при наведении
                if hovered_level == i:
                    # Рисуем прямоугольник вокруг основного текста
                    pygame.draw.rect(screen, WHITE, text_rect.inflate(20, 10), 2)

                screen.blit(text, text_rect)
                screen.blit(desc_text, desc_rect)

            # Рисуем инструкцию
            screen.blit(instruction_text, instruction_rect)

            pygame.display.flip()

    return selected_level

# Показываем меню и получаем выбранный уровень
LEVEL = show_menu()
print(f"Выбран уровень: {LEVEL}")

court_width = int(WIDTH * 1)
court_height = int(HEIGHT * 1)
court_x = (WIDTH - court_width) // 2
court_y = (HEIGHT - court_height) // 2

ball_radius = 10
ball_x = court_x + court_width // 2
ball_y = court_y + 10
ball_speed = 10
angle = random.uniform(-17, 17)
ball_dx = ball_speed * math.sin(math.radians(angle))
ball_dy = ball_speed * math.cos(math.radians(angle))

paddle_width = 100
paddle_height = 20
paddle_x = (WIDTH - paddle_width) // 2
paddle_y = HEIGHT - paddle_height - 10
paddle_speed = 6

paddle2_x = (WIDTH - paddle_width) // 2
paddle2_y = court_y + 10
paddle2_speed = 6

def draw_court():
    pygame.draw.rect(screen, WHITE, (court_x, court_y, court_width, court_height), 2)

def draw_ball(x, y):
    screen.blit(ball, (x - ball_radius, y - ball_radius))

def draw_paddle(x, y):
    screen.blit(paddle, (x, y))

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def clever_motion(paddle2_x, paddle2_y, ball_x, ball_y, ball_dx, ball_dy):
    use_alg1 = True
    use_alg2 = True
    use_alg3 = True
    use_alg4 = True

    res = []

    if (use_alg1):
        if (ball_x < paddle2_x + paddle_width/2 - 0.1 * paddle_width):
            res += [2,6,7]

        if (ball_x > paddle2_x + paddle_width/2 + 0.1 * paddle_width):
            res += [3,4,5]

    if (use_alg2 and ball_dy < 0):
        t_bump = abs((ball_y - paddle2_y) / ball_dy)
        x_bump = ball_x + ball_dx * t_bump
        if (x_bump > WIDTH): x_bump = 2*WIDTH - x_bump
        if (x_bump < 0): x_bump = - x_bump

        if (x_bump > paddle2_x + paddle_width * 0.6): res += [3,4,5]
        if (x_bump < paddle2_x + paddle_width * 0.4): res += [2,6,7]

    if (use_alg3):
        if(ball_dy > 0) and abs(paddle2_y - paddle_y) > HEIGHT * 0.4:
            if (paddle2_x < 0.5 * WIDTH): res += [3] #восток
            if (paddle2_x > 0.5 * WIDTH): res += [2] #запад

    if (use_alg4 and ball_dy < 0 and (abs(ball_y - paddle2_y) < paddle_width * 4.2)):
        t_bump = abs((ball_y - paddle2_y) / ball_dy)
        x_bump = ball_x + ball_dx * t_bump
        if (x_bump > WIDTH): x_bump = 2*WIDTH - x_bump
        if (x_bump < 0): x_bump = - x_bump
        center = paddle2_x + paddle_width * 0.5
        edge1 = paddle2_x
        edge2 = paddle2_x + paddle_width
        shift = paddle_width * 0.2
        point1 = edge1 + shift
        point2 = edge2 - shift
        if (x_bump < center):
            if abs(point1 - x_bump) < paddle_width * 0.1:
                res+=[8]
            elif (point1 < x_bump):
                res += [3,4,5]
            elif (point1 > x_bump):
                res += [2,6,7]
        if (x_bump > center):
            if abs(point2 - x_bump) < paddle_width * 0.1:
                res+=[8]
            elif (point2 < x_bump):
                res += [3]
            elif (point2 > x_bump):
                res += [2]

    return(res)

def calculate_reflection(ball_x, ball_dx, paddle_x):
    hit_position = ball_x - paddle_x
    k = 15
    dr = (ball_x - (paddle_x + paddle_width / 2)) / paddle_width
    new_dx = ball_dx + k * dr
    new_dx1 = new_dx
    if abs(new_dx / ball_dy) > 1:
        new_dx = ball_dy
        if new_dx * new_dx1 < 0: new_dx = -new_dx
    norm = (ball_dy**2 + ball_dx**2)**0.5 / (ball_dy**2 + new_dx**2)**0.5
    return -ball_dy * norm, new_dx * norm

def auto_move_paddle_p1(paddle_x, paddle_y, ball_x, ball_y, paddle_speed):
    target_x = ball_x - paddle_width // 2
    target_y = ball_y - paddle_height // 2
    target_y = HEIGHT - 10
    target_x = max(0, min(target_x, WIDTH - paddle_width))

    if paddle_x < target_x:
        paddle_x += min(paddle_speed, target_x - paddle_x)
    elif paddle_x > target_x:
        paddle_x -= min(paddle_speed, paddle_x - target_x)

    return paddle_x, paddle_y

ball_x_discrete_num = 5
ball_y_discrete_num = 5
paddle_x_discrete_num = 5
paddle_y_discrete_num = 5
paddle2_x_discrete_num = 5
paddle2_y_discrete_num = 5
ball_dx_discrete_num = 5
ball_dy_discrete_num = 5

state_space_size = (ball_x_discrete_num, ball_y_discrete_num, paddle_x_discrete_num, paddle_y_discrete_num, paddle2_x_discrete_num, paddle2_y_discrete_num, ball_dx_discrete_num, ball_dy_discrete_num)

def discretize_state(ball_x, ball_y, paddle_x, paddle_y, paddle2_x, paddle2_y, ball_dx, ball_dy):
    ball_x_discrete = int(np.floor(ball_x / (WIDTH / ball_x_discrete_num)))  # 10 уровней по X
    ball_y_discrete = int(np.floor(ball_y / (HEIGHT / ball_y_discrete_num)))  # 10 уровней по Y
    paddle_x_discrete = int(np.floor(paddle_x / (WIDTH / paddle_x_discrete_num)))  # 10 уровней по X
    paddle_y_discrete = int(np.floor((paddle_y - HEIGHT) / (HEIGHT / paddle_y_discrete_num)))  # 10 уровней по Y
    paddle2_x_discrete = int(np.floor(paddle2_x / (WIDTH / paddle2_x_discrete_num)))  # 10 уровней по X
    paddle2_y_discrete = int(np.floor(paddle2_y / (HEIGHT / paddle2_y_discrete_num)))  # 10 уровней по Y
    ball_dx_discrete = int(np.floor((ball_dx + ball_speed) / (2*ball_speed / ball_dx_discrete_num)))  # 5 уровней по X
    ball_dy_discrete = int(np.floor((ball_dy + ball_speed)/ (2*ball_speed / ball_dy_discrete_num))) # 5 уровней по Y

    ball_x_discrete = np.clip(ball_x_discrete, 0, ball_x_discrete_num - 1)
    ball_y_discrete = np.clip(ball_y_discrete, 0, ball_y_discrete_num - 1)
    paddle_x_discrete = np.clip(paddle_x_discrete, 0, paddle_x_discrete_num - 1)
    paddle_y_discrete = np.clip(paddle_y_discrete, 0, paddle_y_discrete_num - 1)
    paddle2_x_discrete = np.clip(paddle2_x_discrete, 0, paddle2_x_discrete_num - 1)
    paddle2_y_discrete = np.clip(paddle2_y_discrete, 0, paddle2_y_discrete_num - 1)
    ball_dx_discrete = np.clip(ball_dx_discrete, 0, ball_dx_discrete_num - 1)
    ball_dy_discrete = np.clip(ball_dy_discrete, 0, ball_dy_discrete_num - 1)

    return (ball_x_discrete, ball_y_discrete, paddle_x_discrete, paddle_y_discrete, paddle2_x_discrete, paddle2_y_discrete, ball_dx_discrete, ball_dy_discrete)

state_space_size = (ball_x_discrete_num, ball_y_discrete_num, paddle_x_discrete_num, paddle_y_discrete_num, paddle2_x_discrete_num, paddle2_y_discrete_num, ball_dx_discrete_num, ball_dy_discrete_num)
action_space_size = 9

Q = np.random.uniform(low=-0.1, high=0.1, size=state_space_size + (action_space_size,))

def choose_action(state):
    return np.argmax(Q[state])

def choose_action_from_list(Q, state, action_list):
    max = -9999
    choice = 0
    c = 0
    if len(action_list) > 0:
        c = random.choice(action_list)
    if LEVEL == "easy":
        return c

    for i in action_list:
        check = Q[state][i]
        if(check > max):
            max = check
            choice = i
    return (choice)

def auto_move_paddle_with_learning(paddle_x, paddle_y, paddle2_x, paddle2_y, ball_x, ball_y, ball_dx, ball_dy, paddle2_speed):
    global Q, epsilon, old_action

    state = discretize_state(ball_x, ball_y, paddle_x, paddle_y, paddle2_x, paddle2_y, ball_dx, ball_dy)

    action = choose_action(state)

    if use_clever_strategy and (np.random.rand() < 0.9999):
        action_list = clever_motion(paddle2_x, paddle2_y, ball_x, ball_y, ball_dx, ball_dy)
        action = choose_action_from_list(Q, state, action_list)

    if (loop_counter % player2_update_freq != 0
        and distance(paddle2_x + paddle_width/2, paddle2_y, ball_x, ball_y) > paddle_width * 2.2 ):
        action = old_action

    if action == 0:
        paddle2_y -= paddle2_speed
    elif action == 1:
        paddle2_y += paddle2_speed
    elif action == 2:
        paddle2_x -= paddle2_speed
    elif action == 3:
        paddle2_x += paddle2_speed
    elif action == 4:
        paddle2_x += paddle2_speed
        paddle2_y -= paddle2_speed
    elif action == 5:
        paddle2_x += paddle2_speed
        paddle2_y += paddle2_speed
    elif action == 6:
        paddle2_x -= paddle2_speed
        paddle2_y += paddle2_speed
    elif action == 7:
        paddle2_x -= paddle2_speed
        paddle2_y -= paddle2_speed
    elif action == 8:
        pass

    old_action = action

    paddle2_x = max(0, min(paddle2_x, WIDTH - paddle_width))
    paddle2_y = max(paddle_height /2, min(HEIGHT * 0.4 - paddle_height, paddle2_y))

    return paddle2_x, paddle2_y


paddle2_x_old = paddle2_x
paddle2_y_old = paddle2_y

study = False

num_otbito = 0
num_propusk = 0
num_gol = 0
counter = 0
old_action = 8
loop_counter = 0
save_counter = 0
epoch_len = 1000000
vsego_golov = 0
vsego_prop = 0
player2_update_freq = 1

do_save = False
do_load = True
if LEVEL == "easy": do_load = False

auto_player1 = False
ai_player1 = False

load_file = get_proper_file(table_path, LEVEL)
if load_file and do_load:
    Q, alpha, gamma, epsilon, epsilon_decay, epsilon_min, counter = load_q_table_and_params(load_file)

do_draw = True
debug = False
use_clever_strategy = True

if do_draw: do_save = False

running = True
last_update_time = time.time()

screen.blit(background, (0, 0))

# Создаем шрифт для отображения счета
font = pygame.font.Font(None, 74)

# ВЫВОД СЧЕТА num_propusk : num_gol
score_text = font.render(f"{num_propusk} : {num_gol}", True, WHITE)
score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
screen.blit(score_text, score_rect)

# Добавляем текст "Для продолжения нажмите кнопку мыши"
font = pygame.font.Font(None, 44)
continue_text = font.render("Нажмите ЛКМ для продолжения", True, WHITE)
continue_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
screen.blit(continue_text, continue_rect)

pygame.display.flip()

# Ожидание нажатия кнопки мыши
waiting_for_click = True
while waiting_for_click:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            waiting_for_click = False

while running:
    current_time = time.time()
    delta_time = current_time - last_update_time

    if do_draw:
        vis_delta = 1 / 60
        if (debug): vis_delta = 0
    else:
        vis_delta = 0

    if (debug):
        waiting_for_click = True
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting_for_click = False

    if delta_time >= vis_delta:
        loop_counter += 1
        last_update_time = current_time
        if do_draw:
            screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if auto_player1:
            paddle_x, paddle_y = auto_move_paddle_p1(paddle_x, paddle_y, ball_x, ball_y, paddle_speed)
        elif ai_player1:
            paddle_x, paddle_y = ai_move_paddle_p1(paddle_x, paddle_y, paddle2_x, paddle2_y, ball_x, ball_y, ball_dx, ball_dy, paddle_speed)
        else:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            target_x = mouse_x - paddle_width // 2
            target_y = mouse_y - paddle_height // 2
            target_x = max(0, min(target_x, WIDTH - paddle_width))
            target_y = max(HEIGHT * 0.6, min(target_y, HEIGHT - paddle_height))

            if paddle_x < target_x:
                paddle_x += min(paddle_speed, target_x - paddle_x)
            elif paddle_x > target_x:
                paddle_x -= min(paddle_speed, paddle_x - target_x)

            if paddle_y < target_y:
                paddle_y += min(paddle_speed, target_y - paddle_y)
            elif paddle_y > target_y:
                paddle_y -= min(paddle_speed, paddle_y - target_y)

        ball_x += ball_dx
        ball_y += ball_dy

        paddle2_x_temp = paddle2_x
        paddle2_y_temp = paddle2_y

        paddle2_x, paddle2_y = auto_move_paddle_with_learning(paddle_x, paddle_y, paddle2_x, paddle2_y, ball_x, ball_y, ball_dx, ball_dy, paddle2_speed)

        paddle2_x_old = paddle2_x_temp
        paddle2_y_old = paddle2_y_temp

        if (ball_y + ball_radius >= paddle_y and ball_y - ball_radius <= paddle_y + 5 and ball_dy > 0
                and paddle_x <= ball_x <= paddle_x + paddle_width):
            ball_dy, ball_dx = calculate_reflection(ball_x, ball_dx, paddle_x)
            sound_effect.play()

        if (ball_y - ball_radius <= paddle2_y + paddle_height and ball_y + ball_radius >= paddle2_y - 5 and ball_dy < 0
                and paddle2_x <= ball_x <= paddle2_x + paddle_width):
            ball_dy, ball_dx = calculate_reflection(ball_x, ball_dx, paddle2_x)
            sound_effect.play()
            counter += 1
            num_otbito += 1

        if ball_x < ball_radius or ball_x > WIDTH - ball_radius:
            ball_dx = -ball_dx
            sound_effect.play()

        if ball_y >= HEIGHT or ball_y <= 0:
            if ball_y <= 0:
                sound_effect2.play()
                num_propusk += 1
                side = 1
                # ВЫВОД СЧЕТА num_propusk : num_gol
                font = pygame.font.Font(None, 74)
                score_text = font.render(f"{num_propusk} : {num_gol}", True, WHITE)
                score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
                screen.blit(score_text, score_rect)

                # Добавляем текст "Для продолжения нажмите кнопку мыши"
                font = pygame.font.Font(None, 44)
                continue_text = font.render("Нажмите ЛКМ для продолжения", True, WHITE)
                continue_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
                screen.blit(continue_text, continue_rect)

                pygame.display.flip()

                # Ожидание нажатия кнопки мыши
                waiting_for_click = True
                while waiting_for_click:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            waiting_for_click = False

            else:
                sound_effect3.play()
                num_otbito += 1
                num_gol += 1
                side = 2

                # ВЫВОД СЧЕТА num_propusk : num_gol
                font = pygame.font.Font(None, 74)
                score_text = font.render(f"{num_propusk} : {num_gol}", True, WHITE)
                score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
                screen.blit(score_text, score_rect)

                # Добавляем текст "Для продолжения нажмите кнопку мыши"
                font = pygame.font.Font(None, 44)
                continue_text = font.render("Нажмите ЛКМ для продолжения", True, WHITE)
                continue_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
                screen.blit(continue_text, continue_rect)

                pygame.display.flip()

                # Ожидание нажатия кнопки мыши
                waiting_for_click = True
                while waiting_for_click:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            waiting_for_click = False

            counter += 1
            if side == 1:
                ball_x = random.uniform(9, WIDTH - 9)
                ball_y = HEIGHT - 9
                angle = random.uniform(-17, 17)
                ball_dx = - ball_speed * math.sin(math.radians(angle))
                ball_dy = - ball_speed * math.cos(math.radians(angle))
            else:
                ball_x = random.uniform(9, WIDTH - 9)
                ball_y = 9
                angle = random.uniform(-17, 17)
                ball_dx = - ball_speed * math.sin(math.radians(angle))
                ball_dy = ball_speed * math.cos(math.radians(angle))

        if do_draw:
            draw_court()
            draw_ball(ball_x, ball_y)
            draw_paddle(paddle_x, paddle_y)
            draw_paddle(paddle2_x, paddle2_y)

        if counter % epoch_len == 0:
            vsego_golov += num_gol
            vsego_prop += num_propusk
            if (num_otbito + num_propusk > 0):
                num_otbito = 0
                num_propusk = 0
                num_gol = 0
            counter += 1
            save_counter += 1

        if do_draw:
            pygame.display.flip()

pygame.quit()
sys.exit()
