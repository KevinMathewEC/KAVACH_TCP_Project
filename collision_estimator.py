import socket
import ssl
import threading
import json
import time
import subprocess

LIVE_TRAINS = {}
TRACK_DATA = {}

def rx_train_data(ssl_bond, train_ip):
    rxed_data = ssl_bond.recv(1024)
    print('Received:', rxed_data.decode())
    end_time = time.time()
    train_data = json.loads(rxed_data.decode())
    start_time = train_data["start_time"]
    print(f'Latency from train to server {end_time - start_time}')

    track_id = train_data["RFID"][:4]
    rfid_position = int(train_data["RFID"][4:8])
    train_id = train_data["Train_ID"]

    ssl_bond.close()

    if train_id not in LIVE_TRAINS:
        LIVE_TRAINS[train_id] = {'IP':train_ip,'RFID_position':rfid_position,'Direction':None}
    else:
        direction = None
        if LIVE_TRAINS[train_id]['RFID_position'] != rfid_position:
            direction = (LIVE_TRAINS[train_id]['RFID_position'] < rfid_position)
        LIVE_TRAINS[train_id]['Direction'] = direction 
        LIVE_TRAINS[train_id]['RFID_position'] = rfid_position
        LIVE_TRAINS[train_id]['IP'] = train_ip

    if track_id not in TRACK_DATA:
        TRACK_DATA[track_id] = {train_id}
    else:
        id_of_trains_in_track = TRACK_DATA[track_id]
        for id in id_of_trains_in_track:
            if id != train_id:
                other_train_details = LIVE_TRAINS[id]
                distance_between_trains = abs(other_train_details['RFID_position'] - rfid_position)
                in_opposite_direction = (other_train_details['Direction'] != LIVE_TRAINS[train_id]['Direction']) or \
                                        (other_train_details['Direction'] is None) or (LIVE_TRAINS[train_id]['Direction'] is None)
                if (distance_between_trains <= 5 and in_opposite_direction):
                    inform_trains(LIVE_TRAINS[train_id]['IP'], f"{end_time}|STOP Train. Train {id} is only {distance_between_trains} km away.")
                    inform_trains(other_train_details['IP'], f"{end_time}|STOP Train. Train {train_id} is only {distance_between_trains} km away.")

                    for warn_id in id_of_trains_in_track:
                        if warn_id not in [id, train_id]:
                            distance_from_train_1 = abs(other_train_details['RFID_position'] - LIVE_TRAINS[warn_id]['RFID_position'])
                            distance_from_train_2 = abs(rfid_position - LIVE_TRAINS[warn_id]['RFID_position'])
                            warn_message = f"""Warning: Trains {id} and {train_id} in your track 
                                              are {distance_between_trains} apart and is warned to stop.
                                              You are {distance_from_train_1} km away from Train {id} and
                                              {distance_from_train_2} km away from Train {train_id}."""
                            if (other_train_details['Direction'] != LIVE_TRAINS[warn_id]['Direction']):
                                warn_message = warn_message + f'You are in opposite direction of Train {id}'
                            else:
                                warn_message = warn_message + f'You are in opposite direction of Train {train_id}'
                            inform_trains(LIVE_TRAINS[warn_id]['IP'], warn_message)
        TRACK_DATA[track_id].add(train_id)

def listen_to_trains(address):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile='server.crt', keyfile='server.key')

        with context.wrap_socket(sock, server_side=True) as ssock:
            ssock.bind(address)
            ssock.listen(1)
            print('Listening at', address)

            while True:
                try:
                    ssl_bond, train_send_socket = ssock.accept()
                    train_ip = train_send_socket[0]
                    print('Connected by', train_ip)
                    threading.Thread(target=rx_train_data, args=(ssl_bond, train_ip)).start()
                except ssl.SSLError:
                    print("Unauthorized connection attempt was rejected. ")

def inform_trains(train_ip, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        not_connected = True
        while not_connected:
            try:
                sock.connect((train_ip, 64112))
                not_connected = False
            except:
                time.sleep(3)
                print("Could not connect to train. Trying Again.")
        sock.sendall(message.encode('utf-8'))
        print(f'Informed {train_ip} to stop')
        sock.close()

if __name__ == "__main__":
    listen_to_trains(('HandsomePi', 65432))
