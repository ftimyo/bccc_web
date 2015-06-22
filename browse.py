from .models import Fellowship, Sermon, Event, YearlyTheme, SermonCatalog
from django.core.exceptions import ObjectDoesNotExist

def level1():
    sermon_catalogs = SermonCatalog.objects.all()
    message_catalogs = Fellowship.objects.all()
    return {'sermon_catalogs': sermon_catalogs,
            'message_catalogs': message_catalogs,
            }

########################################

def message(request, domain, catalog):
    try:
        catalog = Fellowship.objects.get(pk=catalog)
    except:
        return level1()

    entries = catalog.fellowshipmessage_set.all()

    return {'domain': domain, 'catalog': catalog, 'entries': entries,}

def sermon(request, domain, catalog):
    try:
        catalog = SermonCatalog.objects.get(pk=catalog)
    except:
        return level1()

    entries = catalog.sermon_set.all()

    return {'domain': domain, 'catalog': catalog, 'entries': entries,}

def theme(request, domain):
    entries = YearlyTheme.objects.all()
    return {'domain': domain, 'entries': entries,}

def event(request, domain):
    entries = Event.objects.all()
    return {'domain': domain, 'entries': entries,}


def level2(request, domain):
    catalog = request.GET.get('catalog')

    if domain == 'message':
        return message(request, domain, catalog)

    elif domain == 'sermon':
        return sermon(request, domain, catalog)

    elif domain == 'theme':
        return theme(request, domain)

    elif domain == 'event':
        return event(request, domain)

    else:
        return level1()
