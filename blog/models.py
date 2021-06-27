from django.db import models
from django.utils.text import slugify

class Post(models.Model):
  title = models.CharField(blank=False, max_length=300)
  slug = models.SlugField(blank=True)
  body = models.TextField()
  published = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return "{}".format(self.title)

  class Meta:
    ordering = ['created_at']

  def save(self, *args, **kwargs):
    self.slug = slugify(self.title)
    super().save(*args, **kwargs)