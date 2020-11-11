import sys
from os.path import join
sys.path.insert(1, sys.path[0])
from config import load_config, app_init
from datetime import datetime
from IPython import embed
from flask import request, redirect

app = app_init(__name__)

from tag import Tag # After app_init(), which sets db for the model

cfg = load_config(join(app.root_path, '../shared/config.yml'))

@app.route('/', methods=['GET'])
def show_tags():
    tags = Tag.all()
    tags_html = '\n'.join(list(map(lambda x: x.name + "<br>", tags)))
    form_html = "<form action=\"/tags\" method=\"POST\"><label>Enter a tag: </label><input name=\"tag-name\"></form>"
    #embed()
    return "<h1>The Ultimate Tag Manager</h1><a href=\"/\">Home</a> <a href=\"/about\">About</a><h1>Hello World!</h1><img src=\"%s\" style=\"width:300px\"><div>%s</div><div>%s</div>" % (cfg['awesome_image'],tags_html, form_html)

@app.route('/about', methods=['GET'])
def about():
    return '<h1>The Ultimate Tag Manager</h1><a href=\"/\">Home</a> <a href=\"/about\">About</a><h1>A Uniquely World-Changing Super-Proprietary Way of Managing Tags</h1><p>This is the only website ever designed that has at least one of the properties common to every other website ever designed.</p><p>A highly respected source has said, "I\'d rather use this site than use one of the best sites in the world!"'

@app.route('/tags', methods=['POST'])
def add_tag():
    new_tag = request.form['tag-name']
    tag = Tag.where('tag', new_tag).first()
    if tag is None:
        tag = Tag.create(name=new_tag)

    return redirect('/')
