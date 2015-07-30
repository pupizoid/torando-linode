import sys
import json

from pprintpp import pprint
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado import gen

API_KEY = 'secretkey'

ERR_CODE = {
    0: 'ok',
    1: 'Bad Request',
    3: 'The requested class does not exist',
    4: 'Authentication failed',
    5: 'Object not found',
    6: 'A required property is missing for this action',
    7: 'Property is invalid',
    8: 'A data validation error has occured',
    9: 'Method Not Implemented',
    10: 'Too many batched requests',
    11: 'RequestArray isn\'t valid JSON or WDDX',
    12: 'Batch approaching timeout. Stopping here',
    13: 'Permission denied',
    14: 'API rate limit exceeded',
    30: 'Charging the credit card failed',
    31: 'Credit card expired',
    40: 'Limit of Linodes added per hour reached',
    41: 'Linode must have no disks before delete'
}


class LinodeCommand(object):
    def __init__(self):
        self.api_url = 'https://api.linode.com/?api_key={}'.format(API_KEY)

    @gen.coroutine
    def execute(self, command, **kwargs):
        client = AsyncHTTPClient()
        request = yield client.fetch(
            self.api_url + '&api_action=%s' % command + ''.join(
                '&{0}={1}'.format(*pair) for pair in kwargs.items()
            )
        )
        response = None
        if request.code == 200:
            response = json.loads(request.body)
        else:
            pprint('Error while processing request')
        if response['DATA']:
            raise gen.Return(response['DATA'])
        else:
            for error_array in response['ERRORARRAY']:
                pprint(
                    ERR_CODE.get(
                        error_array['ERRORCODE'],
                        error_array['ERRORMESSAGE']
                    )
                )


if __name__ == '__main__':
    l = LinodeCommand()
    print IOLoop.current().run_sync(lambda: l.execute(sys.argv[1]))