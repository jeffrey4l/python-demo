#-*- coding:utf-8 -*-
import sys

import bottle
from bottle import route


html='''<html><title></title><body>%s</body></html>'''

@route('/')
def hello():
    return html % '<h1>hello world</h1>'


application = bottle.default_app()

if __name__ == '__main__':
    
    from wsgiref.simple_server import make_server
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 80
    httpd = make_server('', port, application)
    # Wait for a single request, serve it and quit.
    httpd.serve_forever()


