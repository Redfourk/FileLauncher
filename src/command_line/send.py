# ###########################################################################################################
#       NOTICE: THIS CODE IS DEPRECIATED, ALL CLI INTEGRATIONS ARE IN DEVELOPMENT ON A SEPARATE BRANCH!
# ###########################################################################################################



import socket

# Connect
s = socket.socket()
s.connect(('1.2.3.4', 5001))

# Read and Send
with open('test.txt', 'rb') as f:
    s.sendall(f.read())
s.close()

