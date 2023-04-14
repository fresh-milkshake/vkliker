import os

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for,
)

from app.bot import Bot, delete_group_by_id
from app.models import Group
from app import db

app = Flask(__name__)
app.config['VK_AUTH_TOKEN'] = os.environ.get('VK_AUTH_TOKEN')
bot = Bot(app.config['VK_AUTH_TOKEN'])
db.init_app(app)


@app.route('/')
def index():
    groups = Group.query.all()
    return render_template('index.html', title='index', groups=groups or None)


@app.route('/group', methods=['POST'])
def like():
    group_id = request.form.get('group_id')
    count = request.form.get('count')
    bot.process_group(int(group_id), int(count))
    return redirect(url_for('index'))


@app.route('/ungroup', methods=['POST'])
def ungroup():
    group_id = request.form.get('group_id')
    count = request.form.get('count')
    bot.unprocess_group(int(group_id), int(count))
    return redirect(url_for('index'))


@app.route('/deletegroup/<int:db_id>')
def delete_all(db_id):
    delete_group_by_id(db_id)
    return redirect(url_for('index'))


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename')
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
