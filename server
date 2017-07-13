import socket
import threading
import os

ip = ""
base_path = ""


def folderPathInput():
    path = input("Save upload file floder path:")
    if not (os.path.exists(path) and os.path.isdir(path)):
        print("Path error，Retry pls")
        path = folderPathInput()
    return path


def tcp_link(sock, addr):
    global ip, base_path
    print('accept new connection from %s:%s' % addr)
    sock.send(("welcome to connect " + ip).encode('utf-8'))
    check_code, file_name, file_size_s = sock.recv(1024).decode('utf-8').split('|')
    file_size = int(file_size_s)
    if check_code == "head":
        recv_size = 0
        file_path = base_path + file_name
        f = open(file_path, 'wb')
        while True:
            if recv_size < file_size:
                data = sock.recv(1024)
                recv_size += len(data)
            else:
                break
            f.write(data)
        f.close()
        sock.send("upload file success".encode('utf-8'))
        print("upload success, file path : ", file_path)
    sock.close()
    print('connection from %s:%s closed.' % addr)


def serverIPInput():
    return input("IP：")


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = serverIPInput()
    base_path = folderPathInput()
    if not base_path.endswith('\\'):
        base_path = base_path + '\\'
    s.bind((ip, 10000))
    s.listen(5)
    print("wait for connection")
    while True:
        this_socket, client_address = s.accept()
        t = threading.Thread(target=tcp_link, args=(this_socket, client_address))
        t.start()
