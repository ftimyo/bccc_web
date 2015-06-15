from django.contrib import admin

# Register your models here.
from .models import Event, Notice, Fellowship, FellowshipMessage
from .models import About, YearlyTheme, Sermon, Contact
from .models import EventAttachment, MessageAttachment
from django.forms import TextInput, Textarea
from django.db import models

class EventAttachmentInline(admin.StackedInline):
    model = EventAttachment
    extra = 1

class MessageAttachmentInline(admin.StackedInline):
    model = MessageAttachment
    extra = 1

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    fieldsets = [
            ('Church Contact Information',
                {'fields' : ('title', 'address', 'phone', 'email')}),
            ]
    list_display = ('address', 'phone', 'email')
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':80})},
    }

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
    fieldsets = [
            ('About Church', {'fields' : ('desc',)}),
            ('About Pastor', {'fields' : ('pastor', 'pastor_profile')}),
            ('About Faith', {'fields' : ('faith',)}),
            ]
    list_display = ('pub_time', 'pastor')

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':80})},
    }


@admin.register(YearlyTheme)
class YearlyThemeAdmin(admin.ModelAdmin):
    list_display = ('theme', 'pub_time')
    list_filter = ['pub_time']
    search_fields = ['desc', 'theme']

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':80})},
    }


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields' : ('event_time','location','title')}),
            (None, {'fields' : ('desc',),}),
            (None, {'fields' : ('flyer',)}),
            ]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':80})},
    }

    list_display = ('event_time', 'location', 'title', 'owner', 'pub_time', 'admin_image')
    list_filter = ['pub_time', 'event_time',]
    search_fields = ['desc', 'title']

    inlines = [
            EventAttachmentInline,
            ]

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

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':80})},
    }

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

@admin.register(Fellowship)
class FellowshipAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields' : ('name', 'schedule', 'location',
                'admin','admin_phone','admin_email','dp_order')}),
            (None, {'fields' : ('desc',)}),
            ]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':80})},
    }

    list_display = ('name', 'admin', 'admin_email', 'admin_phone','location',)

@admin.register(FellowshipMessage)
class FellowshipMessageAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields' : ('fellowship', 'msg',)}),
            ]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':80})},
    }

    list_display = ['fellowship', 'shortened_msg', 'is_biweekly_msg',]
    list_filter = ['pub_time', 'fellowship',]
    search_fields = ['msg',]

    inlines = [
            MessageAttachmentInline,
            ]

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()
