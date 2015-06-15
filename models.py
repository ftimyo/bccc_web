from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import os

def rename_flyer(instance, filename):
    ext = filename.split('.')[-1]
    stamp = timezone.now()
    filename = "f%s.%s" % (stamp.strftime("%y%m%d%H%M%S"), ext)
    return os.path.join('flyer', filename)

def rename_event_file(instance, filename):
    ext = filename.split('.')[-1]
    stamp = timezone.now()
    filename = "e%s.%s" % (stamp.strftime("%y%m%d%H%M%S"), ext)
    return os.path.join('event', filename)

def rename_message_file(instance, filename):
    ext = filename.split('.')[-1]
    stamp = timezone.now()
    filename = "m%s.%s" % (stamp.strftime("%y%m%d%H%M%S"), ext)
    return os.path.join('message', filename)

# Create your models here.
class Notice(models.Model):
    #outdated event won't be displayed according to event_time
    event_time = models.DateTimeField('Notice Until',
            help_text='The notice will be displayed until the specified date time')
    desc = models.TextField('Notice Content',
            help_text='Notice（通啟）消息支持HTML Tags.')
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)
    owner = models.ForeignKey(User, limit_choices_to={'is_staff': True},
            editable=False, verbose_name='Publisher')

    def __unicode__(self):
        return str(self.owner) + ': ' + self.desc[:10] + ' ...'
    def __str__(self):
        return str(self.owner) + ': ' + self.desc[:10] + ' ...'

class Event(models.Model):
    #outdated event won't be displayed according to event_time
    event_time = models.DateTimeField('Event Starting Time',
            help_text='活動開始時間')
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)
    location = models.CharField('Location', max_length=50)
    title = models.CharField('Event Summary', max_length=50)
    desc = models.TextField('Event Description',
            help_text='活動詳細說明 支持 HTML Tags.',
            null=True, blank=True)
    owner = models.ForeignKey(User, verbose_name='Publisher', editable=False)
    flyer = models.ImageField(verbose_name = 'Flyer Image',
            help_text = '活動宣傳圖片',
            upload_to=rename_flyer, null=True, blank=True)

    def admin_image(self):
        if self.flyer:
            return u'<img src="%s" style="height:90px; width:175px;"/>' % self.flyer.url
        else:
            return 'No Flyer'
    def show_flyer(self):
        if self.flyer:
            return u'<img class="img-responsive" src="%s"/>' % self.flyer.url
        else:
            return '<em>No Flyer</em>'

    admin_image.short_description = 'Flyer Preview'
    admin_image.allow_tags = True
    show_flyer.allow_tags = True

    def __unicode__(self):
        return str(self.owner) + ': ' + self.title[:10] + ' ...'
    def __str__(self):
        return str(self.owner) + ': ' + self.title[:10] + ' ...'

class Fellowship(models.Model):

    name = models.CharField('Fellowship Name', max_length=50,
            help_text='團契名稱')
    desc = models.TextField('Fellowship Description',
            help_text='聚會內容 支持 HTML Tags.')
    location = models.CharField('Location', max_length=50, help_text='地點')
    schedule = models.CharField('Time', max_length=50,
            help_text='The time schedule of activities, for example 每週五 晚上7:30.')

    dp_order = models.IntegerField('Display Order', default=2,
            help_text='The fellowships\' info will be displayed in the order of the <em>Display Order</em>')

    #contact info
    admin = models.CharField('Person in Charge', max_length=20,
            help_text='負責人')
    admin_email = models.EmailField('Email')
    admin_phone = models.CharField('Phone', max_length=16,
            help_text='Please use the following format: <em>XXX-XXX-XXXX</em>')

    #Recent Messages
    def recent_msgs(self):
        return self.fellowshipmessage_set.filter(pub_time__gte = timezone.now() - datetime.timedelta(days=15))

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

class FellowshipMessage(models.Model):

    msg = models.TextField('Message')
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)
    fellowship = models.ForeignKey(Fellowship, verbose_name='Fellowship')
    owner = models.ForeignKey(User, verbose_name='Publisher', editable=False)

    def is_biweekly_msg(self):
        return self.pub_time > timezone.now() - datetime.timedelta(days=15)

    def shortened_msg(self):
        return self.msg[:35] + ' ...'

    shortened_msg.short_description = "Message"

    is_biweekly_msg.admin_order_field = 'pub_time'
    is_biweekly_msg.boolean = True
    is_biweekly_msg.short_description = 'Still Shown? (Biweekly Message)'
    is_biweekly_msg.allow_tags = True

    def __unicode__(self):
        return self.fellowship.name + ': ' + self.msg[:10] + ' ...'
    def __str__(self):
        return self.fellowship.name + ': ' + self.msg[:10] + ' ...'

class About(models.Model):
    pub_time = models.DateTimeField('Time Published', auto_now=True)
    desc = models.TextField('Church Description',
            help_text='The content will be displayed in the column of 教會簡介 (This field supports HTML Tags.')
    pastor = models.CharField('Pastor Names', max_length=50)
    pastor_profile = models.TextField('Pastor Profile',
            help_text='The content will be displayed in the column of 牧者簡介 (This field supports HTML Tags)')
    faith = models.TextField('Faith Statement',
            help_text='信仰告白 (This field supports HTML Tags)')
    def __unicode__(self):
        return self.pastor
    def __str__(self):
        return self.pastor

class YearlyTheme(models.Model):
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)
    theme = models.CharField('Theme', max_length=100,
            help_text='教會年度主題 (字數限制, 50 字)')
    desc = models.TextField('Description',
            help_text = '教會年度主題詳盡說明 (字數不限. This field supports HTML Tags)')

    def __unicode__(self):
        return self.theme
    def __str__(self):
        return self.theme

class Sermon(models.Model):
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)
    title = models.CharField('Title', max_length=100)
    author = models.CharField('Author', max_length=50)
    keywords = models.CharField('Keywords', max_length=50, help_text='Used for search')
    #content = models.TextField('Sermon Content', blank=True, null=True)

    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.title

class Contact(models.Model):
    title = models.CharField('Title', max_length=50)
    address = models.CharField('Address', max_length=50)
    email = models.EmailField('Email')
    phone = models.CharField('Phone', max_length=16,
            help_text='Please use the following format: <em>XXX-XXX-XXXX</em>')

    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.title

#####File Management####################
class MessageAttachment(models.Model):
    '''
    MessageAttachment support multiple attachments for FellowshipMessage
    '''
    name = models.CharField('Attachment Name', max_length=255)
    attach = models.FileField(verbose_name = 'Attachment File',
            help_text = '.doc .pdf .docx .mp3 .m4a .wma etc.',
            upload_to=rename_message_file)
    msg = models.ForeignKey(FellowshipMessage, verbose_name='Fellowship Message', editable=False)
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

class EventAttachment(models.Model):
    '''
    EventAttachment support multiple attachments for Event
    '''
    name = models.CharField('Attachment Name', max_length=255)
    attach = models.FileField(verbose_name = 'Attachment File',
            help_text = '.doc .pdf .docx .mp3 .m4a .wma etc.',
            upload_to=rename_event_file)
    msg = models.ForeignKey(Event, verbose_name='Event', editable=False)
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

def rename_sermon_file(instance, filename):
    ext = filename.split('.')[-1]
    stamp = timezone.now()
    filename = "s%s.%s" % (stamp.strftime("%y%m%d%H%M%S"), ext)
    return os.path.join('sermon', filename)

class SermonDocument(models.Model):
    name = models.CharField('Document Name', max_length=255)
    document = models.FileField(verbose_name = 'Document File',
            help_text = '.doc .pdf .docx .mp3 .m4a .wma etc.',
            upload_to=rename_sermon_file)
    sermon = models.ForeignKey(Sermon, verbose_name='Sermon', editable=False)
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name


class PhotoAlbum(models.Model):
    name = models.CharField("Album Title", max_length=255)
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

def rename_photo(instance, filename):
    ext = filename.split('.')[-1]
    stamp = timezone.now()
    filename = "s%s.%s" % (stamp.strftime("%y%m%d%H%M%S"), ext)
    return os.path.join('photo', filename)

class Photo(models.Model):
    carousel = models.BooleanField('Show in Carousel', default=False)
    name = models.CharField('Photo Title', max_length=255)
    image = models.ImageField(verbose_name = 'Photo',
            upload_to=rename_photo)
    album = models.ForeignKey(PhotoAlbum, verbose_name='Photo Album', editable=False)

    pub_time = models.DateTimeField('Time Published', auto_now_add=True)

    def thumbnail(self):
        if self.image:
            return u'<img src="%s" style="height:90px; width:175px;"/>' % self.image.url
        else:
            return 'No Photo'

    thumbnail.short_description = 'Photo Thumbnail'
    thumbnail.allow_tags = True

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
