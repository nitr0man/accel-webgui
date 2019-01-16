import config

def listing(**k):
    return config.DB.select('user', **k)


def option(key):
    result = config.DB.where('options', key=key).first()
    return result['value'] if result else None


def check_login(user, password):
    pass