import socket
import os


def filePathInput():
    path = input("File AllPath：")
    if not (os.path.exists(path) and os.path.isfile(path)):
        print("Path Error,Retry Pls：")
        path = filePathInput()
    return path


def folderPathInput():
    path = input("Folder AllPath：")
    if not (os.path.exists(path) and os.path.isdir(path)):
        print("Path Error,Retry Pls：")
        path = folderPathInput()
    return path


def mode_input():
    m_mode = input("Input number : 1.(upload) or 2.(download):")
    if m_mode.isalnum():
        m_mode = int(m_mode)
        if m_mode != 1 and m_mode != 2:
            print("only 1 or 2 pls !")
            m_mode = mode_input()
    else:
        print("only 1 or 2 pls !")
        m_mode = mode_input()
    return m_mode


def server_ip_input():
    return input("Input Server IP：")


def open_socket(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, 10000))
    print(s.recv(1024).decode('utf-8'))
    return s


def mode_upload(this_socket):
    this_socket.send("upload".encode('utf-8'))
    print(this_socket.recv(1024).decode('utf-8'))
    file_path = filePathInput()
    file_name = os.path.basename(file_path)
    file_size = os.stat(file_path).st_size
    send_file_info = "head|" + file_name + "|" + str(file_size)
    print("FileName：", file_name, "，FileSize：", str(file_size))
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
    print(this_socket.recv(1024).decode('utf-8'))


def mode_download(this_socket):
    this_socket.send("download".encode('utf-8'))
    print(this_socket.recv(1024).decode('utf-8'))
    folder = folderPathInput()
    if not folder.endswith('\\'):
        folder = folder + '\\'
    check_code, file_name, file_size_s = this_socket.recv(1024).decode('utf-8').split('|')
    file_size = int(file_size_s)
    if check_code == "head":
        this_socket.send("ok".encode('utf-8'))
        recv_size = 0
        file_path = folder + file_name
        f = open(file_path, 'wb')
        while True:
            if recv_size < file_size:
                data = this_socket.recv(1024)
                recv_size += len(data)
            else:
                break
            f.write(data)
        f.close()
        this_socket.send("download file success".encode('utf-8'))
        print("receive file success, file path : ", file_path)


if __name__ == '__main__':
    mode = mode_input()
    one_socket = open_socket(server_ip_input())
    try:
        if mode == 1:
            mode_upload(one_socket)
        else:
            mode_download(one_socket)
        one_socket.close()
    except():
        print("Connecting Error，Process Closed")
        if one_socket is not None:
            one_socket.close()
    input("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
