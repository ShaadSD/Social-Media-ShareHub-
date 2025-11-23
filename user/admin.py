from django.contrib import admin
from .models import AuthorAccount,Follower


class UserAdmin(admin.ModelAdmin):
      list_display =['id','username', 'first_name', 'last_name', 'email']


admin.site.register(AuthorAccount,UserAdmin)
    
admin.site.register(Follower)
