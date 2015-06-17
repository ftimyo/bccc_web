from django.shortcuts import render
from django.views.decorators.gzip import gzip_page
from .models import Event, Notice, Fellowship, FellowshipMessage
from .models import About, YearlyTheme, Sermon, Contact
from .models import Photo
from django.utils import timezone
from django.http import FileResponse
import os, datetime

# Create your views here.
@gzip_page
def index(request):
    events = Event.objects.filter(event_date__gte = timezone.now().date() - datetime.timedelta(days=1))
    notices = Notice.objects.filter(effective_date__gte = timezone.now().date() - datetime.timedelta(days=1))
    contacts = Contact.objects.all()[:1]
    themes = YearlyTheme.objects.all()[:1]
    abouts = About.objects.all()[:1]
    fellowships = Fellowship.objects.all()
    sermons = Sermon.objects.all()[:25]
    photos = Photo.objects.filter(carousel=True)[:8]

    context = {
            'events' : events,
            'notices' : notices,
            'contacts' : contacts,
            'themes' : themes,
            'abouts' : abouts,
            'fellowships' : fellowships,
            'sermons' : sermons,
            'photos' : photos,
            }

    return render(request, 'church/index.html', context)
