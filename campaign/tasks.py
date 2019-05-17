"""Celery tasks to process in background."""
from __future__ import absolute_import, unicode_literals
import csv
import io
import json
import time
import smtplib

import chardet
from celery import shared_task
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings
from campaign.models import Campaign
from campaign.models import Mail
from campaign.mail import get_connection
from campaign.mail import close_connection
from campaign.utils import send_mail_object

@shared_task
def process_campaign(cid: str) -> None:
    """Create mails from a campaign."""

    camp: Campaign = Campaign.objects.get(id=cid)

    # Read raw bytes
    data = camp.csv.read()

    # Detect encoding and decode
    encoding = chardet.detect(data)
    if 'encoding' in encoding:
        encoding = encoding['encoding']
    else:
        encoding = 'utf-8'
    data: str = data.decode(encoding)

    # Get rows of data
    rows = list(csv.DictReader(io.StringIO(data)))
    emvar: str = camp.email_variable

    # Create record for each row
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
def send_campaign(cid: str, username: str, password: str) -> None:
    """Send mails from a campaign."""

    # Open a new SMTP connection
    server: smtplib.SMTP
    try:
        server = get_connection(settings.SMTP_SERVER, settings.SMTP_PORT, username, password)
    except smtplib.SMTPException:
        return

    # Get the campaign
    camp: Campaign = Campaign.objects.get(id=cid)

    # Send all remaining emails
    mail: Mail
    try:
        for mail in camp.mails.filter(success=False):
            time.sleep(0.1)
            send_mail_object(server, mail)
    finally:
        # Clean up and mark done
        close_connection(server)
        camp.in_progress = False
        camp.completed = True
        camp.save()
