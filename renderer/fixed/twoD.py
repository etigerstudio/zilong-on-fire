from renderer.base import BaseRenderer
from time import sleep

import pygame
from pygame.locals import*
from sys import exit
import random
import time

class TwoDFixedRenderer(BaseRenderer):
    def __init__(self):
        self.delay = 0.5
        self.event = None
        self.start_game()
        self.step = 0
        # self.mutex = Lock()
        # gamethread=Tread(target=startgame)
        # gamethread.start()

    def setup(self, info=None):
        # self.lock.acquire()
        # if info is not None and 'delay' in info:
        #     self.delay = info['delay']
        #     print(f'GAME START {self.__get_info_text(info)}')
        #     sleep(self.delay)
        self.start_game()
        # rel

    def update(self, state, info=None):
        # print(f'Zilong:{state[0]} Arrow:{state[1]}'
        #       f' {self.__get_info_text(info)}')
        self.mainloop(state)
        sleep(self.delay)


    def close(self, info=None):
        # print(f'GAME OVER {self.__get_info_text(info)}\n')
        self.draw_winner()
        sleep(self.delay)

    def __get_info_text(self, info):
        if info is not None and 'text' in info:
            return info['text']

        return ''

    def draw_window(self,image, tower1, tower2, tower3, tower4, arrow, person, i):
        self.screen.fill((0, 0, 0))
        self.screen.blit(image, (person.x, person.y))
        self.screen.blit(tower1, (60, 180))
        self.screen.blit(tower2, (700, 180))
        self.screen.blit(tower3, (60, 560))
        self.screen.blit(tower4, (700, 560))
        arrow_img = pygame.image.load('F:/gitworkspace/zilong-on-fire/renderer/fixed/arrow' + str(i) + '.png').convert_alpha()
        # pygame.Rect()
        self.screen.blit(arrow_img, (arrow.x, arrow.y))
        # 在新的位置上画图
        pygame.display.update()


    def start_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1024, 960))
        self.toShang = pygame.image.load('F:/gitworkspace/zilong-on-fire/renderer/fixed/上.png').convert_alpha()
        self.toZuo = pygame.image.load('F:/gitworkspace/zilong-on-fire/renderer/fixed/左.png').convert_alpha()
        self.toYou = pygame.image.load('F:/gitworkspace/zilong-on-fire/renderer/fixed/右.png').convert_alpha()
        self.toXia = pygame.image.load('F:/gitworkspace/zilong-on-fire/renderer/fixed/下.png').convert_alpha()
        self.tower1 = pygame.image.load('F:/gitworkspace/zilong-on-fire/renderer/fixed/塔1.png').convert_alpha()
        self.tower2 = pygame.image.load('F:/gitworkspace/zilong-on-fire/renderer/fixed/塔2.png').convert_alpha()
        self.tower3 = pygame.image.load('F:/gitworkspace/zilong-on-fire/renderer/fixed/塔3.png').convert_alpha()
        self.tower4 = pygame.image.load('F:/gitworkspace/zilong-on-fire/renderer/fixed/塔4.png').convert_alpha()
        self.WINNER_FONT = pygame.font.SysFont('comicsans', 100)
        self.WIDTH, self.HEIGHT = 900, 500
        self.WHITE = (255, 255, 255)
        self.WINNER = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def arrow_move(self,arrow, arrow1, arrow2, arrow3, arrow4, person, image, i):
        self.result = 'not finished'
        if i == 1:
            if arrow.x + arrow.w < person.x - 10 and arrow.y + arrow.h < person.y - 10:
                arrow.x += 75
                arrow.y += 20
            else:

                if image == self.toShang:
                    self.result = 'win'
                    self.step += 1
                else:
                    self.result = 'lose'

                arrow.x = 200
                arrow.y = 310
                arrow2.x = 670
                arrow2.y = 310
                arrow3.x = 200
                arrow3.y = 560
                arrow4.x = 670
                arrow4.y = 560

        elif i == 2:
            if arrow.x > person.x + person.w + 10 and arrow.y + arrow.h < person.y - 10:
                arrow.x -= 75
                arrow.y += 20
            else:

                if image == self.toYou:
                    self.result = 'win'
                    self.step += 1
                else:
                    self.result = 'lose'

                arrow1.x = 200
                arrow1.y = 310
                arrow.x = 670
                arrow.y = 310
                arrow3.x = 200
                arrow3.y = 560
                arrow4.x = 670
                arrow4.y = 560

        elif i == 3:
            if arrow.x + arrow.w < person.x - 10 and arrow.y > person.y + person.h + 10:
                arrow.x += 75
                arrow.y -= 20
            else:

                if image == self.toZuo:
                    self.result = 'win'
                    self.step += 1
                else:
                    self.result = 'lose'

                arrow1.x = 200
                arrow1.y = 310
                arrow2.x = 670
                arrow2.y = 310
                arrow.x = 200
                arrow.y = 560
                arrow4.x = 670
                arrow4.y = 560


        elif i == 4:
            if arrow.x > person.x + person.w + 10 and arrow.y > person.y + person.h + 10:
                arrow.x -= 75
                arrow.y -= 20
            else:

                if image == self.toXia:
                    self.result = 'win'
                    self.step += 1
                else:
                    self.result = 'lose'
                arrow1.x = 200
                arrow1.y = 310
                arrow2.x = 670
                arrow2.y = 310
                arrow3.x = 200
                arrow3.y = 560
                arrow.x = 670
                arrow.y = 560
        print(self.result)

    def draw_winner(self):
        if self.result == 'lose':
            print("成功存活时长：" + str(self.step))
            self.step = 0
            text = 'LOSE '+ "成功存活时长：" + str(self.step)
            draw_text = self.WINNER_FONT.render(text, 1, self.WHITE)
            self.WINNER.blit(draw_text, (self.WIDTH / 2 - draw_text.get_width() /
                                    2, self.HEIGHT / 2 - draw_text.get_height() / 2))

            pygame.display.update()
            pygame.time.delay(1000)

    def mainloop(self, state):
        person = pygame.Rect(410, 410, 100, 100)
        arrow1 = pygame.Rect(200, 310, 50, 50)
        arrow2 = pygame.Rect(620, 310, 50, 50)
        arrow3 = pygame.Rect(200, 520, 50, 50)
        arrow4 = pygame.Rect(620, 520, 50, 50)

        clock = pygame.time.Clock()

        run = True
        start_time = time.time()
        arrow = arrow1
        i = 1
        Fullscreen = True
        # arrow_direction = '0'
        while run:
            clock.tick(1)  # 控制每次屏幕刷新的时间间隔
            for eventQ in pygame.event.get():
                if eventQ.type == QUIT:
                    exit()
                if eventQ.type == KEYDOWN:
                    if eventQ.key == K_f:
                        Fullscreen = not Fullscreen
                    if Fullscreen:
                        screen = pygame.display.set_mode((1024, 960), FULLSCREEN)
                    if not Fullscreen:
                        screen = pygame.display.set_mode((1024, 960), RESIZABLE)

            try:
                event = state[0]
            except:
                event = None
            if event == '0':
                image = self.toShang

            elif event == '1':
                image = self.toYou

            elif event == '2':
                image = self.toZuo

            elif event == '3':
                image = self.toXia

            else:
                image = self.toXia


            try:
                arrow_direction = state[1]
            except:
                arrow_direction = '1'

            if arrow_direction == '1':
                arrow = arrow1
                i = 1
            elif arrow_direction == '2':
                arrow = arrow2
                i = 2
            elif arrow_direction == '3':
                arrow = arrow3
                i = 3
            if arrow_direction == '4':
                arrow = arrow4
                i = 4

            self.arrow_move(arrow, arrow1, arrow2, arrow3, arrow4, person, image, i)
            # if reusult == 'lose':
            #     self.draw_winner()
            self.draw_window(image, self.tower1,self.tower2, self.tower3, self.tower4, arrow, person, i)
            time.sleep(0.1)

