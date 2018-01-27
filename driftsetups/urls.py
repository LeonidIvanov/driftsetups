"""driftsetups URL Configuration

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
from django.contrib import admin
from django.views.generic import TemplateView
from home.views import SitemapXmlView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^c/', include('car.urls')),
    url(r'^s/', include('setup.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^', include('home.urls')),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^sitemap\.xml/$', SitemapXmlView.as_view()),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
