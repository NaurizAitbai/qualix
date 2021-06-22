from django.http import JsonResponse, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from core.jsonrpc import Qualix


def auth_check(request):
    qualix = Qualix()

    try:
        data = qualix.auth_check()
        return JsonResponse(data)
    except PermissionDenied:
        return HttpResponseForbidden()