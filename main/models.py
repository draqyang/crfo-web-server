from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from mezzanine.core.fields import FileField, RichTextField
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

# Create your models here.

class PersonalBaseModel(models.Model):
    name = models.CharField(_(u"姓名"), max_length=255)
    cellphone = models.CharField(_(u"手機"), max_length=255)
    email = models.EmailField(_(u"電子信箱"), max_length=255, unicode)
    class Meta:
        abstract = True
    def __unicode__(self):
        return self.name

class ContentBaseModel(models.Model):
    name =  models.CharField(_(u"名稱"), max_length=255)
    content = RichTextField(_(u"內容"))
    class Meta:
        abstract = True
        
class TimeBaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        

class Member1(TimeBaseModel):
    user = models.OneToOneField(User)
    address = models.CharField(_(u"送貨地址"), max_length=255)
    telphone = models.CharField(_(u"電話"), max_length=255)
    cellphone = models.CharField(_(u"手機"), max_length=255)
    def __unicode__(self):
        return self.user.username
    class Meta:
        verbose_name = _(u'會員 one to one')
        verbose_name_plural = _(u'會員 one to one')
        
class Employee(PersonalBaseModel, TimeBaseModel):
    class Meta:
        verbose_name = _(u'員工,業務')
        verbose_name_plural = _(u'員工,業務')
        
class Member2(AbstractBaseUser, PersonalBaseModel, TimeBaseModel):
    address = models.CharField(_(u"送貨地址"), max_length=255)
    telphone = models.CharField(_(u"電話"), max_length=255)
    cellphone = models.CharField(_(u"手機"), max_length=255)
    type = models.CharField(_(u"帳號"), max_length=255)
    empoyee = models.ManyToManyField(Employee)
    recipe = models.ManyToManyField(Recipe)
    class Meta:
        verbose_name = _(u'會員 繼承 AbstractBaseUser')
        verbose_name_plural = _(u'會員 繼承 AbstractBaseUser')


    
class Recipe(TimeBaseModel, ContentBaseModel):
    
    class Meta:
        verbose_name = _(u'食譜')
        verbose_name_plural = _(u'食譜')
        
