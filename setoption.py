#!/usr/bin/env python

import app
import argparse
import db
import getpass


parser = argparse.ArgumentParser(description='Set option')
parser.add_argument('key', help='Option name')
parser.add_argument('value', help='Option value')

args = parser.parse_args()

app.ctx_hook()
db.set_option(args.key, args.value)
