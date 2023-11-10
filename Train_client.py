# TCPIP Networking Lab4
# Description: TCP Client Program in Python


import socket
import threading
import os
import time
import select
import ssl
import json

def receive_data(server_socket):

    server_socket.listen(1)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
       # context.load_cert_chain(certfile='server.crt', keyfile='server.key')
    while True:

    # Accept a client connection
        client_socket, client_address = server_socket.accept()

    # Wrap the socket with SSL
        server_ssl_socket = context.wrap_socket(client_socket, server_side=True)

        try:

        # Receive data from the client
            data = ssl_socket.recv(1024)
            print(f"Received data from client: {data.decode('utf-8')}")

        finally:
                # Close the SSL socket
            ssl_socket.close()
   #     print("Waiting for server")
   #     data = ssl_socket.recv(1024).decode()
   #     print("Received data from server")
   #     while data != 'close':
   #         data = ssl_socket.recv(1024).decode()
   #         if not data:
   #             break
   #         print(f"Received from server: {data}")
   #         print("Server data received   ")
   #         #data = ssl_socket.recv(1024).decode()
   #         print("Server data decoded")
   # except ConnectionRefusedError:
   #     print("Connection with server has been reset")
def send_data(ssl_socket,file_path):
        try:
            # Initialize the current file size
            current_size = 0
            while True:
            # Get the current file size
                new_size = os.path.getsize(file_path)

            # Check if the file size has increased (new data has been written)
                if new_size > current_size:
                # Calculate the size of the new data
                    size_diff = new_size - current_size

                # Read and print the new data
                    with open(file_path, 'r') as file:
                        file.seek(current_size)  # Move the file pointer to the last read position
                        new_data = file.read(size_diff)
                       # json_data=json.dumps(new_data)
                        print("New Data:", new_data)
                        current_timestamp = int(time.time())  # UNIX timestamp
                        message = f"Timestamp: {current_timestamp}\nData: {new_data}"
                        print("Message: ",message)
                        ssl_socket.send(message.encode('utf-8'))

                # Update the current file size
                    current_size = new_size

            # Sleep for a short interval before checking again
                time.sleep(1)  # You can adjust the interval as needed
        except ConnectionResetError:
            print("Connection with server has been reset")


if __name__ == '__main__':
    server_ip = "10.217.61.237"#"HandsomePi"
    port = 65432  # socket server port number
    hostname = socket.gethostname()
    server_port = 5000

    # Get the local IP address
    local_server_ip = socket.gethostbyname(hostname)
    print("local_server_ip",local_server_ip)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the server's IP and port
    server_socket.bind((local_server_ip, server_port))

    # Create an SSL context
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
  #  ssl_context.check_hostname = False
    ssl_context.load_verify_locations('client.crt')
#    ssl_context.verify_mode = ssl.CERT_REQUIRED  # You can set this to ssl.CERT_OPTIONAL or ssl.CERT_REQUIRED for certificate verification
    print("client socket")
    train_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    ssl_socket = ssl_context.wrap_socket(train_client_socket, server_hostname=server_ip)
    ssl_socket.connect((server_ip, port))  # connect to the server

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Define the path to the text file you want to monitor
    file_path = "RFID_data.txt"
    print("file found")
# Create two separate threads for sending and receiving data
    receive_thread = threading.Thread(target=receive_data, args=(server_socket,))
    send_thread = threading.Thread(target=send_data, args=(ssl_socket,file_path))



# Start both threads
    receive_thread.start()
    send_thread.start()

# Wait for both threads to finish
    receive_thread.join()
    send_thread.join()

    ssl_socket.close()


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the server's IP and port
    server_socket.bind((local_server_ip, server_port))

    # Create an SSL context
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
  #  ssl_context.check_hostname = False
    ssl_context.load_verify_locations('client.crt')
#    ssl_context.verify_mode = ssl.CERT_REQUIRED  # You can set this to ssl.CERT_OPTIONAL or ssl.CERT_REQUIRED for certificate verification
    print("client socket")
    train_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    ssl_socket = ssl_context.wrap_socket(train_client_socket, server_hostname=server_ip)
    
    ssl_socket.connect((server_ip, port))  # connect to the server

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Define the path to the text file you want to monitor
    file_path = "RFID_data.txt"
    print("file found")
# Create two separate threads for sending and receiving data
    receive_thread = threading.Thread(target=receive_data, args=(server_socket,))
    send_thread = threading.Thread(target=send_data, args=(ssl_socket,file_path))



# Start both threads
    receive_thread.start()
    send_thread.start()

# Wait for both threads to finish
    receive_thread.join()
    send_thread.join()

    ssl_socket.close()
                                                                                                            
