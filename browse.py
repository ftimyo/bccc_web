from .models import Fellowship, Sermon, Event, YearlyTheme, SermonCatalog
from django.core.exceptions import ObjectDoesNotExist
from .utils import control_filter

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

    context = {'domain': domain, 'catalog': catalog,}
    context.update(control_filter(request, domain, entries))

    return context

def sermon(request, domain, catalog):
    try:
        catalog = SermonCatalog.objects.get(pk=catalog)
    except:
        return level1()

    entries = catalog.sermon_set.all()

    context = {'domain': domain, 'catalog': catalog,}
    context.update(control_filter(request, domain, entries))

    return context

def theme(request, domain):
    entries = YearlyTheme.objects.all()
    context =  {'domain': domain,}
    context.update(control_filter(request, domain, entries))

    return context

def event(request, domain):
    entries = Event.objects.all()
    context = {'domain': domain,}
    context.update(control_filter(request, domain, entries))

    return context


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
