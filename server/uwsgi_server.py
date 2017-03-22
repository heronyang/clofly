import re

import logging
import logstash
import sys
import datetime

from urllib2 import Request, urlopen
from node_simple_function_manager import FunctionManager

FID_LENGTH  = 16
LOG_HOST    = 'log.clofly.com'

def application(env, start_response):

    start_time = datetime.datetime.now()

    try:
        fid = get_fid(env['REQUEST_URI'])
    except Exception as error:
        start_response('440 Not found',
                       [('Content-Type','text/plain')])
        return ['Error: ' + str(error)]

    # load
    fm = FunctionManager()

    print 'Running fid: ' + fid
    try:
        directory = fm.load(fid)
    except Exception as error:
        start_response('500 Internal Server Error',
                       [('Content-Type','text/plain')])
        return ['Error: ' + str(error)]

    print 'Loaded time took: ', datetime.datetime.now() - start_time

    # run
    port, uf_process = fm.run(fid, directory)

    # forward requests to port
    try:
        uf_response = forward_request(port, env)
    except Exception as error:
        start_response('500 Internal Server Error',
                       [('Content-Type','text/plain')])
        return ['Error: ' + str(error)]

    print 'Startup time took: ', datetime.datetime.now() - start_time

    # stop
    # TODO: we may want to deinitializing the task after returned
    fm.stop(uf_process, directory)
    print 'Stop time took: ', datetime.datetime.now() - start_time

    start_response('200 OK', [('Content-Type','text/plain')])

    end_time = datetime.datetime.now()
    log_request(fid, (end_time - start_time).microseconds, env)

    return [uf_response]

def forward_request(port, env):

    url = 'http://localhost:' + str(port) + '/'
    request = Request(url, headers = env)
    response = urlopen(request)
    return response.read()

def get_fid(request_uri):

    m = re.match('^(/[A-Za-z0-9\-\_]+){2,3}$', request_uri)
    if m == None:
        raise Exception('Invalid fid in url')
    return m.group(0)[1:]   # remove first char '/'

def log_request(fid, duration, env):

    logger = logging.getLogger('traffic')
    logger.setLevel(logging.INFO)
    logger.addHandler(logstash.LogstashHandler(LOG_HOST, 5000, version=1, message_type=fid))

    extra = {
        'duration': duration,
        'env': str(env)
    }
    logger.info('request', extra=extra)
