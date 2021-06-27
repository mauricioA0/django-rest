from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from blog.models import Post
from blog.serializers import PostSerializer

class PostViewsTest(APITestCase):
  @classmethod
  def setUpTestData(cls):
    posts = [
      Post.objects.create(title='{} title'.format(number), body='{} body'.format(number)) for number in range(1, 4)
    ]

    cls.posts = posts
    cls.post = posts[0]

  def test_can_read_all_posts(self):
    response = self.client.get(reverse('post-list'))

    self.assertEquals(status.HTTP_200_OK, response.status_code)
    self.assertEquals(len(self.posts), len(response.data))

    for post in self.posts:
      self.assertIn(
        PostSerializer(instance=post).data, response.data
      )

  def test_can_read_single_post(self):
    response = self.client.get(
      reverse('post-detail', args=[self.post.id])
    )
    self.assertEquals(status.HTTP_200_OK, response.status_code)
    self.assertEquals(
      PostSerializer(instance=self.post).data, response.data
    )

  def test_can_add_a_new_post(self):
    payload = { 'title': 'title test', 'body': 'body test' }

    response = self.client.post(reverse('post-list'), payload)
    created_post = Post.objects.get(title=payload['title'])

    self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    for key, value in payload.items():
      self.assertEquals(value, response.data[key])
      self.assertEquals(value, getattr(created_post, key))

  def test_can_add_a_new_post_fail_bad_payload(self):
    payload = { 'title': 'title test', 'body': 'body test', 'no_valid': 'test' }

    response = self.client.post(reverse('post-list'), payload)

    self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

  def test_can_delete_a_post(self):
    response = self.client.delete(
      reverse('post-detail', args=[self.post.id])
    )

    self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)
    self.assertFalse(Post.objects.filter(pk=self.post.id))

  def test_can_update_a_post(self):
    payload = { 'title': 'new title', 'body': 'new body' }

    response = self.client.put(
      reverse('post-detail', args=[self.post.id]), payload
    )

    edited_post = Post.objects.get(title=payload['title'])

    self.assertEquals(status.HTTP_200_OK, response.status_code)
    self.assertEquals(edited_post.title, payload['title'])
  
  def test_post_does_not_exists(self):
    response = self.client.get(
      reverse('post-detail', args=[999999999])
    )

    self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)

  def test_invalid_input_for_new_post(self):
    payload = { 'title': '', 'body': '' }

    response = self.client.post(
      reverse('post-list'), payload
    )

    self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

  def test_invalid_input_for_edit_post(self):
    payload = { 'title': '', 'body': '' }

    response = self.client.put(
      reverse('post-detail', args=[self.post.id]), payload
    )

    self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

class PostModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.title = 'PostModel Title'
    cls.post = Post.objects.create(title=cls.title, body='PostModel Body')

  def test_return_str_when_created(self):
    post = Post.objects.get(title=self.title)
    self.assertEquals(post.__str__(), self.title)
