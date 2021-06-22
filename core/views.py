from django.http import HttpResponse
from core.jsonrpc import Qualix


def auth_check(request):
    qualix = Qualix()
    data = qualix.auth_check()
    return HttpResponse(data)