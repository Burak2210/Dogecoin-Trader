import sys
import pygame
from pygame import mixer
import random
import threading
import time

pygame.init()
mixer.init()

# set screen
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Dogecoin Trader")
pygame.display.set_icon(pygame.image.load("dogecoin.png"))
font = pygame.font.Font('PixeloidSans-mLxMm.ttf', 45)
background = pygame.image.load("bg.png")

# set button hitbox, image and sounds
dogecoin_logo = pygame.image.load("dogecoin.png")
dogecoin_logo = pygame.transform.scale(dogecoin_logo, (dogecoin_logo.get_width() * 0.09, dogecoin_logo.get_height() * 0.09))
buy = pygame.image.load("buy.png")
button_buy = pygame.draw.rect(screen, (0, 0, 0), (210, 130, buy.get_width(), buy.get_height()))
sell = pygame.image.load("sell.png")
button_sell = pygame.draw.rect(screen, (0, 0, 0), (210, 300, sell.get_width(), sell.get_height()))
dollar_image = pygame.image.load("dollar.png")
warning = pygame.image.load("warning.png")
warning = pygame.transform.scale(warning, (warning.get_width() * 0.5, warning.get_height() * 0.5))
coin_sound = mixer.Sound("coin.wav")
mixer.Sound.set_volume(coin_sound, 0.5)
mixer.music.load("background_music.mp3")
mixer.music.set_volume(0.7)
mixer.music.play(-1)

# set values
dollar_wallet = 25
doge_wallet = 0
doge_value = random.randrange(10, 100, 5)


# redraw screen
def update():
    screen.blit(background, (0, 0))
    ui_doge_value = font.render("= " + str(doge_value) + " $", True, (255, 255, 255))
    ui_dollar_wallet = font.render("= " + str(dollar_wallet), True, (255, 255, 255))
    ui_doge_wallet = font.render("= " + str(doge_wallet), True, (255, 255, 255))
    screen.blit(ui_doge_value, (650, 260))
    screen.blit(ui_dollar_wallet, (80, 293))
    screen.blit(ui_doge_wallet, (80, 223))

    global button_buy
    global button_sell
    screen.blit(dogecoin_logo, (590, 260))  # sağ
    screen.blit(dogecoin_logo, (20, 225))  # sol
    screen.blit(dollar_image, (20, 295))
    button_buy = pygame.draw.rect(screen, (0, 0, 0), (210, 130, buy.get_width(), buy.get_height()))
    screen.blit(buy, (210, 130))
    button_sell = pygame.draw.rect(screen, (0, 0, 0), (210, 300, sell.get_width(), sell.get_height()))
    screen.blit(sell, (210, 300))


while True:
    pos = pygame.mouse.get_pos()
    time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # set buttons
            if button_buy.collidepoint(pos):
                if dollar_wallet >= doge_value:
                    dollar_wallet = dollar_wallet - int(doge_value)
                    doge_wallet = doge_wallet + 1
                else:
                    print("not enough dollars")
                mixer.Sound.play(coin_sound)
            if button_sell.collidepoint(pos):
                if doge_wallet >= 1:
                    dollar_wallet = dollar_wallet + int(doge_value)
                    doge_wallet = doge_wallet - 1
                else:
                    print("not enough dogecoin(s)")
                mixer.Sound.play(coin_sound)
    # update doge value
    if time % 2000 == 0:
        doge_value = random.randrange(10, 100, 5)

    update()
    pygame.display.flip()
