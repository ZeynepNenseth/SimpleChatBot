import socket
import sys
import random
import threading
from time import sleep
from bots import all_actionList, extra_actionList

# additional array so that action2 is sometimes empty (none)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = 'localhost'

# handles port number as command line parameter
try:
    server_address = (ip, int(sys.argv[1]))
except IndexError:
    print("Please try again with python .\server.py 26246")
    exit(1)

# assigns an IP address and port number to the socket instance
server_socket.bind(server_address)
print("Starting the server ", server_address)

# socket listens for connections
server_socket.listen()
print("Waiting for connections...")

# lists that will contain information about connected clients and their usernames
clientList = []
usernameList = []

# additional array so that action2 is sometimes empty (none)
additional = random.choice([True, False])
action1 = random.choice(all_actionList)
action2 = None
if additional is False:
    action2 = random.choice(extra_actionList)


# help function that takes in a message and sends it to all clients
def broadcast(message, sender):
    if type(message) == str:
        message = message.encode()

    for client in clientList:
        if client is not sender:
            client.send(message)
    sleep(0.2)


# help function that starts the chat initiated by the host and has the bot with user-input
def chat():
    # creates a suggestion with one or two keywords
    if action2 is not None:
        message = "Host: Hi everyone! It's a beautiful day. Would you like to join me for " + action1 + "ing or " \
                  + action2 + "ing today?"
    else:
        message = "Host: Hi everyone! It's a beautiful day. Would you like to join me for " + action1 + "ing today?"
    print(message)

    # sends the suggestion to all clients and receives bot-quotes from as response and broadcast these to clients
    for client in clientList:
        client.send(message.encode())
    for client in clientList:
        message = client.recv(1024)
        sleep(2)
        broadcast(message, server_socket)

    # sends a question for the server-bot and expects a response (user-input) which are broadcasted to all clients
    message = "Host: Hey, server guy! You haven't said anything. What do you suggest?\n"
    broadcast(message, server_socket)
    inp = "Random server lady: " + input(message)
    broadcast(inp, server_socket)
    sleep(2)


# help function that sends a "good bye" message to clients, clears lists, closes server socket, ends program
def endconnections():
    broadcast("The chat room is closing! Have a nice day...", server_socket)
    usernameList.clear()
    clientList.clear()
    server_socket.close()
    sleep(2)
    quit()


# main function that accept connections, handles user/client lists and starts chat when it's time
def connect():
    # accepts connections while the number of connected bots is less than 5
    while len(clientList) < 4:
        while True:
            client_socket, client_address = server_socket.accept()
            print("Client connected:", {str(client_address)})
            username = client_socket.recv(1024).decode()

            # for each connection, it checks the username. If correct, sends a "welcome" message to the client
            # adds the connection to the lists
            if username not in usernameList:
                print("Server has received the username", username, "from the client")
                client_socket.send("Welcome to the chat room".encode())
                print(username, "with the connection ", client_socket, "is added to the client list.")
                usernameList.append(username)
                clientList.append(client_socket)
                print(usernameList)
                break

            # if username not correct, asks client for a new (correct) one
            else:
                client_socket.send("This username is already taken! Bye... ".encode())
                print("Server has received the username", username, "that is already in use. Client connection will be closed.")
                client_socket.close()

        # when the number of connected bots is 5, starts the chat, closes the chat
        if len(clientList) == 4:
            print("Opening the chat room")
            broadcast("Chat room is ready to start!", server_socket)
            sleep(0.3)

            try:
                thread = threading.Thread(target=chat)
                thread.start()
                thread.join()

                # after chat() function (all clients have said their lines and user has answered),
                # host sends a message about decided action
                # ends connections via the help function endconnections()

                message = ("Host: Thank you for joining the chat today! I think it is best to stick to " + action1 + "ing."
                           "\nHost: See you later today then, bye for now!")
                broadcast(message, server_socket)
                print(message)
                sleep(0.5)
                print("------That's for today!------")
                endconnections()
            except Exception as e:
                print(e)


connect()
