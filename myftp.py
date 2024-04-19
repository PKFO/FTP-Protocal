import socket 
import os

local_ip = "127.0.0.1"
port = 21
local_port = 50000
count = 0
active = 0
all_command = ['open','quit','close','disconnect','ascii','binary','bye','cd','delete','get','ls','put','pwd','rename','user']

def authen():
    clientSocket.sendall("OPTS UTF8 ON\r\n".encode())
    print(clientSocket.recv(2048).decode().strip())
    user = input(f"User ({args[1]}:(none)): ")
    clientSocket.sendall(f'USER {user}\r\n'.encode())
    res_user = clientSocket.recv(4096).decode().strip()
    if '3' in res_user :
        print(res_user)
        password = input("Password: ")
        print()
        clientSocket.sendall(f"PASS {password}\r\n".encode())
        res_password = clientSocket.recv(2048).decode().strip()
        print(res_password)
        if '5' in res_password:
            print("Login failed.")
            
    else:
        print(res_user)
        print("Login failed.")
    
while True: 
    line = input("ftp> ").strip()
    args = line.split() 
    if not args:
        continue
    else:
        command = args[0]

    if command not in all_command:
        print('ambigous command')
        continue
    if command == 'open' and active == 1:
        print('Already connected to ' + last_ip + ', use disconnect first.')
    elif command == 'open' and active == 0:
            if count == 0:
                last_ip = args[1]
                count = 1
            clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            if len(args) == 2:
                clientSocket.connect((args[1],port))
            else:
                clientSocket.connect((args[1],int(args[2])))
            resp = clientSocket.recv(1024)
            print('Connected to ' + args[1])
            print(resp.decode().strip())
            active = 1
            authen()
    if active == 1:
        if command == 'quit':
            if active == 1:
                command_message = "QUIT\r\n"
                clientSocket.sendall(command_message.encode())
                message =  clientSocket.recv(1024).decode().strip()
                print(message)
                print()
            else:
                print()
                active = 0
                count = 0
            break

        elif command == 'disconnect':
            active = 0
            count = 0
            command_message = "QUIT\r\n"
            clientSocket.sendall(command_message.encode())
            message =  clientSocket.recv(1024).decode().strip()
            print(message)
            clientSocket.close()

        elif command == 'ascii':
            command_ascii = "TYPE A\r\n"
            clientSocket.sendall(command_ascii.encode())
            message =  clientSocket.recv(1024).decode().strip()
            print(message)

        elif command == 'binary':
            command_binary = "TYPE I\r\n"
            clientSocket.sendall(command_binary.encode())
            message =  clientSocket.recv(1024).decode().strip()
            print(message)

        elif command == 'bye':
            command_message = "QUIT\r\n"
            clientSocket.sendall(command_message.encode())
            message =  clientSocket.recv(1024).decode().strip()
            print(message)
            print()
            clientSocket.close()
            active = 0
            count = 0
            break
        elif command == 'cd':
            if len(args) == 1:
                Remote_directory = input("Remote directory ")
            elif len(args) == 2:
                Remote_directory = args[1]
            clientSocket.sendall(("CWD " + Remote_directory + "\r\n").encode())
            message =  clientSocket.recv(1024).decode().strip()
            print(message)

        elif command == 'close':
            command_message = "QUIT\r\n"
            clientSocket.sendall(command_message.encode())
            message =  clientSocket.recv(1024).decode().strip()
            print(message)
            clientSocket.close()
            active = 0
            count = 0

        elif command == 'delete':
            if len(args) == 1:
                f = input("Remote file ")
            elif len(args) == 2:
                f = args[1]
            command_del = "DELE " + f + "\r\n"
            clientSocket.sendall(command_del.encode())
            res_del = clientSocket.recv(1024).decode().strip()
            print(res_del)
        elif command == 'get':
            Remote_file = ''
            Local_file = ''
            if len(args) == 1: 
                Remote_file = input("Remote file ")
                Local_file = input("Local file ")
            elif len(args) == 2:
                Remote_file = args[1]
                Local_file = args[1]
            elif len(args) == 3:
                Remote_file = args[1]
                Local_file = args[2]
            if (not (len(Local_file) >= 2 and Local_file[1] == ":")):
                Local_file = os.getcwd()+"\\"+ Local_file
            command_get = "PORT " + ",".join(local_ip.split(".")) + "," + str(local_port//256) + "," + str(local_port%256) + "\r\n"
            clientSocket.sendall(command_get.encode())
            print(clientSocket.recv(2048).decode().strip())
            command_gett = "RETR " + Remote_file + "\r\n"
            clientSocket.sendall(command_gett.encode())
            print(clientSocket.recv(2048).decode().strip())
            data_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            data_socket.bind((local_ip,local_port))
            data_socket.listen(8)
            data_connection,data_addr = data_socket.accept()
            print(clientSocket.recv(2048).decode().strip())
            with open(Local_file, 'wb') as local_fp:
                while True:
                    file_data = data_connection.recv(2048)
                    if not file_data:
                        break
                    local_fp.write(file_data)
            data_socket.close()


        elif command == 'ls':
            command_ls = "PORT " + ",".join(local_ip.split(".")) + "," + str(local_port//256) + "," + str(local_port%256) + "\r\n"
            clientSocket.sendall(command_ls.encode())
            print(clientSocket.recv(2048).decode().strip())
            clientSocket.sendall(("NLST\r\n").encode())
            data_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            data_socket.bind((local_ip,local_port))
            data_socket.listen(8)
        
            print(clientSocket.recv(2048).decode().strip())
            data_connection,data_addr = data_socket.accept()
            data = b''
            while True:
                res_data = data_connection.recv(4096)
                if not res_data:
                    break
                data += res_data

            print(data.decode().strip())
            print(clientSocket.recv(2048).decode().strip())
            data_connection.close()
            data_socket.close()
        elif command == 'put':
            Remote_file = ''
            Local_file = ''
            if len(args) == 1: 
                Remote_file = input("Remote file ")
                Local_file = input("Local file ")
            elif len(args) == 2:
                Remote_file = args[1]
                Local_file = args[1]
            elif len(args) == 3:
                Remote_file = args[1]
                Local_file = args[2]
            if (not (len(Local_file) >= 2 and Local_file[1] == ":")):
                Local_file = os.getcwd()+"\\"+ Local_file
            command_put = "PORT " + ",".join(local_ip.split(".")) + "," + str(local_port//256) + "," + str(local_port%256) + "\r\n"
            clientSocket.sendall(command_put.encode())
            print(clientSocket.recv(2048).decode().strip())
            clientSocket.sendall(("STOR " + Remote_file + "\r\n").encode())
            print(clientSocket.recv(2048).decode().strip())
            data_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            data_socket.bind((local_ip,local_port))
            data_socket.listen(8)
            data_connection,data_addr = data_socket.accept()
            with open(Local_file,"rb") as f:
                data = f.read(1024)
                while data:
                    data_connection.send(data)
                    data = f.read(1024)

            data_connection.close()
            data_socket.close()
            print(clientSocket.recv(2048).decode().strip())

        elif command == 'pwd':
            command_pwd = "XPWD\r\n"
            clientSocket.sendall(command_pwd.encode())
            print(clientSocket.recv(1024).decode().strip())

        elif command == 'rename':
            if len(args) == 1:
                filename = input("From name ")
                if not filename:
                    print('rename from-name to-name.')
                    continue
                changename = input("To name ")
            elif len(args) == 2:
                filename = args[1]
                changename = input("To name ")
            elif len(args) == 3:
                filename = args[1]
                changename = args[2]
            command_rename = "RNFR " + filename + "\r\n"
            clientSocket.sendall(command_rename.encode())
            res_rename = clientSocket.recv(1024).decode().strip()
            if not changename:
                print('rename from-name to-name.')
            elif '5' in res_rename :
                print(res_rename)
            else :
                command_changename = "RNTO " + changename + "\r\n"
                clientSocket.sendall(command_changename.encode())
                res_changename = clientSocket.recv(1024).decode().strip()
                if '350'in res_changename:
                    clientSocket.sendall(command_rename.encode())
                    print(clientSocket.recv(1024).decode().strip())
                else:
                    print(res_changename)

        elif command == 'user':
            if len(args) == 1:
                username = input("Username ")
            elif len(args) == 2:
                username = args[1]
            elif len(args) == 3:
                username = args[1]
                password_user = args[2]
            clientSocket.sendall(f'USER {username}\r\n'.encode())
            res = clientSocket.recv(1024).decode().strip()
            if '501' in res :
                print("Usage: user username [password] [account]")
            elif '331' in res:
                print(res)
                if len(args) != 3:
                    password_user = input("Password: ")
                    print()
                clientSocket.sendall(f"PASS {password_user}\r\n".encode())
                mes = clientSocket.recv(1024).decode().strip()
                print(mes)
                if '530' in mes:
                    print("Login failed.")
                else:
                    active = 1
            else:
                print(res)
                print("Login failed.")
    else:
        print('Not connected.')   

