import web
from utils import checkhash, makehash

def option(key):
    result = web.ctx.db.where('options', key=key).first()
    return result['value'] if result else None


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
