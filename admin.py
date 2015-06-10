from django.contrib import admin

# Register your models here.
from .models import Event, Notice, Fellowship, FellowshipMessage

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields' : ('event_time','location','title')}),
            (None, {'fields' : ('desc',),}),
            (None, {'fields' : ('pdf',)}),
            ]

    list_display = ('event_time', 'location', 'title', 'owner', 'pub_time')
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields' : ('event_time','desc',)}),
            ]
    list_display = ('event_time', 'owner', 'pub_time', 'desc',)
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

@admin.register(Fellowship)
class FellowshipAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields' : ('name','location',
                'admin','admin_email','admin_phone','dp_order')}),
            (None, {'fields' : ('desc',)}),
            ]
    list_display = ('name', 'admin', 'admin_email', 'admin_phone','location',)

@admin.register(FellowshipMessage)
class FellowshipMessageAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields' : ('fellowship', 'msg',)}),
            ]
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()
