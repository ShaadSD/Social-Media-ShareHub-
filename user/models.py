from django.contrib.auth.models import AbstractUser
from django.db import models

class AuthorAccount(AbstractUser):
    image = models.URLField(max_length=200, default="https://media.istockphoto.com/id/2164630967/vector/people-and-person-icon-people-icon-with-modern-flat-design-people-vector-icon-isolated-on.jpg?s=612x612&w=0&k=20&c=lFYjLbYqoPpRsIGAPr3NUAAIR9k6uLqIWFerhR4F0c4=")
    bio = models.TextField(blank=True)
    about = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Follower(models.Model):
    main_user = models.ForeignKey(
        AuthorAccount,
        related_name='followers',
        on_delete=models.CASCADE
    )
    follower = models.ForeignKey(
        AuthorAccount,
        related_name='following',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('main_user', 'follower')

    def __str__(self):
        return f"{self.follower.username} follows {self.main_user.username}"


