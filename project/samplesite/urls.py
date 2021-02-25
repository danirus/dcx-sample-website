"""samplesite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views.i18n import JavaScriptCatalog

from samplesite import views


urlpatterns = [
    re_path(r'^$', views.home, name='homepage'),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
    re_path(r'^jsi18n/$', JavaScriptCatalog.as_view(),
            name='javascript-catalog'),
    re_path(r'^avatar/', include('avatar.urls')),
    re_path(r'^user/', include('users.urls')),
    re_path(r'admin/', admin.site.urls),

]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + staticfiles_urlpatterns()


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [re_path(r'^rosetta/', include('rosetta.urls'))]
