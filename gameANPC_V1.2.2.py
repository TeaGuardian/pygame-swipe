import socket
import pygame
from random import randint
from datetime import datetime, timedelta


class game:
    """исправленная версия"""
    """переменные ip"""
    def __init__(self):
        self.SERVER, self.CLIENT = '', '192.168.43.1'
        self.ora = [60, 60, 60]
        self.grey = [200, 200, 200]
        self.p1 = [100, 180, 20]
        self.p2 = [255, 100, 150]
        self.s1 = [255, 153, 0]
        self.s2 = [220, 20, 60]
        self.s3 = [50, 120, 200]
        self.PORT = 12000
        pygame.init()
        self.screen = pygame.display.set_mode()
        pygame.display.set_caption('V1.2.2')
        self.cx, self.cy = self.screen.get_size()
        pygame.mouse.set_visible(True)
        if 'myboli' not in pygame.font.get_fonts():
            self.b_font = pygame.font.Font(None, 50)
        else:
            self.b_font = pygame.font.SysFont('myboli', 50)
        self.font = pygame.font.Font(None, 50)
        self.X, self.Y = 11, 10
        self.speed_step = 0.001
        print(self.get_ipl())
        while True:
            self.setsIP()
            res = self.start_screen()
            if res['SOLO GAME']:
                self.solo()
                break
            if res['CREATE MASTER']:
                self.server()
                break
            if res["CREATE CLIENT"]:
                self.client()
                break

    def setsIP(self):
        try:
            file = open("game_settings.txt", "r", encoding='Windows-1251')
            data = file.readlines()
            file.close()
        except FileNotFoundError:
            data = f'{self.SERVER}\n{self.CLIENT}'
            with open("game_settings.txt", "w+", encoding='Windows-1251') as f:
                f.writelines(data)
        self.SERVER, self.CLIENT = data[0], data[1]

    def get_ipl(self):
        h_name = socket.gethostname()
        IP_addres = socket.gethostbyname(h_name)
        return [".".join(IP_addres.split('.')[:-1]), IP_addres]

    def seecl(self, n1, event):
        """из-за попытки сделать версию общей для пк и телефона могут возникать ошибки event has not type key,
        в этом случае достаточно убрать ненужный тип управления из этой функции, или изменить параметр CR на True,
        тогда версия перейдёт в телефонную"""
        while pygame.mouse.get_pressed()[0]:
            pass
        CR = False
        n2 = pygame.mouse.get_pos()
        x, y = n1[0] - n2[0], n1[1] - n2[1]
        d = 1.4
        if y < 0 and abs(x) < abs(d * y):
            return 'v'
        elif y > 0 and abs(x) < abs(d * y):
            return 'u'
        elif x > 0 and abs(x) > abs(d * y):
            return '<'
        elif x < 0 and abs(x) > abs(d * y):
            return '>'
        elif n1 == n2 and CR:
            return f'{x} {y}'
        elif event.key == pygame.K_DOWN:
            return 'v'
        elif event.key == pygame.K_UP:
            return 'u'
        elif event.key == pygame.K_LEFT:
            return '<'
        elif event.key == pygame.K_RIGHT:
            return '>'
        else:
            return f'{x} {y}'

    def drawc(self, x, y, h, color):
        """рисуем клеточку"""
        r = h // 5
        pygame.draw.rect(self.screen, color, ((x - r, y), (h + r * 2, h)))
        pygame.draw.rect(self.screen, color, ((x, y - r), (h, h + r * 2)))
        pygame.draw.circle(self.screen, color, (x, y), r)
        pygame.draw.circle(self.screen, color, (x + h, y), r)
        pygame.draw.circle(self.screen, color, (x, y + h), r)
        pygame.draw.circle(self.screen, color, (x + h, y + h), r)

    def button(self, x, y, hx, hy, text, color):
        """рисуем кнопку"""
        r = hy // 5
        pygame.draw.rect(self.screen, color, ((x - r, y), (hx + r * 2, hy)))
        pygame.draw.rect(self.screen, color, ((x, y - r), (hx, hy + r * 2)))
        pygame.draw.circle(self.screen, color, (x, y), r)
        pygame.draw.circle(self.screen, color, (x + hx, y), r)
        pygame.draw.circle(self.screen, color, (x, y + hy), r)
        pygame.draw.circle(self.screen, color, (x + hx, y + hy), r)
        b_text = self.font.render(text, True, [255 - color[0], 255 - color[1], 255 - color[2]])
        self.screen.blit(b_text, (x + hx * 0.65 - len(text) * 30, y + hy * 0.3))
        px, py = pygame.mouse.get_pos()
        return px in range(x, x + hx) and py in range(y, y + hy)

    def start_screen(self):
        titles = ["SOLO GAME", "CREATE MASTER", "CREATE CLIENT"]
        while True:
            titles2 = {"SOLO GAME": False, "CREATE MASTER": True, "CREATE CLIENT": False}
            self.screen.fill(self.ora)
            bhy, bhx = self.cy // 10, int(self.cx * 0.9)
            by = 50
            for ii in range(3):
                titles2[titles[ii]] = self.button(int(self.cx * 0.05), by, bhx, bhy, titles[ii], self.p1)
                by += 250
            for i in pygame.event.get():
                if i.type == pygame.MOUSEBUTTONDOWN and i.button == 1:
                    return titles2
                elif i.type == pygame.MOUSEBUTTONUP and i.button == 1:
                    return titles2
            pygame.display.update()

    def solo(self):
        text = 'V1.2.2'
        schet = 0
        speed = 1
        steps = 0
        sta2 = datetime.now()
        quit = datetime.now()
        time_obj = datetime.now()
        time_2 = False
        mapk = [[self.grey for i in range(self.Y)] for ii in range(self.X)]
        sch = -1
        a = [0, 0]
        lasta = a[:]
        running = 1
        while running:
            self.screen.fill(self.ora)
            """рисуем поле"""
            for i in range(self.X):
                for j in range(self.Y):
                    nc = mapk[i][j]
                    self.drawc(40 + i * 60, 100 + j * 60, 40, nc)
            """проверяем прошедшее время и красим клеточку"""
            if (datetime.now() - time_obj) > timedelta(seconds=speed):
                time_obj = datetime.now()
                speed -= self.speed_step
                i, j = randint(0, self.X - 1), randint(0, self.Y - 1)
                """красим только ту, по которой можно ходить"""
                while mapk[i][j] == self.ora:
                    i, j = randint(0, self.X - 1), randint(0, self.Y - 1)
                if mapk[i][j] == self.grey:
                    mapk[i][j] = self.s1
                elif mapk[i][j] == self.s1:
                    mapk[i][j] = self.s2
                elif mapk[i][j] == self.s2:
                    mapk[i][j] = self.ora
                elif mapk[i][j] == self.s3:
                    mapk[i][j] = self.grey
                if not randint(0, 6) and mapk[i][j] == self.s1:
                    mapk[i][j] = self.s3
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    steps += 1
                    text = self.seecl(pos, event)
                    """определяем вариант свайпа, определяем стены, проверяем есть ли пропость там, куда шагаем"""
                    if text == '0 0':
                        if (datetime.now() - quit) < timedelta(seconds=0.3):
                            running = 0
                        else:
                            quit = datetime.now()
                    elif text == '>' and a[0] < self.X - 1 and mapk[a[0] + 1][a[1]] != self.ora:
                        a[0] += 1
                    elif text == '<' and a[0] > 0 and mapk[a[0] - 1][a[1]] != self.ora:
                        a[0] -= 1
                    elif text == 'u' and a[1] > 0 and mapk[a[0]][a[1] - 1] != self.ora:
                        a[1] -= 1
                    elif text == 'v' and a[1] < self.Y - 1 and mapk[a[0]][a[1] + 1] != self.ora:
                        a[1] += 1
            """если пол под нами провалился завершаем игру"""
            if mapk[lasta[0]][lasta[1]] == self.ora:
                running = 0
            elif mapk[lasta[0]][lasta[1]] == self.s1:
                """если стоим на жёлтом, то меняем на красный"""
                mapk[a[0]][a[1]] = self.s2
            elif mapk[lasta[0]][lasta[1]] == self.s3:
                if not time_2:
                    schet = 0
                    time_2 = datetime.now()
                else:
                    if (datetime.now() - time_2) > timedelta(seconds=10):
                        mapk[lasta[0]][lasta[1]] = self.ora
                    if (datetime.now() - time_2 - timedelta(seconds=schet)) > timedelta(seconds=0.8):
                        schet += 1.1
                    if timedelta(seconds=1) > (datetime.now() - time_2 - timedelta(seconds=schet)) > timedelta(
                            seconds=0.5):
                        i, j = lasta
                        self.drawc(40 + i * 60, 100 + j * 60, 40, self.s2)
            else:
                time_2 = False
                schet = 0
            texte = self.font.render(text, True, [100, 255, 100])
            if lasta == a:
                pygame.draw.circle(self.screen, self.p1, (60 + a[0] * 60, 120 + a[1] * 60), 20)
            else:
                """плавное перемещение"""
                sch += 0.09
                i = sch
                if text in '<u':
                    i = 0 - sch
                if text in '<>':
                    pygame.draw.circle(self.screen, self.p1, (60 + (a[0] + i) * 60, 120 + a[1] * 60), 20)
                else:
                    pygame.draw.circle(self.screen, self.p1, (60 + a[0] * 60, 120 + (i + a[1]) * 60), 20)
                if sch >= 0:
                    lasta = a[:]
                    sch = -1
            textpose = (900, 200)
            self.screen.blit(texte, textpose)
            pygame.display.update()
        r = 1
        tim = datetime.now()
        score = 0
        maxb, bub = 3, 0
        for i in mapk:
            for j in i:
                if j != self.ora:
                    score += 1
        timpes = [[a[0], a[1] + 1], [a[0], a[1] - 1], [a[0] + 1, a[1]], [a[0] - 1, a[1]]]
        for i in range(3):
            po = timpes[i]
            if po[1] in range(self.X) and po[0] in range(self.Y):
                if mapk[po[0]][po[1]] != self.ora:
                    bub += 1
                else:
                    maxb -= 1
            else:
                maxb -= 1
        while r:
            self.screen.fill(self.ora)
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    r = 0
            if maxb == 0:
                text = self.font.render(f'У вас не было выхода...', True, [100, 255, 100])
            else:
                text = self.font.render(f'Спасибо за игру. {maxb, bub}', True, [100, 255, 100])
            textpos = (50, self.cy // 2 - 5)
            self.screen.blit(text, textpos)
            text = self.font.render(f'пройдено шагов: {steps}', True, [100, 255, 100])
            textpos = (50, self.cy // 2 + 35)
            self.screen.blit(text, textpos)
            timet = list(map(int, tim.strftime('%H %M %S').split()))
            started = list(map(int, sta2.strftime('%H %M %S').split()))
            timet = timet[0] * 3600 + timet[1] * 60 + timet[2]
            started = started[0] * 3600 + started[1] * 60 + started[2]
            text = self.font.render(f'прожито секунд: {timet - started} с.', True, [100, 255, 100])
            textpos = (50, self.cy // 2 + 75)
            self.screen.blit(text, textpos)
            text = self.font.render(f'счёт: {self.X * self.Y - score} из {self.X * self.Y}.', True, [100, 255, 100])
            textpos = (50, self.cy // 2 + 135)
            self.screen.blit(text, textpos)
            pygame.display.update()

    def server(self):
        text = 'V1.2.2'
        schet = 0
        speed = 1
        steps = 0
        sta2 = datetime.now()
        quit = datetime.now()
        time_obj = datetime.now()
        time_2 = False
        mapk = [[self.grey for i in range(self.Y)] for ii in range(self.X)]
        sch = -1
        a = [0, 0]
        lasta = a[:]
        running = 1
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSocket.bind((self.SERVER, self.PORT))
        serverSocket.listen(1)
        self.screen.fill(self.ora)
        stext = self.font.render("WAITING FOR CLIENT", True, [255, 255, 255])
        self.screen.blit(stext, (200, 100))
        pygame.display.update()
        connectionSocket, addr = serverSocket.accept()
        connectionSocket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        print(connectionSocket.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE))
        serverSocket.close()

        sentence = f'map#{self.X}#{self.Y}'
        try:
            connectionSocket.send(sentence.encode())
        except ConnectionResetError as e:
            print("Server connection closed")
            return 0

        try:
            sentence2 = connectionSocket.recv(512).decode().split('#')
        except ConnectionResetError as e:
            print("Client connection closed")
            return 0

        if 'map' in sentence2:
            self.X, self.Y = min([int(sentence2[1]), self.X]), min([int(sentence2[2]), self.Y])

        lasc = '0#0#' + '#'.join(list(map(str, self.grey))) + '#0#0'
        while running:
            self.screen.fill(self.ora)
            """рисуем поле"""
            for i in range(self.X):
                for j in range(self.Y):
                    nc = mapk[i][j]
                    self.drawc(40 + i * 60, 100 + j * 60, 40, nc)
            """проверяем прошедшее время и красим клеточку"""
            i, j = a
            lasc = f'{i}#{j}#' + '#'.join(list(map(str, mapk[i][j]))) + f'#{a[0]}#{a[1]}'
            if (datetime.now() - time_obj) > timedelta(seconds=speed):
                time_obj = datetime.now()
                speed -= self.speed_step
                i, j = randint(0, self.X - 1), randint(0, self.Y - 1)
                """красим только ту, по которой можно ходить"""
                while mapk[i][j] == self.ora:
                    i, j = randint(0, self.X - 1), randint(0, self.Y - 1)
                if mapk[i][j] == self.grey:
                    mapk[i][j] = self.s1
                elif mapk[i][j] == self.s1:
                    mapk[i][j] = self.s2
                elif mapk[i][j] == self.s2:
                    mapk[i][j] = self.ora
                elif mapk[i][j] == self.s3:
                    mapk[i][j] = self.grey
                if not randint(0, 6) and mapk[i][j] == self.s1:
                    mapk[i][j] = self.s3
                lasc = f'{i}#{j}#' + '#'.join(list(map(str, mapk[i][j]))) + f'#{a[0]}#{a[1]}'

            try:
                connectionSocket.send(lasc.encode())
            except ConnectionResetError as e:
                print("Server connection closed")
                return 0
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    steps += 1
                    text = self.seecl(pos, event)
                    """определяем вариант свайпа, определяем стены, проверяем есть ли пропость там, куда шагаем"""
                    if text == '0 0':
                        if (datetime.now() - quit) < timedelta(seconds=0.3):
                            running = 0
                        else:
                            quit = datetime.now()
                    elif text == '>' and a[0] < self.X - 1 and mapk[a[0] + 1][a[1]] != self.ora:
                        a[0] += 1
                    elif text == '<' and a[0] > 0 and mapk[a[0] - 1][a[1]] != self.ora:
                        a[0] -= 1
                    elif text == 'u' and a[1] > 0 and mapk[a[0]][a[1] - 1] != self.ora:
                        a[1] -= 1
                    elif text == 'v' and a[1] < self.Y - 1 and mapk[a[0]][a[1] + 1] != self.ora:
                        a[1] += 1
            """если пол под нами провалился завершаем игру"""
            if mapk[lasta[0]][lasta[1]] == self.ora:
                running = 0
            elif mapk[lasta[0]][lasta[1]] == self.s1:
                """если стоим на жёлтом, то меняем на красный"""
                mapk[a[0]][a[1]] = self.s2
            elif mapk[lasta[0]][lasta[1]] == self.s3:
                if not time_2:
                    schet = 0
                    time_2 = datetime.now()
                else:
                    if (datetime.now() - time_2) > timedelta(seconds=10):
                        mapk[lasta[0]][lasta[1]] = self.ora
                    if (datetime.now() - time_2 - timedelta(seconds=schet)) > timedelta(seconds=0.8):
                        schet += 1.1
                    if timedelta(seconds=1) > (datetime.now() - time_2 - timedelta(seconds=schet)) > timedelta(
                            seconds=0.5):
                        i, j = lasta
                        self.drawc(40 + i * 60, 100 + j * 60, 40, self.s2)
            else:
                time_2 = False
                schet = 0
            texte = self.font.render(text, True, [100, 255, 100])

            try:
                lasc2 = list(map(int, connectionSocket.recv(512).decode().split('#')))
                mapk[lasc2[0]][lasc2[1]] = [lasc2[2], lasc2[3], lasc2[4]]
                pygame.draw.circle(self.screen, self.p2, (60 + lasc2[5] * 60, 120 + lasc2[6] * 60), 20)
            except ConnectionResetError as e:
                print("Client connection closed")
                return 0

            if lasta == a:
                pygame.draw.circle(self.screen, self.p1, (60 + a[0] * 60, 120 + a[1] * 60), 20)
            else:
                """плавное перемещение"""
                sch += 0.09
                i = sch
                if text in '<u':
                    i = 0 - sch
                if text in '<>':
                    pygame.draw.circle(self.screen, self.p1, (60 + (a[0] + i) * 60, 120 + a[1] * 60), 20)
                else:
                    pygame.draw.circle(self.screen, self.p1, (60 + a[0] * 60, 120 + (i + a[1]) * 60), 20)
                if sch >= 0:
                    lasta = a[:]
                    sch = -1
            textpose = (900, 200)
            self.screen.blit(texte, textpose)
            pygame.display.update()
        r = 1
        tim = datetime.now()
        score = 0
        maxb, bub = 3, 0
        for i in mapk:
            for j in i:
                if j != self.ora:
                    score += 1
        timpes = [[a[0], a[1] + 1], [a[0], a[1] - 1], [a[0] + 1, a[1]], [a[0] - 1, a[1]]]
        for i in range(3):
            po = timpes[i]
            if po[1] in range(self.X) and po[0] in range(self.Y):
                if mapk[po[0]][po[1]] != self.ora:
                    bub += 1
                else:
                    maxb -= 1
            else:
                maxb -= 1
        while r:
            self.screen.fill(self.ora)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    r = 0
            if maxb == 0:
                text = self.font.render(f'У вас не было выхода...', True, [100, 255, 100])
            else:
                text = self.font.render(f'Спасибо за игру. {maxb, bub}', True, [100, 255, 100])
            textpos = (50, self.cy // 2 - 5)
            self.screen.blit(text, textpos)
            text = self.font.render(f'пройдено шагов: {steps}', True, [100, 255, 100])
            textpos = (50, self.cy // 2 + 35)
            self.screen.blit(text, textpos)
            timet = list(map(int, tim.strftime('%H %M %S').split()))
            started = list(map(int, sta2.strftime('%H %M %S').split()))
            timet = timet[0] * 3600 + timet[1] * 60 + timet[2]
            started = started[0] * 3600 + started[1] * 60 + started[2]
            text = self.font.render(f'прожито секунд: {timet - started} с.', True, [100, 255, 100])
            textpos = (50, self.cy // 2 + 75)
            self.screen.blit(text, textpos)
            text = self.font.render(f'счёт: {self.X * self.Y - score} из {self.X * self.Y}.', True, [100, 255, 100])
            textpos = (50, self.cy // 2 + 135)
            self.screen.blit(text, textpos)
            pygame.display.update()

    def client(self):
        text = 'V1.2.2'
        schet = 0
        speed = 1
        steps = 0
        sta2 = datetime.now()
        quit = datetime.now()
        time_obj = datetime.now()
        time_2 = False
        mapk = [[self.grey for i in range(self.Y)] for ii in range(self.X)]
        sch = -1
        a = [0, 0]
        lasta = a[:]
        running = 1
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.screen.fill(self.ora)
        stext = self.font.render("WAITING FOR SERVER", True, [255, 255, 255])
        self.screen.blit(stext, (200, 100))
        pygame.display.update()

        clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        clientSocket.connect((self.CLIENT, self.PORT))
        print(clientSocket.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE))

        try:
            sentence2 = clientSocket.recv(512).decode().split('#')
        except ConnectionResetError as e:
            print("Client connection closed")
            return 0

        sentence = f'map#{self.X}#{self.Y}'
        try:
            clientSocket.send(sentence.encode())
        except ConnectionResetError as e:
            print("Server connection closed")
            return 0

        if 'map' in sentence2:
            self.X, self.Y = min([int(sentence2[1]), self.X]), min([int(sentence2[2]), self.Y])

        lask2 = ''
        while running:
            self.screen.fill(self.ora)
            """рисуем поле"""
            for i in range(self.X):
                for j in range(self.Y):
                    nc = mapk[i][j]
                    self.drawc(40 + i * 60, 100 + j * 60, 40, nc)
            try:
                lask2 = list(map(int, clientSocket.recv(512).decode().split('#')))
                mapk[lask2[0]][lask2[1]] = [lask2[2], lask2[3], lask2[4]]
            except ConnectionResetError as e:
                print("Client connection closed")
                return 0
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    steps += 1
                    text = self.seecl(pos, event)
                    """определяем вариант свайпа, определяем стены, проверяем есть ли пропость там, куда шагаем"""
                    if text == '0 0':
                        if (datetime.now() - quit) < timedelta(seconds=0.3):
                            running = 0
                        else:
                            quit = datetime.now()
                    elif text == '>' and a[0] < self.X - 1 and mapk[a[0] + 1][a[1]] != self.ora:
                        a[0] += 1
                    elif text == '<' and a[0] > 0 and mapk[a[0] - 1][a[1]] != self.ora:
                        a[0] -= 1
                    elif text == 'u' and a[1] > 0 and mapk[a[0]][a[1] - 1] != self.ora:
                        a[1] -= 1
                    elif text == 'v' and a[1] < self.Y - 1 and mapk[a[0]][a[1] + 1] != self.ora:
                        a[1] += 1
            """если пол под нами провалился завершаем игру"""
            if mapk[lasta[0]][lasta[1]] == self.ora:
                running = 0
            elif mapk[lasta[0]][lasta[1]] == self.s1:
                """если стоим на жёлтом, то меняем на красный"""
                mapk[a[0]][a[1]] = self.s2
            elif mapk[lasta[0]][lasta[1]] == self.s3:
                if not time_2:
                    schet = 0
                    time_2 = datetime.now()
                else:
                    if (datetime.now() - time_2) > timedelta(seconds=10):
                        mapk[lasta[0]][lasta[1]] = self.ora
                    if (datetime.now() - time_2 - timedelta(seconds=schet)) > timedelta(seconds=0.8):
                        schet += 1.1
                    if timedelta(seconds=1) > (datetime.now() - time_2 - timedelta(seconds=schet)) > timedelta(
                            seconds=0.5):
                        i, j = lasta
                        self.drawc(40 + i * 60, 100 + j * 60, 40, self.s2)
            else:
                time_2 = False
                schet = 0
            texte = self.font.render(text, True, [100, 255, 100])

            try:
                i, j = a
                post = f'{i}#{j}#' + '#'.join(list(map(str, mapk[i][j]))) + f'#{a[0]}#{a[1]}'
                clientSocket.send(post.encode())
            except ConnectionResetError as e:
                print("Server connection closed")
                return 0
            pygame.draw.circle(self.screen, self.p2, (60 + lask2[5] * 60, 120 + lask2[6] * 60), 20)
            if lasta == a:
                pygame.draw.circle(self.screen, self.p1, (60 + a[0] * 60, 120 + a[1] * 60), 20)
            else:
                """плавное перемещение"""
                sch += 0.09
                i = sch
                if text in '<u':
                    i = 0 - sch
                if text in '<>':
                    pygame.draw.circle(self.screen, self.p1, (60 + (a[0] + i) * 60, 120 + a[1] * 60), 20)
                else:
                    pygame.draw.circle(self.screen, self.p1, (60 + a[0] * 60, 120 + (i + a[1]) * 60), 20)
                if sch >= 0:
                    lasta = a[:]
                    sch = -1
            textpose = (900, 200)
            self.screen.blit(texte, textpose)
            pygame.display.update()
        r = 1
        tim = datetime.now()
        score = 0
        maxb, bub = 3, 0
        for i in mapk:
            for j in i:
                if j != self.ora:
                    score += 1
        timpes = [[a[0], a[1] + 1], [a[0], a[1] - 1], [a[0] + 1, a[1]], [a[0] - 1, a[1]]]
        for i in range(3):
            po = timpes[i]
            if po[1] in range(self.X) and po[0] in range(self.Y):
                if mapk[po[0]][po[1]] != self.ora:
                    bub += 1
                else:
                    maxb -= 1
            else:
                maxb -= 1
        while r:
            self.screen.fill(self.ora)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    r = 0
            if maxb == 0:
                text = self.font.render(f'У вас не было выхода...', True, [100, 255, 100])
            else:
                text = self.font.render(f'Спасибо за игру. {maxb, bub}', True, [100, 255, 100])
            textpos = (50, self.cy // 2 - 5)
            self.screen.blit(text, textpos)
            text = self.font.render(f'пройдено шагов: {steps}', True, [100, 255, 100])
            textpos = (50, self.cy // 2 + 35)
            self.screen.blit(text, textpos)
            timet = list(map(int, tim.strftime('%H %M %S').split()))
            started = list(map(int, sta2.strftime('%H %M %S').split()))
            timet = timet[0] * 3600 + timet[1] * 60 + timet[2]
            started = started[0] * 3600 + started[1] * 60 + started[2]
            text = self.font.render(f'прожито секунд: {timet - started} с.', True, [100, 255, 100])
            textpos = (50, self.cy // 2 + 75)
            self.screen.blit(text, textpos)
            text = self.font.render(f'счёт: {self.X * self.Y - score} из {self.X * self.Y}.', True, [100, 255, 100])
            textpos = (50, self.cy // 2 + 135)
            self.screen.blit(text, textpos)
            pygame.display.update()


start = game()