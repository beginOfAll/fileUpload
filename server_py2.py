#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import socket
import threading
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

ip = ""
base_path = ""


def folderPathInput():
    path = raw_input("Save upload file folder path：")
    if not (os.path.exists(path) and os.path.isdir(path)):
        print "Path error, retry pls"
        path = folderPathInput()
    return path


def tcp_link(sock, addr):
    global ip, base_path
    print 'accept new connection from %s:%s' % addr
    sock.send(("welcome to connect " + ip).encode())
    check_code, file_name, file_size_s = sock.recv(1024).decode().split('|')
    file_size = int(file_size_s)
    if check_code == "head":
        recv_size = 0
        file_path = base_path + file_name
        f = open(file_path, 'wb')
        while 1:
            if recv_size < file_size:
                data = sock.recv(1024)
                recv_size += len(data)
            else:
                break
            f.write(data)
        f.close()
        sock.send("upload file success".encode())
        print "upload success, file path : "+file_path
    sock.close()
    print 'connection from %s:%s closed.' % addr



if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #ip = raw_input("IP：")
    ip = r"10.194.98.176"
    #base_path = folderPathInput()
    base_path = r"/home/pfscuser/Desktop/recvFile/"
    s.bind((ip, 10000))
    s.listen(5)
    print "wait for connection"
    while 1:
        this_socket, client_address = s.accept()
        t = threading.Thread(target=tcp_link, args=(this_socket, client_address))
        t.start()
