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
import campaign.views as mail_views

admin.site.site_header = 'Cobalt Admin'
handler500 = 'campaign.views.custom_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mail_views.mail, name='default'),
    path('campaign-row/<pk>', mail_views.campaign_row),
    path('send/<pk>', mail_views.start_send),
    path('campaign', mail_views.campaign),
    path('campaign/<pk>', mail_views.campaign_view),
    path('del-campaign/<pk>', mail_views.campaign_del),
    path('preview/<pk>', mail_views.preview),
    path('accounts/login/', LoginView.as_view(template_name='login.html')),
    path('signout', mail_views.cobalt_logout),
]
