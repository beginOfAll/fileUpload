import socket
import os


def filePathInput():
    path = input("File AllPath：")
    if not (os.path.exists(path) and os.path.isfile(path)):
        print("Path Error,Retry Pls：")
        path = filePathInput()
    return path




def serverIPInput():
    return input("Input Server IP：")


def openSocket(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, 10000))
    print(s.recv(1024).decode('utf-8'))
    return s


if __name__ == '__main__':
    file_path = filePathInput()
    file_name = os.path.basename(file_path)
    file_size = os.stat(path=file_path).st_size
    send_file_info = "head|" + file_name + "|" + str(file_size)
    print("FileName：", file_name, "，FileSize：", str(file_size))
    try:
        this_socket = openSocket(serverIPInput())
        this_socket.send(send_file_info.encode('utf-8'))
        send_size = 0
        residue_size = 0
        Flag = True
        f = open(file_path, 'rb')
        while Flag:
            residue_size = file_size - send_size
            if residue_size < 1024:
                data = f.read(residue_size)
                Flag = False
            else:
                data = f.read(1024)
                send_size += 1024
            this_socket.send(data)
        f.close()
        print(this_socket.recv(1024).decode('utf-8'))
        this_socket.close()
    except():
        print("Connecting Error，Process Closed")
        if f != None and f.closed == False:
            f.close()
        if this_socket != None:
            this_socket.close()
    input("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
