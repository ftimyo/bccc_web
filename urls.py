from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^browse', views.browse, name='browse'),
    url(r'^detail', views.detail, name='detail'),
    url(r'^album$', views.album, name='album'),
    url(r'^album/(?P<album>[0-9]+)$', views.album, name='album'),
    url(r'^$', views.index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
