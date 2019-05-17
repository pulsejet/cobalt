"""Misc utilities, some important ones."""
import smtplib
from django.db.models import QuerySet
from django.db.models import Count
from django.db.models import Q
from campaign.models import Campaign
from campaign.models import Mail
from campaign.models import MailSentLog
from campaign.mail import send_html_mail
from renderer import cobalt_render

def send_mail_object(server: smtplib.SMTP, mail: Mail) -> None:
    """Try to send a Mail object with a connection."""

    # Try to send, store error otherwise
    try:
        data = cobalt_render(mail.campaign.template, mail.data)

        send_html_mail(
            server, data, mail.campaign.from_email,
            mail.email, mail.campaign.subject
        )

        MailSentLog.log(mail, data)
        mail.success = True
        mail.error = str()
    except smtplib.SMTPException as smtp_exception:
        mail.error = str(smtp_exception)

    # Increment try count and save
    mail.try_count += 1
    mail.save()

def annotate_campaign_queryset(queryset: QuerySet) -> QuerySet:
    """Set annotations of queryset."""
    queryset = queryset.annotate(num_mails=Count('mails'))
    queryset = queryset.annotate(num_sent=Count('mails', filter=Q(mails__success=True)))
    return queryset

def annotate_campaign_progress(campaign: Campaign):
    """Set progess of campaign."""
    if campaign.num_mails == 0:
        campaign.progress = 0
    else:
        campaign.progress = int((campaign.num_sent / campaign.num_mails) * 100)
