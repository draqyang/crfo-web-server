#-*- encoding: utf-8 -*-
from django.db import transaction
from django.db import models 

from django.utils.decorators import method_decorator
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.html import escape
from django.utils.safestring import mark_safe

from django.contrib import admin
from django.contrib.auth.models import User 
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.forms import AdminPasswordChangeForm, UserCreationForm
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect

from main.models import *

csrf_protect_m = method_decorator(csrf_protect)

class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False
    verbose_name_plural = u'會員'
    
class UserAdmin(UserAdmin):
    inlines = (MemberInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Member)