import socket
import select

# establish core functionality -- server should receive a message from a client socket
def receive_message(client_socket):
    print('about to receive')
    #set up the message to receive a power of 2 that comfortably accommodates the average message size 
    message = client_socket.recv(4096)
    #if for some reason there isn't a message or the message is an empty object, fail outs
    if not (message or len(message)):
        print('Client closed connection or sent malformed message')
    #decode and return the message
    message_decoded = message.decode('utf-8').strip()
    print(f'Received message: {message_decoded}')
    return {'message': message_decoded}

#create the socket and bind it to a port -- TCP protocol 
IP = '127.0.0.1'
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen()
sockets_list = [server_socket]

#establish an open communication channel using selectors, which provide OS-specific I/O management by determining when sockets are ready for input/output operations. I chose to use selectors only in this implementation because they appear to be easier to debug (i.e., more deterministic) and this is a learning exercise
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets:
        print('we have a notfied socket')
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            sockets_list.append(client_socket)
            client_message = receive_message(client_socket)
            print(f'client message: {client_message}')



