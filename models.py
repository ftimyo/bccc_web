from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notice(models.Model):
    #outdated event won't be displayed according to event_time
    event_time = models.DateTimeField('Event Time')
    desc = models.TextField('Notice Content')
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)
    owner = models.ForeignKey(User, limit_choices_to={'is_staff': True},
            editable=False, verbose_name="Publisher")

    def __unicode__(self):
        return str(self.owner) + ': ' + self.desc[:10] + ' ...'
    def __str__(self):
        return str(self.owner) + ': ' + self.desc[:10] + ' ...'

class Event(models.Model):
    #outdated event won't be displayed according to event_time
    event_time = models.DateTimeField('Event Time')
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)
    location = models.CharField('Location', max_length=50)
    title = models.CharField('Event Summary', max_length=50)
    desc = models.TextField('Event Description')
    owner = models.ForeignKey(User, verbose_name="Publisher", editable=False)
    pdf = models.FileField(verbose_name = "Flyer", upload_to='pdfs', null=True, blank=True)

    def __unicode__(self):
        return str(self.owner) + ': ' + self.title[:10] + ' ...'
    def __str__(self):
        return str(self.owner) + ': ' + self.title[:10] + ' ...'

class Fellowship(models.Model):

    name = models.CharField('Fellowship Name', max_length=50)
    desc = models.TextField('Fellowship Description')
    location = models.CharField('Location', max_length=50)

    dp_order = models.IntegerField('Display Order', default=2)

    #contact info
    admin = models.CharField('Person in Charge', max_length=20)
    admin_email = models.EmailField('Email')
    admin_phone = models.CharField('Phone', max_length=16)
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

class FellowshipMessage(models.Model):

    msg = models.TextField('Message')
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)
    fellowship = models.ForeignKey(Fellowship, verbose_name='Fellowship')
    owner = models.ForeignKey(User, verbose_name="Publisher", editable=False)

    def __unicode__(self):
        return self.fellowship.name + ': ' + self.msg[:10] + ' ...'
    def __str__(self):
        return self.fellowship.name + ': ' + self.msg[:10] + ' ...'
