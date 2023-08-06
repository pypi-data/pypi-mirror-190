import flask
import season
import os
import traceback
import time
import datetime

log_level = season.log.warning
plugin = ['workspace', 'branch', 'setting', 'plugin']
theme = "default"
home = "ui/workspace"
category = [
    {'id': 'page', 'title': 'Page'},
    {'id': 'view', 'title': 'View'},
    {'id': 'modal', 'title': 'Modal'}
]

def acl(wiz):
    try:
        role = wiz.server.flask.session['role']
        if role == 'admin':
            return True
    except Exception as e:
        pass
    wiz.response.abort(401)

def on_error(wiz, e):
    pass

def before_request(wiz):
    try:
        wiz.server.flask.session.permanent = True
        wiz.server.wsgi.flask.permanent_session_lifetime = datetime.timedelta(minutes=360)
        wiz.server.wsgi.flask.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=360)
    except Exception as e:
        pass

def after_request(wiz, response):
    response.headers['Service-Worker-Allowed'] = '/'
    if wiz.is_dev():
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        response.headers['Cache-Control'] = 'public, max-age=0'
    else:
        if wiz.request.uri().split("/")[1] != "resources":
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            response.headers['Cache-Control'] = 'public, max-age=0'
    return response

def build_resource(resource_dirpath, resource_filepath):
    try:
        cache = season.cache
        if 'resources' not in cache:
            cache.resources = season.stdClass()

        _, ext = os.path.splitext(resource_filepath)
        filepath = os.path.join(resource_dirpath, resource_filepath)

        try:
            mode = flask.request.cookies.get("season-wiz-devmode")
        except Exception as e:
            mode = False

        if mode != 'true':
            if filepath in cache.resources:
                return cache.resources[filepath]

        ext = ext.lower()

        allowed = ['.less', '.scss']
        if ext not in allowed:
            return None

        if ext == '.less':
            import lesscpy
            from six import StringIO

            f = open(filepath, 'r')
            lessfile = f.read()
            f.close()
            cssfile = lesscpy.compile(StringIO(lessfile), minify=True)
            response = flask.Response(str(cssfile))
            response.headers['Content-Type'] = 'text/css'
            cache.resources[filepath] = response
            return cache.resources[filepath]

        if ext == '.scss':
            import sass
            f = open(filepath, 'r')
            css = f.read()
            f.close()
            css = sass.compile(string=css)
            css = str(css)
            response = flask.Response(css)
            response.headers['Content-Type'] = 'text/css'
            cache.resources[filepath] = response
            return cache.resources[filepath]        
    except Exception as e:
        pass
    return None