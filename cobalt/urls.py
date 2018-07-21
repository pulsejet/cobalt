"""cobalt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib.auth.views import login
from django.urls import path
import mail.views as mail_views

urlpatterns = [
    path('cobalt/admin/', admin.site.urls),
    path('cobalt/mail/', mail_views.mail),
    path('cobalt/mail/send/<pk>', mail_views.start_send),
    path('cobalt/mail/campaign', mail_views.campaign),
    path('cobalt/mail/campaign/<pk>', mail_views.campaign_view),
    path('cobalt/mail/del-campaign/<pk>', mail_views.campaign_del),
    path('cobalt/mail/preview/<pk>', mail_views.preview),
    path('cobalt/accounts/login/', login, {'template_name': 'admin/login.html'}),
    path('cobalt/', mail_views.mail),
]
