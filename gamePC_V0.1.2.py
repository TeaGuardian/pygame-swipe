import pygame
from random import randint
from datetime import datetime, timedelta
ora = [60, 60, 60]
grey = [200, 200, 200]
p1 = [100, 180, 20]
s1 = [255, 153, 0]
s2 = [220, 20, 60]
s3 = [50, 120, 200]
pygame.init()
steps = 0
sta2 = datetime.now()
quit = datetime.now()
screen = pygame.display.set_mode()
x, y = screen.get_size()
running = True
text = '$'
pygame.mouse.set_visible(True)
font = pygame.font.Font(None, 50)
time_obj = datetime.now()
time_2 = False
schet = 0
"""размер поля, начальное время между разрушением и шаг уменьшения времени"""
X, Y = 11, 10
speed = 1
speed_step = 0.001
mapk = [[grey for i in range(Y)] for ii in range(X)]


def seecl(event):
    bb = 1
    while bb:
        for event1 in pygame.event.get():
            if event1.type == pygame.KEYUP:
                bb = 0
    if event.key == pygame.K_s:
        return 'v'
    elif event.key == pygame.K_w:
        return 'u'
    elif event.key == pygame.K_a:
        return '<'
    elif event.key == pygame.K_d:
        return '>'
    else:
        return f'0 0'


def drawc(x, y, h, color):
    """рисуем клеточку"""
    r = h // 5
    pygame.draw.rect(screen, color, ((x - r, y), (h + r * 2, h)))
    pygame.draw.rect(screen, color, ((x, y - r), (h, h + r * 2)))
    pygame.draw.circle(screen, color, (x, y), r)
    pygame.draw.circle(screen, color, (x + h, y), r)
    pygame.draw.circle(screen, color, (x, y + h), r)
    pygame.draw.circle(screen, color, (x + h, y + h), r)


sch = -1
a = [0, 0]
lasta = a[:]
while running:
    screen.fill(ora)
    """рисуем поле"""
    for i in range(X):
        for j in range(Y):
            nc = mapk[i][j]
            drawc(40 + i * 60, 100 + j * 60, 40, nc)
    """проверяем прошедшее время и красим клеточку"""
    if (datetime.now() - time_obj) > timedelta(seconds=speed):
        time_obj = datetime.now()
        speed -= speed_step
        i, j = randint(0, X - 1), randint(0, Y - 1)
        """красим только ту, по которой можно ходить"""
        while mapk[i][j] == ora:
            i, j = randint(0, X - 1), randint(0, Y - 1)
        if mapk[i][j] == grey:
            mapk[i][j] = s1
        elif mapk[i][j] == s1:
            mapk[i][j] = s2
        elif mapk[i][j] == s2:
            mapk[i][j] = ora
        elif mapk[i][j] == s3:
            mapk[i][j] = grey
        if not randint(0, 6) and mapk[i][j] == s1:
            mapk[i][j] = s3
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.KEYDOWN:
            steps += 1
            text = seecl(event)
            """определяем вариант свайпа, определяем стены, проверяем есть ли пропость там, куда шагаем"""
            if text == '0 0':
                if (datetime.now() - quit) < timedelta(seconds=0.3):
                    running = 0
                else:
                    quit = datetime.now()
            elif text == '>' and a[0] < X - 1 and mapk[a[0] + 1][a[1]] != ora:
                a[0] += 1
            elif text == '<' and a[0] > 0 and mapk[a[0] - 1][a[1]] != ora:
                a[0] -= 1
            elif text == 'u' and a[1] > 0 and mapk[a[0]][a[1] - 1] != ora:
                a[1] -= 1
            elif text == 'v' and a[1] < Y - 1 and mapk[a[0]][a[1] + 1] != ora:
                a[1] += 1
    """если пол под нами провалился завершаем игру"""
    if mapk[lasta[0]][lasta[1]] == ora:
        running = 0
    elif mapk[lasta[0]][lasta[1]] == s1:
        """если стоим на жёлтом, то меняем на красный"""
        mapk[a[0]][a[1]] = s2
    elif mapk[lasta[0]][lasta[1]] == s3:
        if not time_2:
            schet = 0
            time_2 = datetime.now()
        else:
            if (datetime.now() - time_2) > timedelta(seconds=10):
                mapk[lasta[0]][lasta[1]] = ora
            if (datetime.now() - time_2 - timedelta(seconds=schet)) > timedelta(seconds=0.8):
                schet += 1.1
            if timedelta(seconds=1) > (datetime.now() - time_2 - timedelta(seconds=schet)) > timedelta(seconds=0.5):
                i, j = lasta
                drawc(40 + i * 60, 100 + j * 60, 40, s2)
    else:
        time_2 = False
        schet = 0
    texte = font.render(text, True, [100, 255, 100])
    if lasta == a:
        pygame.draw.circle(screen, p1, (60 + a[0] * 60, 120 + a[1] * 60), 20)
    else:
        """плавное перемещение"""
        sch += 0.09
        i = sch
        if text in '<u':
            i = 0 - sch
        if text in '<>':
            pygame.draw.circle(screen, p1, (60 + (a[0] + i) * 60, 120 + a[1] * 60), 20)
        else:
            pygame.draw.circle(screen, p1, (60 + a[0] * 60, 120 + (i + a[1]) * 60), 20)
        if sch >= 0:
            lasta = a[:]
            sch = -1
    textpose = (900, 200)
    screen.blit(texte, textpose)
    pygame.display.update()
r = 1
tim = datetime.now()
score = 0
maxb, bub = 3, 0
for i in mapk:
    for j in i:
        if j != ora:
            score += 1
timpes = [[a[0], a[1] + 1], [a[0], a[1] - 1], [a[0] + 1, a[1]], [a[0] - 1, a[1]]]
for i in range(3):
    po = timpes[i]
    if po[1] in range(X) and po[0] in range(Y):
        if mapk[po[0]][po[1]] != ora:
            bub += 1
        else:
            maxb -= 1
    else:
        maxb -= 1
while r:
    screen.fill(ora)
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            r = 0
    if maxb == 0:
        text = font.render(f'У вас не было выхода...', True, [100, 255, 100])
    else:
        text = font.render(f'Спасибо за игру. {maxb, bub}', True, [100, 255, 100])
    textpos = (50, y // 2 - 5)
    screen.blit(text, textpos)
    text = font.render(f'пройдено шагов: {steps}', True, [100, 255, 100])
    textpos = (50, y // 2 + 35)
    screen.blit(text, textpos)
    timet = list(map(int, tim.strftime('%H %M %S').split()))
    started = list(map(int, sta2.strftime('%H %M %S').split()))
    timet = timet[0] * 3600 + timet[1] * 60 + timet[2]
    started = started[0] * 3600 + started[1] * 60 + started[2]
    text = font.render(f'прожито секунд: {timet - started} с.', True, [100, 255, 100])
    textpos = (50, y // 2 + 75)
    screen.blit(text, textpos)
    text = font.render(f'счёт: {X * Y - score} из {X * Y}.', True, [100, 255, 100])
    textpos = (50, y // 2 + 135)
    screen.blit(text, textpos)
    pygame.display.update()
