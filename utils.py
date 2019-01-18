import hashlib
import os
import socket
import subprocess
import uuid


def makehash(password):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
    return ':'.join((hashed_password, salt))


def checkhash(password, hash):
    hashed_password, salt = hash.split(':')
    return hashed_password == hashlib.sha512(
        (password + salt).encode('utf-8')).hexdigest()


def netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    ret = b''
    data = True
    while data:
        data = s.recv(4096)
        ret += data
    s.close()
    return ret


def accelcmd(cmd):
    return netcat('127.0.0.1', 2001, cmd).decode('utf-8', 'backslashreplace')


def readint(path):
    print(path)
    if os.path.exists(path):
        return int(open(path).read())
