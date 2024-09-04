from django.db import models
from django.contrib.auth.models import User
from categories.models import Category


# Class provided by DRF-API walkthrough.
class Post(models.Model):
   
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_post_ml2gkn', blank=True
    )
   
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 

    class Meta:
        """
        Order posts by date created.
        Display by most recent first.
        """
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title} {self.content}'
