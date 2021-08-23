from celery.contrib.testing.worker import start_worker
from django.contrib.auth import get_user_model
from django.test import Client
from django.test import tag
from django.test import TestCase
from django.test import TransactionTestCase
from django.test.client import RequestFactory
from django.urls import reverse

from .forms import CommentForm
from .models import Category
from .models import Comment
from .models import Post
from .tasks import post_unpublished_to_telegram
from .views import PostDetailView
from core_config.celery import app

REGULAR_USER_EMAIL = 'normal@user.com'


# 1. MODELS / MANAGERS
class ModelsTests(TestCase):
    comment_content = None
    post_commenter = None
    comment_model = None
    post_content = None
    post_slug = None
    post_title = None
    post_author = None
    post_model = None
    post_category = None
    user_model = None

    # Tests are more readable and it’s more maintainable to create objects using the ORM
    @classmethod
    def setUpTestData(cls):
        cls.post_model = Post
        cls.user_model = get_user_model()
        cls.post_category = Category
        cls.comment_model = Comment

        cls.post_author = cls.user_model.objects.create_user(email=REGULAR_USER_EMAIL,
                                                             password='foo')
        cls.post_commenter = cls.user_model.objects.create_user(email='normal_commenter@user.com',
                                                                password='bar')

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
        self.assertEqual(str(new_post.categories.get(name='cool_python')), str(self.post_category))

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


class PostCreateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.template_name = 'blog/post_create.html'
        cls.user = get_user_model().objects.create_user(email=REGULAR_USER_EMAIL, password='foo')

    def test_render_post_create_view(self):
        # 2. Authorize user
        is_authorized = self.client.login(username=REGULAR_USER_EMAIL, password='foo')
        self.assertTrue(is_authorized)

        # 3. Visit blog:post-create url
        response = self.client.get(reverse('blog:post-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)

    def test_post_create_view_success(self):
        is_authorized = self.client.login(username=REGULAR_USER_EMAIL, password='foo')
        self.assertTrue(is_authorized)

        new_post = {
            'author': self.user,
            'title': 'New cool post',
            'slug': 'new_cool_post',
            'content': 'lorem ipsum lorem ipsum lorem ipsum lorem ipsum',
            'categories': ['python-code']
        }
        response = self.client.post(reverse('blog:post-create'), kwargs=new_post)
        self.assertEqual(response.status_code, 200)


class PostDetailViewTests(TestCase):
    fixtures = ['users.json', 'posts.json', 'categories.json', 'comments.json']

    @classmethod
    def setUpTestData(cls):
        cls.template_name = 'blog/post_detail.html'
        cls.user = get_user_model().objects.create_user(email=REGULAR_USER_EMAIL, password='foo')

    def test_render_post_detail_view(self):
        is_authorized = self.client.login(username=REGULAR_USER_EMAIL, password='foo')
        self.assertTrue(is_authorized)

        post = Post.objects.filter(comments__isnull=False).first()
        response = self.client.get(reverse('blog:post-detail', kwargs={'slug': post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('comments', response.context)

    def test_add_comment(self):
        user = get_user_model().objects.get(pk=1)
        post = Post.objects.get(pk=1)
        data = {
            'commenter_name': 'I\'ll not tell you mu name.',
            'post_id': post.id,
            'author': user,
            'content': 'cool article, yo!'
        }
        comment_form = CommentForm(data={**data})
        new_comment = comment_form.save(commit=False)
        new_comment.post = post
        comment_form.save()
        self.assertTrue(comment_form.is_valid())


class PostUpdateViewTests(TestCase):
    fixtures = ['users.json', 'posts.json', 'categories.json']

    @classmethod
    def setUpTestData(cls):
        cls.template_name = 'blog/post_update.html'
        cls.user = get_user_model().objects.create_user(email=REGULAR_USER_EMAIL, password='foo')

    def test_render_post_update_view(self):
        is_authorized = self.client.login(username=REGULAR_USER_EMAIL, password='foo')
        self.assertTrue(is_authorized)

        response = self.client.get(reverse('blog:post-update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)

    def test_post_update_view_success(self):
        is_authorized = self.client.login(username=REGULAR_USER_EMAIL, password='foo')
        self.assertTrue(is_authorized)

        post = Post.objects.get(pk=1)
        post.title = 'updated title'
        post.content = 'updated content'
        post.categories.add(2)
        post.save()

        response = self.client.put(reverse('blog:post-update', kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, 200)


class PostDeleteViewTests(TestCase):
    fixtures = ['users.json', 'posts.json', 'categories.json']

    @classmethod
    def setUpTestData(cls):
        cls.template_name = 'blog/post_delete.html'
        cls.user = get_user_model().objects.create_user(email=REGULAR_USER_EMAIL, password='foo')

    def test_render_post_delete_view(self):
        is_authorized = self.client.login(username=REGULAR_USER_EMAIL, password='foo')
        self.assertTrue(is_authorized)

        response = self.client.get(reverse('blog:post-delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)

    def test_post_delete_view(self):
        is_authorized = self.client.login(username=REGULAR_USER_EMAIL, password='foo')
        self.assertTrue(is_authorized)

        response = self.client.post(reverse('blog:post-update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)


class PostsByCategoryViewTests(TestCase):
    fixtures = ['users.json', 'posts.json', 'categories.json']

    @classmethod
    def setUpTestData(cls):
        cls.template_name = 'blog/post_category.html'

    def test_posts_list_by_category(self):
        category = Category.objects.get(pk=1)
        response = self.client.get(reverse('blog:post-category', kwargs={'category': category.name}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertIn('posts', response.context)


# TASKS
@tag('exclude')
class TasksTests(TransactionTestCase):
    """Invoking your Celery tasks inside your tests with the apply() method executes the task synchronously and
    locally. This allows you to write tests that look and feel very similar to the ones for your API endpoints."""
    celery_worker = None
    post_model = None
    databases = '__all__'
    fixtures = ['users.json', 'posts.json', 'categories.json', 'comments.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post_model = Post

        # Start up celery worker
        cls.celery_worker = start_worker(app, perform_ping_check=False)
        cls.celery_worker.__enter__()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        # Close worker
        cls.celery_worker.__exit__(None, None, None)

    def test_post_unpublished_to_telegram_success(self):
        self.post_model.objects.all().update(is_published_to_telegram=False)
        self.task = post_unpublished_to_telegram.apply()
        self.result = self.task.get()
        self.assertTrue(self.result)

    def test_post_unpublished_to_telegram_no_fresh_posts(self):
        self.post_model.objects.all().update(is_published_to_telegram=True)
        self.task = post_unpublished_to_telegram.apply()
        self.result = self.task.get()
        self.assertFalse(self.result)
