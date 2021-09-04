from django.db import models
from piblitz_org.utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
# Create your models here.



class Organisation(models.Model):
    
    name=models.CharField(max_length=20 ,null=True )
    slug = models.SlugField(unique=True)
    description=models.TextField(max_length=200 , null=True)
    country=models.CharField(max_length=30 , null=True)
    state=models.CharField(max_length=20 , null=True)
    city=models.CharField(max_length=30 , null=True)
    logo =models.ImageField(upload_to='images/', null=True, blank=True)
    owner=models.ForeignKey(User, on_delete=models.CASCADE , related_name='administrator')
    members=models.ManyToManyField(User)


    def __str__(self):
        return self.name


def save_name_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(save_name_slug, sender=Organisation)




