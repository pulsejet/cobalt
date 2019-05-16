from django.conf import settings
from django.db.models import Count
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from django.views.decorators.http import require_http_methods
import campaign.tasks as tasks
from campaign.models import Campaign, Mail
from campaign.forms import NewCampaignForm
from campaign.mail import test_auth

@login_required
def mail(request, form=None):
    queryset = Campaign.objects.all().order_by('-time_of_creation')
    queryset = annotate_campaign_queryset(queryset)

    for camp in queryset:
        annotate_campaign_progress(camp)

    context = {"campaigns": queryset, "form": form, "settings": settings}
    return render(request, 'default.html', context=context)

@login_required
def campaign_row(request, pk):
    """Single row of campaign HTML."""
    queryset = Campaign.objects.filter(id=pk)
    queryset = annotate_campaign_queryset(queryset)
    camp = queryset.first()
    annotate_campaign_progress(camp)
    context = {"camp": camp}
    return render(request, 'campaign_row.html', context=context)

def annotate_campaign_queryset(queryset):
    """Set annotations of queryset."""
    queryset = queryset.annotate(num_mails=Count('mails'))
    queryset = queryset.annotate(num_sent=Count('mails', filter=Q(mails__success=True)))
    return queryset

def annotate_campaign_progress(camp):
    """Set progess of campaign."""
    if camp.num_mails == 0:
        camp.progress = 0
    else:
        camp.progress = int((camp.num_sent / camp.num_mails) * 100)

@login_required
@require_http_methods(["POST"])
def start_send(request, pk):
    """Start sending a campaign."""

    username = request.POST['username']
    password = request.POST['password']
    if not test_auth(settings.SMTP_SERVER, settings.SMTP_PORT, username, password):
        return HttpResponse("Authentication failed!", status=401)

    camp = Campaign.objects.get(id=pk)
    if not camp.in_progress:
        camp.in_progress = True
        camp.save()
        tasks.send_campaign.delay(camp.id, username, password)
        return HttpResponseRedirect(reverse('default'))

    return HttpResponse("Job in progress!")

@login_required
@require_http_methods(["POST"])
def campaign(request):
    form = NewCampaignForm(request.POST, request.FILES)
    if form.is_valid():
        name = request.POST['name']
        from_email = request.POST['from_email']
        subject = request.POST['subject']
        template = request.POST['template']
        emailvar = request.POST['emailvar']

        # Create new campaign
        camp = Campaign.objects.create(
            name=name, from_email=from_email, template=template, subject=subject,
            csv=request.FILES['csv'], email_variable=emailvar)
        tasks.process_campaign.delay(camp.id)
    else:
        return mail(request, form=form)

    return HttpResponseRedirect(reverse('default'))

@login_required
def campaign_view(request, pk):
    queryset = Campaign.objects.get(id=pk)
    context = {"campaign": queryset, "settings": settings}
    return render(request, 'campaign.html', context=context)

@login_required
def preview(request, pk):
    queryset = Mail.objects.get(id=pk)
    return HttpResponse(tasks.cobalt_render(queryset.campaign.template, queryset.data))

@login_required
@require_http_methods(["POST"])
def campaign_del(request, pk):
    queryset = Campaign.objects.get(id=pk)
    queryset.delete()
    return HttpResponseRedirect(reverse('default'))

def cobalt_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('default'))
