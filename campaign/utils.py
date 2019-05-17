"""Misc utilities, some important ones."""
import smtplib
from django.conf import settings
from django.db.models import QuerySet
from django.db.models import Count
from django.db.models import Q
from campaign.models import Campaign
from campaign.models import Mail
from campaign.models import MailSentLog
from campaign.mail import send_html_mail
from campaign.mail import get_connection
from campaign.mail import close_connection
from renderer import cobalt_render
from renderer import get_log_mail

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

def annotate_campaign_progress(campaign: Campaign) -> None:
    """Set progess of campaign."""
    if campaign.num_mails == 0:
        campaign.progress = 0
    else:
        campaign.progress = int((campaign.num_sent / campaign.num_mails) * 100)

def notify_campaign_created(campaign: Campaign) -> None:
    """Notify the user of campaign creation."""

    # Check if we want to notify people
    if not settings.COBALT_USER:
        return

    # Open a new SMTP connection
    server: smtplib.SMTP
    try:
        server = get_connection(
            settings.SMTP_SERVER, settings.SMTP_PORT,
            settings.COBALT_USER, settings.COBALT_PASS
        )
    except smtplib.SMTPException:
        return

    # Render the first mail object
    mail = campaign.mails.first()
    if not mail:
        return
    data = get_log_mail(mail, cobalt_render(mail.campaign.template, mail.data))

    # Send creation email
    try:
        send_html_mail(
            server, data, settings.COBALT_EMAIL,
            mail.campaign.created_by.email,
            'Your campaign %s was created successfully' % campaign.name
        )
    finally:
        close_connection(server)
