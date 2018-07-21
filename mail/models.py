"""Models for bulk mails!"""
from uuid import uuid4
from django.db import models

class BulkMail(models.Model):
    """A single bulk mail request."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    time_of_creation = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    from_email = models.EmailField()
    in_progress = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    template = models.TextField()
    subject = models.CharField(max_length=150, default="")

    def __str__(self):
        return self.name

class Mail(models.Model):
    """A single queued email."""
    bulk = models.ForeignKey(BulkMail, on_delete=models.CASCADE, related_name='mails')
    email = models.EmailField()
    data = models.TextField(blank=True)
    sent = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)

    def __str__(self):
        return self.bulk.name + ' - ' + self.email
