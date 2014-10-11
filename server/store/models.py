from django.db import models

# Create your models here.
class userDetail (models.Model):
    uname    = models.CharField (max_length = 20)
    email    = models.EmailField ()
    phone    = models.IntegerField()
    msg      = models.CharField (max_length = 300)
    homelo   = models.DecimalField(max_digits=9, decimal_places=6)
    homela   = models.DecimalField(max_digits=9, decimal_places=6)
    officelo = models.DecimalField(max_digits=9, decimal_places=6)
    officela = models.DecimalField(max_digits=9, decimal_places=6)

class authDb (models.Model):
    from_user = models.CharField (max_length = 20)
    to_user   = models.CharField (max_length = 20)
    re_status = models.CharField (max_length = 30)

class logDb (models.Model):
    from_user = models.CharField (max_length = 20)
    to_user   = models.CharField (max_length = 20)
    re_type   = models.CharField (max_length = 30)
    re_msg    = models.CharField (max_length = 30)
