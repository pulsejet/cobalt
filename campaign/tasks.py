from __future__ import absolute_import, unicode_literals
import io
import smtplib
import csv
import json
from celery import shared_task
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings
from campaign.models import Campaign
from campaign.models import Mail
from campaign.mail import get_connection
from campaign.mail import close_connection
from campaign.mail import sendmail

def cobalt_render(template, valjson):
    """Render a template to the email."""

    # Convert json to dict
    values = json.loads(valjson)

    # Variable substitution
    for col in values:
        template = template.replace('{{' + col + '}}', values[col])

    return template


def send_mail(server, mail):
    """Try to send the mail with a connection."""

    # Try to send, store error otherwise
    try:
        data = cobalt_render(mail.campaign.template, mail.data)
        sendmail(server, data, mail.campaign.from_email, mail.email, mail.campaign.subject)
        mail.success = True
        mail.error = ''
    except smtplib.SMTPException as smtp_exception:
        mail.error = str(smtp_exception)

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
def send_campaign(cid, user, passw):
    """Send mails from a campaign."""

    # Open a new SMTP connection
    try:
        server = get_connection(settings.SMTP_SERVER, settings.SMTP_PORT, user, passw)
    except smtplib.SMTPException:
        return

    # Get the campaign
    camp = Campaign.objects.get(id=cid)

    # Send all remaining emails
    try:
        for mail in camp.mails.filter(success=False):
            send_mail(server, mail)
    finally:
        # Clean up and mark done
        close_connection(server)
        camp.in_progress = False
        camp.completed = True
        camp.save()
