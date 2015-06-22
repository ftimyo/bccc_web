from .models import Event, Fellowship, FellowshipMessage
from .models import YearlyTheme, Sermon, SermonCatalog

def detail_page(request, domain, catalog, entry_id):
    if domain == 'message':
        try:
            catalog = Fellowship.objects.get(pk=catalog)
        except:
            return {}

        try:
            entry = catalog.fellowshipmessage_set.get(pk=entry_id)
        except:
            return {}

        return {'entry': entry, 'domain': domain, 'catalog': catalog,}

    elif domain == 'sermon':
        try:
            catalog = SermonCatalog.objects.get(pk=catalog)
        except:
            return {}

        try:
            entry = catalog.sermon_set.get(pk=entry_id)
        except:
            return {}

        return {'entry': entry, 'domain': domain, 'catalog': catalog,}

    elif domain == 'theme':
        try:
            entry = YearlyTheme.objects.get(pk=entry_id)
        except:
            return {}

        return {'entry': entry, 'domain': domain, 'catalog': catalog,}

    elif domain == 'event':
        try:
            entry = Event.objects.get(pk=entry_id)
        except:
            return {}

        return {'entry': entry, 'domain': domain, 'catalog': catalog,}

    else:
        return {}
