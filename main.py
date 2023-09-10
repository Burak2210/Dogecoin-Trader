import sys
import pygame
from pygame import mixer
import random
import json
import threading
import time

pygame.init()
mixer.init()

debug = False

# defining screen etc.
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Dogecoin Trader")
pygame.display.set_icon(pygame.image.load("assets/dogecoin.bmp"))
font = pygame.font.Font('assets/font.ttf', 45)
font_bigger = pygame.font.Font('assets/font.ttf', 55)
font_smaller = pygame.font.Font('assets/font.ttf', 20)
# defining images of buttons
buy_image = pygame.image.load("assets/buy.bmp")
shop_image = pygame.image.load("assets/shop.bmp")
sell_image = pygame.image.load("assets/sell.bmp")
back_image = pygame.image.load("assets/back.bmp")
reset_image = pygame.image.load("assets/reset.bmp")
reset_image = pygame.transform.scale(reset_image, (reset_image.get_width() * 1.5, reset_image.get_height() * 1.5))
shop_doge_happy_image = pygame.image.load("assets/doge_happy.bmp")
shop_doge_happy_image = pygame.transform.scale(shop_doge_happy_image, (
    shop_doge_happy_image.get_width() * 0.8, shop_doge_happy_image.get_height() * 0.8))
# defining buttons
buy_button = pygame.draw.rect(screen, (0, 0, 0), (0, 0, buy_image.get_width(), buy_image.get_height()))
sell_button = pygame.draw.rect(screen, (0, 0, 0), (0, 0, sell_image.get_width(), sell_image.get_height()))
shop_button = pygame.draw.rect(screen, (0, 0, 0), (0, 0, shop_image.get_width(), shop_image.get_height()))
back_button = pygame.draw.rect(screen, (0, 0, 0), (0, 0, back_image.get_width(), back_image.get_height()))
reset_button = pygame.draw.rect(screen, (0, 0, 0), (0, 0, reset_image.get_width(), reset_image.get_height()))
shop_doge_happy_button = pygame.draw.rect(screen, (0, 0, 0),
                                          (0, 0, shop_doge_happy_image.get_width(), shop_doge_happy_image.get_height()))
# defining images
background = pygame.image.load("assets/bg.bmp")
dogecoin_logo = pygame.image.load("assets/dogecoin.bmp")
dogecoin_logo = pygame.transform.scale(dogecoin_logo,
                                       (dogecoin_logo.get_width() * 0.09, dogecoin_logo.get_height() * 0.09))
dollar_image = pygame.image.load("assets/dollar.bmp")
warning = pygame.image.load("assets/warning.bmp")
warning = pygame.transform.scale(warning, (warning.get_width() * 0.09, warning.get_height() * 0.09))
# defining sounds

coin_sound = mixer.Sound("sounds/coin.wav")
mixer.Sound.set_volume(coin_sound, 0.4)
coin_sound_2 = mixer.Sound("sounds/coin2.wav")
mixer.Sound.set_volume(coin_sound_2, 0.5)
mixer.music.load("sounds/background_music.mp3")
mixer.music.set_volume(0.7)
mixer.music.play(-1)

# setting values

save_value = {
    'dollar_wallet': 25,
    'doge_wallet': 0,
    'doge_happy': False,
}
try:
    with open('data/save.json') as save_read:
        save_value = json.load(save_read)
except:
    pass
dollar_wallet = save_value['dollar_wallet']
doge_wallet = save_value['doge_wallet']
doge_happy = save_value['doge_happy']
doge_value = 55


# defining multithreading for doge value update
def doge_value_update_func():
    global doge_value
    while True:
        time.sleep(2)
        doge_value = random.randrange(10, 100, 5)


doge_value_update_thread = threading.Thread(target=doge_value_update_func, daemon=True)

# defining multithreading for get mouse pos (debug)

# screen.blit(pos_text, (500, 0))


# defining multithreading for warnings

buy_warn = False
sell_warn = False


def buy_warn_func():
    global buy_warn
    while True:
        if buy_warn:
            time.sleep(2)
            buy_warn = False


def sell_warn_func():
    global sell_warn
    while True:
        if sell_warn:
            time.sleep(2)
            sell_warn = False


buy_warn_thread = threading.Thread(target=buy_warn_func, daemon=True)
sell_warn_thread = threading.Thread(target=sell_warn_func, daemon=True)

# defining multithreading for delaying shop and back buttons

sbbp = False  # shop or back button pressed
sent_by_end_screen = False


def sbbp_func():
    global sbbp
    while True:
        if sbbp:
            time.sleep(1)
            sbbp = False


sbbp_thread = threading.Thread(target=sbbp_func, daemon=True)


def main_menu():
    global buy_button, sell_button, shop_button, sbbp
    global buy_warn, sell_warn, buy_warn_thread, sell_warn_thread
    global doge_value, dollar_wallet, doge_wallet, doge_happy, save_value
    global sent_by_end_screen
    while True:
        # display images
        screen.blit(background, (0, 0))
        if doge_happy:
            if not sent_by_end_screen:
                ending()
            else:
                doge_happy_info = font_smaller.render("Note: doge is happy, there is no point after that.", True,
                                                      (255, 255, 255))
                screen.blit(doge_happy_info, (10, 0))
        pos_text = font.render(str(pygame.mouse.get_pos()), True, (255, 0, 0))
        if debug:
            screen.blit(pos_text, (500, 0))
        screen.blit(dogecoin_logo, (590, 260))  # right
        screen.blit(dogecoin_logo, (20, 225))  # left
        screen.blit(dollar_image, (20, 295))

        # display buttons with images
        buy_button = pygame.draw.rect(screen, (0, 0, 0), (210, 130, buy_image.get_width(), buy_image.get_height()))
        screen.blit(buy_image, (210, 130))

        sell_button = pygame.draw.rect(screen, (0, 0, 0), (210, 300, sell_image.get_width(), sell_image.get_height()))
        screen.blit(sell_image, (210, 300))

        shop_button = pygame.draw.rect(screen, (0, 0, 0), (600, 500, shop_image.get_width(), shop_image.get_height()))
        screen.blit(shop_image, (600, 500))

        # display text
        ui_doge_value = font.render("= " + str(doge_value) + " $", True, (255, 255, 255))
        ui_dollar_wallet = font.render("= " + str(dollar_wallet), True, (255, 255, 255))
        ui_doge_wallet = font.render("= " + str(doge_wallet), True, (255, 255, 255))
        screen.blit(ui_doge_value, (650, 260))
        screen.blit(ui_dollar_wallet, (80, 293))
        screen.blit(ui_doge_wallet, (80, 223))

        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # save values
                save_value = {
                    'dollar_wallet': dollar_wallet,
                    'doge_wallet': doge_wallet,
                    'doge_happy': doge_happy,
                }
                with open("data/save.json", "w") as save_write:
                    json.dump(save_value, save_write)

                pygame.quit()
                sys.exit()
            # check if buttons clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if buy_button.collidepoint(pos):
                    if dollar_wallet >= doge_value:
                        dollar_wallet = dollar_wallet - int(doge_value)
                        doge_wallet = doge_wallet + 1
                        mixer.Sound.play(coin_sound)
                    else:
                        # start thread if not enough dollars (don't start if already started)
                        buy_warn = True
                        mixer.Sound.play(coin_sound_2)
                if sell_button.collidepoint(pos):
                    if doge_wallet >= 1:
                        dollar_wallet = dollar_wallet + int(doge_value)
                        doge_wallet = doge_wallet - 1
                        mixer.Sound.play(coin_sound)
                    else:
                        # start thread if not enough doges (don't start if already started)
                        sell_warn = True
                        mixer.Sound.play(coin_sound_2)
                if shop_button.collidepoint(pos):
                    if not sbbp:
                        sbbp = True
                        mixer.Sound.play(coin_sound)
                        shop()
                    if sbbp:
                        mixer.Sound.play(coin_sound_2)
        # check if warning should be shown
        if buy_warn is True:
            screen.blit(warning, (15, 350))
        if sell_warn is True:
            screen.blit(warning, (15, 160))

        pygame.display.update()


def shop():
    global shop_doge_happy_button, back_button, sbbp
    global doge_wallet, doge_happy, save_value
    while True:
        # display images
        screen.blit(background, (0, 0))
        if doge_happy:
            doge_happy_info = font_smaller.render("Note: doge is happy, there is no point after that.", True,
                                                  (255, 255, 255))
            screen.blit(doge_happy_info, (10, 0))
        pos_text = font.render(str(pygame.mouse.get_pos()), True, (255, 0, 0))
        if debug:
            screen.blit(pos_text, (500, 0))
        # display buttons with images
        shop_doge_happy_button = pygame.draw.rect(screen, (0, 0, 0),
                                                  (50, 50, shop_doge_happy_image.get_width(),
                                                   shop_doge_happy_image.get_height()))
        screen.blit(shop_doge_happy_image, (50, 50))

        back_button = pygame.draw.rect(screen, (0, 0, 0), (600, 500, back_image.get_width(), back_image.get_height()))
        screen.blit(back_image, (600, 500))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # save values
                save_value = {
                    'dollar_wallet': dollar_wallet,
                    'doge_wallet': doge_wallet,
                    'doge_happy': doge_happy,
                }
                with open("data/save.json", "w") as save_write:
                    json.dump(save_value, save_write)

                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # come back to main menu when pressed
                if back_button.collidepoint(pos):
                    if not sbbp:
                        sbbp = True
                        mixer.Sound.play(coin_sound)
                        main_menu()
                    if sbbp:
                        mixer.Sound.play(coin_sound_2)
                if shop_doge_happy_button.collidepoint(pos):
                    if doge_wallet >= 1000000 and not doge_happy:
                        doge_wallet = doge_wallet - 1000000
                        mixer.Sound.play(coin_sound)
                        doge_happy = True
                        ending()
                    else:
                        mixer.Sound.play(coin_sound_2)

        pygame.display.update()


def ending():
    global back_button, back_image
    global reset_button, reset_image
    global save_value
    global sent_by_end_screen

    while True:
        screen.fill((0, 0, 0))
        pos_text = font.render(str(pygame.mouse.get_pos()), True, (255, 0, 0))
        if debug:
            screen.blit(pos_text, (500, 0))
        doge_happy_text = font_bigger.render("U made doge happy :)", True, (255, 255, 255))
        screen.blit(doge_happy_text, (90, 160))
        back_button = pygame.draw.rect(screen, (0, 0, 0),
                                       (80, 350, back_image.get_width() * 1.5, back_image.get_height() * 1.5))
        screen.blit(pygame.transform.scale(back_image, (back_image.get_width() * 1.5, back_image.get_height() * 1.5)),
                    (80, 350))
        reset_button = pygame.draw.rect(screen, (0, 0, 0),
                                        (450, 350, reset_image.get_width(), reset_image.get_height()))
        screen.blit(reset_image, (450, 350))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # save values
                save_value = {
                    'dollar_wallet': dollar_wallet,
                    'doge_wallet': doge_wallet,
                    'doge_happy': doge_happy,
                }
                with open("data/save.json", "w") as save_write:
                    json.dump(save_value, save_write)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # come back to main menu when pressed
                if back_button.collidepoint(pos):
                    mixer.Sound.play(coin_sound)
                    sent_by_end_screen = True
                    main_menu()
                if reset_button.collidepoint(pos):
                    save_value = {
                        'dollar_wallet': 25,
                        'doge_wallet': 0,
                        'doge_happy': False,
                    }
                    with open("data/save.json", "w") as save_write:
                        json.dump(save_value, save_write)
                    mixer.Sound.play(coin_sound)
                    pygame.quit()
                    sys.exit()
                pygame.quit()
                sys.exit()
        pygame.display.update()


doge_value_update_thread.start()
buy_warn_thread.start()
sell_warn_thread.start()
sbbp_thread.start()

main_menu()
