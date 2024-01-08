# Ex 4.4 - HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

# TO DO: import modules
import socket
import os

# TO DO: set constants
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 0.1



def get_file_data(filename):
    """ Get data from file """
    size_of_file = os.path.getsize(filename)
    file = open(filename,"rb")
    rfile = file.read(size_of_file)
    file.close()
    return rfile


def find_a_file(name, path):
    # print("now im in " +path)
    for root, dirs, files in os.walk(path):
        # print("my files is " + str(files))
        # print("searching for " + name + " in list: " + str(files))
        if name in files:
            # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@found!!!!!!!!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            return True ,os.path.join(root, name)
        else:
            for i in range(len(dirs)):
               find_a_file(name,os.path.join(path, dirs[i]))
            #    print("******************************getting out from "+dirs[i] + "******************************")
    return False ,"no path found!"
        
    
def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response
    position_of_end_file_name_text = resource.find("HTTP")-1 
    file_name_request = os.path.basename(resource[4:position_of_end_file_name_text])
    request = resource[4:position_of_end_file_name_text]
    
    
    if request[:20] == "/calculate-next?num=":
        find_equal_oper = request.find("=")
        num = int(request[find_equal_oper + 1:])
        returnNum = num + 1
        client_socket.send(str(returnNum).encode()) 
        
    elif request[:16] == "/calculate-area?":
        first_equal_index = request.find("=")
        secound_equal_index = request.find("=",first_equal_index + 1)
        find_and_parameter = request.find("&")
        height = int(request[first_equal_index + 1:find_and_parameter])
        width = int(request[secound_equal_index + 1:len(request)])
        area = (height*width)/2
        client_socket.send(str(area).encode())
        
    elif request == "/":
      if resource[4:position_of_end_file_name_text] == '/':
                    if os.path.isfile("C:\wwwroot\index.html"):
                        size_of_file = os.path.getsize("C:\wwwroot\index.html")
                        f = open("C:\wwwroot\index.html","rb")
                        l = f.read(size_of_file)
                        client_socket.send(l)
                        f.close()   
                        url = resource
    else:
            url = resource
            valid_path,updated_path_to_request_file = find_a_file(file_name_request,"C:\wwwroot")
            
            # if request[:20] == "/calculate-next?num=":
            #         client_socket.send(str(returnNum).encode()) 
            #         print("yesssssss")
                                   
            if not valid_path and request[:20] != "/calculate-next?num=" and request[:16] != "/calculate-area?":
                client_socket.send("(NOT FOUND)404".encode())
                print("404 NotFound " + updated_path_to_request_file + "resource " + resource)
                client_socket.close()
            else:
                size_of_file = os.path.getsize(updated_path_to_request_file)
                
                
                http_header = ("\r\n1.1 \r\n" +"200 \r\n"  + str(size_of_file) + "\r\n")
                
                # TO DO: check if URL had been redirected, not available or other error code. For example:
                if not(valid_path):
                    # TO DO: send 302 redirection response
                    client_socket.send("302".encode())
                    client_socket.send(url[:4].encode() + "C:\wwwroot\redirected\index2.html".encode() + url[:-9].encode())
                    print("302 CODE NOT EXIST")
                    
                if file_name_request == "favicon.ico":
                    http_header = http_header + "403 Forbidden"
                # TO DO: extract requested file type from URL (html, jpg etc)
                
                slice = file_name_request.find('.')
                filetype = file_name_request[slice:]  
                if filetype == '.html':
                    http_header = http_header + "text/html; charset=utf-8"
                    # TO DO: generate proper HTTP header
                elif filetype == '.jpg':
                    http_header = http_header + "image/jpeg"
                    # TO DO: generate proper jpg header
                # TO DO: handle all other headers
                elif filetype == '.js':
                    http_header = http_header + "text/javascript; charset=UTF-8"
                    
                elif filetype == '.css':
                    http_header = http_header + "text/css"

                # TO DO: read the data from the file
                data = get_file_data(updated_path_to_request_file)
                client_socket.send(data)
                print (resource)
                print("sent successfulllll")
                client_socket.send(http_header.encode())
    

def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    # TO DO: write function
    if request[:3] == "GET":
        return True,request
    return False,request

def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    
    while True:
        # TO DO: insert code that receives client request
        # ...
        client_socket.settimeout(None)
        client_request = client_socket.recv(1024).decode()
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            client_socket.close()
            print('Error: Not a valid HTTP request')
            break
    
    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(None)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()