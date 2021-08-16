from django.contrib.auth import get_user_model
from django.test import Client
from django.test import tag
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from .models import Category
from .models import Comment
from .models import Post
from .views import PostDetailView


# 1. MODELS / MANAGERSnce for the entire
class ModelsTests(TestCase):
    comment_content = None
    post_commenter = None
    comment_model = None
    post_content = None
    post_slug = None
    post_title = None
    post_author = None
    post_model = None
    post_category_model = None
    user_model = None

    # Tests are more readable and it’s more maintainable to create objects using the ORM
    @classmethod
    def setUpTestData(cls):
        cls.post_model = Post
        cls.user_model = get_user_model()
        cls.post_category_model = Category
        cls.comment_model = Comment

        cls.post_author = cls.user_model.objects.create_user(email='normal@user.com',
                                                             password='foo')
        cls.post_commenter = cls.user_model.objects.create_user(email='normal_commenter@user.com',
                                                                password='bar')

        cls.post_category_model = cls.post_category_model.objects.create(name='cool_python')
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

        new_post.categories.add(cls.post_category_model)

        cls.comment_content = 'Very good post!'
        cls.new_comment = cls.comment_model.objects.create(post=new_post, author=cls.post_commenter,
                                                           content=cls.comment_content)

    @tag('on_creation')
    def test_create_post(self):
        new_post = self.post_model.objects.get(id=1)
        self.assertEqual(new_post.author, self.post_author)
        self.assertEqual(new_post.title, self.post_title)
        self.assertEqual(new_post.slug, self.post_slug)
        self.assertEqual(new_post.content, self.post_content)
        self.assertFalse(new_post.is_published_to_telegram)
        self.assertIsInstance(new_post, Post)

        self.assertEqual(str(new_post), new_post.title)
        self.assertEqual(str(new_post.categories.get(name='cool_python')), str(self.post_category_model))

    def test_get_absolute_url(self):
        new_post = self.post_model.objects.get(id=1)
        self.path = reverse('blog:post-detail', kwargs={'slug': new_post.slug})
        self.request = RequestFactory().get(self.path)
        self.response = PostDetailView.as_view()(self.request, slug=new_post.slug)
        self.assertEqual(new_post.get_absolute_url(), self.path)
        self.assertEqual(self.response.status_code, 200)

    def test_count_comments_under_moderation(self):
        new_post = self.post_model.objects.get(id=1)
        self.assertEqual(new_post.count_comments_under_moderation, 1)

    def test_comments_under_moderation(self):
        new_post = self.post_model.objects.get(id=1)
        self.assertEqual(len(new_post.comments_under_moderation()), 1)

    def test_comment_str(self):
        new_post = self.post_model.objects.get(id=1)
        comment = new_post.comments.first()
        self.assertEqual(str(comment), f'Comment {comment.content} by {comment.commenter_name}')

    def test_comment_get_model_name(self):
        new_post = self.post_model.objects.get(id=1)
        comment = new_post.comments.first()
        self.assertEqual(comment.get_model_name(), 'Comment')


# 2. VIEWS
class PostListViewTests(TestCase):
    # https://docs.djangoproject.com/en/3.2/topics/testing/tools/#fixture-loading
    fixtures = ['users.json', 'posts.json', 'categories.json', 'comments.json']

    def setUp(self):
        # Such client have context and templates that were rendered (cf. simpler RequestFactory)
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        cls.posts = Post.objects.all()[:5]

    def test_post_list(self):
        response = self.client.get(reverse('blog:post-list'))
        self.assertQuerysetEqual(
            response.context['posts'],
            self.posts,
        )
