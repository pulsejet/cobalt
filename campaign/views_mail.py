"""Views for Mail objects."""
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import HttpResponse
from campaign.models import Mail
from renderer import cobalt_render

@login_required
def mail_preview(request: HttpRequest, pk: str) -> HttpResponse:
    """Render a mail and send the response as raw HTML."""
    queryset: Mail = Mail.objects.get(id=pk, campaign__created_by=request.user)
    return HttpResponse(cobalt_render(queryset.campaign.template, queryset.data))
