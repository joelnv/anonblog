from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from .models import Post
from .forms import CreatePosts
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
import requests

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
        response = self.client.get(reverse('posts:anon_edit', kwargs={'id': self.posts.id, 'skey': self.posts.skey}))
        self.assertContains(response, 'ORM testing links', status_code=200)
        wrong_skey = 'aaaaaaaaa'
        response = self.client.get(reverse('posts:anon_edit', kwargs={'id': self.posts.id, 'skey': wrong_skey}))
        self.assertEqual(response.status_code,404)

    def test_edit_fields_of_post_successfully(self):
        edit_input = {'title':'I have edited','body':'Title and body are edited'}
        response = self.client.post(reverse('posts:anon_edit' , kwargs={'id': self.posts.id, 'skey': self.posts.skey}) , edit_input , follow=True)
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
        self.assertContains(self.response, '<h1>This is the main heading </h1> &lt;script&gt;alert("Hello");&lt;/script&gt;<h2>This is the sub heading </h2>', status_code=200)

    def test_to_check_Headings_in_outline(self):
        self.assertContains(self.response, '<ul><li>This is the main heading  </li></ul><ul><ul><li>This is the sub heading  </li></ul></ul>', status_code=200)

class SignUpLogInTest(TestCase):
    def setUp(self):
        self.signup1 = {'username': 'testuser2' , 'password1' : 'aaaa1234', 'password2' : 'aaaa1234'}
        self.signup2 = {'username': 'testuser3' , 'password1' : 'aaaaaaaa', 'password2' : 'aaaacccc'}
        self.signup3 = {'username': 'testuser', 'password1': 'aaaa1111', 'password2': 'aaaa1111'}
        self.login = {'username': 'testuser','password': 'secret'}
        self.login2 = {'username': 'testuser','password': 'secretsssss'}
        self.login3 = {'username': 'notuser', 'password': 'aassd22222'}
        User.objects.create_user(**self.login)

    def test_signup(self):
        response = self.client.post(reverse('signup'), self.signup1, follow=True)
        self.assertTrue(response.context['user'].is_active)
        self.assertRedirects(response, reverse('posts:create'))


    def test_signup_with_already_exsisting_user(self):
        response = self.client.post(reverse('signup'), self.signup3, follow=True)
        error = 'A user with that username already exists.'
        self.assertFalse(response.context['user'].is_active)
        self.assertContains(response, error, status_code= 200)

    def test_signup_wrong_password(self):
        response = self.client.post(reverse('signup'), self.signup2, follow=True)
        error = "The two password fields didn&#39;t match."
        self.assertFalse(response.context['user'].is_active)
        self.assertContains(response, error, status_code= 200)

    def test_login(self):
        response = self.client.post(reverse('login'), self.login, follow=True)
        self.assertTrue(response.context['user'].is_active)
        self.assertRedirects(response, reverse('posts:create'))

    def test_login_wrong_password(self):
        response = self.client.post(reverse('login'), self.login2, follow=True)
        self.assertFalse(response.context['user'].is_active)

    def test_unregistered_user_login(self):
        response = self.client.post(reverse('login'), self.login3, follow=True)
        self.assertFalse(response.context['user'].is_active)

class LoggedInUserArticleTest(TestCase):

    def setUp(self):
        self.signup1 = {'username': 'testuser2', 'password1': 'aaaa1234', 'password2': 'aaaa1234'}
        self.login = {'username': 'testuser2', 'password': 'aaaa1234'}
        User.objects.create_user(**self.login)
        self.input = {'title':'What a super day', 'body':'this would have been a great day if...'}

    def test_login_post_creation_and_checking_mine_link(self):
        response = self.client.post(reverse('login'), self.login, follow=True)
        self.assertTrue(response.context['user'].is_active)
        response = self.client.post(reverse('posts:create'), self.input)
        instance = Post.objects.get(id= response.url.split('/')[2])
        self.assertRedirects(response, reverse('posts:post', kwargs={'id': instance.id}), status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        response = self.client.get(reverse('posts:myposts'), follow=True)
        title = self.input['title']
        body = self.input['body']
        self.assertContains(response, title, status_code=200)
        self.assertNotContains(response, body, status_code=200)

    def test_anonymous_user_has_no_mine_link(self):
        response = self.client.post(reverse('logout'), follow=True)
        self.assertFalse(response.context['user'].is_active)
        url = self.client.get(reverse('posts:myposts'), follow=True)
        self.assertEqual(url.status_code, 404)

class EditPageTest(TestCase):
    def setUp(self):
        self.signup1 = {'username': 'testuser2', 'password1': 'aaaa1234', 'password2': 'aaaa1234'}
        self.login = {'username': 'testuser2', 'password': 'aaaa1234'}
        self.response = self.client.post(reverse('signup'), self.signup1, follow=True)
        self.input = {'title': 'What a super day', 'body': 'this would have been a great day if...'}
        self.edit_input = {'title': 'I have edited', 'body': 'Title and body are edited'}

    def test_logged_in_user_edit_page_without_secretkey(self):
        r = self.client.post(reverse('posts:create'), self.input)
        instance = Post.objects.get(id=r.url.split('/')[2])
        response = self.client.get(reverse('posts:edit', kwargs={'id': instance.id }))
        self.assertContains(response, self.input['body'], status_code=200)
        response = self.client.post(reverse('posts:edit', kwargs={'id': instance.id }), self.edit_input, follow=True)
        self.assertContains(response, self.edit_input['title'], status_code=200)

    def test_logged_in_user_edit_anonymous_post_with_secretkey(self):
        self.client.post(reverse('logout'), follow=True)
        r = self.client.post(reverse('posts:create'), self.input)
        instance = Post.objects.get(id=r.url.split('/')[2])
        self.client.post(reverse('login'), self.login, follow=True)
        self.client.get(reverse('posts:anon_edit', kwargs={'id': instance.id, 'skey' : instance.skey}))
        response = self.client.post(reverse('posts:anon_edit', kwargs={'id': instance.id, 'skey': instance.skey}),
                                    self.edit_input, follow=True)
        self.assertContains(response, self.edit_input['title'], status_code=200)

    def test_anonymous_user_edit_page_without_secretkey(self):
        self.client.post(reverse('logout'), follow=True)
        r = self.client.post(reverse('posts:create'), self.input)
        instance = Post.objects.get(id=r.url.split('/')[2])
        url = self.client.get(reverse('posts:edit', kwargs={'id': instance.id }))
        self.assertEqual(url.status_code, 404)

class ClaimPostTest(TestCase):
    def setUp(self):
        self.input = {'title': 'This is cool post','body': '<h1>This is the main heading </h1> <script>alert("Hello");</script><h2>This is the sub heading </h2>the is para one\n\n what an awsome post by somebody cool.'}
        self.r = self.client.post(reverse('posts:create'), self.input)
        self.instance = Post.objects.get(id=self.r.url.split('/')[2])
        self.signup1 = {'username': 'testuser2', 'password1': 'aaaa1234', 'password2': 'aaaa1234'}

    def test_claim_function_loggedin_user(self):
        self.client.post(reverse('signup'), self.signup1, follow=True)
        self.client.post(reverse('posts:claim', kwargs={'id': self.instance.id, 'skey': self.instance.skey}))
        response = self.client.get(reverse('posts:myposts'), follow=True)
        title = self.input['title']
        self.assertContains(response, title, status_code=200)

    def test_get_method_error_claim_function_loggedin_user(self):
        self.client.post(reverse('signup'), self.signup1, follow=True)
        self.client.get(reverse('posts:claim', kwargs={'id': self.instance.id, 'skey': self.instance.skey}))
        response = self.client.get(reverse('posts:myposts'), follow=True)
        title = self.input['title']
        self.assertNotContains(response, title, status_code=200)

    def test_Anonymous_user_dont_have_claim_button_(self):
        response = self.client.get(reverse('posts:anon_edit', kwargs={'id': self.instance.id, 'skey': self.instance.skey}))
        self.assertNotContains(response, 'Claim this Post as yours', status_code=200)
