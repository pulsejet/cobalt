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
from django.urls import path
import mail.views as mail_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mail/', mail_views.mail),
    path('mail/send/<pk>', mail_views.start_send),
    path('mail/campaign', mail_views.campaign),
    path('mail/campaign/<pk>', mail_views.campaign_view),
    path('mail/preview/<pk>', mail_views.preview),
]
