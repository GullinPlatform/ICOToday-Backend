"""ICOToday URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static
from django.contrib import admin
import debug_toolbar
from django.conf import settings

from .apps.accounts import urls as account_urls
from .apps.companies import urls as company_urls
from .apps.conversation import urls as message_urls
from .apps.projects import urls as project_urls
from .apps.feeds import urls as feed_urls
from .apps.notifications import urls as notification_urls
from .apps.wallets import urls as wallet_urls

urlpatterns = [
	url(r'^6y07cs0yq9/', admin.site.urls),
	url(r'^ac/', include(account_urls)),
	url(r'^cp/', include(company_urls)),
	url(r'^ms/', include(message_urls)),
	url(r'^fd/', include(feed_urls)),
	url(r'^nt/', include(notification_urls)),
	url(r'^pj/', include(project_urls)),
	url(r'^wl/', include(wallet_urls)),
]

if settings.DEBUG:
	urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
