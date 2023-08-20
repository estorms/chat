import socket
import select
import errno
import sys

HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 1234
my_username = input('Username: ')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#look at this vs bind
client_socket.connect((IP, PORT))

#look at this
client_socket.setblocking(False)

username = my_username.encode('utf-8')
print(username)


client_socket.send(username)

while True:
    message = input(f'username{my_username} > ')
    if message:
        message = message.encode('utf-8')
        message_header = f'{len(message) :< {HEADER_LENGTH}}'.encode('utf-8')
        client_socket.send(message_header + message)

    try:
        while True:
            #receive things
            username_header = client_socket.recv(HEADER_LENGTH)
            print(f'received a username header: {username_header}')
            if not len(username_header):
                print('connection closed by the server')
                sys.exit()
            
            username_length = int(username_length.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')
            message_header = client_socket.recv(4096)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8').strip()
            print(f'{username}: + {message}')

    except IOError as e:
        #errors you would get when no more messages are available to be receiveds
        if e.errno != errno.EAGAIN or e.errno != errno.EWOULDBLOCK:
            print(f'Error reading messages: {str(e)}')
        continue
    except Exception as e:
        print(str(e)) 
        sys.exit()       