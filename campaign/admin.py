from django.contrib import admin
from django.utils.safestring import mark_safe
from campaign.models import Campaign
from campaign.models import Mail
from campaign.models import MailSentLog

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

class MailSentLogAdmin(admin.ModelAdmin):
    list_display = ('campaign_name', 'email', 'time_of_creation', 'username')
    list_filter = ('username', 'time_of_creation')
    ordering = ('-time_of_creation',)
    readonly_fields = ('username', 'email', 'campaign_name', 'data_html', 'data')

    def data_html(self, obj):
        return mark_safe(obj.data)
    data_html.short_description = "Data HTML"

admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Mail, MailAdmin)
admin.site.register(MailSentLog, MailSentLogAdmin)
