from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from redactor.fields import RedactorField
from .utils import MediaFileSystemStorage
import hashlib
import datetime
import os

class About(models.Model):
    desc = RedactorField(verbose_name='教會簡介', redactor_options={'focus': 'true'},
            allow_file_upload=False, allow_image_upload=False)
    pastor = models.CharField('牧者', max_length=50, help_text='限50字')
    pastor_profile = RedactorField(verbose_name='牧者介紹', redactor_options={'focus': 'true'},
            allow_file_upload=False, allow_image_upload=False)
    faith = RedactorField(verbose_name='信仰告白', redactor_options={'focus': 'true'},
            allow_file_upload=False, allow_image_upload=False)

    update_time = models.DateTimeField('修改時間', auto_now=True)

    def __unicode__(self):
        return self.pastor
    def __str__(self):
        return self.pastor

class YearlyTheme(models.Model):
    title = models.CharField('教會年度主題', max_length=100, help_text='限50字')
    text = RedactorField(verbose_name='主題內容', redactor_options={'focus': 'true'},
            allow_file_upload=False, allow_image_upload=False)

    pub_time = models.DateTimeField('發布時間', auto_now_add=True)

    class Meta:
        ordering = ['-pub_time']

    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.title


class Contact(models.Model):
    title = models.CharField('聯絡信息標題', max_length=50, help_text='限50字')
    address = models.CharField('地址', max_length=255, help_text='限255字')
    phone = models.CharField('電話', max_length=16, help_text='格式: <em>XXX-XXX-XXXX</em>')
    email = models.EmailField('Email')
    latitude = models.DecimalField('地址緯度',
        help_text='可從此網站獲得 http://www.mapcoordinates.net',
            max_digits=20, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField('地址經度',
        help_text='可從此網站獲得 http://www.mapcoordinates.net',
            max_digits=20, decimal_places=10, null=True, blank=True)

    update_time = models.DateTimeField('修改時間', auto_now=True)

    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.title

######Notice############################
class Notice(models.Model):
    effective_date = models.DateField('有效日期', help_text='格式YYYY-MM-DD')
    desc = RedactorField(verbose_name='通知內容', redactor_options={'focus': 'true'},
            allow_file_upload=False, allow_image_upload=False)
    pub_time = models.DateTimeField('發布時間', auto_now_add=True)
    owner = models.ForeignKey(User, editable=False, verbose_name='發布者')

    class Meta:
        ordering = ['-effective_date']

    def is_effective_notice(self):
        return self.effective_date >= timezone.now().date() - datetime.timedelta(days=1)

    is_effective_notice.admin_order_field = 'effective_date'
    is_effective_notice.boolean = True
    is_effective_notice.short_description = '有效?'
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

    if not h:
        md5 = hashlib.md5()
        for chunk in instance.flyer.chunks():
            md5.update(chunk)
        h = md5.hexdigest()
        instance.md5sum = h

    return os.path.join('flyer', h[0:1], h[1:2], h + ext.lower())

class Event(models.Model):
    event_date = models.DateField('活動日期', help_text='格式YYYY-MM-DD')
    event_time = models.TimeField('活動時間 (Optional)',
            help_text='格式HH:MM:SS (二十四小時)', null=True, blank=True)
    location = models.CharField('活動地點', max_length=50, help_text='限50字')

    title = models.CharField('活動標題', help_text='限50字', max_length=50)
    text = RedactorField(verbose_name='活動詳情 (Optional)', null=True, blank=True,
            redactor_options={'focus': 'true'},
            allow_file_upload=False, allow_image_upload=False)

    flyer = models.ImageField(verbose_name='活動宣傳圖片 (Optional)',
            upload_to=rename_flyer, blank=True)

    md5sum = models.CharField(max_length=36, editable=False)

    def attachments(self):
        return self.eventattachment_set.all()

    #Auto Generated Fields
    owner = models.ForeignKey(User, verbose_name='發布者', editable=False)
    pub_time = models.DateTimeField('發布時間', auto_now_add=True)

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

    admin_image.short_description = '活動宣傳圖片預覽'
    admin_image.allow_tags = True
    show_flyer.allow_tags = True

    def is_effective_event(self):
        return self.event_date >= timezone.now().date() - datetime.timedelta(days=1)

    is_effective_event.admin_order_field = 'effective_date'
    is_effective_event.boolean = True
    is_effective_event.short_description = '有效?'
    is_effective_event.allow_tags = True


    def save(self, *args, **kwargs):
        if not self.pk and self.flyer:
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
    name = models.CharField('附件名稱 (限50字)', max_length=255)
    attach = models.FileField(verbose_name='附件', upload_to=rename_event_file)
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

    name = models.CharField('團契間稱', max_length=20, help_text = '限20字')
    full_name = models.CharField('團契全稱', max_length=50, help_text='限50字')
    desc = RedactorField(verbose_name='團契(事工)介紹', redactor_options={'focus': 'true'},
            allow_file_upload=False, allow_image_upload=False)
    location = models.CharField('地點', max_length=50, help_text='限50字', blank=True, null=True)
    schedule = models.CharField('團契時間', max_length=50, blank=True, null=True,
            help_text='(限50字), 例如: 每週五 晚上7:30.')

    #contact info
    admin = models.CharField('負責人', max_length=20, help_text = '限50字', blank=True, null=True)
    admin_email = models.EmailField('Email', blank=True, null=True)
    admin_phone = models.CharField('電話', max_length=16, help_text='格式: <em>XXX-XXX-XXXX</em>', blank=True, null=True)
    admin_other = models.CharField('其他聯絡方式', max_length=100,
            help_text='例如: QQ, Wechat, facebook等.', blank=True, null=True)

    #display option
    display = models.BooleanField('在網站上顯示?', default=True)
    priorities = zip(range(0,5), range(0, 5))
    priority = models.IntegerField('顯示優先次序', default = 2, choices=priorities,
            help_text='0為最高優先級, 默認為2')

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

    fellowship = models.ForeignKey(Fellowship, verbose_name='選擇資訊所屬團契(事工)')
    effective_date = models.DateField('有效日期', help_text='格式:YYYY-MM-DD')
    title = models.CharField('資訊標題', max_length=50, help_text='限50字')
    text = RedactorField(verbose_name='資訊詳情 (Optional)', null=True, blank=True,
            redactor_options={'focus': 'true'},
            allow_file_upload=False, allow_image_upload=False)

    def attachments(self):
        return self.messageattachment_set.all()

    #Auto Generated Fields
    pub_time = models.DateTimeField('發布時間', auto_now_add=True)
    owner = models.ForeignKey(User, verbose_name='發布者', editable=False)

    #Order by effective_time
    class Meta:
        ordering = ['effective_date']

    def is_effective_msg(self):
        return self.effective_date >= timezone.now().date() - datetime.timedelta(days=1)

    is_effective_msg.admin_order_field = 'effective_date'
    is_effective_msg.boolean = True
    is_effective_msg.short_description = '有效?'
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
    name = models.CharField('附件名稱 (限255字)', max_length=255)
    attach = models.FileField(verbose_name = '附件', upload_to=rename_message_file)
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
    name = models.CharField('證道信息類別名稱', max_length=50, help_text='限50字')

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

class Sermon(models.Model):
    title = models.CharField('證道信息標題', max_length=100, help_text='限100字')
    author = models.CharField('作者', max_length=50, help_text='限50字')
    keywords = models.CharField('關鍵字', max_length=50, help_text='限50字')
    text = RedactorField(verbose_name='證道信息文本 (Optional)', null=True, blank=True,
            redactor_options={'focus': 'true'},
            allow_file_upload=False, allow_image_upload=False)
    catalog = models.ForeignKey(SermonCatalog, verbose_name='選擇證道信息類別')

    def attachments(self):
        return self.sermondocument_set.all()

    #Auto Generated Field
    pub_time = models.DateTimeField('發布時間', auto_now_add=True)

    class Meta:
        ordering = ['-pub_time']

    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.title

def rename_sermon_file(instance, filename):
    h = instance.md5sum
    basename, ext = os.path.splitext(filename)
    return os.path.join('sermon', h[0:1], h[1:2], h + ext.lower())

class SermonDocument(models.Model):
    name = models.CharField('附件文件名稱 (限255字)', max_length=255)
    attach = models.FileField(verbose_name='附件', upload_to=rename_sermon_file)
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
    name = models.CharField('相簿名稱', max_length=255, help_text = '限255字')
    pub_time = models.DateTimeField('發布時間', auto_now_add=True)
    album = models.BooleanField('在網頁中顯示該相簿?', default=False)

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
    carousel = models.BooleanField('在首頁顯示?', default=False)
    name = models.CharField('相片標題', max_length=255, help_text='限255字')
    image = models.ImageField(verbose_name = '相片文件', upload_to=rename_photo)
    album = models.ForeignKey(PhotoAlbum, verbose_name='相簿',
            editable=True, help_text='選擇所屬相冊')
    pub_time = models.DateTimeField('發布時間', auto_now_add=True)

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

    thumbnail.short_description = '預覽'
    thumbnail.allow_tags = True

    photo_size.short_description = "尺寸"
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
