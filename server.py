#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

questions =[]
answers=[]

sports = ["Ques 1 :Who is the captain of Indian cricket team?","A. Virat kohli","B. M.S. Dhoni","C. Suresh raina","D. Yuzvendra chahal","Ques 2 : Who is the captain of Football club Barcelona?","A. Lionel Messi","B. Cristiano Ronaldo","C. Marc-André ter Stegen","D. Jordi alba","Ques 3 : Who is the goalkeeper of Footbal club Barcelona?","A. Marc-André ter Stegen","B. Arnau Tenas Ureña","C. Neto","D. Iñaki Peña Sotorres","Ques 4 : Who is the wicket keeper of Indian cricket team ? ","A. Virat kohli","B. M.S. Dhoni","C. Suresh raina","D. Yuzvendra chahal","Ques 5 : Who won the IPL 2020?","A. Delhi Capitals","B. Mumbai Indians","C. Chennai Super kings","D. Royal challengers bangalore"]
ans1=['A','A','A','B','B']
tv = ["Ques 1 :What does Joey never share?","A. His books","B. His information","C. His food","D. His DVDs","Ques 2 : How many claps are there in F.R.I.E.N.D.S.’ theme song? ","A. 3","B. 4","C. 5","D. 6","Ques 3 : What’s the name of Joey’s penguin?","A. Snowflake","B. Waddle","C. Huggsy","D. Bobber","Ques 4 : How many times has ross been divorced ? ","A. 0","B. 1","C. 2","D. 3","Ques 5 : What song is Phoebe best known for?","A. Smelly Cat","B. Smelly Dog","C. Smelly Pig","D. Smelly Chandler"]
ans2=['C','B','C','D','A']
oops = ["Ques 1 : Which of the following concepts means determining at runtime what method to invoke?","A. Data hiding","B. Dynamic binding","C. Dynamic typing","D. Dynamic loading","Ques 2 : Which of the following is not the member of class?","A. Static function","B. Friend function","C. Const function","D. Virtual function","Ques 3 : Which of the following is not a type of constructor?","A. Copy constructor","B. Default constructor","C. Friend constructor","D. Parameterized constructor","Ques 4 : Which of the following type of class allows only one object of it to be created?","A. Virtual class","B. Abstract class","C. Singleton class","D. Friend class","Ques 5 : Which of the following are not visible in the class inheritance?","A. Public data members","B. Private data members","C. Protected data members","D. Member functions"]
ans3=['B','B','C','B','B']

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
            questions = tv
            answers = ans2
        elif ans == 'B' or ans == 'b' :
            category = 1
            questions = sports
            answers = ans1
        else :
            category = 2
            questions = oops
            answers = ans3

    else :
        wait()
        if category == 0 :
            cat = 'TV Quiz'
            questions = tv
            answers = ans2
        elif category == 1 :
            cat = 'Sports'
            questions = sports
            answers = ans1
        else :
            cat = 'Object Oriented Programming'
            questions = oops
            answers = ans3
        msg = 'Your opponent chose the category: ' + cat
        client.send(bytes(msg, "utf8"))



    j=0
    wait()
    client.send(bytes("************************************************************************", "utf8"))
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
                msg = client.recv(BUFSIZ)
                wait()
                client.send(bytes(name+" : ","utf8")+msg)
                wait()
                client.send(bytes("************************************************************************", "utf8"))
                completed(client)
                # client.send(bytes("{quit}", "utf8"))
                # client.close()
                # del clients[client]
                # broadcast(bytes("%s has left the game." % name, "utf8"))
                # no_of_clients-=1
                # break
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            no_of_clients-=1
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
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