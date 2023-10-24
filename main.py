import sys

import pygame
import random
import copy
#import sys

pygame.init()

#Разрешение задней поферхности
RESOLUTION = 850,700
#ФПС
FPS=120
#Количество квадратиков-полей (горизонталь, вертикаль)
W, H = 10, 15
#Размеры квадратиков-поля
SQUARE=40

#Игровой баланс
animation_speed=40
main_animation_limit=2400
animation_limit=main_animation_limit
animation_current=0
speed_if_K_DOWN=160
score=0
plus_score=100
delta_for_up_score=10
plus_animation_speed=2

#Название игры
pygame.display.set_caption("Tetris from КНТ")
#Создание игрового таймера
clock = pygame.time.Clock()

#Создаем задний экран игры
back_screen=pygame.display.set_mode(RESOLUTION)

#Формируем экран из квадратиков
screen=pygame.Surface((W*SQUARE,H*SQUARE))

#Загрузка картинок
icon = pygame.image.load('images/icon1.jpg')
HSE = pygame.image.load('images/hss.png').convert()
background = pygame.image.load('images/back.jfif')
#Загрузка шрифтов
score_font=pygame.font.Font('font/Metal_Mania/MetalMania-Regular.ttf',50)
head_font=pygame.font.Font('font/Playpen_Sans/PlaypenSans-VariableFont_wght.ttf',70)

#Создание иконки для приложения
pygame.display.set_icon(icon)

#Создание сетки поля, rect() отвечает за координаты квадрата. 1-коорд по х 2-коорд по у 3-размер первой стороны 4-размер второй стороны
grid = [pygame.Rect(x*SQUARE,y*SQUARE,SQUARE,SQUARE) for x in range (W) for y  in range(H)]

#Создание всех 7 фигур. 1 координата в каждом из 7 подмассивов отвечает за центр вращения фигуры
figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

#Создание фигур, фигура появляется в центре W, центр вращения на 1 клетку ниже
figures = [[pygame.Rect(x + W//2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
#Объект, отвечающий за отрисовку квадратика. -2 для того, чтобы квадратик не перерисовывал стенки
figure_rect = pygame.Rect(0, 0, SQUARE - 2, SQUARE - 2)


#Функция проеврки выхода за границы
def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True

#Формирование фигур в рандомным цветом (начинаем от 100, таким образом цвета будут ярче)
def get_color():
    return (random.randint(100,255),random.randint(100,255),random.randint(100,255))


#Функция создания файла для best_score
def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')

#Функция переопределения рекорда
def set_record(record, score):
    best_record = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(best_record))


#Игровое поле, в котором будут отмечаться уже упавшие фигуры
field = [[0 for i in range(W)] for j in range(H+1)]


#Создание первоначальной фигуры
figure=copy.deepcopy(figures[random.randint(0,6)])
color=get_color()
next_figure=copy.deepcopy(figures[random.randint(0,6)])
next_color=get_color()

#Созданеи заготовок для текста
HEAD_text=head_font.render('Tetris from KHT',True,'gold')
SCORE_text=score_font.render('SCORE',True,'orange')
CUR_SCORE_text=score_font.render('0',True,'orange')
BEST_RECORD_text=score_font.render('BEST',True,'orange')
VALUE_BEST_RECORD_text=score_font.render(str(get_record()),True,'orange')
NEXT_FIGURE_text=score_font.render('NEXT',True,'blue')

while True:
    #Задний фон
    back_screen.blit(background,(0,0))
    #Заголовок
    back_screen.blit(HEAD_text,(RESOLUTION[0]//5,0))
    #Score
    back_screen.blit(SCORE_text,(RESOLUTION[0]//2+W*SQUARE//1.6,RESOLUTION[1] // 1.6))
    #Cur score
    back_screen.blit(CUR_SCORE_text, (RESOLUTION[0] // 2 + W * SQUARE // 1.4, RESOLUTION[1] // 1.4))
    #Основной экран игры
    back_screen.blit(screen,( RESOLUTION[0]//2-W*SQUARE//2 , 0.15*H*SQUARE))
    #Иконка HSE
    back_screen.blit(HSE,(0,0))
    #Надпись BEST
    back_screen.blit(BEST_RECORD_text,(RESOLUTION[0]//1.95-W*SQUARE,RESOLUTION[1]//1.8))
    #Надпись Score под Best
    back_screen.blit(SCORE_text, (RESOLUTION[0] // 2 - W * SQUARE, RESOLUTION[1] // 1.6))
    #Best record value
    back_screen.blit(VALUE_BEST_RECORD_text,(RESOLUTION[0] // 1.9 - W * SQUARE, RESOLUTION[1] // 1.4))
    #Next
    back_screen.blit(NEXT_FIGURE_text,(RESOLUTION[0]//2+W*SQUARE//1.6,RESOLUTION[1]//4))
    #Цвет игрового поля
    screen.fill(pygame.Color('black'))

    dx = 0
    flag_rotate = False
    record=get_record()

    #Выход из программы при закрытии окна
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        #Отслеживание перемещения фигуры влево вправо
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                dx-=1
            if event.key==pygame.K_RIGHT:
                dx+=1
            if event.key==pygame.K_DOWN:
                animation_limit=speed_if_K_DOWN
            if event.key==pygame.K_UP:
                flag_rotate = True


    #Отрисовка сетки поля
    [pygame.draw.rect(screen, ("lime"), i_rect, 1) for i_rect in grid]

    #Отрисовка следующей фигуры
    for i in range(4):
        figure_rect.x=RESOLUTION[0]//2+W*SQUARE//4+SQUARE*next_figure[i].x
        figure_rect.y=RESOLUTION[1]//3+SQUARE*next_figure[i].y
        pygame.draw.rect(back_screen,next_color,figure_rect)

    #Сдвиг фигуры вниз на 1 единицу при превышении лимита анимации
    animation_current+=animation_speed
    if animation_current>animation_limit:
        animation_current=0
        figure_old=copy.deepcopy(figure)
        for i in range(4):
            figure[i].y+=1
            if not check_borders():
                for i in range (4):
                    field[figure_old[i].y][figure_old[i].x] = color
                color = next_color
                figure = next_figure
                next_figure=copy.deepcopy(figures[random.randint(0,6)])
                next_color=get_color()
                animation_limit = main_animation_limit
                break

    #Перемещение всех 4 квадратиков на dx c проверкой выхода за границу
    figure_old = copy.deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = copy.deepcopy(figure_old)
            break


    # переворот фигуры
    if flag_rotate == True and figures[1]!=figure:
        center = figure[0]
        figure_old = copy.deepcopy(figure)
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = copy.deepcopy(figure_old)
                break

    #Отрисовка фигуры путем рисования 4-х квадратиков
    for i in range(4):
        figure_rect.x = figure[i].x * SQUARE
        figure_rect.y = figure[i].y * SQUARE
        pygame.draw.rect(screen,color,figure_rect)


    #Проверка заполненности линии и сдвиг линий при полностью заполненной линии
    line = H - 1
    for i in range(H - 1, -1, -1):
        flag = True
        if all(field[i][j]!=0 for j in range (W)):
            flag = False
            score+=plus_score
            plus_score+=delta_for_up_score
            CUR_SCORE_text=score_font.render(str(score),True,'orange')
            animation_speed+=plus_animation_speed

        field[line] = copy.deepcopy(field[i])
        if flag: line -= 1


    #Алгоритм отображения занятых клеток
    for y in range(H):
        for x in range(W):
            if field[y][x]:
                pygame.draw.rect(screen, field[y][x], (x*SQUARE,y*SQUARE,SQUARE-2,SQUARE-2))

    #Концовка игры
    if any(field[0][j]!=0 for j in range (W)):
        #Финальная сцена
        field = [[0 for i in range(W)] for j in range(H + 1)]
        for y in range(H//2+1):
            for x in range(W):
                pygame.draw.rect(screen, get_color(), (x * SQUARE, y * SQUARE, SQUARE - 2, SQUARE - 2))
                pygame.draw.rect(screen, get_color(), (x * SQUARE, (H-y-1) * SQUARE, SQUARE - 2, SQUARE - 2))
                back_screen.blit(screen,( RESOLUTION[0]//2-W*SQUARE//2 , 0.15*H*SQUARE))
                clock.tick(20)
                pygame.display.flip()
        for y in range(H // 2 + 1):
            for x in range(W):
                pygame.draw.rect(screen, 'black', (x * SQUARE, y * SQUARE, SQUARE - 2, SQUARE - 2))
                pygame.draw.rect(screen, 'black',(x * SQUARE, (H - y - 1) * SQUARE, SQUARE - 2, SQUARE - 2))
                back_screen.blit(screen, (RESOLUTION[0] // 2 - W * SQUARE // 2, 0.15 * H * SQUARE))
                clock.tick(20)
                pygame.display.flip()
        field = [[0 for i in range(W)] for j in range(H + 1)]
        #Рисование сердечка
        if score > int(record):
            field[8][4] = 1
            field[8][5] = 1
            field[7][3] = 1
            field[7][6] = 1
            field[6][2] = 1
            field[6][7] = 1
            field[5][1] = 1
            field[5][8] = 1
            field[4][2] = 1
            field[4][7] = 1
            field[3][3] = 1
            field[3][6] = 1
            field[4][4] = 1
            field[4][5] = 1
            for y in range(H):
                for x in range(W):
                    if field[y][x]:
                        pygame.draw.rect(screen, 'red', (x * SQUARE, y * SQUARE, SQUARE - 2, SQUARE - 2))
            back_screen.blit(screen, (RESOLUTION[0] // 2 - W * SQUARE // 2, 0.15 * H * SQUARE))
            pygame.display.flip()
            clock.tick(1)
            clock.tick(1)
            clock.tick(1)
            clock.tick(1)
            VALUE_BEST_RECORD_text = score_font.render(str(score), True, 'orange')
            set_record(record, score)
        # Обновление экрана игры и показателей при проигрыше
        field = [[0 for i in range(W)] for j in range(H + 1)]
        animation_speed = 40
        animation_limit = main_animation_limit
        animation_current = 0
        score = 0
        plus_score = 100
        CUR_SCORE_text = score_font.render('0', True, 'orange')

    #Обновление игрового экрана
    pygame.display.flip()
    clock.tick(FPS)

