from . import converters
from .blueprints import dbutil
from flask import Flask, g
from jinja2 import evalcontextfilter, Markup, escape
from werkzeug.utils import find_modules, import_string
import os
import re


def create_app(config=None):
    app = Flask(__name__, static_url_path='', static_folder='web/static', template_folder='web/templates')
    app.config.from_object(__name__)

    app.url_map.converters['int_list'] = converters.IntListConverter
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True

    app.config.update(
        DATABASE=os.path.join(app.root_path, 'database/database.db'),
        DISPLAY_CARD_IMAGES=False
    )
    app.config.update(config or {})

    register_blueprints(app)
    register_cli(app)
    register_teardowns(app)
    register_template_filters(app)

    return app


def register_blueprints(app):
    for name in find_modules('fusionhelper.blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None


def register_cli(app):
    @app.cli.command('initdb')
    def initdb_command():
        dbutil.initdb()


def register_teardowns(app):
    @app.teardown_appcontext
    def close_db(error):
        if hasattr(g, 'sqlite_db'):
            g.sqlite_db.close()


def register_template_filters(app):
    @app.template_filter()
    @evalcontextfilter
    def nl2br(eval_ctx, value):
        _paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
        result = u'\n\n'.join(u'%s <br>' % p.replace('\n', '<br>\n')
                              for p in _paragraph_re.split(escape(value)))
        if eval_ctx.autoescape:
            result = Markup(result)
        return result
