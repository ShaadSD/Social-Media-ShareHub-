from django.contrib import admin
from .models import AuthorAcount,Follower,Following
admin.site.register(AuthorAcount)
admin.site.register(Follower)
admin.site.register(Following)
# Register your models here.