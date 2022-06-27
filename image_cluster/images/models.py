from distutils.command.upload import upload
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Image(models.Model):
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False, verbose_name=_('owner'), related_name='image' )
    image = models.ImageField(_('image'),null=False, blank=False, upload_to='images/user_uploaded_images')
    image_name = models.CharField(_('image name'), max_length=250, unique=False) # Needs to be cnaged to detect and ingnore nonunique values.
    is_image_grouped = models.BooleanField(_('is image grouped'), null=True, blank=True)
    image_group = models.CharField(_('image group'), max_length=5, unique=False, null=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

