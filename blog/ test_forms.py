# blog/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment
from .forms import CommentForm, PostForm
from django.urls import reverse
from django.utils.text import slugify

class TestCommentForm(TestCase):
    """Test Comment Form functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='Test content',
            author=self.user,
            status=1  # Published
        )
    
    def test_form_is_valid(self):
        """Test valid comment form"""
        comment_form = CommentForm({'body': 'This is a great post'})
        self.assertTrue(comment_form.is_valid(), msg='Form should be valid with body')
    
    def test_form_is_invalid_empty(self):
        """Test invalid comment form with empty body"""
        comment_form = CommentForm({'body': ''})
        self.assertFalse(comment_form.is_valid(), msg='Form should be invalid with empty body')
        self.assertIn('body', comment_form.errors)
    
    def test_form_is_invalid_too_long(self):
        """Test invalid comment form with body too long"""
        long_text = 'x' * 1001  # Assuming max_length=1000
        comment_form = CommentForm({'body': long_text})
        self.assertFalse(comment_form.is_valid(), msg='Form should be invalid with too long body')
    
    def test_form_save(self):
        """Test saving comment form"""
        comment_form = CommentForm({
            'body': 'This is a test comment',
            'post': self.post.id
        })
        self.assertTrue(comment_form.is_valid())
        
        # Test saving with user
        comment = comment_form.save(commit=False)
        comment.author = self.user
        comment.post = self.post
        comment.save()
        
        self.assertEqual(comment.body, 'This is a test comment')
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.post, self.post)


class TestPostModel(TestCase):
    """Test Post Model functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='author',
            password='testpass123'
        )
    
    def test_create_post(self):
        """Test creating a post"""
        post = Post.objects.create(
            title='Test Post Title',
            slug='test-post-title',
            content='Test content here',
            author=self.user,
            status=1
        )
        
        self.assertEqual(post.title, 'Test Post Title')
        self.assertEqual(post.slug, 'test-post-title')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.status, 1)
        self.assertTrue(post.created_on)
    
    def test_post_str_method(self):
        """Test string representation of Post"""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='Content',
            author=self.user
        )
        self.assertEqual(str(post), 'Test Post')
    
    def test_post_get_absolute_url(self):
        """Test get_absolute_url method"""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='Content',
            author=self.user,
            status=1
        )
        expected_url = reverse('post_detail', kwargs={'slug': 'test-post'})
        self.assertEqual(post.get_absolute_url(), expected_url)


class TestCommentModel(TestCase):
    """Test Comment Model functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='commenter',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='Content',
            author=self.user,
            status=1
        )
    
    def test_create_comment(self):
        """Test creating a comment"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body='Test comment body',
            approved=True
        )
        
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.body, 'Test comment body')
        self.assertTrue(comment.approved)
        self.assertTrue(comment.created_on)
    
    def test_comment_str_method(self):
        """Test string representation of Comment"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body='Short comment',
            approved=True
        )
        # Assuming __str__ returns first 50 chars of body
        expected_str = 'Short comment'[:50]
        self.assertEqual(str(comment), expected_str)
    
    def test_comment_ordering(self):
        """Test that comments are ordered by created_on"""
        comment1 = Comment.objects.create(
            post=self.post,
            author=self.user,
            body='First comment',
            approved=True
        )
        comment2 = Comment.objects.create(
            post=self.post,
            author=self.user,
            body='Second comment',
            approved=True
        )
        
        comments = Comment.objects.all()
        self.assertEqual(comments[0], comment2)  # Most recent first
        self.assertEqual(comments[1], comment1)  # Older second


class TestViews(TestCase):
    """Test Blog Views"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='Test content',
            author=self.user,
            status=1
        )
    
    def test_home_view(self):
        """Test home page loads correctly"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')
        self.assertContains(response, 'AddisTalk')
    
    def test_post_detail_view(self):
        """Test post detail page loads correctly"""
        response = self.client.get(reverse('post_detail', kwargs={'slug': 'test-post'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, 'Test Post')
    
    def test_post_detail_view_404(self):
        """Test non-existent post returns 404"""
        response = self.client.get(reverse('post_detail', kwargs={'slug': 'non-existent'}))
        self.assertEqual(response.status_code, 404)
    
    def test_comment_post_view_authenticated(self):
        """Test authenticated user can post comment"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('add_comment', kwargs={'slug': 'test-post'}),
            {'body': 'Test comment from view'}
        )
        # Should redirect after posting
        self.assertEqual(response.status_code, 302)
        
        # Check comment was created
        comment = Comment.objects.first()
        self.assertEqual(comment.body, 'Test comment from view')
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.post, self.post)
    
    def test_comment_post_view_unauthenticated(self):
        """Test unauthenticated user cannot post comment"""
        response = self.client.post(
            reverse('add_comment', kwargs={'slug': 'test-post'}),
            {'body': 'Test comment'}
        )
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)


class TestURLs(TestCase):
    """Test URL patterns"""
    
    def test_home_url(self):
        """Test home URL resolves"""
        url = reverse('home')
        self.assertEqual(url, '/')
    
    def test_post_detail_url(self):
        """Test post detail URL resolves"""
        url = reverse('post_detail', kwargs={'slug': 'test-post'})
        self.assertEqual(url, '/post/test-post/')
    
    def test_add_comment_url(self):
        """Test add comment URL resolves"""
        url = reverse('add_comment', kwargs={'slug': 'test-post'})
        self.assertEqual(url, '/post/test-post/comment/')


class TestAuthentication(TestCase):
    """Test authentication-related functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_login_view(self):
        """Test login page loads"""
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
    
    def test_user_login(self):
        """Test user can login"""
        login_success = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login_success)
    
    def test_user_logout(self):
        """Test user can logout"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 302)  # Redirect after logout


class TestContextProcessors(TestCase):
    """Test custom context processors"""
    
    def test_world_time_context_processor(self):
        """Test world_time context processor returns expected keys"""
        from blog.context_processors import world_time
        
        # Create a mock request
        class MockRequest:
            pass
        
        request = MockRequest()
        context = world_time(request)
        
        # Check all expected keys are present
        expected_keys = [
            'ireland_time', 'ireland_date', 'ireland_timezone',
            'ethiopia_time', 'ethiopia_date', 'ethiopia_timezone',
            'time_difference', 'time_error'
        ]
        
        for key in expected_keys:
            self.assertIn(key, context, f'Key {key} missing from context')
        
        # Check time_error is boolean
        self.assertIsInstance(context['time_error'], bool)
        
        # Check times are strings
        self.assertIsInstance(context['ireland_time'], str)
        self.assertIsInstance(context['ethiopia_time'], str)


class TestTemplateTags(TestCase):
    """Test custom template tags if you have any"""
    
    def test_template_tags_exist(self):
        """Test that template tags can be loaded"""
        try:
            from blog.templatetags import blog_tags
            self.assertTrue(hasattr(blog_tags, 'register'))
        except ImportError:
            # It's okay if you don't have template tags yet
            pass


# Run specific tests
if __name__ == '__main__':
    # This allows running tests directly: python blog/tests.py
    import django
    django.setup()
    from django.test.runner import DiscoverRunner
    runner = DiscoverRunner()
    runner.run_tests(['blog'])