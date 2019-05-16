"""Models for bulk mails!"""
import uuid
from django.db import models
# from campaign.mail import sendmail
# from campaign.mail import get_connection
# from campaign.mail import close_connection

class Campaign(models.Model):
    """A single campaign that may contain multiple email."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time_of_creation = models.DateTimeField(auto_now_add=True)

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
