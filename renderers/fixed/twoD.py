from renderer.base import BaseRenderer
from time import sleep
from multiprocessing import Process, Lock
from enum import Enum

import random
import time
import pygame
import pygame.locals


class GameEvent:
    def __init__(self, type, state):
        self.type = type
        self.state = state


class GameEventType(Enum):
    SETUP = 1
    UPDATE = 2
    CLOSE = 3

class TwoDFixedRenderer(BaseRenderer):
    def __init__(self):
        self.delay = 0.5
        self.game_event = None
        self.start_game() #初始化游戏界面和参数
        self.step = 0
        self.round = 1
        self.actor_facing = 0
        self.arrow_direction = 0

    def setup(self, info=None):
        self.game_event = GameEvent(GameEventType.SETUP, None)
        self.one_loop()

    def update(self, state, info=None):
        self.game_event = GameEvent(GameEventType.UPDATE, state)
        for i in range(0, 15):
            self.one_loop()

    def close(self, info=None):
        self.game_event = GameEvent(GameEventType.CLOSE, None)
        self.one_loop()

    def start_game(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1024, 500
        self.WHITE = (255, 255, 255)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.toShang = pygame.image.load('../../renderer/fixed/上.png').convert_alpha()
        self.toZuo = pygame.image.load('../../renderer/fixed/左.png').convert_alpha()
        self.toYou = pygame.image.load('../../renderer/fixed/右.png').convert_alpha()
        self.toXia = pygame.image.load('../../renderer/fixed/下.png').convert_alpha()
        self.tower1 = pygame.image.load('../../renderer/fixed/塔1.png').convert_alpha()
        self.tower2 = pygame.image.load('../../renderer/fixed/塔2.png').convert_alpha()
        self.tower3 = pygame.image.load('../../renderer/fixed/塔3.png').convert_alpha()
        self.tower4 = pygame.image.load('../../renderer/fixed/塔4.png').convert_alpha()
        self.WINNER_FONT = pygame.font.SysFont('microsoftyaqiheibold', 66)
        self.person = pygame.Rect(410, 410, 100, 100)
        self.arrow0 = pygame.Rect(200, 310, 50, 50)
        self.arrow1 = pygame.Rect(620, 310, 50, 50)
        self.arrow2 = pygame.Rect(200, 520, 50, 50)
        self.arrow3 = pygame.Rect(620, 520, 50, 50)
        self.screen = pygame.display.set_mode((1024, 960))

    def draw_window(self, image, tower1, tower2, tower3, tower4, arrow, person, i):
        self.screen.fill((0, 0, 0))
        self.screen.blit(image, (person.x, person.y))
        self.screen.blit(tower1, (60, 180))
        self.screen.blit(tower2, (700, 180))
        self.screen.blit(tower3, (60, 560))
        self.screen.blit(tower4, (700, 560))
        arrow_img = pygame.image.load('../../renderer/fixed/arrow' + str(i) + '.png').convert_alpha()
        # pygame.Rect()
        self.screen.blit(arrow_img, (arrow.x, arrow.y))
        # 在新的位置上画图
        pygame.display.update()
        
    def arrow_move(self,arrow, arrow1, arrow2, arrow3, arrow4, person, image, i):
        self.result = 'not finished'
        if i == 0:
            if arrow.x + arrow.w < person.x - 10 and arrow.y + arrow.h < person.y - 10:
                arrow.x += 3
                arrow.y += 1
            else:

                # if image == self.toShang:
                #     self.result = 'win'
                #     self.step += 1
                # else:
                #     self.result = 'lose'
                #     self.step = 0
                # self.round += 1

                arrow.x = 200
                arrow.y = 310
                arrow2.x = 670
                arrow2.y = 310
                arrow3.x = 200
                arrow3.y = 560
                arrow4.x = 670
                arrow4.y = 560

        elif i == 1:
            if arrow.x > person.x + person.w + 10 and arrow.y + arrow.h < person.y - 10:
                arrow.x -= 3
                arrow.y += 1
            else:

                # if image == self.toYou:
                #     self.result = 'win'
                #     self.step += 1
                # else:
                #     self.result = 'lose'
                #     self.step = 0
                # self.round += 1

                arrow1.x = 200
                arrow1.y = 310
                arrow.x = 670
                arrow.y = 310
                arrow3.x = 200
                arrow3.y = 560
                arrow4.x = 670
                arrow4.y = 560

        elif i == 2:
            if arrow.x + arrow.w < person.x - 10 and arrow.y > person.y + person.h + 10:
                arrow.x += 3
                arrow.y -= 1
            else:

                # if image == self.toZuo:
                #     self.result = 'win'
                #     self.step += 1
                # else:
                #     self.result = 'lose'
                #     self.step = 0
                # self.round += 1

                arrow1.x = 200
                arrow1.y = 310
                arrow2.x = 670
                arrow2.y = 310
                arrow.x = 200
                arrow.y = 560
                arrow4.x = 670
                arrow4.y = 560


        elif i == 3:
            if arrow.x > person.x + person.w + 10 and arrow.y > person.y + person.h + 10:
                arrow.x -= 3
                arrow.y -= 1
            else:

                # if image == self.toXia:
                #     self.result = 'win'
                #     self.step += 1
                # else:
                #     self.result = 'lose'
                #     self.step = 0
                # self.round += 1

                arrow1.x = 200
                arrow1.y = 310
                arrow2.x = 670
                arrow2.y = 310
                arrow3.x = 200
                arrow3.y = 560
                arrow.x = 670
                arrow.y = 560
        print(self.result)
    def draw_result(self):

        text = "成功存活时长：" + str(self.step)
        draw_text = self.WINNER_FONT.render(text, 1, self.WHITE)
        self.screen.blit(draw_text, (self.WIDTH / 2 - draw_text.get_width() /
                                     2, self.HEIGHT / 2 - draw_text.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(1000)

    def draw_slogon(self):

        slogon = 'ROUND ' + str(self.round)
        draw_text = self.WINNER_FONT.render(slogon, 1, self.WHITE)
        self.screen.blit(draw_text, (self.WIDTH / 2 - draw_text.get_width() /
                                     2, self.HEIGHT / 2 - draw_text.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(100)

    def draw_lose(self):

        if self.result == 'lose':
            text = "LOSE"
            draw_text = self.WINNER_FONT.render(text, 1, self.WHITE)
            self.screen.blit(draw_text, (self.WIDTH / 2 - draw_text.get_width() /
                                         2, self.HEIGHT / 2 - draw_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(1000)

    def one_loop(self):
        clock = pygame.time.Clock()
        # person_direction = 3
        # arrow_direction = 0  # 默认从左上方发出，人面向右下方
        if self.game_event is not None:
            if self.game_event.type == GameEventType.SETUP:
                self.draw_slogon()  # 标明是第几回合
            elif self.game_event.type == GameEventType.UPDATE:
                if self.game_event.state is not None:
                    self.actor_facing = self.game_event.state[0]
                    self.arrow_direction = self.game_event.state[1]
                    self.step += 1
            elif self.game_event.type == GameEventType.CLOSE:
                self.draw_result()
                self.step = 0
            self.game_event.type = None

        image = None
        if self.actor_facing == 0:
            image = self.toShang
        elif self.actor_facing == 1:
            image = self.toYou
        elif self.actor_facing == 2:
            image = self.toZuo
        elif self.actor_facing == 3:
            image = self.toXia

        i = None
        arrow = None
        if self.arrow_direction == 0:
            arrow = self.arrow0
            i = 0
        elif self.arrow_direction == 1:
            arrow = self.arrow1
            i = 1
        elif self.arrow_direction == 2:
            arrow = self.arrow2
            i = 2
        elif self.arrow_direction == 3:
            arrow = self.arrow3
            i = 3
        self.arrow_move(arrow, self.arrow0, self.arrow1, self.arrow2, self.arrow3, self.person, image, i)
        self.draw_lose()
        self.draw_window(image, self.tower1,self.tower2, self.tower3, self.tower4, arrow, self.person, i)

        clock.tick(30)  # 控制每次屏幕刷新的时间间隔

