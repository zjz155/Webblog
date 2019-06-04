from django.db import models

# Create your models here.
from userinfo.models import UserInfo


class Blog(models.Model):
    # 博客名
    name = models.CharField(max_length=100)
    # 个性答名
    tagline = models.TextField(null=True)

    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "博客"
        verbose_name_plural = verbose_name


class Entry(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    # 博客用户
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    abstract = models.TextField(max_length=255, null=True)
    body_text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)

    n_comments = models.IntegerField(default=0)
    n_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    blog = models.ManyToManyField(Blog, through="Comment", through_fields=("entry", "blog"))

    def __str__(self):
        return self.headline

    class Meta:
        verbose_name = "博文"
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post-detail', args=[self.user.username, str(self.id)])
        # return "%s/article/details/%d"%(self.blog.user.username, self.id)


class Comment(models.Model):
    entry = models.ForeignKey(Entry, related_name="entry_comment_set", on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,related_name="blog_comment_set", on_delete=models.CASCADE)

    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    replys = models.ManyToManyField(Blog, through="Reply", through_fields=("comment", "reply_from"))
    class Meta:
        ordering = ("created",)
        verbose_name="评论"
        verbose_name_plural=verbose_name

    def __str__(self):
      return "{} : {} 评论了 {}".format("comment_id:" + str(self.id),self.blog, self.entry)

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply_from = models.ForeignKey(Blog, related_name="reply_from_set", on_delete=models.CASCADE)

    reply_to = models.ForeignKey(Blog, related_name="reply_to_set", on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    class Meta:
        ordering = ("created",)
        verbose_name = "回复"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} 回复了 {}".format(self.reply_from.name, self.reply_to.name)


class Tag(models.Model):
    tag = models.CharField(max_length=30)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

class Category(models.Model):
    category = models.CharField(max_length=30)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category




class Test_Entry(models.Model):
    MEDIA_CHOICES = (
        ('Audio', (
            ('vinyl', 'Vinyl'),
            ('cd', 'CD'),
        )
         ),
        ('Video', (
            ('vhs', 'VHS Tape'),
            ('dvd', 'DVD'),
        )
         ),
        ('unknown', 'Unknown'),
    )
    test = models.CharField(max_length=20, default="myproduct")
    stauts = models.CharField(max_length=20, choices=MEDIA_CHOICES, default="unknown")






