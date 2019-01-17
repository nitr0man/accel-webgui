import web
from utils import checkhash, makehash

def option(key):
    result = web.ctx.db.where('options', key=key).first()
    return result['value'] if result else None


def check_login(user, password):
    result = web.ctx.db.where('user', login=user).first()
    return checkhash(password, result['password']) if result else False


def create_login(user, password, update=False):
    password = makehash(password)
    result = web.ctx.db.where('user', login=user).first()
    if result and update:
        web.ctx.db.update(
            'user', where='login=$user', password=password, vars=locals())
    else:
        web.ctx.db.insert('user', login=user, password=password)
