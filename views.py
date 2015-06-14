from django.shortcuts import render
from django.views.decorators.gzip import gzip_page
from .models import Event, Notice, Fellowship, FellowshipMessage
from .models import About, YearlyTheme, Sermon, Contact
from django.utils import timezone
from django.http import FileResponse
import os

# Create your views here.
@gzip_page
def index(request):
    events = Event.objects.filter(event_time__gte = timezone.now())
    notices = Notice.objects.filter(event_time__gte = timezone.now())
    contacts = Contact.objects.all()[:1]
    themes = YearlyTheme.objects.all()[:1]
    abouts = About.objects.all()[:1]
    fellowships = Fellowship.objects.all()

    context = {
            'events' : events,
            'notices' : notices,
            'contacts' : contacts,
            'themes' : themes,
            'abouts' : abouts,
            'fellowships' : fellowships,
            }

    return render(request, 'church/index.html', context)

@gzip_page
def showfile(request, filename):
    response = FileResponse(open(os.path.join('media', filename), 'rb'))
    return response
