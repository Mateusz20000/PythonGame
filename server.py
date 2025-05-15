import socket
from _thread import *
import sys

server = "192.168.0.157"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    str(e)



s.listen(5)
print("Server Started, Waiting for a connection...")

def threaded_client(conn):

    conn.send(str.encode("Connected"))
    
    replay = ""
    while True:
        
        try:
            data = conn.recv(2048)
            replay = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break

            else:
                print("Recived: ", replay)
                print("Sending: ", replay)
            
            conn.sendall(str.encode(replay))

        except:
            break

    print("Lost connection")
    conn.close()


    


        



while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))