# add in settings - MIDDLEWARE - as a last line

from django.shortcuts import render
from django.http import HttpResponseServerError
import logging

class DisplayErrorMessageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 500:
            return render(request, 'errors/500.html', {'path': request.path})
        # 400 - Bad Request
        elif response.status_code == 400:
            return render(request, 'errors/400.html', {'path': request.path})
        # 403 - Forbidden
        elif response.status_code == 403:
            return render(request, 'errors/403.html', {'path': request.path})
        # 404 - Not Found
        elif response.status_code == 404:
            return render(request, 'errors/404.html', {'path': request.path})

        return response

"""
This middleware catches any unhandled exceptions that occur while processing the request 
and returns a simple error message instead of the standard Django error page. 
"""
class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            response = HttpResponseServerError("Oops! Something went wrong.")
        return response



class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logging.info(f"Incoming request: {request.method} {request.path}")
        response = self.get_response(request)
        logging.info(f"Outgoing response: {response.status_code}")
        return response