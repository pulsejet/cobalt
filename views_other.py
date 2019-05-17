"""Misc views for error, login etc."""
import sys
from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpRequest
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse

def custom_500(request: HttpRequest) -> HttpResponse:
    """Custom internal server error page."""
    value = sys.exc_info()[1]
    return error(request, value)

def error(request: HttpRequest, message: str, status: int = 400) -> HttpResponse:
    """Return an error."""
    context = {"error": str(message), "settings": settings}
    return render(request, 'error.html', context=context, status=status)

def cobalt_logout(request: HttpRequest) -> HttpResponse:
    """Logout current user."""
    logout(request)
    return HttpResponseRedirect(reverse('default'))
