from .models import Event, Fellowship, FellowshipMessage
from .models import YearlyTheme, Sermon, SermonCatalog

def detail_page(request, domain, catalog, entry_id):
    if domain == 'message':
        try:
            catalog = Fellowship.objects.get(pk=catalog)
        except:
            return {}

        try:
            message = catalog.fellowshipmessage_set.get(pk=entry_id)
        except:
            return {}

        return {'message_entry': message}

    elif domain == 'sermon':
        try:
            catalog = SermonCatalog.objects.get(pk=catalog)
        except:
            return {}

        try:
            sermon = catalog.sermon_set.get(pk=entry_id)
        except:
            return {}

        return {'sermon_entry': sermon}

    elif domain == 'theme':
        try:
            theme = YearlyTheme.objects.get(pk=entry_id)
        except:
            return {}

        return {'theme_entry': theme}

    elif domain == 'event':
        try:
            event = Event.objects.get(pk=entry_id)
        except:
            return {}

        return {'event_entry': event}

    else:
        return {}
