# import socket module
from socket import *
import sys  # In order to terminate the program

# Create server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverPort = 6789
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("Web server is running on port", serverPort)

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        message = connectionSocket.recv(1024).decode()
        if message and len(message.split()) >= 2:
            filename = message.split()[1]
        else:
            # Berikan fallback jika request tidak valid atau kosong
                filename = "/index.html"

        with open(filename[1:], "r", encoding="utf-8") as f:
            outputdata = f.read()

        # Send one HTTP header line into socket
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()

    except IOError:
        # Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>\r\n".encode())

        # Close client socket
        connectionSocket.close()

# Close server socket
serverSocket.close()
sys.exit()