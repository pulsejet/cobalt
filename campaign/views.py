from django.db.models import Count
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from django.views.decorators.http import require_http_methods
import campaign.tasks as tasks
from campaign.models import Campaign, Mail
from campaign.forms import NewCampaignForm

@login_required
def mail(request, form=None):
    queryset = Campaign.objects.all().order_by('-time_of_creation')
    queryset = queryset.annotate(num_mails=Count('mails'))
    queryset = queryset.annotate(num_sent=Count('mails', filter=Q(mails__success=True)))

    for camp in queryset:
        # Check for no mail
        if camp.num_mails == 0:
            camp.progress = 0
        else:
            camp.progress = int((camp.num_sent / camp.num_mails) * 100)

    context = {"campaigns": queryset, "form": form}
    return render(request, 'mail.html', context=context)

@login_required
@require_http_methods(["POST"])
def start_send(request, pk):
    camp = Campaign.objects.get(id=pk)
    if not camp.in_progress:
        camp.in_progress = True
        camp.save()
        for mid in camp.mails.values_list('id', flat=True):
            tasks.send_mail.delay(mid)
        return HttpResponseRedirect(reverse('default'))

    return HttpResponse("Job already started!")

@login_required
@require_http_methods(["POST"])
def campaign(request):
    form = NewCampaignForm(request.POST, request.FILES)
    if form.is_valid():
        name = request.POST['name']
        from_email = request.POST['from_email']
        subject = request.POST['subject']
        template = request.POST['template']

        # Create new campaign
        camp = Campaign.objects.create(
            name=name, from_email=from_email, template=template, subject=subject, csv=request.FILES['csv'])
        tasks.process_campaign.delay(camp.id)
    else:
        return mail(request, form=form)

    return HttpResponseRedirect(reverse('default'))

@login_required
def campaign_view(request, pk):
    queryset = Campaign.objects.get(id=pk)
    context = {"campaign": queryset}
    return render(request, 'campaign.html', context=context)

@login_required
def preview(request, pk):
    queryset = Mail.objects.get(id=pk)
    return HttpResponse(queryset.data)

@login_required
@require_http_methods(["POST"])
def campaign_del(request, pk):
    queryset = Campaign.objects.get(id=pk)
    queryset.delete()
    return HttpResponseRedirect(reverse('default'))
