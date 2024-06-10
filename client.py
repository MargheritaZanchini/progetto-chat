#!/usr/bin/env python3

import socket
import threading
import tkinter

def receive():
    while True:
        try:
            data = CLIENT_SOCKET.recv(SIZE_BUFFER)
            messaggio = data.decode('utf-8')
            msg_list.insert(tkinter.END, messaggio)
        except OSError:
            break

def send(event=None):
    messaggio = input.get() #prendo dal campo di input sulla GUI il messaggio
    input.set('')  #svuoto il campo di input sulla GUI
    CLIENT_SOCKET.send(messaggio.encode('utf-8'))
    if messaggio == '{quit}':
        exit()

def exit(event=None):
    exit_message = '{quit}'
    CLIENT_SOCKET.send(exit_message.encode('utf-8'))
    CLIENT_SOCKET.close()
    finestra.quit()

def on_closing(event=None):
    exit()

finestra = tkinter.Tk()
frame_messaggi = tkinter.Frame(finestra)
input = tkinter.StringVar() #qui verranno messi i messaggi da inviare
scrollbar = tkinter.Scrollbar(frame_messaggi) #per vedere anche i messaggi precedenti

msg_list = tkinter.Listbox(frame_messaggi, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
frame_messaggi.pack()

input_field = tkinter.Entry(finestra, textvariable=input)
input_field.bind("<Return>", send)

input_field.pack()
send_button = tkinter.Button(finestra, text="Invio", command=send)
send_button.pack()

exit_button = tkinter.Button(finestra, text="Esci", command=exit)
exit_button.pack()

finestra.protocol('VM_DELETE_WINDOW', on_closing)

#diciamo a quale indirizzo e porta vogliamo connetterci
HOST = '127.0.0.1'
PORT = 60000
SIZE_BUFFER = 1024
ADDR = (HOST, PORT)

CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT_SOCKET.connect(ADDR) #mi connetto al server

receive_thread = threading.Thread(target=receive)
receive_thread.start()

tkinter.mainloop()