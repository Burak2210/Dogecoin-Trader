import sys
import pygame
from pygame import mixer
import random
import json
import threading
import time

pygame.init()
mixer.init()

# set screen
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Dogecoin Trader - v1.0.3")
pygame.display.set_icon(pygame.image.load("assets/dogecoin.png"))
font = pygame.font.Font('assets/font.ttf', 45)
background = pygame.image.load("assets/bg.png")

# set button hitbox, image and sounds
dogecoin_logo = pygame.image.load("assets/dogecoin.png")
dogecoin_logo = pygame.transform.scale(dogecoin_logo,
                                       (dogecoin_logo.get_width() * 0.09, dogecoin_logo.get_height() * 0.09))
buy = pygame.image.load("assets/buy.png")
button_buy = pygame.draw.rect(screen, (0, 0, 0), (210, 130, buy.get_width(), buy.get_height()))
sell = pygame.image.load("assets/sell.png")
button_sell = pygame.draw.rect(screen, (0, 0, 0), (210, 300, sell.get_width(), sell.get_height()))
dollar_image = pygame.image.load("assets/dollar.png")
warning = pygame.image.load("assets/warning.png")
warning = pygame.transform.scale(warning, (warning.get_width() * 0.09, warning.get_height() * 0.09))
coin_sound = mixer.Sound("sounds/coin.wav")
mixer.Sound.set_volume(coin_sound, 0.5)
mixer.music.load("sounds/background_music.mp3")
mixer.music.set_volume(0.7)
mixer.music.play(-1)

# setting values

save_value = {
    'dollar_wallet': 25,
    'doge_wallet': 0,
}
try:
    with open('data/save.json') as save_read:
        save_value = json.load(save_read)
except:
    pass
dollar_wallet = save_value['dollar_wallet']
doge_wallet = save_value['doge_wallet']
doge_value = 55

# redraw screen
buy_warning = False
sell_warning = False


def update():
    screen.blit(background, (0, 0))
    global button_buy, button_sell
    global buy_warning, sell_warning
    screen.blit(dogecoin_logo, (590, 260))  # sağ
    screen.blit(dogecoin_logo, (20, 225))  # sol
    screen.blit(dollar_image, (20, 295))
    button_buy = pygame.draw.rect(screen, (0, 0, 0), (210, 130, buy.get_width(), buy.get_height()))
    screen.blit(buy, (210, 130))
    button_sell = pygame.draw.rect(screen, (0, 0, 0), (210, 300, sell.get_width(), sell.get_height()))
    screen.blit(sell, (210, 300))

    ui_doge_value = font.render("= " + str(doge_value) + " $", True, (255, 255, 255))
    ui_dollar_wallet = font.render("= " + str(dollar_wallet), True, (255, 255, 255))
    ui_doge_wallet = font.render("= " + str(doge_wallet), True, (255, 255, 255))
    screen.blit(ui_doge_value, (650, 260))
    screen.blit(ui_dollar_wallet, (80, 293))
    screen.blit(ui_doge_wallet, (80, 223))
    if buy_warning is True:
        screen.blit(warning, (15, 350))
    if sell_warning is True:
        screen.blit(warning, (15, 160))


# defining multithreading for warnings
buy_warn_thread_started = False
sell_warn_thread_started = False


def buy_warn():
    global buy_warning
    global buy_warn_thread_started
    buy_warning = True
    time.sleep(2)
    buy_warning = False
    buy_warn_thread_started = False


def sell_warn():
    global sell_warning
    global sell_warn_thread_started
    sell_warning = True
    time.sleep(2)
    sell_warning = False
    sell_warn_thread_started = False


while True:
    pos = pygame.mouse.get_pos()
    ticks = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_value = {
                'dollar_wallet': dollar_wallet,
                'doge_wallet': doge_wallet,
            }
            with open("data/save.json", "w") as save_write:
                json.dump(save_value, save_write)
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # set buttons
            if button_buy.collidepoint(pos):
                if dollar_wallet >= doge_value:
                    dollar_wallet = dollar_wallet - int(doge_value)
                    doge_wallet = doge_wallet + 1
                else:
                    if not buy_warn_thread_started:
                        buy_warn_thread = threading.Thread(target=buy_warn, daemon=True)
                        buy_warn_thread.start()
                        buy_warn_thread_started = True
                mixer.Sound.play(coin_sound)
            if button_sell.collidepoint(pos):
                if doge_wallet >= 1:
                    dollar_wallet = dollar_wallet + int(doge_value)
                    doge_wallet = doge_wallet - 1
                else:
                    if not sell_warn_thread_started:
                        sell_warn_thread = threading.Thread(target=sell_warn, daemon=True)
                        sell_warn_thread.start()
                        sell_warn_thread_started = True
                mixer.Sound.play(coin_sound)
    # update doge value
    if ticks % 2000 == 0:
        doge_value = random.randrange(10, 100, 5)

    update()
    pygame.display.flip()
