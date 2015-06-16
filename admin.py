from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
from .models import Event, Notice, Fellowship, FellowshipMessage
from .models import About, YearlyTheme, Sermon, Contact
from .models import EventAttachment, MessageAttachment, SermonDocument
from .models import Photo, PhotoAlbum
from django.forms import TextInput, Textarea
from django.db import models

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    fieldsets = [
            ('About Church', {'fields' : ('desc',)}),
            ('About Pastor', {'fields' : ('pastor', 'pastor_profile')}),
            ('About Faith', {'fields' : ('faith',)}),
            ]
    list_display = ('update_time', 'pastor')

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

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    fieldsets = [
            ('Church Contact Information',
                {'fields' : ('title', 'address', 'phone', 'email')}),
            ]
    list_display = ('update_time', 'address', 'phone', 'email')
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':80})},
    }

########################################
######Notice Admin######################
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields' : ('effective_date','desc',)}),
            ]
    list_display = ('effective_date', 'owner', 'pub_time', 'desc',)
    list_filter = ['pub_time', 'effective_date',]
    search_fields = ['desc']

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':80})},
    }

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

########################################
######Event Admin#######################
class EventAttachmentInline(admin.StackedInline):
    model = EventAttachment
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields' : ('event_date', 'event_time', 'location',)}),
            (None, {'fields' : ('title', 'desc',),}),
            (None, {'fields' : ('flyer',)}),
            ]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':80})},
    }

    list_display = ('event_date', 'location', 'title', 'owner', 'pub_time', 'admin_image')
    list_filter = ['pub_time', 'event_date',]
    search_fields = ['desc', 'title']

    inlines = [
            EventAttachmentInline,
            ]

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

########################################
######Fellowship Admin##################
class MessageAttachmentInline(admin.StackedInline):
    model = MessageAttachment
    extra = 1

@admin.register(Fellowship)
class FellowshipAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields' : ('name', 'schedule', 'location',
                'admin','admin_phone','admin_email')}),
            (None, {'fields' : ('desc',)}),
            ]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':80})},
    }

    list_display = ('name', 'admin', 'admin_email', 'admin_phone', 'location',)

@admin.register(FellowshipMessage)
class FellowshipMessageAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields' : ('fellowship', 'effective_date')}),
            (None, {'fields' : ('subject', 'msg',)}),
            ]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':80})},
    }

    list_display = ['fellowship', 'subject', 'is_effective_msg',]
    list_filter = ['pub_time', 'effective_date', 'fellowship',]
    search_fields = ['msg',]

    inlines = [
            MessageAttachmentInline,
            ]

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

########################################
######Sermon Admin######################
class SermonDocumentInline(admin.TabularInline):
    model = SermonDocument
    extra = 1

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
    }
    list_display = ('title', 'author', 'pub_time')
    list_filter = ['pub_time']
    search_fields = ['keywords', 'title']
    inlines = [
            SermonDocumentInline,
            ]

########################################
######Photo Album Admin#################
class PhotoInline(admin.TabularInline):
    model = Photo
    #show Thumbnail in admin page
    fields = ('carousel', 'name', 'image', 'thumbnail')
    readonly_fields = ['thumbnail',]
    extra = 1

@admin.register(PhotoAlbum)
class PhotoAlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'pub_time')
    inlines = [
            PhotoInline,
            ]
