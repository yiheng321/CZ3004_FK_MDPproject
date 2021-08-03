import socket
import time


def sent(msg):
    import select
    import errno
    import sys
    HEADER_LENGTH = 10

    # IP = "127.0.0.1"
    IP='192.168.7.176'
    # IP='192.168.7.159'
    PORT = 10016

    # PORT = 1234
    # my_username = input("Username: ")

    # Create a socket
    # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
    # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to a given ip and port
    #client_socket.connect((IP, PORT))

    # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
    client_socket.setblocking(False)


    message=msg
    client_socket.send(message.encode('utf-8'))
    # while True:

        # Wait for user to input a message
        # message = input(f'{my_username} > ')
        # If message is not empty - send it
        # if message:
        #     time.sleep(1)
        #     # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        #     # message = message.encode('utf-8')
        #     # message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        #     for i in ['A', 'B', 'W', 'Q']:
        #         time.sleep(1)
        #         client_socket.send(i.encode('utf-8'))
            # client_socket.send(message.encode('utf-8'))
sent('GG')
        # try:
        #     # Now we want to loop over received messages (there might be more than one) and print them
        #     while True:
        #         time.sleep(1)
        #         # Receive our "header" containing username length, it's size is defined and constant
        #         username_header = client_socket.recv(HEADER_LENGTH)
        #
        #         # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        #         if not len(username_header):
        #             print('Connection closed by the server')
        #             sys.exit()
        #
        #         # Convert header to int value
        #         username_length = int(username_header.decode('utf-8').strip())
        #
        #         # Receive and decode username
        #         username = client_socket.recv(username_length).decode('utf-8')
        #
        #         # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
        #         message_header = client_socket.recv(HEADER_LENGTH)
        #         message_length = int(message_header.decode('utf-8').strip())
        #         message = client_socket.recv(message_length).decode('utf-8')
        #
        #         # Print message
        #         print(f'{username} > {message}')
        #
        # except IOError as e:
        #
        #     if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
        #         print('Reading error: {}'.format(str(e)))
        #         sys.exit()
        #
        #     # We just did not receive anything
        #     continue
        #
        # except Exception as e:
        #     # Any other exception - something happened, exit
        #     print('Reading error: '.format(str(e)))
        #     sys.exit()















# import socket
# import time
#
# PORT = 36126
# IP='192.168.7.159'
# HEADERSIZE = 10
#
# # recever
# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# s.connect((IP,PORT))
#
# while True:
#     full_msg = ''
#     new_msg = True
#     while True:
#         msg = s.recv(16)
#         if new_msg:
#             print("new msg len:",msg[:HEADERSIZE])
#             msglen = int(msg[:HEADERSIZE])
#             new_msg = False
#
#         print(f"full message length: {msglen}")
#
#         full_msg += msg.decode("utf-8")
#
#         print(len(full_msg))
#
#
#         if len(full_msg)-HEADERSIZE == msglen:
#             print("full msg recvd")
#             print(full_msg[HEADERSIZE:])
#             new_msg = True