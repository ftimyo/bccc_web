from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

def rename_flyer(instance, filename):
    ext = filename.split('.')[-1]
    filename = "flyer_%s.%s" % (instance.id, ext)
    return filename

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
    flyer = models.FileField(verbose_name = 'Flyer File', upload_to=rename_flyer, null=True, blank=True)

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
    author = models.CharField('Author', max_length=20)
    content = models.TextField('Sermon Content')

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
