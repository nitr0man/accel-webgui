import web
import db
import config


def prelogin(session):
    pass


def get(session, version):
    data = web.input();
    print (data)
    if data.action == 'prelogin1':
        return prelogin(session)
    elif data.action == 'login':
        pass
    return {}


def post(session, version):
    data = web.data();
    print ('POST', data)
    return {}
