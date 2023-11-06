
import socket
import threading
import os
import time
import select
import ssl

def receive_data(ssl_socket):
    try:
        data = ssl_socket.recv(1024).decode()
        while data != 'close':
            if not data:
                break
            print(f"Received from server: {data}")
            data = ssl_socket.recv(1024).decode()
    except ConnectionRefusedError:
        print("Connection with server has been reset")
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
                        print("New Data:", new_data)
                        ssl_socket.send(new_data.encode('utf-8'))

                # Update the current file size
                    current_size = new_size

            # Sleep for a short interval before checking again
                time.sleep(1)  # You can adjust the interval as needed
        except ConnectionResetError:
            print("Connection with server has been reset")


if __name__ == '__main__':
    server_ip = "10.217.61.237"
    port = 5000  # socket server port number
    # Create an SSL context
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
   # ssl_context.load_verify_locations('client-cert.pem')
    ssl_context.verify_mode = ssl.CERT_NONE  # You can set this to ssl.CERT_OPTIONAL or ssl.CERT_REQUIRED for certificate verification

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    ssl_socket = ssl_context.wrap_socket(client_socket, server_hostname=server_ip)
    ssl_socket.connect((server_ip, port))  # connect to the server

    # Define the path to the text file you want to monitor
    file_path = "RFID_data.txt"
# Create two separate threads for sending and receiving data
    receive_thread = threading.Thread(target=receive_data, args=(ssl_socket,))
    send_thread = threading.Thread(target=send_data, args=(ssl_socket,file_path))

# Start both threads
    receive_thread.start()
    send_thread.start()

# Wait for both threads to finish
    receive_thread.join()
    send_thread.join()

    ssl_socket.close()
