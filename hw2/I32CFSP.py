import socket

def connect(host: str, port: int):
    I32CFSP = socket.socket()
    I32CFSP.connect((host, port))
    I32CFSP_input = I32CFSP.makefile('r')
    I32CFSP_output = I32CFSP.makefile('w')
    return I32CFSP, I32CFSP_input, I32CFSP_output

def send(connection: 'connection', message: str):
    I32CFSP, I32CFSP_input, I32CFSP_output = connection
    I32CFSP_output.write(message + '\r\n')
    I32CFSP_output.flush()

def receive(connection: 'connection'):
    I32CFSP, I32CFSP_input, I32CFSP_output = connection
    data = I32CFSP_input.readline()[:-1]
    return data

