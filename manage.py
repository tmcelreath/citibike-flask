import os
from app import create_app
from flask.ext.script import Manager, Shell
from flask_debugtoolbar import DebugToolbarExtension

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.debug = True
app.config['SECRET_KEY'] = 'ADMIN'
DEBUG_TOOLBAR = DebugToolbarExtension(app)

manager = Manager(app)


def make_shell_context():
    return dict(app=app)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()

