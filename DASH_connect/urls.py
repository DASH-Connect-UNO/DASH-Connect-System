from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', views.home, name='home'),
    path('pillars/', include('DASH_pillars.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':
            settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root':
        settings.STATIC_ROOT}),
]
