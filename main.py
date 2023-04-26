import os
import sys

import pygame
import requests

api_server = "http://static-maps.yandex.ru/1.x/"

ZOOM = 5
LON, LAT = "23.734862", "37.975487"

params = {
    "ll": ",".join([LON, LAT]),
    "z": ZOOM,
    "l": "map"
}

map_file = "map.png"


def file_update(ZOOM, LON, LAT):
    params = {
        "ll": ",".join([LON, LAT]),
        "z": ZOOM,
        "l": "map"
    }
    response = requests.get(api_server, params=params)

    if not response:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))


params = {
        "ll": ",".join([LON, LAT]),
        "z": ZOOM,
        "l": "map"
    }
response = requests.get(api_server, params=params)

if not response:
    print("Ошибка выполнения запроса:")
    print(response.url)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

with open(map_file, "wb") as file:
    file.write(response.content)


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
            print(LAT)
            if event.key == pygame.K_PAGEUP:
                if ZOOM < 23:
                    ZOOM += 1
                    file_update(ZOOM, LON, LAT)
            elif event.key == pygame.K_PAGEDOWN:
                if ZOOM > 0:
                    ZOOM -= 1
                    file_update(ZOOM, LON, LAT)
            elif event.key == pygame.K_UP:

                if float(LAT) + 5 <= 87:
                    LAT = str(float(LAT) + 5)
                    file_update(ZOOM, LON, LAT)
            elif event.key == pygame.K_DOWN:
                if float(LAT) - 5 >= -87:
                    LAT = str(float(LAT) - 5)
                    file_update(ZOOM, LON, LAT)

            elif event.key == pygame.K_RIGHT:
                if float(LON) + 5 <= 180:
                    LON = str(float(LON) + 5)
                    file_update(ZOOM, LON, LAT)
                else:
                    LON = str(-((float(LON) + 5) % 180) - 180)
            elif event.key == pygame.K_LEFT:
                if float(LON) - 5 >= -180:
                    LON = str(float(LON) - 5)
                    file_update(ZOOM, LON, LAT)
                else:
                    LON = str(180 - (float(LON) - 5 + 180))

    pygame.display.flip()


pygame.quit()
os.remove(map_file)
