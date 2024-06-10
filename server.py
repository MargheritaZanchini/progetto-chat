#!/usr/bin/env python3

import socket
import threading

#funzione che gestisce i client che vogliono connettersi al server
def accetta_connessioni():
    while True:
        try:
            client_socket, client_address = SERVER_SOCKET.accept()  #l'esecuzione del programma si 
                                                #blocca fino a quando non arriva una richiesta di connessione da un client
            print(client_address, "si è collegato")
            entry_message = 'Ciao ' + HOST + ' benvenuto sul server. Inserisci il tuo nome'
            client_socket.send(entry_message.encode('utf-8'))
            indirizzi[client_socket] = client_address #aggiungiamo al dizionario l'indirizzo del nuovo client
            #attiviamo il thread per quel client
            threading.Thread(target=gestione_client, args=(client_socket,)).start()
        except Exception as e:
            print("Si è verificato un errore nell'accettare una connessione. Errore: "+e)
            break

def gestione_client(client_socket):
    try:
        nome = client_socket.recv(SIZE_BUFFER).decode('utf-8') #riceviamo il nome scelto dal client
        clients[client_socket] = nome #aggiorniamo il dizionario con il nuovo nome
        messaggio = nome + ' si è unito!' 
        broadcast(messaggio, '') #mandiamo a tutti il messaggio che un client si è unito
    except Exception as e:
        print("Si è verificato un errore nella gestione iniziale del client. Errore: "+e)

    while True:
        try:
            messaggio = client_socket.recv(SIZE_BUFFER).decode('utf-8')
            if messaggio != '{quit}':
                broadcast(messaggio, nome+': ')
            else:
                del clients[client_socket]
                exit_message = nome + ' ha abbandonato'
                broadcast(exit_message, '')
                break
        except Exception as e:
            print("Si è verificato un errore nel riceve/inviare messaggi dai/ai client. Errore: "+e)
        

def broadcast(messaggio, nome):
    for client in clients:
        try:
            new_msg = nome + '' + messaggio
            client.send(new_msg.encode('utf-8'))
        except Exception as e:
            print("errore nell'inviare un messaggio in broadcast. Errore: "+e)

#dizionari per la registrazione dei client e dei relativi indirizzi
clients = {}
indirizzi = {}

HOST = ''
PORT = 60000 #definiamo la porta
SIZE_BUFFER = 1024 #definiamo la dimensione del buffer
ADDR = (HOST, PORT)

#uso dei socket TCP
SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER_SOCKET.bind(ADDR) #in questo modo leghiamo il socket all'indirizzo e alla porta specificati

if __name__ == "__main__":
    SERVER_SOCKET.listen(5)
    print("In attesa di connessioni...")
    ACCEPT_THREAD = threading.Thread(target=accetta_connessioni)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER_SOCKET.close()