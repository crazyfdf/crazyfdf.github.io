from django.contrib import admin

from eva.models import UserProfile
from eva.models import Userinfo
from eva.models import Personalauthentication

# Register your models here.
admin.site.register(Userinfo)
admin.site.register(UserProfile)
admin.site.register(Personalauthentication)




