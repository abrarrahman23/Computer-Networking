# import socket module
from socket import *
# In order to terminate the program
import sys

def webServer(port=13331):
  serverSocket = socket(AF_INET, SOCK_STREAM)
  
  #Prepare a server socket
  serverSocket.bind(("", port))
  
  #Fill in start
  serverSocket.listen(1)
  #Fill in end

  while True:
    #Establish the connection
    # print('Ready to serve...')  # ← comment out prints for Gradescope
    connectionSocket, addr = serverSocket.accept()     #Fill in start -are you accepting connections?     #Fill in end
    
    try:
      message = connectionSocket.recv(1024).decode()   #Fill in start -a client is sending you a message   #Fill in end 
      if not message:
        connectionSocket.close()
        continue

      filename = message.split()[1]
      
      # opens the client requested file. Read as *binary* for socket send
      f = open(filename[1:], 'rb')     #fill in start              #fill in end

      # Status line and headers for success (HTTP/1.1 200 OK)
      status_line = b"HTTP/1.1 200 OK\r\n"
      outputdata = (
        b"Content-Type: text/html; charset=UTF-8\r\n"
        b"Server: TinyPythonWeb/1.0\r\n"
        b"Connection: close\r\n"
      )

      # Read body
      body_bytes = b""
      for i in f:  # for line in file
        body_bytes += i  # append html file contents
      f.close()

      headers = (
        status_line +
        outputdata +
        b"Content-Length: " + str(len(body_bytes)).encode() + b"\r\n\r\n"
      )
        
      # Send everything in one go
      connectionSocket.sendall(headers + body_bytes)
      connectionSocket.close() #closing the connection socket
      
    except Exception:
      # 404 Not Found response
      body = b"""<html><head><title>404 Not Found</title></head>
<body><h1>404 Not Found</h1><p>The requested file was not found.</p></body></html>"""
      headers = (
        b"HTTP/1.1 404 Not Found\r\n"
        b"Content-Type: text/html; charset=UTF-8\r\n"
        b"Server: TinyPythonWeb/1.0\r\n"
        b"Connection: close\r\n"
        b"Content-Length: " + str(len(body)).encode() + b"\r\n\r\n"
      )
      connectionSocket.sendall(headers + body)
      connectionSocket.close()

  #serverSocket.close()
  #sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
  webServer(13331)
