#!/usr/bin/env python

import app
import argparse
import db
import getpass


parser = argparse.ArgumentParser(description='Show options')

args = parser.parse_args()

app.ctx_hook()
options = db.options_list()
print("Current options values:")
for o in options:
    print(o['key'],'=', o['value'])
