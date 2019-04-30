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

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name