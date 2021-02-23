from django.db import models
from django.utils.translation import gettext as _


class UserProfile(models.Model):
    login = models.CharField(max_length=50,unique=True, verbose_name=_('Name'))
    is_online = models.BooleanField(default=False)


class UserConnection(models.Model):
    sid = models.CharField(max_length=250,unique=True, verbose_name=_('SID'))
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class Sdp(models.Model):
    sdp = models.TextField(verbose_name=_('Sdp'))
    conn = models.ForeignKey(UserConnection, on_delete=models.CASCADE)


class Ice(models.Model):
    ice = models.TextField(verbose_name=_('Ice'))
    sdp = models.ForeignKey(Sdp, on_delete=models.CASCADE)