from django.contrib import admin

# Register your models here.
from .models import Event, Notice, Fellowship, FellowshipMessage
from .models import About, YearlyTheme, Sermon
from django.forms import TextInput, Textarea
from django.db import models

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':80, 'cols':80})},
    }
    list_display = ('title', 'author', 'pub_time')
    list_filter = ['pub_time']
    search_fields = ['content', 'title']


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    pass

@admin.register(YearlyTheme)
class YearlyThemeAdmin(admin.ModelAdmin):
    list_display = ('theme', 'desc', 'pub_time')
    list_filter = ['pub_time']
    search_fields = ['desc', 'theme']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields' : ('event_time','location','title')}),
            (None, {'fields' : ('desc',),}),
            (None, {'fields' : ('pdf',)}),
            ]

    list_display = ('event_time', 'location', 'title', 'owner', 'pub_time')
    list_filter = ['pub_time', 'event_time',]
    search_fields = ['desc', 'title']
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields' : ('event_time','desc',)}),
            ]
    list_display = ('event_time', 'owner', 'pub_time', 'desc',)
    list_filter = ['pub_time', 'event_time',]
    search_fields = ['desc']
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

@admin.register(Fellowship)
class FellowshipAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields' : ('name', 'schedule', 'location',
                'admin','admin_email','admin_phone','dp_order')}),
            (None, {'fields' : ('desc',)}),
            ]
    list_display = ('name', 'admin', 'admin_email', 'admin_phone','location',)

@admin.register(FellowshipMessage)
class FellowshipMessageAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields' : ('fellowship', 'msg',)}),
            ]

    list_filter = ['pub_time', 'fellowship']
    search_fields = ['msg',]

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()
