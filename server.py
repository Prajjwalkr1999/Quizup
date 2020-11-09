#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

questions =["Sample Question 1","Sample Question 2","Sample question 3","Sample Question 4","Sample Question 5","Sample question 6","Sample Question 7","Sample Question 8","Sample Question 9","Sample Question 10"]
answers=['1','2','3','4','5','6','7','8','9','10']

# i=0

score=0

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    global score
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.\n' % name
    client.send(bytes(welcome, "utf8"))
    # msg = "%s has joined the chat!" % name
    # broadcast(bytes(msg, "utf8"))
    clients[client] = name
    i=0
    quesFirst=questions[i]
    i+=1
    client.send(bytes(quesFirst+"\n","utf8"))
    while True:
        msg = client.recv(BUFSIZ)
        ans = msg.decode("utf8") + ""
        if ans==answers[i-1] :
            score+=10
        if msg != bytes("{quit}", "utf8"):
            # broadcast(msg, name+": ")
            ques=questions[i]
            client.send(bytes(name+":","utf8")+msg)
            # Add 10 sec counter here before sending question
            # client.send(bytes(ques, "utf8"))
            client.send(bytes("\n"+ques+"\n", "utf8"))
            i+=1
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

        
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
