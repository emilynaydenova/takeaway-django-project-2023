from django.http import HttpResponse, Http404
from django.shortcuts import render


def handle_exception(get_response):
    def middleware(request):
        response = get_response(request)
        if response.status_code >= 500:
            # show views
            return render(request,"errors/500.html")
        elif response.status_code >= 400:
            # show views
            return Http404()

    return middleware


# add in settings - MIDDLEWARE - at last line

"""
400 - Bad Request
404 - Not Found
403 - Forbidden
"""
