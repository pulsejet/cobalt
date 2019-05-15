from __future__ import absolute_import, unicode_literals
import io
import smtplib
import csv
from celery import shared_task
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from campaign.models import Campaign
from campaign.models import Mail

@shared_task
def send_mail(mail):
    """Try to send the mail with a new connection."""
    mail = Mail.objects.get(id=mail)

    # Open a new SMTP connection
    #server = get_connection('smtp-auth.iitb.ac.in', 25, 'mlc', '')

    # Try to send, store error otherwise
    try:
        print('SENT MAIL ' + str(mail.email))
        #sendmail(server, self.data, self.campaign.from_email, self.email, self.campaign.subject)
        mail.success = True
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
    for row in rows:
        # Check validity of email
        if 'email' not in row or not row['email']:
            continue
        try:
            validate_email(row['email'])
        except ValidationError:
            continue

        # Put in values
        body = str(camp.template)
        for col in row:
            body = body.replace('{{' + col + '}}', row[col])

        # Create object
        Mail.objects.create(campaign=camp, email=row['email'], data=body)

    camp.processing = False
    camp.save()
