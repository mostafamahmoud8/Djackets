from django.db import models
from django.core.files import File
from django.utils.text import slugify
from django.urls import reverse
from io import BytesIO

from PIL import Image
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ("name",)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('',kwargs={'slug':self.slug}) 
    
    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_added",)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product:detail',kwargs={'slug':self.slug}) 
    
    def __str__(self) -> str:
        return self.name
    
    def get_image(self):
        if self.image:
            return self.image.url
        return ''
    
    def make_thumbnail(self, image, size=(300,200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
        else:
            return ''
            