from django.db.models import fields
from rest_framework import serializers
from blog.models import Post

class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = ['id', 'title', 'slug', 'body', 'published', 'created_at', 'updated_at']