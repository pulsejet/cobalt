"""Views for campaign objects."""
from typing import List
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from django.views.decorators.http import require_http_methods
import campaign.tasks as tasks
from campaign.models import Campaign
from campaign.models import Mail
from campaign.forms import NewCampaignForm
from campaign.mail import test_auth
from campaign.utils import annotate_campaign_progress
from campaign.utils import annotate_campaign_queryset
from views_other import error

@login_required
def campaign_home(request: HttpRequest, form: NewCampaignForm = None) -> HttpResponse:
    """Default view."""
    queryset = Campaign.objects.filter(created_by=request.user).order_by('-time_of_creation')
    queryset = annotate_campaign_queryset(queryset)

    for camp in queryset:
        annotate_campaign_progress(camp)

    context = {"campaigns": queryset, "form": form, "settings": settings}
    return render(request, 'default.html', context=context)


@login_required
@require_http_methods(["POST"])
def campaign_create(request: HttpRequest) -> HttpResponse:
    """Create a new campaign from POST."""

    form = NewCampaignForm(request.POST, request.FILES)
    if form.is_valid():
        # Get all fields
        name = request.POST['name']
        from_email = request.POST['from_email']
        subject = request.POST['subject']
        template = request.POST['template']
        emailvar = request.POST['emailvar']
        mailtrack = 'mailtrack' in request.POST

        # Construct bcc string
        bcc = list()
        if 'bcc_user' in request.POST:
            bcc.append(request.user.email)
        if 'bcc_from' in request.POST:
            bcc.append(from_email)
        bcc = ', '.join(bcc)

        # Create new campaign
        camp = Campaign.objects.create(
            name=name, from_email=from_email, template=template, subject=subject,
            csv=request.FILES['csv'], email_variable=emailvar, created_by=request.user,
            mailtrack=mailtrack, bcc=bcc)
        tasks.process_campaign.delay(camp.id)
    else:
        return campaign_home(request, form=form)

    return HttpResponseRedirect(reverse('default'))

@login_required
def campaign_get(request: HttpRequest, pk: str) -> HttpResponse:
    """View for a single campaign."""

    camp: Campaign = Campaign.objects.get(id=pk, created_by=request.user)
    mails: List[Mail] = camp.mails.order_by('success')
    context = {"campaign": camp, "settings": settings, "mails": mails}
    return render(request, 'campaign.html', context=context)


@login_required
@require_http_methods(["POST"])
def campaign_destroy(request: HttpRequest, pk: str) -> HttpResponse:
    """Delete a campaign."""

    queryset: Campaign = Campaign.objects.get(id=pk, created_by=request.user)
    queryset.delete()
    return HttpResponseRedirect(reverse('default'))


@login_required
@require_http_methods(["POST"])
def campaign_send(request: HttpRequest, pk: str) -> HttpResponse:
    """Start sending a campaign."""

    username: str = request.POST['username']
    password: str = request.POST['password']
    auth_err: str = test_auth(settings.SMTP_SERVER, settings.SMTP_PORT, username, password)
    if auth_err:
        return error(request, auth_err, 401)

    camp: Campaign = Campaign.objects.get(id=pk, created_by=request.user)
    if not camp.in_progress:
        camp.in_progress = True
        camp.save()
        tasks.send_campaign.delay(camp.id, username, password)
        return HttpResponseRedirect(reverse('default'))

    return error(request, 'Cannot start a job currently in progress', 401)


@login_required
def campaign_row(request: HttpRequest, pk: str) -> HttpResponse:
    """Single row of campaign HTML."""

    queryset = Campaign.objects.filter(id=pk, created_by=request.user)
    queryset = annotate_campaign_queryset(queryset)
    camp: Campaign = queryset.first()

    if not camp:
        return error(request, '404 Not Found')

    annotate_campaign_progress(camp)
    context = {"camp": camp}
    return render(request, 'campaign_row.html', context=context)
