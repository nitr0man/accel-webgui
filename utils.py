import hashlib
import os
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


def accelcmd(cmd):
    cmd = cmd.split(' ')
    cmd.insert(0, 'accel-cmd')
    return subprocess.check_output(cmd)


def readint(path):
    print(path)
    if os.path.exists(path):
        return int(open(path).read())
