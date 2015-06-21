from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.gzip import gzip_page
from .models import Event, Notice, Fellowship, FellowshipMessage
from .models import About, YearlyTheme, Sermon, Contact
from .models import Photo
from django.utils import timezone
from django.http import FileResponse
import os, datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .search import get_query
from .browse import level1, level2
from .detail import detail_page

# Create your views here.

@gzip_page
def browse(request):
    context = dict()
    domain = request.GET.get('domain')
    catalog = request.GET.get('catalog')
    if not domain:
        context.update(level1())
    else:
        context.update(level2(domain, catalog))

    return render(request, "church/browse.html", context)

@gzip_page
def search(request):
    return render(request, "church/search.html", {})

@gzip_page
def detail(request):
    context = dict()
    domain = request.GET.get('domain')
    catalog = request.GET.get('catalog')
    entry_id = request.GET.get('entry_id')
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

    paginator = Paginator(sermon_list, 7)
    page = request.GET.get('page')
    try:
        sermons = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sermons = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sermons = paginator.page(paginator.num_pages)

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
