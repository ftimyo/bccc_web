from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notice(models.Model):
    #outdated event won't be displayed according to event_time
    event_time = models.DateTimeField('Event Time')
    desc = models.CharField('Notice Content', max_length=500)
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)
    owner = models.ForeignKey(User, limit_choices_to={'is_staff': True}, verbose_name="Publisher")

class Event(models.Model):
    #outdated event won't be displayed according to event_time
    event_time = models.DateTimeField('Event Time')
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)
    location = models.CharField('Location', max_length=150)
    title = models.CharField('Event Summary', max_length=150)
    desc = models.CharField('Event Description', max_length=800)
    owner = models.ForeignKey(User, verbose_name="Publisher")
    pdf = models.FileField(verbose_name = "Flyer", upload_to='pdfs')

class Fellowship(models.Model):

    name = models.CharField('Fellowship Name', max_length=100)
    desc = models.CharField('Fellowship Description', max_length=1000)
    location = models.CharField('Location', max_length=100)

    dp_order = models.IntegerField('Display Order')

    #contact info
    admin = models.CharField('Person in Charge', max_length=30)
    admin_email = models.EmailField('Email')
    admin_phone = models.CharField('Phone', max_length=16, blank = True)

class FellowshipMessage(models.Model):
    msg = models.CharField('Message', max_length=150)
    pub_time = models.DateTimeField('Time Published', auto_now_add=True)
    fellowship = models.ForeignKey(Fellowship, verbose_name='Fellowship')
    owner = models.ForeignKey(User, verbose_name="Publisher")
