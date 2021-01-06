import pygame
import sys
import random

# Инициализируем игру
pygame.init()

# Задаём необходимые значения
# Скорость
speed = [4, 4]
# Кол-во подарков на поле
presents = 2
# Желаемое кол-во fps (кадров в секунду)
fps = 60
# Цвета
black = 0, 0, 0
white = 255, 255, 255
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
player = pygame.transform.scale(pygame.image.load("player.png"), (200, 200))
player_rect = player.get_rect()
player_rect.update(150, 10, 200, 200)
# Подарки
present = pygame.transform.scale(pygame.image.load("present.png"), (100, 100))
present_rects = []
for i in range(0, presents):
    present_rect = present.get_rect()
    present_rect.update(random.randint(0, 900), random.randint(0, 700), 100, 100)
    present_rects.append(present_rect)

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
        player_rect = player_rect.move(-8, 0)
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_rect = player_rect.move(8, 0)

    # Обрабатываем клавиши вертикального передвижения
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_rect = player_rect.move(0, -8)
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_rect = player_rect.move(0, 8)

    # Запрещаем игроку выходить за поле
    if player_rect.left < 0:
        player_rect.left = 0
    elif player_rect.left > 800:
        player_rect.left = 800

    if player_rect.top < 0:
        player_rect.top = 0
    elif player_rect.top > 600:
        player_rect.top = 600

    # Смотрим, собрал ли игрок подарок
    for present_rect in present_rects:
        if player_rect.contains(present_rect):
            # Если собрал, то перемещаем подарок в другое место и прибавляем 1 к очкам
            present_rect.update(random.randint(0, 900), random.randint(0, 700), 100, 100)
            score += 1
    # Начинаем рисовать
    # Фон
    screen.fill(white)
    # Игрок
    screen.blit(player, player_rect)
    # Подарки
    for present_rect in present_rects:
        screen.blit(present, present_rect)
    # Очки
    text = font.render(str(score), True, black)
    screen.blit(text, (50, 50))

    # Обновляем экран
    pygame.display.update()

    # А как это работает я не знаю, но без него нельзя
    clock.tick(fps)
