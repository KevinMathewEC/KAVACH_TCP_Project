Instructions for execution

1. "collision_estimator.py" is the python code for server.

2. "data_push_and_alert.py" is the python code for trains.

3. For ssl authentication server.crt file should be present at location of the python code in trains.

4. Server requires server.crt and server.key files at location of python code.

5. The server.crt and server.key were generated using openssl tool with the command "openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.crt", where Common Name must be given as hostname of server.

6. At trains RFID_DATA.txt is where RFID tag details are read by the python code. At both trains this file should be present at location of python code.

7. RFID_data.txt will be having "Tag_ID" which is in HEX format. When converted into decimal, only the last 8 digits are used for computation. Of these 8 digits, the first 4 digits indicate Track ID and the next 4 digits indicate RFID position. The last 4 digits can be modified to simulate different distances.

8. The hostname of server used is "HandsomePi". At trains the ip of server and hostname should be added in "/etc/hosts".
