from django.db import models

# Create your models here.
from userinfo.models import UserInfo


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField(null=True)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author, null=True)
    n_comments = models.IntegerField(default=0)
    n_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField()

    def __str__(self):
        return self.headline

class Test_Entry(models.Model):
    body_text = models.TextField()

