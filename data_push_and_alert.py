import socket
import threading
import os
import time
import ssl
import json
 
DATA_TO_SEND = {"Train_ID":"32998"}
IS_NEW_DATA = False
 
def send_data():
    global IS_NEW_DATA
    server_host_name = "HandsomePi"
    server_port = 65432
    file_path = "RFID_data.txt"
    current_size = 0
    while True:
        start_time=time.time()
        new_size = os.path.getsize(file_path)

        if IS_NEW_DATA:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                context.load_verify_locations('server.crt')
 
                with context.wrap_socket(sock, server_hostname='HandsomePi') as ssock:
                    not_connected = True
              
                    while not_connected:
                        try:
                            ssock.connect((server_host_name, server_port))
                            not_connected = False
                        except:
                            time.sleep(3)
                            print("Could not connect to server. Trying Again.")
                    print('Connected to', server_host_name)
                    DATA_TO_SEND["start_time"]=start_time
                    ssock.sendall(json.dumps(DATA_TO_SEND).encode('utf-8'))
                    IS_NEW_DATA = False
 
def receive_data():
    local_host_name = "ubuntumat"
    local_port = 64112
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
 
        sock.bind((local_host_name, local_port))
        sock.listen(1)
        print('Listening at ', local_port)
 
        while True:
            source, source_ip = sock.accept()
            print('Connected by', source_ip)
            received_data = source.recv(1024)
            end_time=time.time()
            start_time1=(received_data.decode()).split('|')
            start_time2=start_time1[0]
            start_time3=float(start_time2)
            latency=end_time-start_time3
           
            print('Received:', start_time1[1])
            print('Latency from server to train:',latency)
 
def monitor_data():
    global IS_NEW_DATA
    file_path = "RFID_data.txt"
    current_size = 0
    while True:
        new_size = os.path.getsize(file_path)
        if new_size > current_size:
            size_diff = new_size - current_size
            with open(file_path, 'r') as file:
                file.seek(current_size)
                rfid_hex = json.loads(file.read(size_diff))['Tag_ID'][16:25]
                DATA_TO_SEND["RFID"] = str(int(rfid_hex, 16))
                IS_NEW_DATA = True
                print("Message: ", DATA_TO_SEND)
        current_size = new_size
        time.sleep(1)
 
if __name__ == '__main__':
    threading.Thread(target=monitor_data).start()
    threading.Thread(target=send_data).start()
    threading.Thread(target=receive_data).start()
