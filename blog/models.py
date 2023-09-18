from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User



class Blog (models.Model):
    title = models.CharField(max_length=500 , unique=True)
    description = models.TextField()
    image = models.FileField(blank=True)
    body = RichTextField()
    category = models.ManyToManyField('blog.BlogCategory')
    created = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=500 , unique=True)

    def __str__ (self):
        return {self.title}


class BlogCategory(models.Model):
    category = models.CharField(max_length=250)
    homepage = models.BooleanField(default=False)


    def __str__ (self):
        return self.category
    

class BlogComment (models.Model):
    username = models.CharField(max_length=250)
    blog_post = models.ForeignKey(Blog , on_delete=models.PROTECT , related_name='comment')
    body = models.TextField()
    publish = models.BooleanField(default=False)
    admin_reply = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body