from django.contrib import admin

# Register your models here.
from .models import Event, Notice, Fellowship, FellowshipMessage

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields' : ('event_time','location','title')}),
            (None, {'fields' : ('desc',), 'classes' : ('wide', 'extrapretty',)}),
            (None, {'fields' : ('pdf',)}),
            ]

    list_display = ('event_time', 'location', 'title', 'owner', 'pub_time')
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

admin.site.register(Notice)
admin.site.register(Fellowship)
admin.site.register(FellowshipMessage)
