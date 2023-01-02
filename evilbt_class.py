from ctypes import addressof
from unicodedata import name
from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3
from colorama import *
import time
import bluetooth

class Evil_database:
    
    def __init__(self, addr, name, info):
        self.evil_addr = addr
        self.evil_name = name
        self.evil_info = info

    def insert(addr,name,info):
        try:
            with sqlite3.connect("server/database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO victime (addr, name, info) VALUES (?,?,?)",(addr,name,info) )
            
                con.commit()
                print(Fore.CYAN+"[~]"+Fore.WHITE+" Record successfully added",addr,name,info)
        except:
            print(Fore.RED+"[!]"+Fore.WHITE+" Record successfully fail !")


class Evil_scan:

    def __init__(self, addr, name, info):
        self.name = name
        self.addr = addr
        self.info = info


    def scan():
        nearby_devices = bluetooth.discover_devices(lookup_names=True)

        count = 0
        lists_name = []
        lists_addr = []
        for addr, name in nearby_devices:
            count = count + 1
            lists_name.append(name) 
            lists_addr.append(addr)
    

        return lists_addr, lists_name


