# -*- coding: utf-8 -*-
import socket
import time
import select



comandos = ['!join ', '!quit', '!whisper ', '!listusers']
usuarios_conectados = {}
socketlist = []

def Start():
    host = 'localhost'
    porta = 1234

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((host,porta))
    serverSocket.listen()
    socketlist.append(serverSocket)
    usuarios_conectados[serverSocket] = '#server'
    print('Esperando clientes...')

    while True:
        read,write,error = select.select(socketlist,[],[],0)
        for socket_from in read:
            if socket_from == serverSocket:
                clientSocket, clientAddress = serverSocket.accept()
                print('Conexão de: ', clientAddress)
                print('Solicitando nickname para ', clientAddress)
                socketlist.append(clientSocket)
                clientSocket.send('!nick'.encode())
            else:
                msg = socket_from.recv(2048)
                msg = msg.decode()
                if msg.startswith('!join '):
                    Join(clientSocket, serverSocket, msg)
                elif msg.startswith('!sendwhisper '):
                    msgparts = msg.split(' ')
                    if(len(msgparts) == 3):
                        SendWhisper(socket_from, msgparts[1], msgparts[2])
                elif msg.startswith('!quit'):
                    Quit(serverSocket, socket_from)
                elif msg.startswith('!listusers'):
                    ListUsers(socket_from, serverSocket)
                else:
                    SendAll(socket_from, serverSocket, msg)
        time.sleep(0.1)


def Quit(serverSocket, socket_from):
    socket_from.close()
    mensagem = '%s saiu' % (usuarios_conectados[socket_from])
    socketlist.remove(socket_from)
    del usuarios_conectados[socket_from]
    SendAll(serverSocket, serverSocket, mensagem)


def Join(clientSocket, serverSocket, msg):
    nick = msg.split(' ')[1]
    usuarios_conectados[clientSocket] = nick
    mensagem = '%s entrou' % (nick)
    SendAll(serverSocket, serverSocket, mensagem)


def SendWhisper(socket_from, username, msg):
    socket_to = GetSocketFromUsername(username)
    if socket_to is not None:
        msg = '%s (privado): %s' % (usuarios_conectados[socket_from], msg)
        socket_from.send(msg.encode())
        socket_to.send(msg.encode())

def SendAll(socket_from, server_socket, msg):
    msg = '%s: %s' % (usuarios_conectados[socket_from], msg)
    print(msg)
    for s in socketlist:
        if s != server_socket and socket_from in socketlist:
            s.send(msg.encode())

def ListUsers(socket_from, server_socket):
    listnames = list(usuarios_conectados[s] for s in usuarios_conectados if s != server_socket)
    msg = 'usuários conectados: %s' % (listnames)
    socket_from.send(msg.encode())

def SendList(username, listnames):
    pass

def Ok(arg):
    pass

def GetSocketFromUsername(username):
    for s, name in usuarios_conectados.items():
        if name == username:
            return s

if __name__ == '__main__':
    Start()