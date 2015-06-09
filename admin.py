from django.contrib import admin

# Register your models here.
from .models import Event, Notice, Fellowship, FellowshipMessage

admin.site.register(Event)
admin.site.register(Notice)
admin.site.register(Fellowship)
admin.site.register(FellowshipMessage)
