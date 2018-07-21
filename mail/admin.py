from django.contrib import admin
from mail.models import BulkMail
from mail.models import Mail

admin.site.register(BulkMail)
admin.site.register(Mail)
