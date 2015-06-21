from .models import Fellowship, Sermon, Event, YearlyTheme, SermonCatalog

def level1():
    sermon_catalogs = SermonCatalog.objects.all()
    message_catalogs = Fellowship.objects.all()
    return {
            'level1': 1,
            'sermon_catalogs': sermon_catalogs,
            'message_catalogs': message_catalogs}
