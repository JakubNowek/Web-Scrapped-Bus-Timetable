# TODO
# automatyczny wybór WiFi
# zmiana przystanków
# wyświetlanie na wyświetlaczu**
# wyświetlanie polskich znaków***

import urequests as requests
import network
import socket
import ntptime
from time import sleep, localtime, ticks_ms as timer
from picozero import pico_led
from machine import reset, Timer
import re
from replaceunicode import txtReplace

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
pico_led.off()
wlan.disconnect()

ntptime.host = "tempus1.gum.gov.pl"


def connect(wifi):
    ssid = wifi[0]
    passwd = wifi[1]
    #Connect to WLAN
    wlan.connect(ssid, passwd)
    print("Connecting to", ssid)
    sleep(10)
    if wlan.isconnected() == True:    
        print('Connected to:',wlan.ifconfig())
        pico_led.on()
    else:
        print("Connection timed out")
        wlan.disconnect()
        pico_led.off()
    
    
def connect_aval_wlan(list_of_wifi,wlan):
    # znajdowanie dostępnych wifi z listy
    wifi_scan = wlan.scan()
    access_list = []
    for network in wifi_scan:
        for wifi in list_of_wifi:
            if str(network[0].decode("utf-8")) == wifi[0]:
                access_list.append(wifi)
    # łączenie ze znalezionymi sieciami              
    print('Nawiązywanie połączenia')
    if len(access_list) > 0:
        for n in range (0, len(access_list)):
            connect(access_list[n])
            if wlan.isconnected() == True:
                break
    else:
        print('No wifi avaliable')
        sleep(4)             


def get_and_display():
    board = []
    try:
        # Plac Galczynskiego (9)   
        #res = requests.get(url='https://www.zditm.szczecin.pl/json/tablica.inc.php?lng=pl&slupek=12111&t=0.8450320169628875', timeout=15)
        # Bogumily (9,1)
        page = requests.get(url='https://www.zditm.szczecin.pl/json/tablica.inc.php?lng=pl&slupek=30812&t=0.8865995302992444', timeout=15).json()
        # wyswietlanie komunikatu przystanku
    except:
        print("HTTP response error")
    else:    
        text = page["tresc"]
        komunikat = page["komunikat"]
        print(komunikat)
        # zamiana znakow HTML i polskich 
        text = txtReplace(text)
        
        match = True
        while match:
            m = re.search(r'">(.+?)<\\*', text)
            if m:
                match = True
                found = m.group(1)
                ind = m.span()[1]
                text = text[ind:]
                board.append(found)
            else:
                match = False
                #print(dir(m.group(1)))
        print(board)        
        print("------------------------")


def last_update_t():
    last_update = localtime()
    print(f'Last update:{last_update[3]}:{last_update[4]}:{last_update[5]}')

    
# generowanie przerwań cyklicznych do synchrnizacji czasu z serwerem ntp
timer = Timer(period=18000000, mode=Timer.PERIODIC, callback=lambda t: ntptime.settime)

# wczytywanie listy wifi jako tupli
with open('config.txt', 'r') as f:
    wifi_list = [tuple(i.strip('\n\r').split(',')) for i in f]

while True:
    while wlan.isconnected() == False:
        connect_aval_wlan(wifi_list,wlan)   
        sleep(2)
         
    sleep(3)
    get_and_display()
    last_update_t() 
