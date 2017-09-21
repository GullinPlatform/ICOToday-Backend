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
from .apps.projects import urls as post_urls
from .apps.feeds import urls as discussion_urls
from .apps.notifications import urls as notification_urls
from .apps.wallets import urls as wallet_urls

urlpatterns = [
	url(r'^6y07cs0yq9/', admin.site.urls),
	url(r'^account/', include(account_urls)),
	url(r'^discussion/', include(discussion_urls)),
	url(r'^post/', include(post_urls)),
	url(r'^notification/', include(notification_urls)),
	url(r'^wallet/', include(wallet_urls)),

]

if settings.DEBUG:
	# static files (images, css, javascript, etc.)
	urlpatterns += staticfiles_urlpatterns()
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
