"""Views for Mail objects."""
import base64
import smtplib
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django.http import HttpRequest
from django.shortcuts import HttpResponse, HttpResponseRedirect, reverse
from campaign.mail import get_connection
from campaign.mail import close_connection
from campaign.models import Mail
from campaign.utils import send_mail_object
from renderer import cobalt_render

PIXEL_GIF_DATA = base64.b64decode(b"R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")

@login_required
def mail_preview(request: HttpRequest, pk: str) -> HttpResponse:
    """Render a mail and send the response as raw HTML."""
    queryset: Mail = Mail.objects.get(id=pk, campaign__created_by=request.user)
    return HttpResponse(cobalt_render(queryset.campaign.template, queryset.data))

@login_required
@require_http_methods(["POST"])
def mail_send(request: HttpRequest, pk: str) -> HttpResponse:
    """(Re)send a single email synchronously."""

    username: str = request.POST['username']
    password: str = request.POST['password']
    server: smtplib.SMTP = get_connection(settings.SMTP_SERVER, settings.SMTP_PORT, username, password)
    mail: Mail = Mail.objects.get(id=pk, campaign__created_by=request.user)
    send_mail_object(server, mail)
    close_connection(server)

    return HttpResponseRedirect(reverse('campaign', args=[mail.campaign.id]))

@never_cache
def mail_track(request: HttpRequest, pk: str) -> HttpResponse:
    """Returns a blank pixel and increments read count."""

    # Increment read count
    mail: Mail = Mail.objects.filter(id=pk).first()
    if mail:
        mail.read_count += 1
        mail.save()

    # Return blank pixel
    return HttpResponse(PIXEL_GIF_DATA, content_type='image/gif')
