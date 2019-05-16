from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=12)
    sex = models.BooleanField(default=0)
    is_active = models.BooleanField(default=0)
    is_superuser = models.BooleanField(default=0)
    date_join = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    email = models.EmailField(null=True)

    followers = models.ManyToManyField("self", through="Contact", symmetrical=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class Contact(models.Model):
    user_from = models.ForeignKey(UserInfo, related_name="rel_from_set", on_delete=models.CASCADE)
    user_to = models.ForeignKey(UserInfo, related_name="rel_to_set", on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created",)
        verbose_name="关注"
        verbose_name_plural=verbose_name

    def __str__(self):
        return "{} 关注了 {}".format(self.user_from, self.user_to)
