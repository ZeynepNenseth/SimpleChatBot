import socket
import sys
from bots import alice, bob, musti, hellokitty

userList = ["alice", "bob", "musti", "hellokitty"]

# creates a TCP socket for IPv4
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# handles IP and port as command line parameters
try:
    client_address = (sys.argv[1], int(sys.argv[2]))
except Exception as e:
    print("Try again with python .\client.py localhost 26246")
    exit(1)

# connects to a server that is listening for connections
try:
    client_socket.connect(client_address)
except Exception as e:
    print("Please start the server first!")
    client_socket.close()
    quit()

# server asks client to choose an available username to be able to get accepted to the chat room
username = input("Choose your username: alice, bob, musti, hellokitty\n")
while username.lower() not in userList:
    username = input("This username does not exist! Please write a valid username:\n")

# client sends correct username and receives a "welcome to the chat room" message
client_socket.send(username.lower().encode())
data = client_socket.recv(1024).decode()
print(data, username.lower(), "!")


# help function: recognizes and extracts the keyword (action) that the bots are going to use in their line of text
# connects the username of the client with the corresponding chatbot
def bot(data):
    if data.startswith("Host: Hi everyone!"):
        words = data.split()
        activity = words[14].rstrip("ing")
        try:
            activity2 = words[16].rstrip("ing")
        except:
            activity2 = None

        if username == userList[0]:
            client_socket.send(alice(activity, activity2).encode())
        elif username == userList[1]:
            client_socket.send(bob(activity, activity2).encode())
        elif username == userList[2]:
            client_socket.send(musti(activity, activity2).encode())
        elif username == userList[3]:
            client_socket.send(hellokitty(activity, activity2).encode())


# main function that keeps the client connection open
# continuously listens for messages from the server and does three different things depending on the message:
# 1: calls the bot() function that extracts the keyword and keeps the chat going
# 2: closes the connection after the appropriate message from the host
def wait():  # keeps the client connection open
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if message == "The chat room is closing! Have a nice day...":
                print(message)
                client_socket.close()
                quit()
            if message == "":
                client_socket.close()
                quit()
            print(message)
            bot(message)
    except:
        exit()


wait()

