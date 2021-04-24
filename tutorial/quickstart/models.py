from django.db import models


class Tweet(models.Model):
    text = models.TextField(max_length=280)
    photo = models.URLField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'[{self.author.username}]{self.text}'


class Followers(models.Model):
    follower = models.ForeignKey(
        'auth.User', related_name='follows', on_delete=models.CASCADE)
    follows = models.ForeignKey(
        'auth.User', related_name='followers', on_delete=models.CASCADE)
    followed = models.DateTimeField(auto_now_add=True)
