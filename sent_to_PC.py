import socket
import time

def sent_toPC(msg):

    HEADER_LENGTH = 10

    # IP = "127.0.0.1"
    IP='192.168.7.159'

    PORT = 10009

    # Create a socket
    # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
    # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to a given ip and port
    client_socket.connect((IP, PORT))

    # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
    client_socket.setblocking(False)


    message=msg
    client_socket.send(message.encode('utf-8'))
    while True:

        # Wait for user to input a message
        # message = input(f'{my_username} > ')
        # If message is not empty - send it
        if message:
            time.sleep(1)

            for i in ['A', 'B', 'W', 'Q']:
                time.sleep(1)
                print (i)
                client_socket.send(i.encode('utf-8'))
            # client_socket.send(message.encode('utf-8'))

