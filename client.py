# -*- coding: utf-8 -*-
import socket
import select
import sys
import time


def main():
    host = 'localhost'
    porta = 1234

    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSocket.connect((host, porta))

    inputlist = [sys.stdin, serverSocket]
    while True:
        readinputs,write,error = select.select(inputlist , [], [])
        for readinput in readinputs:
            if readinput == serverSocket:
                msg = serverSocket.recv(2048)
                msg = msg.decode()
                if not msg:
                    print('Desconectado')
                    sys.exit()
                else:
                    if '!nick' in msg:
                        nick = input('Nick: ')
                        serverSocket.send(('!join %s' % (nick)).encode())
                    else:
                        sys.stdout.write('\r' + msg)
                        sys.stdout.write('\n>')
                        sys.stdout.flush()
            else:
                sys.stdout.write('>')
                sys.stdout.flush()
                msg = input()
                serverSocket.send(msg.encode())
        time.sleep(0.1)


def receber_mensagem(serverSocket):
    try:
        mensagem_servidor, serverAddress = serverSocket.recvfrom(2048)
        return mensagem_servidor.decode('utf-8')
    except socket.error:
        print ('eeeei')


def enviar_mensagem(socket, mensagem):
    socket.send(mensagem.encode('utf-8'))

if __name__ == "__main__":
    main()