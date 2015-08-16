from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from redactor.fields import RedactorField
from .utils import MediaFileSystemStorage
import hashlib
import datetime
import os

class About(models.Model):
    desc = RedactorField(verbose_name='Church Description', redactor_options={'focus': 'true'},
            allow_file_upload=False, allow_image_upload=False)
    pastor = models.CharField('Pastor Names', max_length=50)
    pastor_profile = RedactorField(verbose_name='Pastor Profile', redactor_options={'focus': 'true'},
            allow_file_upload=False, allow_image_upload=False)
    faith = RedactorField(verbose_name='Faith Statement', redactor_options={'focus': 'true'},
            allow_file_upload=False, allow_image_upload=False)

    update_time = models.DateTimeField('Time Modified', auto_now=True)

    def __unicode__(self):
        return self.pastor
    def __str__(self):
        return self.pastor

class YearlyTheme(models.Model):
    title = models.CharField('Theme', max_length=100, help_text='教會年度主題 (字數限制, 50 字)')
    text = RedactorField(verbose_name='Description', redactor_options={'focus': 'true'},
            allow_file_upload=False, allow_image_upload=False)

    pub_time = models.DateTimeField('Time Published', auto_now_add=True)

    class Meta:
        ordering = ['-pub_time']

    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.title


class Contact(models.Model):
    title = models.CharField('Title', max_length=50)
    address = models.CharField('Address', max_length=200)
    phone = models.CharField('Phone', max_length=16, help_text='Format: <em>XXX-XXX-XXXX</em>')
    email = models.EmailField('Email')
    latitude = models.DecimalField('Latitude', help_text='Use http://www.mapcoordinates.net to get Latitude',
            max_digits=20, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField('Longitude', help_text='Use http://www.mapcoordinates.net to get Longitude',
            max_digits=20, decimal_places=10, null=True, blank=True)

    update_time = models.DateTimeField('Time Modified', auto_now=True)

    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.title

######Notice############################
class Notice(models.Model):
    effective_date = models.DateField('Effective Date')
    desc = RedactorField(verbose_name='Notice Description', redactor_options={'focus': 'true'},
            allow_file_upload=False, allow_image_upload=False)
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)
    owner = models.ForeignKey(User, editable=False, verbose_name='Publisher')

    class Meta:
        ordering = ['-effective_date']

    def is_effective_notice(self):
        return self.effective_date >= timezone.now().date() - datetime.timedelta(days=1)

    is_effective_notice.admin_order_field = 'effective_date'
    is_effective_notice.boolean = True
    is_effective_notice.short_description = 'Still Shown?'
    is_effective_notice.allow_tags = True

    def __unicode__(self):
        return str(self.owner) + ': ' + self.desc[:15] + ' ...'
    def __str__(self):
        return str(self.owner) + ': ' + self.desc[:15] + ' ...'

########################################
######Event Model#######################
def rename_flyer(instance, filename):
    h = instance.md5sum
    basename, ext = os.path.splitext(filename)
    return os.path.join('flyer', h[0:1], h[1:2], h + ext.lower())

class Event(models.Model):
    event_date = models.DateField('Event Date', help_text='活動日期')
    event_time = models.TimeField('Event Time (Optional)', help_text='活動時間', null=True, blank=True)
    location = models.CharField('Location', max_length=50)

    title = models.CharField('Event Title', help_text='活動標題', max_length=50)
    text = RedactorField(verbose_name='Event Description (Optional)', null=True, blank=True,
            redactor_options={'focus': 'true'},
            allow_file_upload=False, allow_image_upload=False)

    flyer = models.ImageField(verbose_name='Flyer Image (Optional)', help_text='活動宣傳圖片',
            upload_to=rename_flyer, null=True, blank=True)

    md5sum = models.CharField(max_length=36, editable=False)

    def attachments(self):
        return self.eventattachment_set.all()

    #Auto Generated Fields
    owner = models.ForeignKey(User, verbose_name='Publisher', editable=False)
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)

    class Meta:
        ordering = ['event_date', 'event_time']

    def admin_image(self):
        if self.flyer:
            return u'<img src="%s" style="height:90px; width:175px;"/>' % self.flyer.url
        else:
            return 'No Flyer'
    def show_flyer(self):
        if self.flyer:
            return u'<img class="img-responsive" src="%s"/>' % self.flyer.url
        else:
            return ''

    admin_image.short_description = 'Flyer Preview'
    admin_image.allow_tags = True
    show_flyer.allow_tags = True

    def is_effective_event(self):
        return self.event_date >= timezone.now().date() - datetime.timedelta(days=1)

    is_effective_event.admin_order_field = 'effective_date'
    is_effective_event.boolean = True
    is_effective_event.short_description = 'Still Shown?'
    is_effective_event.allow_tags = True


    def save(self, *args, **kwargs):
        if not self.pk and self.flyer:  # file is new
            md5 = hashlib.md5()
            for chunk in self.flyer.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        super().save(*args, **kwargs)

    def __unicode__(self):
        return str(self.owner) + ': ' + self.title[:10] + ' ...'
    def __str__(self):
        return str(self.owner) + ': ' + self.title[:10] + ' ...'

def rename_event_file(instance, filename):
    h = instance.md5sum
    basename, ext = os.path.splitext(filename)
    return os.path.join('event', h[0:1], h[1:2], h + ext.lower())

class EventAttachment(models.Model):
    name = models.CharField('Attachment Name', max_length=255)
    attach = models.FileField(verbose_name='Attachment File', upload_to=rename_event_file)
    md5sum = models.CharField(max_length=36, editable=False)

    #Auto Generated Field
    event = models.ForeignKey(Event, verbose_name='Event', editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:  # file is new
            md5 = hashlib.md5()
            for chunk in self.attach.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        super().save(*args, **kwargs)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
######Event Model END###################

########################################
######Fellowship Model##################
class Fellowship(models.Model):

    name = models.CharField('Fellowship Name', max_length=20, help_text='團契間稱')
    full_name = models.CharField('Fellowship Full Name', max_length=50, help_text='團契全稱')
    desc = RedactorField(verbose_name='Fellowship Description', redactor_options={'focus': 'true'},
            allow_file_upload=False, allow_image_upload=False)
    location = models.CharField('Location', max_length=50, help_text='地點', blank=True, null=True)
    schedule = models.CharField('Time', max_length=50, blank=True, null=True,
            help_text='The time schedule of activities, for example 每週五 晚上7:30.')

    #contact info
    admin = models.CharField('Person in Charge', max_length=20, help_text='負責人', blank=True, null=True)
    admin_email = models.EmailField('Email', blank=True, null=True)
    admin_phone = models.CharField('Phone', max_length=16, help_text='Format: <em>XXX-XXX-XXXX</em>', blank=True, null=True)
    admin_other = models.CharField('Other Contact Information', max_length=100,
	    help_text='Other Contact Information, for example QQ, Wechat, facebook etc.', blank=True, null=True)

    #display option
    display = models.BooleanField('Show on Website', default=True)
    priorities = zip(range(0,5), range(0, 5))
    priority = models.IntegerField('Displaying Priority', default = 2, choices=priorities)

    #Ordered by update time
    update_time = models.DateTimeField('Update Time', auto_now=True)
    class Meta:
        ordering = ['priority', '-update_time']

    #Recent Messages
    def recent_msgs(self):
        return self.fellowshipmessage_set.filter(effective_date__gte = timezone.now().date() - datetime.timedelta(days=1))

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

class FellowshipMessage(models.Model):

    fellowship = models.ForeignKey(Fellowship, verbose_name='Fellowship')
    effective_date = models.DateField('Effective Date')
    title = models.CharField('Subject', max_length=50)
    text = RedactorField(verbose_name='Message (Optional)', null=True, blank=True,
            redactor_options={'focus': 'true'},
            allow_file_upload=False, allow_image_upload=False)

    def attachments(self):
        return self.messageattachment_set.all()

    #Auto Generated Fields
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)
    owner = models.ForeignKey(User, verbose_name='Publisher', editable=False)

    #Order by effective_time
    class Meta:
        ordering = ['effective_date']

    def is_effective_msg(self):
        return self.effective_date >= timezone.now().date() - datetime.timedelta(days=1)

    is_effective_msg.admin_order_field = 'effective_date'
    is_effective_msg.boolean = True
    is_effective_msg.short_description = 'Still Shown?'
    is_effective_msg.allow_tags = True

    def __unicode__(self):
        return self.fellowship.name + ': ' + self.title
    def __str__(self):
        return self.fellowship.name + ': ' + self.title

def rename_message_file(instance, filename):
    h = instance.md5sum
    basename, ext = os.path.splitext(filename)
    return os.path.join('message', h[0:1], h[1:2], h + ext.lower())

class MessageAttachment(models.Model):
    name = models.CharField('Attachment Name', max_length=255)
    attach = models.FileField(verbose_name = 'Attachment File', upload_to=rename_message_file)
    msg = models.ForeignKey(FellowshipMessage, verbose_name='Fellowship Message', editable=False)
    md5sum = models.CharField(max_length=36, editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:  # file is new
            md5 = hashlib.md5()
            for chunk in self.attach.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        super().save(*args, **kwargs)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
######Fellowship END####################

########################################
######Sermon Model######################
class SermonCatalog(models.Model):
    name = models.CharField("Catalog Name", max_length=50)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

class Sermon(models.Model):
    title = models.CharField('Title', max_length=100)
    author = models.CharField('Author', max_length=50)
    keywords = models.CharField('Keywords', max_length=50, help_text='Used for search')
    text = RedactorField(verbose_name='Sermon Text (Optional)', null=True, blank=True,
            redactor_options={'focus': 'true'},
            allow_file_upload=False, allow_image_upload=False)
    catalog = models.ForeignKey(SermonCatalog, verbose_name='Catalog')

    def attachments(self):
        return self.sermondocument_set.all()

    #Auto Generated Field
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)

    class Meta:
        ordering = ['-pub_time']

    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.title

def rename_sermon_file(instance, filename):
    h = instance.md5sum
    basename, ext = os.path.splitext(filename)
    return os.path.join('event', h[0:1], h[1:2], h + ext.lower())

class SermonDocument(models.Model):
    name = models.CharField('Document Name', max_length=255)
    attach = models.FileField(verbose_name='Document File', upload_to=rename_sermon_file)
    sermon = models.ForeignKey(Sermon, verbose_name='Sermon', editable=False)
    md5sum = models.CharField(max_length=36, editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:  # file is new
            md5 = hashlib.md5()
            for chunk in self.attach.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        super().save(*args, **kwargs)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
######Sermon Model END##################

########################################
######Photo Album Model#################
class PhotoAlbum(models.Model):
    name = models.CharField("Album Title", max_length=255)
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)
    album = models.BooleanField('Show on PhotoAlbum', help_text='在相冊中顯示', default=False)

    class Meta:
        ordering = ['-pub_time']

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

def rename_photo(instance, filename):
    h = instance.md5sum
    basename, ext = os.path.splitext(filename)
    return os.path.join('photo', h[0:1], h[1:2], h + ext.lower())

class Photo(models.Model):
    carousel = models.BooleanField('Show in Carousel', default=False)
    name = models.CharField('Photo Title', max_length=255)
    image = models.ImageField(verbose_name = 'Photo', upload_to=rename_photo)
    album = models.ForeignKey(PhotoAlbum, verbose_name='Photo Album', editable=True)
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)

    md5sum = models.CharField(max_length=36, editable=False)

    class Meta:
        ordering = ['pub_time']

    #show Thumbnail in admin page
    def thumbnail(self):
        if self.image:
            return u'<img src="%s" style="height:90px; width:175px;"/>' % self.image.url
        else:
            return 'No Photo'
    def photo_size(self):
        if self.image:
            return u'%dx%d' % (self.image.width, self.image.height)
        else:
            return '---'

    thumbnail.short_description = 'Photo Thumbnail'
    thumbnail.allow_tags = True

    photo_size.short_description = "Photo Size"
    photo_size.allow_tags = True

    def save(self, *args, **kwargs):
        if not self.pk:  # file is new
            md5 = hashlib.md5()
            for chunk in self.image.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        super().save(*args, **kwargs)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
######Photo Album Model END#############
