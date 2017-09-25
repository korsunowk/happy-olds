"""happy_olds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from boarding_visit.views import CalendarPageView
from happy_olds.utils import generate_fake_data


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', CalendarPageView.as_view(), name='home_page'),
    url(r'generate/$', generate_fake_data, name='generate_fake_date')
]

admin.AdminSite.site_header = 'Happy Olds administration'
admin.AdminSite.site_title = 'Happy Olds admin'
admin.AdminSite.index_title = 'Happy Olds project'
