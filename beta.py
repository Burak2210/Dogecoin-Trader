import sys
import pygame
import random
import threading
import time

pygame.init()

#set screen
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Dogecoin Trader")
pygame.display.set_icon(pygame.image.load("dogecoin.png"))
font = pygame.font.SysFont('Calibri', 45, bold=True)
background = pygame.image.load("bg.png")

#set button hitbox and images
dogecoin_logo = pygame.image.load("dogecoin.png")
buy = pygame.image.load("buy.png")
button_buy = pygame.draw.rect(screen, (0, 0, 0), (210, 130, buy.get_width(), buy.get_height()))
sell = pygame.image.load("sell.png")
button_sell = pygame.draw.rect(screen, (0, 0, 0), (210, 300, sell.get_width(), sell.get_height()))
dollar_image = pygame.image.load("dollar.png")
dollar_image = pygame.transform.scale(dollar_image, (dollar_image.get_width() * 0.07, dollar_image.get_height() * 0.07))
warning = pygame.image.load("warning.png")
warning = pygame.transform.scale(warning, (warning.get_width() * 0.5, warning.get_height() * 0.5))

#set values
dollar_wallet = 25
doge_wallet = 0
doge_value = random.randrange(10, 100, 5)

#redraw screen
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
    screen.blit(dogecoin_logo, (590, 255))  # sağ
    screen.blit(dogecoin_logo, (20, 220))  # sol
    screen.blit(dollar_image, (22, 290))
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
            #set buttons
            if button_buy.collidepoint(pos):
                if dollar_wallet >= doge_value:
                    dollar_wallet = dollar_wallet - int(doge_value)
                    doge_wallet = doge_wallet + 1
                else:
                    print("not enough dollars")

            if button_sell.collidepoint(pos):
                if doge_wallet >= 1:
                    dollar_wallet = dollar_wallet + int(doge_value)
                    doge_wallet = doge_wallet - 1
                else:
                    print("not enough dogecoin(s)")

    #update doge value
    if time % 2000 == 0:
        doge_value = random.randrange(10, 100, 5)

    update()
    pygame.display.flip()
