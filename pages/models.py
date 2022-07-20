from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactModel(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('name'))
    email = models.EmailField(verbose_name=_('email'))
    message = models.TextField(verbose_name=_('message'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')


class HomePageBannerModel(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('title'))
    collections = models.CharField(max_length=30, verbose_name='collections')
    body = models.TextField(verbose_name=_('body'))
    image = models.ImageField(upload_to='home-page_banner/', verbose_name=_('home page banner'))
    is_active = models.BooleanField(default=False, blank=True, verbose_name=_('is active'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('main banner')
        verbose_name_plural = _('main banners')