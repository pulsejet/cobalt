from django.contrib import admin
from campaign.models import Campaign
from campaign.models import Mail

class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'from_email', 'created_by', 'mail_count', 'time_of_creation')
    list_filter = ('created_by', 'time_of_creation')
    ordering = ('-time_of_creation',)
    def mail_count(self, obj):
        return '%d (%d)' % (obj.mails.count(), obj.mails.filter(success=True).count())
    mail_count.short_description = "Mails"

class MailAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'email', 'success', 'time_of_creation')
    list_filter = ('campaign__created_by', 'success', 'time_of_creation')
    ordering = ('-time_of_creation',)

admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Mail, MailAdmin)
