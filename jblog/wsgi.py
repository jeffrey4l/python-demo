#-*- coding:utf-8 -*-
import sys

import bottle
from bottle import route

from conf import CFG, DB, get_logger

LOG=get_logger(__file__)


html='''<html><title></title><body>%s</body></html>'''

@route('/')
def hello():

    LOG.info('in the hello method')

    table = '<table>'
    for k in CFG:
        table +='<tr><td>%s</td><td>%s</td></tr>' % (k, CFG[k])
    table +='<tr><td>DB</td><td>%s</td></tr>' %  DB
    table += '</table>'
    LOG.error('I am going to out of hello method')
    return html % table


application = bottle.default_app()

if __name__ == '__main__':
    
    from wsgiref.simple_server import make_server
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 80
    httpd = make_server('', port, application)
    # Wait for a single request, serve it and quit.
    httpd.serve_forever()


