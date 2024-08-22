from django.contrib.auth.models import User
from .models import Like
from posts.models import Post
from comments.models import Comment
from rest_framework.test import APITestCase
from rest_framework import status


class LikeListViewTests(APITestCase):
    """
    Tests for the Like list view.
    List likes, create a like on a post.
    Logged out user cannot create a like.
    User can not like the same thing multiple times.
    """

    def setUp(self):
        self.adam = User.objects.create_user(username='adam', password='pass')
        self.brian = User.objects.create_user(
            username='brian', password='pass'
            )
        self.post = Post.objects.create(
            owner=self.brian, title='this is a title'
            )

    def test_logged_in_user_can_like_post(self):
        self.client.login(username='adam', password='pass')
        post = Post.objects.get(title='this is a title')
        response = self.client.post('/likes/', {'post': post.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cannot_like(self):
        post = Post.objects.get(title='this is a title')
        response = self.client.post('/likes/', {'post': post.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_like_same_thing_multiple_times(self):
        self.client.login(username='adam', password='pass')
        post = Post.objects.get(title='this is a title')
        response = self.client.post('/likes/', {'post': post.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/likes/', {'post': post.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LikeDetailViewTests(APITestCase):
    """
    Tests for the Like detail view.
    Like can be deleted from a post by its owner.
    Like can not be deleted from a post by an unauthenticated user.
    An owners Like can not be deleted by another user.
    """
    def setUp(self):
        self.adam = User.objects.create_user(username='adam', password='pass')
        self.brian = User.objects.create_user(
            username='brian', password='pass'
            )
        self.post = Post.objects.create(
            owner=self.brian, title='this is a title'
            )

    def test_owner_can_delete_like_from_post(self):
        self.client.login(username='adam', password='pass')
        like = Like.objects.create(owner=self.adam, post=self.post)
        response = self.client.delete(f'/likes/{like.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_user_cannot_delete_like_from_post(self):
        like = Like.objects.create(owner=self.adam, post=self.post)
        response = self.client.delete(f'/likes/{like.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owners_like_cannot_be_deleted_by_another_user(self):
        self.client.login(username='brian', password='pass')
        like = Like.objects.create(owner=self.adam, post=self.post)
        response = self.client.delete(f'/likes/{like.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
