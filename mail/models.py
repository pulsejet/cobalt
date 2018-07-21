"""Models for bulk mails!"""
import time
from django.db import models
from django_tasker.decoration import queueable
from mail.mail import sendmail

class BulkMail(models.Model):
    """A single bulk mail request."""

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

    @queueable
    def send_mails(self, *args, **kwargs):
        for m in self.mails.all():
            print("Sending email to", m.email)

            # Sleep
            time.sleep(2)

            # Try to blast
            try:
                sendmail(m.data, m.bulk.from_email, m.email, m.bulk.subject)
            except Exception:
                m.failed = True

            # Mark sent
            m.sent = True
            m.save()

        # Mark campaign done
        self.in_progress = False
        self.completed = True
        self.save()

    def send(self):
        if not self.in_progress and not self.completed:
            self.in_progress = True
            self.save()
            self.send_mails.queue()
            return True
        else:
            return False

class Mail(models.Model):
    """A single queued email."""
    bulk = models.ForeignKey(BulkMail, on_delete=models.CASCADE, related_name='mails')
    email = models.EmailField()
    data = models.TextField(blank=True)
    sent = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)

    def __str__(self):
        return self.bulk.name + ' - ' + self.email
