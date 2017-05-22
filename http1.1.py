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
        sys.stderr.write('Usage: python http1.1.py [ADDRESS]\n')
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
        # sock_file = sock.makefile()
        state = 0
        read = 0
        length = 1
        data = ''
        i = 0
        stop =0
        byte = 0

        while(1):
            line = ''
            while(1) :
                data = sock.recv(1)
                if (data == '\r') :
                    read = 1

                line = line + data

                if (read == 1 and data == '\n'):
                    break

                if (state ==2 ):
                    byte += 1

                if (byte >= length) :
                    break

            if (line == 'HTTP/1.1 200 OK\r\n'):
                state = 1
            if (state == 1 and line == '\r\n'):
                state = 2
                continue

            if (state == 2):
                fout.write(line)
                i+=len(line)

            if (i >= length):
                break

            elif(state == 0):
                sys.stderr.write('Cannot receive \'HTTP/1.1 200 OK\'\n')
                exit()

            #get length
            if ('Content-Length: ' in line):
                index = line.rfind('Content-Length: ');
                tmp = line[index+len('Content-Length: '):]
                length = int(tmp)

        sock.close()
        fout.close()

    except:
        sys.stderr.write(traceback.format_exc())
        exit()

if __name__ == '__main__':
    main()