#-*- encoding: utf-8 -*-
from django.db import transaction
from django.db import models 

from django.utils.decorators import method_decorator
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.html import escape
from django.utils.safestring import mark_safe

from django.contrib import admin
# from django.contrib.auth.models import User 
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.forms import AdminPasswordChangeForm, UserCreationForm
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect

from main.models import *
# from main.forms import *
from django.contrib.auth.models import AbstractUser
csrf_protect_m = method_decorator(csrf_protect)

#廣告區塊
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_picture', 'link', 'display', 'status_boolean')
    fields = ('title', 'link', 'display', 'status')
    list_filter = ('display','status', )
    search_fields = ('display','status', )
    list_display_links = ('title', 'display_picture', )
    
    def display_picture(self, obj):
        return u"<img src='/static/media/%s' width='200px' border='0px'/>" % obj.picture
    display_picture.shor_description = u"廣告圖片"
    display_picture.allow_tags = True
    def status_boolean(self, obj):
        if obj.status == True:
            return u"是"
        else:
            return u"否"
    status_boolean.short_description = _(u"發布")
admin.site.register(Ad, AdAdmin)

#Member 
# class MemberAdmin(UserAdmin):
    # add_form = MemberCreateForm
    # form = MemberChangeForm
    
    # list_display = ('username', 'email', 'member_number', 'name', 'employee', 'is_superuser')
    # list_filter = ('employee', 'is_superuser')
    # search_fields = ('username', 'email', 'member_number', 'name', 'employee')
    # ordering = ('member_number','username', )
    
    # filter_horizontal = ('groups', 'user_permissions',)
    # fieldsets = (
        # (None, {'fields': ('username','member_num', 'email', 'password')}),
        # ('Personal info', {'fields':('name','telphone','address','employee', )}),
        # ('Permissions', {'fields': ('is_active',
                                # 'is_staff',
                                # 'is_superuser',
                                # 'groups',
                                # 'user_permissions')}),
        # ('Important dates', {'fields': ('last_login',)}),
    # )
    
    # add_fieldsets = (
        # (None, {
            # 'classes': ('wide',),
            # 'fields': ('username', 'email',
                        # 'password1', 'password2')}
        # ),
    # )

# admin.site.register(Member, MemberAdmin)

class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False
    verbose_name_plural = u'會員'
    
class UserAdmin(UserAdmin):
    inlines = (MemberInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# admin.site.register(Member1)
# admin.site.register(Member2)