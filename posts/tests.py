from django.test import TestCase,Client
from django.urls import reverse
from .models import Post
from .forms import CreatePosts

# Create your tests here.

class UserErrorResponse(TestCase):
    @classmethod
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def test_users_error_response_when_title_greater_than_body(self):
        input = {'title': 'fsssssaaadssnnnnndsared', 'body': 'asddddxxanns'}
        error = 'body should be longer than title'
        response = self.client.post(reverse('posts:create'), input)
        self.assertContains(response, error, status_code= 200)

    def test_users_error_response_when_title_less_than_ten(self):
        input = {'title': 'fsssssaa', 'body': 'asddddxxxxxxanns'}
        error = 'The value should be more than 10.'
        response = self.client.post(reverse('posts:create'), input)
        self.assertContains(response, error, status_code= 200)

    def test_users_error_response_when_content_less_than_ten(self):
        input = {'title': 'fsssssaaadssnnn', 'body': 'asddddxxa'}
        error = 'The value should be more than 10.'
        response = self.client.post(reverse('posts:create'), input)
        self.assertContains(response, error, status_code= 200)



class PostCreate(TestCase):

    def test_title_is_less_than_ten(self):
        input = {'title': 'fssarjked', 'body': 'asdddajsnsdsdsdsdsdd'}
        form = CreatePosts(data = input)
        self.assertEqual(len(form.errors), 1)
        self.assertEquals(form.errors['title'], ['The value should be more than 10.'])


    def test_content_is_less_than_ten(self):
        input = {'title': 'fasas', 'body': 'ddddd'}
        form = CreatePosts(data = input)
        self.assertEqual(len(form.errors), 2)
        self.assertEquals(form.errors['body'], ['The value should be more than 10.'])

    def test_content_is_less_than_title(self):
        input = {'title': 'fasasasassassasdasdassarjked', 'body': 'asaddasdasdasdd'}
        form = CreatePosts(data = input)
        self.assertEqual(len(form.errors), 1)
        self.assertEquals(form.errors['__all__'], ['body should be longer than title'])