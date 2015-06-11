from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notice(models.Model):
    #outdated event won't be displayed according to event_time
    event_time = models.DateTimeField('Event Time',
            help_text='The notice will be displayed until the specified event time')
    desc = models.TextField('Notice Content')
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)
    owner = models.ForeignKey(User, limit_choices_to={'is_staff': True},
            editable=False, verbose_name='Publisher')

    def __unicode__(self):
        return str(self.owner) + ': ' + self.desc[:10] + ' ...'
    def __str__(self):
        return str(self.owner) + ': ' + self.desc[:10] + ' ...'

class Event(models.Model):
    #outdated event won't be displayed according to event_time
    event_time = models.DateTimeField('Event Time',
            help_text='The event will be displayed until the specified event time')
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)
    location = models.CharField('Location', max_length=50)
    title = models.CharField('Event Summary', max_length=50)
    desc = models.TextField('Event Description')
    owner = models.ForeignKey(User, verbose_name='Publisher', editable=False)
    pdf = models.FileField(verbose_name = 'Flyer PDF', upload_to='pdfs', null=True, blank=True)

    def __unicode__(self):
        return str(self.owner) + ': ' + self.title[:10] + ' ...'
    def __str__(self):
        return str(self.owner) + ': ' + self.title[:10] + ' ...'

class Fellowship(models.Model):

    name = models.CharField('Fellowship Name', max_length=50,
            help_text='團契名稱')
    desc = models.TextField('Fellowship Description')
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
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

class FellowshipMessage(models.Model):

    msg = models.TextField('Message')
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)
    fellowship = models.ForeignKey(Fellowship, verbose_name='Fellowship')
    owner = models.ForeignKey(User, verbose_name='Publisher', editable=False)

    def __unicode__(self):
        return self.fellowship.name + ': ' + self.msg[:10] + ' ...'
    def __str__(self):
        return self.fellowship.name + ': ' + self.msg[:10] + ' ...'

class About(models.Model):
    pub_time = models.DateTimeField('Time Published', auto_now=True)
    desc = models.TextField('Church Description',
            help_text='The content will be displayed in the column of 教會簡介')
    pastor = models.CharField('Pastor Names', max_length=50)
    pastor_profile = models.TextField('Pastor Profile',
            help_text='The content will be displayed in the column of 牧者簡介')
    faith = models.TextField('Faith Statement',
            help_text='信仰告白')
    def __unicode__(self):
        return self.pastor
    def __str__(self):
        return self.pastor

class YearlyTheme(models.Model):
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)
    theme = models.CharField('Theme', max_length=100,
            help_text='教會年度主題 (字數限制, 50 字)')
    desc = models.TextField('Description',
            help_text = '教會年度主題詳盡說明 (字數不限)')

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
