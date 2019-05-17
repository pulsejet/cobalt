"""Models for bulk mails!"""
import uuid
from django.db import models
from django.contrib.auth.models import User
from renderer import get_log_mail

class Campaign(models.Model):
    """A single campaign that may contain multiple email."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time_of_creation = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    from_email = models.CharField(max_length=150)
    email_variable = models.CharField(max_length=150, default='email')
    in_progress = models.BooleanField(default=False)
    processing = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    template = models.TextField()
    csv = models.FileField(null=True)
    subject = models.CharField(max_length=150, default='')

    progress = 0

    def __str__(self):
        return self.name

class Mail(models.Model):
    """A single queued email."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time_of_creation = models.DateTimeField(auto_now_add=True)

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='mails')
    email = models.EmailField()
    data = models.TextField(blank=True)
    try_count = models.IntegerField(default=False)
    success = models.BooleanField(default=False)
    error = models.TextField(blank=True)

    def __str__(self):
        return self.campaign.name + ' - ' + self.email

class MailSentLog(models.Model):
    """A single email that has been sent."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time_of_creation = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=150, blank=True)
    campaign_name = models.CharField(max_length=150, blank=True)

    email = models.EmailField(blank=True)
    data = models.TextField(blank=True)

    def __str__(self):
        return self.campaign_name + ' - ' + self.email

    @staticmethod
    def log(mail: Mail, rendered: str) -> None:
        """Log using a Mail object and rendered mail."""

        data = get_log_mail(mail, rendered)

        MailSentLog.objects.create(
            username=mail.campaign.created_by.username, campaign_name=mail.campaign.name,
            email=mail.email, data=data)
