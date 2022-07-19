from flask import Flask, Response
from markupsafe import escape
from os.path import abspath, exists

app = Flask(__name__)

@app.route('/')
def root_path():
    return Response(open(abspath('index.html')))

@app.route('/<path:subpath>')
def server_route(subpath):
    orig_path = subpath

    # Removes special characters from URL
    new_path = ''
    remove = ['\'', '\"'] # Pretend that more characters are added
    for i in range(len(orig_path)):
        char = orig_path[i]
        if char not in remove:
            new_path = f'{new_path}{char}'
    orig_path = new_path

    path = orig_path

    def get_path():
        return abspath(path)

    def f_exists():
        return exists(get_path())

    # Checks different URL patterns
    while True:
        # Plain URL
        if f_exists():
            break
        # HTML file
        path = f'{orig_path}.html'
        if f_exists():
            break
        # Index file
        path = f'{orig_path}/index.html'
        if f_exists():
            break
        # File does not exists
        return f'File {get_path()} does not exists'
        
    f = open(get_path())

    return Response(f)

