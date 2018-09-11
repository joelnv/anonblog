from django.test import TestCase,Client
from django.urls import reverse
from .models import Post
from .forms import CreatePosts

# Create your tests here.
# class PostCreateView(TestCase):
#     def test_create_page_valid(self):
#         response = self.client.get(reverse('posts:create'))
#         self.assertEqual(response.status_code, 200)
class UserInterface(TestCase):
    def test_users_error_response_when_title_greater_than_body(self):
        client = Client(enforce_csrf_checks=True)
        input = {'title': 'fsssssaaadssnnnnndsared', 'body': 'asddddxxanns'}
        error = 'body should be longer than title'
        response = self.client.post(reverse('posts:create'), input)
        self.assertContains(response, error, status_code= 200)

    def test_users_error_response_when_title_less_than_ten(self):
        client = Client(enforce_csrf_checks=True)
        input = {'title': 'fsssssaa', 'body': 'asddddxxxxxxanns'}
        error = 'The value should be more than 10.'
        response = self.client.post(reverse('posts:create'), input)
        self.assertContains(response, error, status_code= 200)

    def test_users_error_response_when_content_less_than_ten(self):
        client = Client(enforce_csrf_checks=True)
        input = {'title': 'fsssssaaadssnnn', 'body': 'asddddxxa'}
        error = 'The value should be more than 10.'
        response = self.client.post(reverse('posts:create'), input)
        self.assertContains(response, error, status_code= 200)



class PostCreate(TestCase):

    def test_views_title_is_less_than_ten(self):
        input = {'title': 'fssarjked', 'body': 'asdddajsnsdsdsdsdsdd'}
        form = CreatePosts(data = input)
        self.assertFalse(form.is_valid())

    def test_views_content_is_less_than_ten(self):
        input = {'title': 'fasasasassasssarjked', 'body': 'asadddd'}
        form = CreatePosts(data = input)
        self.assertFalse(form.is_valid())

    def test_views_content_is_less_than_title(self):
        input = {'title': 'fasasasassassasdasdassarjked', 'body': 'asaddasdasdasdd'}
        form = CreatePosts(data = input)
        self.assertFalse(form.is_valid())