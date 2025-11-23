from django.db import models
from user.models import AuthorAccount


class ContactUs(models.Model):
    user = models.ForeignKey(AuthorAccount, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=40)
    email=models.CharField(max_length=50)
    message=models.TextField()
    
    def __str__(self):
        return self.email
    class Meta:
        verbose_name_plural="Contact Us"