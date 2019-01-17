#!/usr/bin/env python

import app
import argparse
import db
import getpass


parser = argparse.ArgumentParser(description='Create/update users')
parser.add_argument('login', help='User login')
parser.add_argument(
    '--update', '-u', action='store_true', help='update existing user')

parser.add_argument(
    '--superuser', '-s', action='store_true', help='create superuser')

args = parser.parse_args()

password = getpass.getpass()
password2 = getpass.getpass('Re-type password:')

if password != password2:
    print("Passwords are different!")
    exit()

print(args.login, password, args)

app.ctx_hook()
db.create_login(args.login, password, args.update, args.superuser)
