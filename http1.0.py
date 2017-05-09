#support python2.x
import socket
import sys
import traceback

def main():

    argv = sys.argv
    argc = len(argv)

    http = 'http://'
    slash = '/'
    port = 80

    # check commandline parameter
    if (argc != 2):
        sys.stderr.write('Usage: python http1.0.py [ADDRESS]\n')
        exit()

    try:
        #set domain and filepath
        index = argv[1].find(http)
        temp = argv[1][index+len(http):]
        index = temp.find(slash)
        domain = temp[:index]
        file_path = temp[index:]

        #connect
        address = (socket.gethostbyname(domain), port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)

        #set message
        message = 'GET {0} HTTP/1.0\r\n\r\n'.format(file_path)

        #send message
        sock.sendall(message.encode())
        index = file_path.rfind(slash)
        file_name = file_path[index+len(slash):]
        fout = open(file_name, 'wb')
        sock_file = sock.makefile()
        state = 0

        #read lines
        for line in sock_file.readlines():

            if (line == 'HTTP/1.1 200 OK\r\n'):
                state = 1
            if (state == 1 and line == '\r\n'):
                state = 2
                continue
            if (state == 2 and line == '\r\n'):
                state = 3
                continue
            if (state == 3):
                fout.write(line)
            elif(state == 0):
                sys.stderr.write('Cannot receive \'HTTP/1.1 200 OK\'\n')
                exit()

        sock.close()

    except:
        sys.stderr.write(traceback.format_exc())
        exit()



if __name__ == '__main__':
    main()