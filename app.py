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

delete_js = '''
<script type="text/javascript" src="static/js/lib/jquery-3.5.1.js"></script>
<script type="text/javascript">
$('.delete_link').on('click', function(e) {
  var url = "http://localhost:5555" + $(this).attr('href');
  var xhr = new XMLHttpRequest();
  xhr.open("DELETE", url, true);
  xhr.send(null);
  window.location.href='/';  // Redirect
  return false;
});
</script>
'''

@app.route('/', methods=['GET'])
def show_tags():
    tags = Tag.all()
    tags_html = '\n'.join(list(map(lambda x: "<a class=\"delete_link\" href=\"/tags/%s\">%s</a><br>" % (x.name, x.name), tags)))
    form_html = "<form action=\"/tags\" method=\"POST\"><label>Enter a tag: </label><input name=\"tag-name\"></form>"
    #embed()
    return "<h1>The Ultimate Tag Manager</h1><h1>Hello World!</h1><img src=\"%s\" style=\"width:300px\"><div>%s</div><div>%s</div>%s" % (cfg['awesome_image'],tags_html, form_html, delete_js)

@app.route('/tags', methods=['POST'])
def add_tag():
    new_tag = request.form['tag-name']
    tag = Tag.where('tag', new_tag).first()
    if tag is None:
        tag = Tag.create(name=new_tag)

    return redirect('/')

@app.route('/tags/<tag>', methods=['DELETE'])
def remove_tag(tag):
    tag_to_remove = Tag.where('name', tag).first()
    if tag_to_remove is not None:
        tag_to_remove.delete()

    return '', 204  # No need to return any content, since Javascript will redirect anyway
