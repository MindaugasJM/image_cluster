from distutils.command.upload import upload
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import os

def image_path_n_file_name(instance, filename):
    last_img_id = Image.objects.values_list('id',flat=True).last()
    # if last_img_id == None: last_img_id = 1
    name_of_file = str(last_img_id)+str(filename)
    custom_path = 'images/user_uploaded_images/'
    return custom_path+name_of_file

    
class Image(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=False, blank=False, verbose_name=_('owner'), related_name='image' )
    image = models.ImageField(_('image'),null=False, blank=False, upload_to=image_path_n_file_name)
    image_name = models.CharField(_('image name'), max_length=250, unique=False)
    image_group = models.IntegerField (_('image group'), unique=False, null=True)

    def __str__(self):
        return f' {self.owner}, {self.image_name}, {self.image_group}, {self.image}' 

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

