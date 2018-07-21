import io
import csv
from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_http_methods
from mail.models import BulkMail, Mail
from .forms import NewCampaignForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def mail(request):
    context = {"bulks": BulkMail.objects.all()}
    return render(request, 'mail.html', context=context)

@require_http_methods(["POST"])
def start_send(request, pk):
    camp = BulkMail.objects.get(id=pk)
    if camp.send():
        return mail(request)
    else:
        return HttpResponse("Job already done!")

@require_http_methods(["POST"])
def campaign(request):
    form = NewCampaignForm(request.POST, request.FILES)
    if form.is_valid():
        name = request.POST['name']
        from_email = request.POST['from_email']
        subject = request.POST['subject']
        template = request.POST['template']

        # Create new campaign
        camp = BulkMail.objects.create(
            name=name, from_email=from_email, template=template, subject=subject)

        # Set description if valid
        if "description" in request.POST and request.POST['description'] != "":
            camp.description = request.POST['description']

        # Save
        camp.save()

        # Create mails
        data = request.FILES['csv'].read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(data))
        rows = [row for row in reader]
        for row in rows:
            # Check validity of email
            if 'email' not in row or not row['email']:
                continue
            try:
                validate_email(row['email'])
            except ValidationError as e:
                continue

            # Put in values
            body = str(template)
            for col in row:
                body = body.replace('{{' + col + '}}', row[col])

            # Create object
            Mail.objects.create(bulk=camp, email=row['email'], data=body)

    else:
        context = {"bulks": BulkMail.objects.all(), "form": form}
        return render(request, 'mail.html', context=context)

    return mail(request)
