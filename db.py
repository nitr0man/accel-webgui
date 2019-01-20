import web
from utils import checkhash, makehash

def option(key):
    result = web.ctx.db.where('options', key=key).first()
    return result['value'] if result else None


def options_list():
    result = web.ctx.db.select('options', order='key')
    return result


def set_option(key, value):
    result = web.ctx.db.where('options', key=key).first()
    if result:
        web.ctx.db.update(
            'options', where='key=$key', vars=locals(), value=value)
    else:
        web.ctx.db.insert('options', key=key, value=value)


def check_login(user, password):
    result = web.ctx.db.where('user', login=user).first()
    return checkhash(password, result['password']) if result else False


def create_login(user, password, update=False, superuser=None):
    hash = makehash(password)
    result = web.ctx.db.where('user', login=user).first()
    data = {}
    if password:
        data['password'] = hash
    if superuser is not None:
        data['superuser'] = superuser
    if result and update:
        web.ctx.db.update(
            'user', where='login=$user', vars=locals(), **data)
    else:
        web.ctx.db.insert('user', login=user, **data)
