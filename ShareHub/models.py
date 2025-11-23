from django.db import models
from user.models import AuthorAccount


class PostCreate(models.Model):
    image = models.URLField(max_length=200, blank=True, null=True)
    video = models.URLField(max_length=200, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(AuthorAccount, on_delete=models.CASCADE, related_name='created_posts')

    def __str__(self):
        return f"post created by {self.created_by.username}"

class Like(models.Model):
    like_post = models.ForeignKey(PostCreate, on_delete=models.CASCADE)
    user = models.ForeignKey(AuthorAccount, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('like_post', 'user')

    def __str__(self):
        return f'like by {self.user.username}'

class Comment(models.Model):
    commentpost = models.ForeignKey(PostCreate, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(AuthorAccount, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f'comment by {self.user.username}'