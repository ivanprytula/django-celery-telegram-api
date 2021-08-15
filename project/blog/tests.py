from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from .models import Category
from .models import Post
from .views import PostDetailView


# 1. MODELS / MANAGERS
class PostsTests(TestCase):
    post_content = None
    post_slug = None
    post_title = None
    post_author = None
    post_model = None
    post_category = None
    user_model = None

    @classmethod
    def setUpTestData(cls):
        cls.post_model = Post
        cls.user_model = get_user_model()
        cls.post_category = Category

        cls.post_author = cls.user_model.objects.create_user(email='normal@user.com',
                                                             password='foo')
        cls.post_category = cls.post_category.objects.create(name='cool_python')
        cls.post_title = 'The very first test post'
        cls.post_slug = 'any-slug-name'
        cls.post_content = '''
            This
            can be
            any
            lorem ipsum
            text.
        '''
        new_post = cls.post_model.objects.create(author=cls.post_author, title=cls.post_title, slug=cls.post_slug,
                                                 content=cls.post_content,
                                                 is_published_to_telegram=False)

        new_post.categories.add(cls.post_category)

    def test_create_post(self):
        new_post = self.post_model.objects.get(id=1)
        self.assertEqual(new_post.author, self.post_author)
        self.assertEqual(new_post.title, self.post_title)
        self.assertEqual(new_post.slug, self.post_slug)
        self.assertEqual(new_post.content, self.post_content)
        self.assertFalse(new_post.is_published_to_telegram)
        self.assertIsInstance(new_post, Post)

        self.assertEqual(str(new_post), new_post.title)
        self.assertEqual(str(new_post.categories.get(name='cool_python')), str(self.post_category))

    def test_get_absolute_url(self):
        new_post = self.post_model.objects.get(id=1)
        self.path = reverse('blog:post-detail', kwargs={'slug': new_post.slug})
        self.request = RequestFactory().get(self.path)
        self.response = PostDetailView.as_view()(self.request, slug=new_post.slug)
        self.assertEqual(new_post.get_absolute_url(), self.path)
        self.assertEqual(self.response.status_code, 200)
