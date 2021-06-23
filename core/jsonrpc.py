import ssl
import json
import urllib.request
import tempfile
from django.conf import settings
from django.core.exceptions import PermissionDenied


class Qualix:
    def __init__(self):
        self.base_url = settings.QUALIX_BASEURL
        self.crt = settings.QUALIX_CRT
        self.key = settings.QUALIX_KEY

        crt_file = tempfile.NamedTemporaryFile(mode='wt')
        key_file = tempfile.NamedTemporaryFile(mode='wt')
        crt_file.write(self.crt)
        key_file.write(self.key)
        crt_file.flush()
        key_file.flush()

        self.context = ssl.create_default_context()
        self.context.load_cert_chain(crt_file.name, key_file.name)

        crt_file.close()
        key_file.close()

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

        request = urllib.request.Request(self.base_url, data, headers=headers, method='POST')
        response = urllib.request.urlopen(request, context=self.context)

        data = json.loads(response.read())
        print(data)

        if 'error' in data:
            error_code = data['error']['code']
            message = data['error']['message']

            if error_code == 1:
                raise PermissionDenied(message)

        return data
    
    def auth_check(self):
        data = self.run_method('auth.check', 1, None)
        return data