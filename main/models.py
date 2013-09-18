from django.db import models

from mezzanine.core.fields import FileField, RichTextField
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

# Create your models here.

class ContentBaseModel(models.Model):
    name =  models.CharField(_(u"標題"), max_length=255)
    content = RichTextField(_(u"內容"))
    class Meta:
        abstract = True
        
class TimeBaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
class Member(TimeBaseModel):
    user = models.OneToOneField(User)
    address = models.CharField(_(u"送貨地址"), max_length=255)
    telphone = models.CharField(_(u"電話"), max_length=255)
    cellphone = models.CharField(_(u"手機"), max_length=255)
    
    def __unicode__(self):
        return user