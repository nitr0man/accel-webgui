import json
import web
import config, db, api

urls = (
    '/', 'Index',
    '/api/v(\d+)/', 'API'
)

session = None


t_globals = dict(
  datestr=web.datestr,
)
render = web.template.render('templates/', cache=config.cache,
    globals=t_globals)
render._keywords['globals']['render'] = render


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
        return self.json(api.get(session, version))

    def POST(self, version):
        return self.json(api.post(session, version))


class Index:
    def GET(self):
        return render.index(db.option('hostname'))


if __name__ == "__main__":
    app = web.application(urls, globals())
    session = web.session.Session(app, web.session.DiskStore('sessions'))
    app.internalerror = web.debugerror
    app.run()
