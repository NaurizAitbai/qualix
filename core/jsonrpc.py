import ssl
import json
import urllib.request
from django.conf import settings



class Qualix:
    def __init__(self):
        self.base_url = settings.QUALIX_BASEURL
        self.crt = settings.QUALIX_CRT
        self.key = settings.QUALIX_KEY

    def run_method(self, method, id, data=None):
        if not data:
            data = {}

        data = dict({
            'jsonrpc': '2.0',
            'method': method,
            'id': id,
        }, **data)

        headers = {
            'Content-Type': 'application/json'
        }

        data = json.dumps(data).encode(encoding='utf-8')

        context = ssl.create_default_context()
        context.load_cert_chain(settings.QUALIX_CRT, settings.QUALIX_KEY)

        request = urllib.request.Request(self.base_url, data, headers=headers, method='POST')
        response = urllib.request.urlopen(request, context=context)

        data = response.read()

        return data
    
    def auth_check(self):
        data = self.run_method('auth.check', 1, None)
        return data