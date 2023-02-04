import os
import sys

import pygame
import requests

api_server = "http://static-maps.yandex.ru/1.x/"

ZOOM = 12
LON, LAT = "23.734862", "37.975487"

params = {
    "ll": ",".join([LON, LAT]),
    "z": ZOOM,
    "l": "map"
}

map_file = "map.png"


def file_update(params):
    response = requests.get(api_server, params=params)

    if not response:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    with open(map_file, "wb") as file:
        file.write(response.content)


file_update(params)


pygame.init()
pygame.display.set_caption('Большая задача по Maps API')
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if params['z'] < 23:
                    params['z'] += 1
            if event.key == pygame.K_DOWN:
                if params['z'] > 0:
                    params['z'] -= 1
    file_update(params)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()


pygame.quit()
os.remove(map_file)
