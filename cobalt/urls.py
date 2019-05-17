"""cobalt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path
import campaign.views_campaign as views_campaign
import campaign.views_mail as views_mail
import views_other

admin.site.site_header = 'Cobalt Admin'
handler500 = 'views_ther.custom_500'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views_campaign.campaign_home, name='default'),
    path('campaign-row/<pk>', views_campaign.campaign_row),
    path('send/<pk>', views_campaign.campaign_send),
    path('campaign', views_campaign.campaign_create),
    path('campaign/<pk>', views_campaign.campaign_get),
    path('del-campaign/<pk>', views_campaign.campaign_destroy),

    path('preview/<pk>', views_mail.mail_preview),

    path('accounts/login/', LoginView.as_view(template_name='login.html')),
    path('signout', views_other.cobalt_logout),
]
