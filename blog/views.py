from django.http import Http404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from blog.models import Post
from blog.serializers import PostSerializer
from blog.decorators import only_allow_this_fields

class InjectPostModel(APIView):
  def __init__(self, *args, **kwargs):
    self._post_model = Post.objects
    super().__init__(*args, **kwargs)

@method_decorator(cache_page(1), name='dispatch')
class PostList(InjectPostModel):
  def get(self, request):
    posts = self._post_model.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

  @only_allow_this_fields(["title", "body", "published"])
  def post(self, request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(InjectPostModel):
  def _get_object(self, id):
    try:
      return self._post_model.get(pk=id)
    except Post.DoesNotExist:
      raise Http404
  
  def get(self, request, id):
    post = self._get_object(id)
    serializer = PostSerializer(post)
    return Response(serializer.data)

  @only_allow_this_fields(["title", "body", "published"])
  def put(self, request, id):
    post = self._get_object(id)
    post_serializer = PostSerializer(post, data=request.data)
    if post_serializer.is_valid():
        post_serializer.save()
        return Response(post_serializer.data)
    return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, id):
    post = self._get_object(id)
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
