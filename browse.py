from .models import Fellowship, Sermon, Event, YearlyTheme, SermonCatalog
from django.core.exceptions import ObjectDoesNotExist

def message_all(catalog):
    messages = None
    try:
        messages = Fellowship.objects.get(pk=catalog)
    except:
        messages = None
    return messages

def sermon_all(catalog):
    sermons = None
    try:
        sermons = SermonCatalog.objects.get(pk=catalog)
    except:
        sermons = None
    return sermons


def level1():
    sermon_catalogs = SermonCatalog.objects.all()
    message_catalogs = Fellowship.objects.all()
    return {
            'level1': 1,
            'sermon_catalogs': sermon_catalogs,
            'message_catalogs': message_catalogs}

def message(catalog):
    catalog = message_all(catalog)
    domain = "message"

    if catalog == None:
        return level1()
    messages = catalog.fellowshipmessage_set.all()

    context = {'domain': domain, 'level2_message': 2, 'catalog': catalog, 'messages': messages}

    return context

def sermon(catalog):
    catalog = sermon_all(catalog)
    domain = "sermon"

    if catalog == None:
        return level1()
    sermons = catalog.sermon_set.all()

    context = {'domain': domain, 'level2_sermon': 2, 'catalog': catalog, 'sermons': sermons}

    return context

def theme():
    themes = YearlyTheme.objects.all()
    domain = "theme"
    context = {'domain': domain, 'level2_theme': 2, 'themes': themes}
    return context

def event():
    events = Event.objects.all()
    domain = "event"
    context = {'domain': domain, 'level2_event': 2, 'events': events}
    return context

def level2(domain, catalog):

    if domain == 'message': 
        return message(catalog)

    elif domain == 'sermon':
        return sermon(catalog)

    elif domain == 'theme':
        return theme()

    elif domain == 'event':
        return event()

    else:
        return level1()
