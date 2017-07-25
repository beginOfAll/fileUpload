#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import socket
import threading
import os
import sys
import zipfile

reload(sys)
sys.setdefaultencoding('utf-8')

upload_folder_path = ""
download_folder_path = ""


def server_ip_input():
    return raw_input("IP：")


def folder_path_input(message):
    path = raw_input("Save " + message + " file folder path:")
    if not (os.path.exists(path) and os.path.isdir(path)):
        print("Path error，Retry pls")
        path = folder_path_input(message)
    else:
        if not path.endswith('/'):
            path = path + '/'
    return path


def mode_upload(this_socket):
    global upload_folder_path
    check_code, file_name, file_size_s = this_socket.recv(1024).decode('utf-8').split('|')
    file_size = int(file_size_s)
    if check_code == "head":
        this_socket.send("ok".encode('utf-8'))
        recv_size = 0
        file_path = upload_folder_path + file_name
        f = open(file_path, 'wb')
        while True:
            if recv_size < file_size:
                data = this_socket.recv(1024)
                recv_size += len(data)
            else:
                break
            f.write(data)
        f.close()
        this_socket.send("upload file success".encode('utf-8'))
	print "upload success, file path : "+file_path


def zip_model(path):
    os.chdir(path)
    file_tree = os.walk('.')
    zip_file = zipfile.ZipFile("../file.zip", 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in file_tree:
        for one_file in files:
            zip_file.write(os.path.join(root, one_file))
        if len(files) == 0:
            empty_dir = zipfile.ZipInfo(root + '/')
            zip_file.writestr(empty_dir, '')
    zip_file.close()
    return os.path.abspath("../file.zip")


def mode_download(this_socket):
    global download_folder_path
    f_list = os.listdir(download_folder_path)
    if len(f_list) == 0:
        pass
    else:
        if len(f_list) == 1 and os.path.isfile(os.path.join(download_folder_path, f_list[0])):
            file_path = os.path.join(download_folder_path, f_list[0])
        else:
            file_path = zip_model(download_folder_path)
        file_name = os.path.basename(file_path)
        file_size = os.stat(file_path).st_size
        send_file_info = "head|" + file_name + "|" + str(file_size)
        this_socket.send(send_file_info.encode('utf-8'))
        if this_socket.recv(1024).decode('utf-8') == 'ok':
            flag = True
        send_size = 0
        f = open(file_path, 'rb')
        while flag:
            residue_size = file_size - send_size
            if residue_size < 1024:
                data = f.read(residue_size)
                flag = False
            else:
                data = f.read(1024)
                send_size += 1024
            this_socket.send(data)
        f.close()
        print this_socket.recv(1024).decode('utf-8')


def tcp_link(sock, addr, ip):
    print 'accept new connection from %s:%s' % addr
    sock.send(("welcome to connect " + ip).encode('utf-8'))

    mode = sock.recv(1024).decode('utf-8')
    if mode == 'upload':
        sock.send("begin to upload ".encode('utf-8'))
        mode_upload(sock)
    else:
        sock.send("begin to download ".encode('utf-8'))
        mode_download(sock)
    sock.close()
    print 'connection from %s:%s closed.' % addr


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # self_ip = server_ip_input()
    self_ip = "10.194.98.176"
    # upload_folder_path = folder_path_input("upload")
    upload_folder_path = r"/home/pfscuser/Desktop/recvFile/"
    # download_folder_path = folder_path_input("download")
    download_folder_path = r"/home/pfscuser/Desktop/downloadFile/"

    s.bind((self_ip, 10000))
    s.listen(5)
    print("wait for connection")
    while 1:
        one_socket, client_address = s.accept()
        t = threading.Thread(target=tcp_link, args=(one_socket, client_address, self_ip))
        t.start()
