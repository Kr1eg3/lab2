import numpy as np
import pygame
import random

pygame.init()                    # Запустили пайгейм
fpsClock = pygame.time.Clock()   # Функция для ФПС



not_done = True
""" Объявлем константы
"""
DIS_SIZE = (600, 400)
FPS = 100


DISPLAY = pygame.display.set_mode(DIS_SIZE)              # Поверхность для отрисовки
pygame.display.set_caption('Molecular dinamics')         # Название экрана 


class Particle:
    """ Класс, который создает частицу

        Arguments:
            radius  {int} -- радиус частицы
            posx {int} -- начальная координата Х
            posy {int} -- начальная координата Y
            color {tuple} -- цвет частицы в RGB 
    """

    def __init__(self, radius, posx, posy, color):
        self.radius = radius
        self.posx = posx
        self.posy = posy
        self.r = np.array([self.posx, self.posy])
        self.color = color
        self.speed = np.array([float(random.randint(1, 4)), float(random.randint(1, 4))])
        #self.speed = np.array([0, 0]) 
        self.pygame = pygame
         
    def render(self):
        """ Отрисовывает частицу
        """
        self.pygame.draw.circle(DISPLAY, center = (self.r[0], self.r[1]), color = self.color, radius = self.radius)
        #self.pygame.draw.circle(DISPLAY, center = (self.r[0], self.r[1]), color = (255, 255, 255), radius = self.radius, width = 3) 

    def collision(self, particles):    
        parts = self.neighbours(particles)
        if self.r[0] >= 600 - self.radius or self.r[0] <= 0 + self.radius:
            self.speed[0] *= -1
        elif self.r[1] >= 400 - self.radius or self.r[1] <= 0 + self.radius:
            self.speed[1] *= -1       
        for i in range(len(parts)):
            if self.interval(self.r[0], self.r[1], parts[i].r[0], parts[i].r[1]) <= 2*self.radius:
                self.speed *= -1
    
    def coord_update(self, particles):
        dt = 0.05
        #self.r += self.speed + self.LJ(particles)  
        self.r += self.LJ(particles)                   

    def interval(self, x1, y1, x2, y2):
        interval = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return interval

    def neighbours(self, particles):       
        part = particles  
        check_rad = 4*self.radius
        neib_list = []
        for i in range(len(part)):      
            if self.interval(self.r[0], self.r[1], part[i].r[0], part[i].r[1]) <= check_rad and \
                self.interval(self.r[0], self.r[1], part[i].r[0], part[i].r[1]) != 0:
                neib_list.append(part[i])
        return neib_list

    def sumF(self):
        sumF = np.array([0, 0])
        return sumF
    
    def F1(self, particles):
        G = 100
        F = 0
        a = 0
        for i in range(len(self.neighbours(particles))):
            r = self.interval(self.r[0], self.r[1], self.neighbours(particles)[i].r[0], self.neighbours(particles)[i].r[1])
            F += G / r ** 2
            a += np.array([self.neighbours(particles)[i].r[0] - self.r[0], self.neighbours(particles)[i].r[1] - self.r[1]]) / r * F
        return a   

    def LJ(self, particles):
        D = 0.5e-1
        a = 0.0001
        F = 0
        for i in range(len(self.neighbours(particles))):
            r = self.interval(self.r[0], self.r[1], self.neighbours(particles)[i].r[0], self.neighbours(particles)[i].r[1])
            F += (12 * D / a * ((a/r)**13 - (a/r)**7)) * np.array([(self.neighbours(particles)[i].r[0] - self.r[0])/r, \
                (self.neighbours(particles)[i].r[1] - self.r[1])/r]) * 1e32
            print(F) 
        return F 

    def _is_it_me(self, x2, y2):
        # Если интервал 0, то выведи True, иначе False
        pass

    def _func(self):
        pass


# Цикл который создает лист p с экзеплярами класса частиц (то есть сами частицы)

num = 100
p = [] 
                             
# for particles in range(num):
#     p.append(Particle(30, float(random.randint(20, 500)), float(random.randint(20, 350)), (255, 0, 0)))

for x in range(0,200,10):
    for y in range(0,200,10):
        p.append(Particle(3, 250.0 + x, 150.0 + y, (255, 0, 0)))
# for x in range(300, 300 + (n[0] - 1) * 2*5 + 1, 2*5 + 1):
#     for y in range(100, 100 + (n[1] - 1) * 2*5 + 1, 2*5+1):
#         p.append(Particle(5, x, y, (255, 0, 0)))


def main():
    """ Главный цикл

    """

    while not_done:
        """ 1. Обновляем лист 
            2. Проверяем на нажатие Х
            3. Отрисовываем круг
            4. Меням позицию Х
            5. Меняем позицию У
            6. Обновляем весь лист
        """
        # Чистим лист
        DISPLAY.fill((0, 0, 0))
    
        # Проверка на то, что мы нажали на крестик    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print(p[0].interval(1, 1, 2, 2))
                
        # Отрисовка объекта
        for particle in range(num):
            p[particle].render()

        # Проверка на стенку
        for particle in range(num):
            p[particle].collision(p)
            p[particle].coord_update(p)
        
        # Обновить лист
        pygame.display.flip() 

        #print(p[0].LJ(p))
    
        # Вывод каждого 30 кадра
        fpsClock.tick(FPS)


if __name__ == '__main__':    # PEP-8
    main()
    

