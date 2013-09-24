#-*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from mezzanine.core.fields import FileField, RichTextField
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from mezzanine.core.models import TimeStamped, Displayable, Orderable
from django.core.validators import MinValueValidator, MaxValueValidator



#廣告顯示區塊
AD_DISPLAY_CHOICES = (
    ("index", u"首頁"),
    ("product", u"商品主頁"),
    ("product_content", u"商品內頁"),
    ("recipe", u"食譜主頁"),
    ("recipe_content", u"食譜內頁"),
    ("account", u"資料維護"),
    ("order", u"訂單維護"),
)

class PictureBase(models.Model):
    picture = models.ImageField(u"顯示圖片", upload_to="pics")

    class Meta:
        abstract = True

class Ad(TimeStamped):
    title = models.CharField(u"名稱", max_length=200)
    picture = models.ImageField(u"顯示圖片", upload_to="ads")
    link = models.URLField(u"連結目標")
    display = models.CharField(u'顯示位置', max_length=20, choices=AD_DISPLAY_CHOICES)
    status = models.BooleanField(u"發布狀態", default=False, help_text=u"勾選即可發布於前台")
    
    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'廣告')
        verbose_name_plural = _(u'廣告區塊')
              
class PersonalBaseModel(models.Model):
    name = models.CharField(_(u"姓名"), max_length=255,blank=True, null=True)
    phone = models.CharField(_(u"電話"), max_length=255, blank=True, null=True)
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return self.name

class ContentBaseModel(models.Model):
    name =  models.CharField(_(u"名稱"), max_length=255)
    content = RichTextField(_(u"內容"))
    
    class Meta:
        abstract = True
        
class Employee(PersonalBaseModel, TimeStamped):
    employee_num = models.CharField(u"原始業務編號", max_length=255, db_index=True)
    class Meta:
        verbose_name = _(u'業務')
        verbose_name_plural = _(u'業務列表')

class Member(PersonalBaseModel, TimeStamped):
    user = models.OneToOneField(User)
    member_num = models.CharField(u"原始會員編號", max_length=255)
    address = models.CharField(u"送貨地址", max_length=255)
    employee = models.ForeignKey(Employee, verbose_name = u'負責業務', blank=True, null=True)
    
    def __unicode__(self):
        return self.username
        
    class Meta:
        verbose_name = _(u'會員')
        verbose_name_plural = _(u'會員列表')
        
CATEGORY_CHOICES = (
    ('category1', u'分類1'),
    ('category2', u'分類2'),
    ('category3', u'分類3'),
    ('category4', u'分類4'),
    ('category5', u'分類5'),
    ('category6', u'分類6'),
)
    
class cuisine(ContentBaseModel, TimeStamped):
    category = models.CharField(u"分類", max_length="50", choices=CATEGORY_CHOICES)
    price = models.IntegerField(u"價格", validators=[MinValueValidator(0)])
    author = models.ForeignKey(Member, verbose_name=u'會員')
    class Meta:
        verbose_name = _(u'菜單')
        verbose_name_plural = _(u'菜單列表')
    
    
class Recipe(ContentBaseModel):
    video = FileField(verbose_name=_(u"上傳影片"), upload_to="video", format="Video", max_length=255, null=True, blank=True)
    video_link = models.URLField(verbose_name=_(u"影片連結"), null=True, blank=True)
    quantity = models.IntegerField(u'單位數量', blank=True, null=True, validators=[MinValueValidator(0)])
    cooktime = models.IntegerField(u'料理時間', blank=True, null=True, validators=[MinValueValidator(0)], help_text=u"單位:分鐘")
    class Meta:
        verbose_name = _(u'食譜')
        verbose_name_plural = _(u'食譜')
        
class RecipePicture(PictureBase):
    recipe = models.ForeignKey(Recipe, verbose_name = u'食譜')
    class Meta:
        verbose_name = u'食譜照片'
        verbose_name_plural = u'食譜照片'
        
        
class RecipeUtensil(models.Model):
    recipe = models.ForeignKey(Recipe, verbose_name = u'食譜')
    name = models.CharField(u'用具', blank=True, null=True, max_length=50)
    quantity = models.IntegerField(u'單位數量', blank=True, null=True, validators=[MinValueValidator(0)])
    unit = models.CharField(u'單位', blank=True, null=True, max_length=50)
    class Meta:
        verbose_name = u'用具'
        verbose_name_plural = u'用具清單'
        
class RecipeFood(models.Model):
    recipe = models.ForeignKey(Recipe, verbose_name = u'食譜')
    name = models.CharField(u'食材', blank=True, null=True, max_length=50)
    quantity = models.IntegerField(u'單位數量', blank=True, null=True, validators=[MinValueValidator(0)])
    unit = models.CharField(u'單位', blank=True, null=True, max_length=50)
    class Meta:
        verbose_name = u'食材'
        verbose_name_plural = u'食材清單'

class RecipeStep(PictureBase):
    recipe = models.ForeignKey(Recipe, verbose_name = u'食譜')
    order = models.IntegerField(u'步驟', blank=True, null=True, validators=[MinValueValidator(0)])
    text = models.CharField(u'文字敘述', blank=True, null=True, max_length=50)
    class Meta:
        verbose_name = u'步驟'
        verbose_name_plural = u'作法步驟'

class Product(ContentBaseModel):
    