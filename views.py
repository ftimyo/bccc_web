from django.shortcuts import render
from django.views.decorators.gzip import gzip_page
from .models import Event, Notice, Fellowship, FellowshipMessage
from .models import About, YearlyTheme, Sermon, Contact
from .models import Photo
from django.utils import timezone
from django.http import FileResponse
import os, datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .search import get_query

# Create your views here.

@gzip_page
def search(request):
    found_entries = None
    query_string = ''
    search_domains = [['Sermon','講道'], ['Event','活動'], ['Message','訊息']]
    search_domain = search_domains[0][0]
    search_results = None
    sort_results = [['Newest', '由新到舊排列'], ['Oldest', '由舊到新排列']]
    orderby = sort_results[0][0]


    if 'search_domain' in request.GET:
        search_domain = request.GET['search_domain']
    if 'orderby' in request.GET:
        orderby = request.GET['orderby']
    if 'query_string' in request.GET:
        query_string = request.GET['query_string'].strip()

    if query_string != '':
        if search_domain == 'Message':
            query = get_query(query_string, ['title', 'text'])
            found_entries = FellowshipMessage.objects.filter(query)

        elif search_domain == 'Event':
            query = get_query(query_string, ['title', 'text',])
            found_entries = Event.objects.filter(query)
        else:
            search_domain = 'Sermon'
            query = get_query(query_string, ['title', 'text', 'keywords'])
            found_entries = Sermon.objects.filter(query)

        if orderby == 'Oldest':
            found_entries = found_entries.order_by('pub_time')
        else:
            found_entries = found_entries.order_by('-pub_time')


        paginator = Paginator(found_entries, 7)
        page = request.GET.get('page')
        try:
            search_results = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            search_results = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            search_results = paginator.page(paginator.num_pages)

    context = {
            'query_string': query_string,
            'search_domains': search_domains,
            'search_domain': search_domain,
            'search_results': search_results,
            'sort_results': sort_results,
            'orderby': orderby,
            }


    return render(request, 'church/search.html', context)

@gzip_page
def index(request):
    search_domains = [['Sermon','講道'], ['Event','活動'], ['Message','訊息']]
    search_domain = search_domains[0][0]

    events = Event.objects.filter(event_date__gte = timezone.now().date() - datetime.timedelta(days=1))
    notices = Notice.objects.filter(effective_date__gte = timezone.now().date() - datetime.timedelta(days=1))
    contacts = Contact.objects.all()[:1]
    themes = YearlyTheme.objects.all()[:1]
    abouts = About.objects.all()[:1]
    fellowships = Fellowship.objects.all()
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
            'search_domains': search_domains,
            'search_domain': search_domain,
            }

    return render(request, 'church/index.html', context)
