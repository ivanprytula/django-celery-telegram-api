from django.contrib.auth import get_user_model
from django.test import override_settings
from django.test import TestCase
from django.test.client import RequestFactory

from .context_processors import secret_for_invitation


# 1. MODELS / MANAGERS
class UsersManagersTests(TestCase):

    def test_create_user(self):
        user_model = get_user_model()
        user = user_model.objects.create_user(email='normal@user.com',
                                              password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(str(user), user.email)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            user_model.objects.create_user()
        with self.assertRaises(TypeError):
            user_model.objects.create_user(email='')
        with self.assertRaises(ValueError):
            user_model.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        user_model = get_user_model()
        admin_user = user_model.objects.create_superuser('super@user.com',
                                                         'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            user_model.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)


# 2. VIEWS

# 3. TEMPLATES

# 3. URLS

# 4. FORMS

# 5. CONTEXT
class ContextProcessorsTests(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    @override_settings(USER_INVITATION_SECRET='super-user-secret')
    def test_secret_for_invitation(self):
        request_at_root_path = self.request_factory.get('/')
        context = secret_for_invitation(request_at_root_path)

        self.assertIn('super-user-secret', context.values())

        request_at_non_root_page = self.request_factory.get('/pages/about/')
        context = secret_for_invitation(request_at_non_root_page)
        self.assertFalse(context.values())

# 5. ADMIN
