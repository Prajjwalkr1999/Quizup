#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

questions =["Sample Question 1","Sample Question 2","Sample question 3","Sample Question 4","Sample Question 5","Sample question 6","Sample Question 7","Sample Question 8","Sample Question 9","Sample Question 10"]
answers=['1','2','3','4','5','6','7','8','9','10']


completion=0

def completed(client) :
    global completion
    completion+=1
    name = clients[client]
    score = final_scores[client]
    wait()
    while True :
        if completion==2 :
            break
    score1 = -1
    score2 = -1
    for ele in final_scores :
        if score1==-1 :
            score1 = final_scores[ele]
        else :
            score2 = final_scores[ele]
    name1 = 'temp'
    name2 = 'temp'
    for ele in clients :
        if name1=='temp' :
            name1 = clients[ele]
        else :
            name2 = clients[ele]

    wait()
    client.send(bytes(' ', "utf8"))    
    wait()

    broadcast(bytes(name + "'s Final score: " + str(score), "utf8"))
    wait()
    client.send(bytes(' ', "utf8"))  
    wait()
    if score1 == score2 :
        client.send(bytes("It's a draw!", "utf8"))
    elif score1 > score2 :
        client.send(bytes(name1 + " wins!", "utf8"))
    else :
        client.send(bytes(name2 + " wins!", "utf8"))



def wait() :
    currtime = time.perf_counter()
    newtime = currtime
    while newtime - currtime < 0.5 :
        newtime=time.perf_counter()



def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Welcome to Quizup! Please enter your name.", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    global score
    global completion
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    # msg = "%s has joined the chat!" % name
    # broadcast(bytes(msg, "utf8"))
    final_scores[client] = 0
    clients[client] = name
    i=0
    quesFirst=questions[i]
    i+=1
    wait()
    client.send(bytes(quesFirst,"utf8"))

    while True:
        msg = client.recv(BUFSIZ)
        ans = msg.decode("utf8") + ""
        if ans==answers[i-1] :
            final_scores[client]+=10
        if msg != bytes("{quit}", "utf8"):
            # broadcast(msg, name+": ")
            ques=questions[i]
            client.send(bytes(name+":","utf8")+msg)
            wait()
            
            # client.send(bytes(ques, "utf8"))
            client.send(bytes(ques, "utf8"))
            i+=1
            if i==5 :
                wait()
                client.send(bytes(name+":","utf8")+msg)
                completed(client)
                break
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

final_scores = {}        
clients = {}
addresses = {}

HOST = ''
PORT = 33001
BUFSIZ = 2048
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