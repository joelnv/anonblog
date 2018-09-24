from django.test import TestCase,Client
from django.urls import reverse
from .models import Post
from .forms import CreatePosts

# Create your tests here.

class UserErrorResponse(TestCase):
    @classmethod
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.input = {'title':'This is cool post' , 'body':'what an awsome post by somebody cool.'}

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

    def test_verify_content_newline_as_br(self):
        input = {'title':'verfing newline as br','body':'This first line. \n This is second line.'}
        response = self.client.post(reverse('posts:create'), input, follow= True)
        self.assertContains(response,'This first line. <br /> This is second line.', status_code=200)


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


class EditLinkTestingORM(TestCase):
    def setUp(self):
        self.posts = Post.objects.create(title='ORM testing links' , body='This is edit link test orm' ,skey='123456789')
        self.posts.save()

    def test_redirect_edit_link(self):
        response = self.client.get(reverse('posts:edit', kwargs={'id': self.posts.id, 'skey': self.posts.skey}))
        self.assertContains(response, 'ORM testing links', status_code=200)
        wrong_skey = 'aaaaaaaaa'
        response = self.client.get(reverse('posts:edit', kwargs={'id': self.posts.id, 'skey': wrong_skey}))
        self.assertEqual(response.status_code,404)

    def test_edit_fields_of_post_successfully(self):
        edit_input = {'title':'I have edited','body':'Title and body are edited'}
        response = self.client.post(reverse('posts:edit' , kwargs={'id': self.posts.id, 'skey': self.posts.skey}) , edit_input , follow=True)
        self.assertContains(response, 'Title and body are edited', status_code=200)

class PostPageTesting(TestCase):
    def setUp(self):
        self.input = {'title':'This is cool post', 'body':'<h1>This is the main heading </h1> <script>alert("Hello");</script><h2>This is the sub heading </h2>the is para one\n\n what an awsome post by somebody cool.'}
        self.response = self.client.post(reverse('posts:create'), self.input, follow=True)
        self.instance = Post.objects.get()
        self.assertRedirects(self.response, reverse('posts:post', kwargs={'id': self.instance.id}), status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_rendering_multiple_paragraphs(self):
        self.assertContains(self.response, '<p> what an awsome post by somebody cool.</p>', status_code=200)

    def test_no_rendering_unsafe_tags(self):
        self.assertContains(self.response, '&lt;script&gt;alert("Hello");&lt;/script&gt;', status_code=200)

    def test_to_check_Headings_in_outline(self):
        self.assertContains(self.response, '<ul><li>This is the main heading <br /> </li></ul><ul><ul><li>This is the sub heading <br /> </li></ul></ul>', status_code=200)