import datetime
import db
import os
import re
import web
import utils


RE_IFMATCH = re.compile('[a-z0-9]+', re.I)


def accelcmd(cmd):
    return utils.accelcmd(cmd, db.option('accel_password'))


def auth_required(fn):
    def wrapped(*args,  **kwargs):
        if web.ctx.session.get('authenticated'):
            return fn(*args,  **kwargs)
        else:
            return {
                'error': 'Authentication is required!',
                'logout': True
            }
    return wrapped


def checkiface(fn):
    def wrapped(data, *args,  **kwargs):
        iface = data.get('interface')
        if not iface or not RE_IFMATCH.match(iface.strip()):
            return {'error': 'Wrong interface'}
        return fn(data, *args,  **kwargs)
    return wrapped


def prelogin():
    return {
        'authenticated': web.ctx.session.get('authenticated', False),
        'login': web.ctx.session.get('login', '')
    }


def login(data):
    web.ctx.session.login = data.login
    if db.check_login(data.login, data.password):
        web.ctx.session.authenticated = True
        return {}
    return {'error': 'Wrong login or password'}


def logout():
    web.ctx.session.kill()
    return {}


@auth_required
def stat():
    return {
        'output': accelcmd('show stat')
    }


@auth_required
def users():
    lines = accelcmd('show sessions').splitlines()
    lines = [
        l.replace('|', '</td><td>')
        for l in lines
    ]
    table = "</td></tr>\n<tr><td>".join(lines)
    table = re.sub('<tr><td>$', '', table)

    table = '<table id="tusers" class="cell-border"><tbody><tr><td>' + table + "</tbody></table>"

    return {
        'output': table
    }


@auth_required
@checkiface
def ifstat(data):
    iface = data.interface.strip()

    path = os.path.join('/', 'sys', 'class', 'net', iface, 'statistics')
    return {
        'stamp': datetime.datetime.now().timestamp() * 1000,
        'rxbytes': utils.readint(os.path.join(path, 'rx_bytes')),
        'txbytes': utils.readint(os.path.join(path, 'tx_bytes')),
        'rxpackets': utils.readint(os.path.join(path, 'rx_packets')),
        'txpackets': utils.readint(os.path.join(path, 'tx_packets')),
    }


@auth_required
@checkiface
def kill(data, hard):
    iface = data.interface.strip()
    accelcmd('terminate if {} {}'.format(iface, 'hard' if hard else 'soft'))
    return {}


def get(version):
    data = web.input();
    if not data.get('action'):
        return {'error': 'Bad request'}
    if data.action == 'prelogin':
        return prelogin()
    elif data.action == 'stat':
        return stat()
    elif data.action == 'users':
        return users()
    elif data.action == 'ifstat':
        return ifstat(data)
    return {'error': 'Wrong action'}


def post(version):
    data = web.input();
    if not data.get('action'):
        return {'error': 'Bad request'}
    if data.action == 'prelogin':
        return prelogin()
    elif data.action == 'login':
        return login(data)
    elif data.action == 'logout':
        return logout()
    elif data.action == 'stat':
        return stat()
    elif data.action == 'users':
        return users()
    elif data.action == 'ifstat':
        return ifstat(data)
    elif data.action == 'killsoft':
        return kill(data, False)
    elif data.action == 'killhard':
        return kill(data, True)
    return {'error': 'Wrong action'}
