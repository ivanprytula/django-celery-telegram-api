from django.test import TestCase
from django.urls import reverse


class AboutPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.template_name = 'pages/about.html'

    def test_about_page(self):
        response = self.client.get(reverse('pages:about'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)


class LinksDepotPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.template_name = 'pages/links_depot.html'

    def test_about_page(self):
        response = self.client.get(reverse('pages:links-depot'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)


class MindMapPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.template_name = 'pages/mind_map.html'

    def test_about_page(self):
        response = self.client.get(reverse('pages:python-mind-map'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
