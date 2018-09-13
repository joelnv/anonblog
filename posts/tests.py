from django.test import TestCase,Client
from django.urls import reverse
from .models import Post
from .forms import CreatePosts

# Create your tests here.

class UserErrorResponse(TestCase):
    @classmethod
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.input = {'title':'This is cool post' ,'body':'what an awsome post by somebody cool.'}

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

    def test_verify_redirect(self):
        response = self.client.post(reverse('posts:create'), self.input)
        instance = Post.objects.get()
        self.assertRedirects(response,reverse('posts:post', kwargs={'id': instance.id}),status_code=302, target_status_code=200,fetch_redirect_response=True)

    def test_verify_content_is_in_html(self):
        response = self.client.post(reverse('posts:create'), self.input,follow=True)
        self.assertContains(response,'This is cool post',status_code=200,html=True )
        self.assertContains(response,'what an awsome post by somebody cool.', status_code=200, html=True)

    def test_verify_correct_edit_link(self):
        response = self.client.post(reverse('posts:create'), self.input,follow=True)
        instance = Post.objects.get()
        link = '/posts/{id}/edit/{skey}'.format(id=instance.id, skey=instance.skey)
        self.assertContains(response, link, status_code=200)
        self.assertContains(response, 'This is cool post', status_code=200,html=True)
        self.assertContains(response, 'what an awsome post by somebody cool.', status_code=200,html=True)
        reloaded_page = self.client.get(reverse('posts:post', kwargs={'id': instance.id}))
        self.assertNotContains(reloaded_page, link, status_code=200)

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