# using library from https://github.com/rdagger/micropython-ili9341

import ili9341
import utime
import mySetup

from machine import Pin, SPI
from sys import implementation
from os import uname
from xglcd_font import XglcdFont
led = Pin(21, Pin.OUT)
led.high()
display = mySetup.createMyDisplay()
unispace = XglcdFont('lib/fonts/Unispace12x24.c', 12, 24)
text = "Linia Kierunek      Odjazd"
line = "1"
direction = "Potulicka"
departure = "za 12 min"


def print_board(linia, kierunek, odjazd):
    text2 = '{:' '<3}'.format(linia[:3]) +\
            ' ' + '{:' '<11}'.format(kierunek[:11]) +\
            ' ' + '{:>9}'.format(odjazd[:9])          
    display.draw_text(0, 0, text, unispace,
                      ili9341.color565(10, 200, 252))  # ostatnia wyświetlana linia
    display.draw_text(0, 36, text2, unispace,
                      ili9341.color565(0, 0, 200))
    display.draw_text(0, 72, text2, unispace,
                      ili9341.color565(200, 200, 200))
    display.draw_text(0, 108, text2, unispace,
                      ili9341.color565(200, 200, 200))
    display.draw_text(0, 144, text2, unispace,
                      ili9341.color565(200, 200, 200))
    display.draw_text(0, 180, text2, unispace,
                      ili9341.color565(200, 200, 200))
    display.draw_text(0, 216, text2, unispace,
                      ili9341.color565(200, 20, 10))  # ostatnia wyświetlana linia

# generowanie przerwań cyklicznych do synchrnizacji czasu z serwerem ntp
#timer = Timer(period=18000000, mode=Timer.PERIODIC, callback=lambda t: ntptime.settime)
   
   
print_board(line,direction,departure)   
# wczytywanie danych sieci i url przystanków z pliku konfiguracyjnego   
# with open('config.json', 'r') as f:
#     data = json.load(f)
#     wifi_list = data['networks']
#     stops_list = data['transport_stop']
# 
# print("Poczekajmy")
# # sleep(10)
# while True:
#     while wlan.isconnected() == False:
#         connect_aval_wlan(wifi_list,wlan)   
#         sleep(2)        
#     sleep(3)  # okres odświeżania
#     get_and_display(stops_list)
    
    


