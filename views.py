import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.gzip import gzip_page
from .models import Event, Notice, Fellowship, FellowshipMessage
from .models import About, YearlyTheme, Sermon, Contact
from .models import Photo
from django.utils import timezone
from django.http import FileResponse
import os, datetime
from .utils import pager, get_query
from .browse import level1, level2
from .detail import detail_page
from .album import show_albums, show_photos

# Create your views here.

@gzip_page
def album(request, album = None):
    context = {}

    if not album:
        context.update(show_albums())
    else:
        context.update(show_photos(album))

    return render(request, "church/album.html", context)


@gzip_page
def browse(request, domain = None, catalog = None):
    '''
    domain = None
    domain = request.GET.get('domain')
    '''

    context = {}

    if not domain:
        context.update(level1())
    else:
        context.update(level2(request, domain, catalog))

    return render(request, "church/browse.html", context)

@gzip_page
def detail(request, domain = None, catalog = None, entry_id = None):
    context = dict()
    context.update(detail_page(request, domain, catalog, entry_id))

    if not context:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    return render(request, "church/detail.html", context)

@gzip_page
def index(request):
    events = Event.objects.filter(event_date__gte = timezone.now().date() - datetime.timedelta(days=1))
    notices = Notice.objects.filter(effective_date__gte = timezone.now().date() - datetime.timedelta(days=1))
    contacts = Contact.objects.all()[:1]
    themes = YearlyTheme.objects.all()[:1]
    abouts = About.objects.all()[:1]
    fellowships = Fellowship.objects.filter(display=True)
    sermon_list = Sermon.objects.all()[:100]
    photos = Photo.objects.filter(carousel=True)[:8]
    page = request.GET.get('page')
    sermons = pager(sermon_list, page)

    context = {
            'events': events,
            'notices': notices,
            'contacts': contacts,
            'themes': themes,
            'abouts': abouts,
            'fellowships': fellowships,
            'sermons': sermons,
            'photos': photos,
            }

    return render(request, 'church/index.html', context)
