from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import os

class About(models.Model):
    desc = models.TextField('Church Description', help_text='教會簡介 (support HTML Tags.')
    pastor = models.CharField('Pastor Names', max_length=50)
    pastor_profile = models.TextField('Pastor Profile', help_text='牧者簡介 (support HTML Tags)')
    faith = models.TextField('Faith Statement', help_text='信仰告白 (support HTML Tags)')

    update_time = models.DateTimeField('Time Modified', auto_now=True)

    def __unicode__(self):
        return self.pastor
    def __str__(self):
        return self.pastor

class YearlyTheme(models.Model):
    theme = models.CharField('Theme', max_length=100, help_text='教會年度主題 (字數限制, 50 字)')
    desc = models.TextField('Description', help_text = '教會年度主題詳盡說明 (support HTML Tags)')

    pub_time = models.DateTimeField('Time Published', auto_now_add=True)

    class Meta:
        ordering = ['-pub_time']

    def __unicode__(self):
        return self.theme
    def __str__(self):
        return self.theme


class Contact(models.Model):
    title = models.CharField('Title', max_length=50)
    address = models.CharField('Address', max_length=200)
    phone = models.CharField('Phone', max_length=16, help_text='Format: <em>XXX-XXX-XXXX</em>')
    email = models.EmailField('Email')

    update_time = models.DateTimeField('Time Modified', auto_now=True)

    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.title

######Notice############################
class Notice(models.Model):
    effective_date = models.DateField('Effective Date')
    desc = models.TextField('Notice Content', help_text='通啟 (支持HTML Tags)')
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)
    owner = models.ForeignKey(User, editable=False, verbose_name='Publisher')

    class Meta:
        ordering = ['-effective_date']

    def __unicode__(self):
        return str(self.owner) + ': ' + self.desc[:15] + ' ...'
    def __str__(self):
        return str(self.owner) + ': ' + self.desc[:15] + ' ...'

########################################
######Event Model#######################
def rename_flyer(instance, filename):
    ext = filename.split('.')[-1]
    stamp = timezone.now()
    filename = "f%s.%s" % (stamp.strftime("%y%m%d%H%M%S"), ext)
    return os.path.join('flyer', filename)

class Event(models.Model):
    event_date = models.DateField('Event Date', help_text='活動日期')
    event_time = models.TimeField('Event Time (Optional)', help_text='活動時間', null=True, blank=True)
    location = models.CharField('Location', max_length=50)

    title = models.CharField('Event Title', help_text='活動標題', max_length=50)
    desc = models.TextField('Event Description', help_text='活動詳細說明 (支持HTML Tags.)', null=True, blank=True)
    flyer = models.ImageField(verbose_name='Flyer Image', help_text='活動宣傳圖片',
            upload_to=rename_flyer, null=True, blank=True)

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

    def __unicode__(self):
        return str(self.owner) + ': ' + self.title[:10] + ' ...'
    def __str__(self):
        return str(self.owner) + ': ' + self.title[:10] + ' ...'

def rename_event_file(instance, filename):
    ext = filename.split('.')[-1]
    stamp = timezone.now()
    filename = "e%s.%s" % (stamp.strftime("%y%m%d%H%M%S"), ext)
    return os.path.join('event', filename)

class EventAttachment(models.Model):
    name = models.CharField('Attachment Name', max_length=255)
    attach = models.FileField(verbose_name='Attachment File', upload_to=rename_event_file)

    #Auto Generated Field
    msg = models.ForeignKey(Event, verbose_name='Event', editable=False)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
######Event Model END###################

########################################
######Fellowship Model##################
class Fellowship(models.Model):

    name = models.CharField('Fellowship Name', max_length=50, help_text='團契名稱')
    desc = models.TextField('Fellowship Description', help_text='團契說明 (支持HTML Tags.)')
    location = models.CharField('Location', max_length=50, help_text='地點')
    schedule = models.CharField('Time', max_length=50,
            help_text='The time schedule of activities, for example 每週五 晚上7:30.')

    #contact info
    admin = models.CharField('Person in Charge', max_length=20, help_text='負責人')
    admin_email = models.EmailField('Email')
    admin_phone = models.CharField('Phone', max_length=16, help_text='Format: <em>XXX-XXX-XXXX</em>')

    #Ordered by update time
    update_time = models.DateTimeField('Update Time', auto_now=True)
    class Meta:
        ordering = ['-update_time']

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
    subject = models.CharField('Subject', max_length=50)
    msg = models.TextField('Message', blank=True, null=True)

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
    is_effective_msg.short_description = 'Still Shown? (Effective Message)'
    is_effective_msg.allow_tags = True

    def __unicode__(self):
        return self.fellowship.name + ': ' + self.subject
    def __str__(self):
        return self.fellowship.name + ': ' + self.subject

def rename_message_file(instance, filename):
    ext = filename.split('.')[-1]
    stamp = timezone.now()
    filename = "m%s.%s" % (stamp.strftime("%y%m%d%H%M%S"), ext)
    return os.path.join('message', filename)

class MessageAttachment(models.Model):
    name = models.CharField('Attachment Name', max_length=255)
    attach = models.FileField(verbose_name = 'Attachment File', upload_to=rename_message_file)
    msg = models.ForeignKey(FellowshipMessage, verbose_name='Fellowship Message', editable=False)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
######Fellowship END####################

########################################
######Sermon Model######################
class Sermon(models.Model):
    title = models.CharField('Title', max_length=100)
    author = models.CharField('Author', max_length=50)
    keywords = models.CharField('Keywords', max_length=50, help_text='Used for search')

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
    ext = filename.split('.')[-1]
    stamp = timezone.now()
    filename = "s%s.%s" % (stamp.strftime("%y%m%d%H%M%S"), ext)
    return os.path.join('sermon', filename)

class SermonDocument(models.Model):
    name = models.CharField('Document Name', max_length=255)
    document = models.FileField(verbose_name='Document File', upload_to=rename_sermon_file)
    sermon = models.ForeignKey(Sermon, verbose_name='Sermon', editable=False)

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

    class Meta:
        ordering = ['-pub_time']

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
    image = models.ImageField(verbose_name = 'Photo', upload_to=rename_photo)
    album = models.ForeignKey(PhotoAlbum, verbose_name='Photo Album', editable=False)
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)

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

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
######Photo Album Model END#############
