import pygame
import sys
import random


class Player:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("player.png"), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.update(150, 10, 100, 100)


class Tree:
    def __init__(self, _player, trees=[], presents=[]):
        self.image = pygame.transform.scale(pygame.image.load("tree.png"), (150, 150))
        self.rect = self.image.get_rect()
        self.rect.update(random.randint(0, 850), random.randint(0, 650), 150, 150)
        for present in presents:
            for tree in trees:
                while (self.rect.colliderect(_player.rect) == 1) or (self.rect.colliderect(tree.rect) == 1) or (
                        self.rect.colliderect(present.rect) == 1):
                    self.rect.update(random.randint(0, 900), random.randint(0, 700), 150, 150)


class Present:
    def __init__(self, trees, _player, presents=[]):
        self.image = pygame.transform.scale(pygame.image.load("present.png"), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.update(random.randint(0, 900), random.randint(0, 700), 50, 50)
        for present in presents:
            for TREE in trees:
                while (self.rect.colliderect(TREE.rect) == 1) or (self.rect.colliderect(_player.rect) == 1) or (
                        self.rect.colliderect(present.rect) == 1):
                    self.rect.update(random.randint(0, 900), random.randint(0, 700), 50, 50)


# Инициализируем игру
pygame.init()

# Задаём необходимые значения
# Кол-во подарков на поле
presents = 4
# Кол-во препятствий (деревьев) на поле
trees_count = 3
# Желаемое кол-во fps (кадров в секунду)
fps = 60
# Цвета
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
# Размер окна
size = width, height = 1000, 800
# Кол-во собранных подарков
score = 0

# Выполняем приготовления
# Создаём окно
screen = pygame.display.set_mode(size)
# Устанавливаем заголовок окна
pygame.display.set_caption("Happy New Year")

# Получаем необходиые элементы
clock = pygame.time.Clock()
font = pygame.font.Font(None, 100)

# Создаём и настраиваем объекты
# Игрок
player = Player()

# Деревья
tree_list = []
for i in range(0, trees_count):
    tree = Tree(player, tree_list)
    tree_list.append(tree)

# Подарки
present_list = []
for i in range(0, presents):
    present = Present(tree_list, player, present_list)
    present_list.append(present)

while True:
    # Обработка выхода из игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(f"Goodbye. Your score was {str(score)}.")
            sys.exit()

    # Получаем нажатые клавиши
    keys = pygame.key.get_pressed()
    # Обрабатываем клавиши горизонтального передвижения
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.rect = player.rect.move(-6, 0)
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.rect = player.rect.move(6, 0)

    # Обрабатываем клавиши вертикального передвижения
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.rect = player.rect.move(0, -6)
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.rect = player.rect.move(0, 6)

    # Запрещаем игроку выходить за поле
    if player.rect.left < 0:
        player.rect.left = 0
    elif player.rect.left > 900:
        player.rect.left = 900

    if player.rect.top < 0:
        player.rect.top = 0
    elif player.rect.top > 700:
        player.rect.top = 700

    # Смотрим, собрал ли игрок подарок
    for present in present_list:
        if player.rect.contains(present.rect):
            # Если собрал, то перемещаем подарок в другое место и прибавляем 1 к очкам
            present_list.remove(present)
            new_present = Present(tree_list, player)
            present_list.append(new_present)
            score += 1

    for tree in tree_list:
        if tree.rect.contains(player.rect) == 1:
            # Если игрок врезался в ёлку
            tree_list.remove(tree)
            new_tree = Tree(player, tree_list)
            tree_list.append(new_tree)
            score -= 2
    # Начинаем рисовать
    # Фон
    screen.fill(white)
    # Игрок
    screen.blit(player.image, player.rect)
    # Подарки
    for present in present_list:
        screen.blit(present.image, present.rect)
    # Деревья
    for tree in tree_list:
        screen.blit(tree.image, tree.rect)
    # Очки
    if score < 0:
        text = font.render(str(score), True, red)
    else:
        text = font.render(str(score), True, black)
    screen.blit(text, (50, 50))

    # Обновляем экран
    pygame.display.update()

    # А как это работает я не знаю, но без него нельзя
    clock.tick(fps)
