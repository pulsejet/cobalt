from __future__ import absolute_import, unicode_literals
import io
import smtplib
import random
import csv
import json
from celery import shared_task
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from campaign.models import Campaign
from campaign.models import Mail

def cobalt_render(template, valjson):
    """Render a template to the email."""

    # Convert json to dict
    values = json.loads(valjson)

    # Variable substitution
    for col in values:
        template = template.replace('{{' + col + '}}', values[col])

    return template


def send_mail(mail, template):
    """Try to send the mail with a new connection."""

    # Open a new SMTP connection
    #server = get_connection('smtp-auth.iitb.ac.in', 25, 'mlc', '')

    # Try to send, store error otherwise
    try:
        data = cobalt_render(template, mail.data)
        #sendmail(server, self.data, self.campaign.from_email, self.email, self.campaign.subject)
        mail.success = random.randint(0, 10) > 3
        mail.error = ''
    except smtplib.SMTPException as smtp_exception:
        mail.error = str(smtp_exception)

    # Close the connection
    #close_connection(server)

    # Increment try count and save
    mail.try_count += 1
    mail.save()

@shared_task
def process_campaign(cid):
    """Create mails from a campaign."""

    camp = Campaign.objects.get(id=cid)

    data = camp.csv.read().decode('utf-8')
    rows = list(csv.DictReader(io.StringIO(data)))
    emvar = camp.email_variable

    for row in rows:
        # Check validity of email
        if emvar not in row or not row[emvar]:
            continue
        try:
            validate_email(row[emvar])
        except ValidationError:
            continue

        # Create object
        Mail.objects.create(campaign=camp, email=row[emvar], data=json.dumps(row))

    camp.processing = False
    camp.save()

@shared_task
def send_campaign(cid):
    """Send mails from a campaign."""

    camp = Campaign.objects.get(id=cid)
    try:
        for mail in camp.mails.filter(success=False):
            send_mail(mail, camp.template)
    finally:
        camp.in_progress = False
        camp.completed = True
        camp.save()
