from django.db import models

# Create your models here.
from userinfo.models import UserInfo


class Blog(models.Model):
    # 博客名
    name = models.CharField(max_length=100)
    # 个性答名
    tagline = models.TextField(null=True)
    # 博客用户
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "博客"
        verbose_name_plural = verbose_name


class Author(models.Model):
    name = models.CharField(max_length=200)
    author = models.OneToOneField(UserInfo,on_delete=models.CASCADE, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "作者"
        verbose_name_plural = verbose_name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    abstract = models.TextField(max_length=255, null=True)
    body_text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)
    authors = models.ManyToManyField(Author, blank=True)
    n_comments = models.IntegerField(default=0)
    n_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.headline

    class Meta:
        verbose_name = "博文"
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return "%s/article/details/%d"%(self.blog.user.username, self.id)

class Tag(models.Model):
    category = models.CharField(max_length=30)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)


class Test_Entry(models.Model):
    body_text = models.TextField()

