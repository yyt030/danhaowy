# coding: utf-8
import os
# import daemon
from flask.ext.script import Manager
from web import create_app
from flask.ext.migrate import Migrate, MigrateCommand
from web.models import db

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    """启动网站"""
    app.run(host="localhost", port=5000, threaded=True)


@manager.command
def run_80():
    """启动网站"""
    app.run(host="0.0.0.0", port=80, threaded=True)


if __name__ == "__main__":
    manager.run()
