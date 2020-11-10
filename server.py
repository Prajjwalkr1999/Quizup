#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time


sports = ["Ques 1 :Who is the captain of Indian cricket team?","A. Virat kohli","B. M.S. Dhoni","C. Suresh raina","D. Yuzvendra chahal","Ques 2 : Who is the captain of Football club Barcelona?","A. Lionel Messi","B. Cristiano Ronaldo","C. Marc-André ter Stegen","D. Jordi alba","Ques 3 : Who is the goalkeeper of Footbal club Barcelona?","A. Marc-André ter Stegen","B. Arnau Tenas Ureña","C. Neto","D. Iñaki Peña Sotorres","Ques 4 : Who is the wicket keeper of Indian cricket team ? ","A. Virat kohli","B. M.S. Dhoni","C. Suresh raina","D. Yuzvendra chahal","Ques 5 : Who won the IPL 2020?","A. Delhi Capitals","B. Mumbai Indians","C. Chennai Super kings","D. Royal challengers bangalore"]
# questions =["Who is the father of Ross' child ?","Sample Question 2","Sample question 3","Sample Question 4","Sample Question 5","Sample question 6","Sample Question 7","Sample Question 8","Sample Question 9","Sample Question 10"]
questions = []

answers=['Ross','2','3','4','5','6','7','8','9','10']

completion=0
category=-1
no_of_clients=0

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
    global category
    global no_of_clients
    no_of_clients+=1

    if no_of_clients>2 :
        wait()
        sorry="**************Sorry! Two players are already playing QUIZUP******************"
        client.send(bytes(sorry, "utf8"))
        no_of_clients-=1
        wait()
        client.close()
        return
    
    if no_of_clients < 2:
        hold_on="Waiting for the other player to join...."
        client.send(bytes(hold_on, "utf8"))

    while True :
        if no_of_clients>1 :
            break
    
    wait()

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    # msg = "%s has joined the chat!" % name
    # broadcast(bytes(msg, "utf8"))
    final_scores[client] = 0
    clients[client] = name
    i=0

    wait()
    
    if category == -1 :
        msg = 'Please choose a category out of the following: '
        client.send(bytes(msg, "utf8"))
        wait()
        msg = 'A. TV Quiz        B. Sports        C. Object Oriented Programming'
        client.send(bytes(msg, "utf8"))
        wait()
        msg = client.recv(BUFSIZ)
        ans = msg.decode("utf8") + ""
        if ans == 'A' or ans == 'a' :
            category = 0
        elif ans == 'B' or ans == 'b' :
            category = 1
        else :
            category = 2

    else :
        wait()
        if category == 0 :
            cat = 'TV Quiz'
        elif category == 1 :
            cat = 'Sports'
        else :
            cat = 'Object Oriented Programming'
        msg = 'Your opponent chose the category: ' + cat
        client.send(bytes(msg, "utf8"))



    questions = sports

    j=0
    wait()

    while j<5 :
        ques=questions[(5*i) + j]
        client.send(bytes(ques, "utf8"))
        wait()
        j+=1

    i+=1
    

    while True:
        msg = client.recv(BUFSIZ)
        ans = msg.decode("utf8") + ""
        if ans==answers[i-1] :
            final_scores[client]+=10
        if msg != bytes("{quit}", "utf8"):
            # broadcast(msg, name+": ")
            
            client.send(bytes(name+":","utf8")+msg)
            wait()
            

            j=0
            client.send(bytes("************************************************************************", "utf8"))
            wait()
            while j<5 :
                ques=questions[(5*i) + j]
                client.send(bytes(ques, "utf8"))
                wait()
                j+=1

            
            i+=1
            if i==5 :
                wait()
                client.send(bytes(name+":","utf8")+msg)
                completed(client)
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                broadcast(bytes("%s has left the game." % name, "utf8"))
                no_of_clients-=1
                break
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            no_of_clients-=1
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