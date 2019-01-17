#!/usr/bin/env python

import json
import web
import config, api, db

urls = (
    '/', 'Index',
    '/api/v(\d+)/', 'API'
)

app = web.application(urls, globals())
app.internalerror = web.debugerror

if web.config.get('_session') is None:
    session = web.session.Session(
        app, web.session.DiskStore('sessions'),
        initializer={'authenticated': False, 'login': ''}
    )
    web.config._session = session
else:
    session = web.config._session

# Database initialization
database = web.database(**config.database)

render = web.template.render('templates/', cache=config.cache)

# Save session and db in web.ctx
def ctx_hook():
    web.ctx.session = web.config._session
    web.ctx.db = database

app.add_processor(web.loadhook(ctx_hook))

if __name__ == "__main__":
    app.run()


class JsonHelper:
    def json(self, data):
        web.header('Content-Type', 'application/json')
        try:
            if data.get('error'):
                web.ctx.status = '400 Bad Request'
        except:
            pass
        return json.dumps(data)


class API(JsonHelper):
    def GET(self, version):
        return self.json(api.get(version))

    def POST(self, version):
        return self.json(api.post(version))


class Index:
    def GET(self):
        return render.index(db.option('hostname'))
