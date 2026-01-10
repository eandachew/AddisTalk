from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from django.utils.text import slugify
from .models import Post, Comment


class TestBlogViews(TestCase):

    def setUp(self):
        # Create users
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="user@test.com"
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            password="otherpass123",
            email="other@test.com"
        )
        
        # Create a post
        self.post = Post.objects.create(
            title="Test Blog Post",
            slug="test-blog-post",
            author=self.user,
            content="This is test blog content.",
            status=1  # Published
        )
    
    def test_post_list_view_renders(self):
        """Test that post list view loads correctly"""
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')
        self.assertIn('post_list', response.context)
    
    def test_post_detail_view_renders(self):
        """Test that post detail view loads correctly"""
        response = self.client.get(reverse(
            'post_detail', args=[self.post.slug]
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertIn('post', response.context)
        self.assertEqual(response.context['post'], self.post)
        self.assertIn('comments', response.context)
        self.assertIn('user_has_liked', response.context)
        self.assertIn(b"Test Blog Post", response.content)
        self.assertIn(b"This is test blog content", response.content)
    
    def test_post_detail_with_nonexistent_slug(self):
        """Test 404 for non-existent post"""
        response = self.client.get(reverse(
            'post_detail', args=['nonexistent-slug']
        ))
        self.assertEqual(response.status_code, 404)
    
    def test_post_detail_unpublished_post(self):
        """Test 404 for unpublished post"""
        unpublished_post = Post.objects.create(
            title="Draft Post",
            slug="draft-post",
            author=self.user,
            content="Draft content",
            status=0  # Draft
        )
        response = self.client.get(reverse(
            'post_detail', args=[unpublished_post.slug]
        ))
        self.assertEqual(response.status_code, 404)
    
    def test_authenticated_user_sees_own_unapproved_comments(self):
        """Test that users can see their own unapproved comments"""
        # Create an unapproved comment
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body="My unapproved comment",
            approved=False
        )
        
        # Login and access the post
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse(
            'post_detail', args=[self.post.slug]
        ))
        
        # User should see their own unapproved comment
        self.assertIn(comment, response.context['comments'])
        self.assertIn(b"My unapproved comment", response.content)
    
    def test_user_does_not_see_others_unapproved_comments(self):
        """Test that users cannot see other users' unapproved comments"""
        # Create unapproved comment from other user
        comment = Comment.objects.create(
            post=self.post,
            author=self.other_user,
            body="Other's unapproved comment",
            approved=False
        )
        
        # Login as first user
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse(
            'post_detail', args=[self.post.slug]
        ))
        
        # Should not see other user's unapproved comment
        self.assertNotIn(comment, response.context['comments'])
        self.assertNotIn(b"Other's unapproved comment", response.content)
    
    def test_add_comment_requires_login(self):
        """Test that adding a comment requires authentication"""
        response = self.client.post(reverse(
            'add_comment', args=[self.post.slug]
        ), {'body': 'Test comment'})
        
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_add_comment_authenticated(self):
        """Test adding a comment when authenticated"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse(
            'add_comment', args=[self.post.slug]
        ), {'body': 'My new comment'}, follow=True)
        
        # Check redirection
        self.assertEqual(response.status_code, 200)
        
        # Check message
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('awaiting approval', str(messages[0]))
        
        # Check comment was created (unapproved)
        comment = Comment.objects.get(post=self.post, author=self.user)
        self.assertEqual(comment.body, 'My new comment')
        self.assertFalse(comment.approved)
    
    def test_add_empty_comment(self):
        """Test that empty comments are rejected"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse(
            'add_comment', args=[self.post.slug]
        ), {'body': ''}, follow=True)
        
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('cannot be empty', str(messages[0]))
        
        # No comment should be created
        comment_count = Comment.objects.filter(
            post=self.post, author=self.user
        ).count()
        self.assertEqual(comment_count, 0)
    
    def test_comment_edit_requires_login(self):
        """Test that editing a comment requires authentication"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body="Original comment",
            approved=True
        )
        
        response = self.client.get(reverse(
            'comment_edit', args=[self.post.slug, comment.id]
        ))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_comment_edit_own_comment(self):
        """Test editing own comment"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body="Original comment",
            approved=True
        )
        
        self.client.login(username='testuser', password='testpass123')
        
        # GET request to edit form
        response = self.client.get(reverse(
            'comment_edit', args=[self.post.slug, comment.id]
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/comment_edit.html')
        self.assertEqual(response.context['comment'], comment)
        
        # POST request to update
        response = self.client.post(reverse(
            'comment_edit', args=[self.post.slug, comment.id]
        ), {'body': 'Updated comment'}, follow=True)
        
        # Check updates
        comment.refresh_from_db()
        self.assertEqual(comment.body, 'Updated comment')
        self.assertFalse(comment.approved)  # Should need re-approval
        
        # Check message
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('updated successfully', str(messages[0]))
    
    def test_comment_edit_others_comment_denied(self):
        """Test that users cannot edit others' comments"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.other_user,
            body="Other's comment",
            approved=True
        )
        
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse(
            'comment_edit', args=[self.post.slug, comment.id]
        ), {'body': 'Trying to edit'}, follow=True)
        
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('only edit your own', str(messages[0]))
        
        # Comment should not be changed
        comment.refresh_from_db()
        self.assertEqual(comment.body, "Other's comment")
    
    def test_comment_delete_requires_login(self):
        """Test that deleting a comment requires authentication"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body="Comment to delete"
        )
        
        response = self.client.post(reverse(
            'comment_delete', args=[self.post.slug, comment.id]
        ))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_comment_delete_own_comment(self):
        """Test deleting own comment"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body="Comment to delete"
        )
        
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse(
            'comment_delete', args=[self.post.slug, comment.id]
        ), follow=True)
        
        # Check deletion
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=comment.id)
        
        # Check message
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('deleted successfully', str(messages[0]))
    
    def test_comment_delete_others_comment_denied(self):
        """Test that users cannot delete others' comments"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.other_user,
            body="Other's comment"
        )
        
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse(
            'comment_delete', args=[self.post.slug, comment.id]
        ), follow=True)
        
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('only delete your own', str(messages[0]))
        
        # Comment should still exist
        self.assertTrue(Comment.objects.filter(id=comment.id).exists())
    
    def test_comment_confirm_delete_view(self):
        """Test the comment confirmation delete view"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body="Comment to delete"
        )
        
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse(
            'comment_confirm_delete', args=[self.post.slug, comment.id]
        ))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/comment_confirm_delete.html')
        self.assertEqual(response.context['comment'], comment)
        self.assertEqual(response.context['post'], self.post)
    
    def test_post_like_requires_login(self):
        """Test that liking a post requires authentication"""
        response = self.client.post(reverse(
            'post_like', args=[self.post.slug]
        ))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_post_like_toggle(self):
        """Test toggling post like"""
        self.client.login(username='testuser', password='testpass123')
        
        # First like
        response = self.client.post(reverse(
            'post_like', args=[self.post.slug]
        ))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                'liked': True,
                'like_count': 1,
                'message': 'You liked this post.'
            }
        )
        self.assertTrue(self.post.likes.filter(id=self.user.id).exists())
        
        # Then unlike
        response = self.client.post(reverse(
            'post_like', args=[self.post.slug]
        ))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                'liked': False,
                'like_count': 0,
                'message': 'You unliked this post.'
            }
        )
        self.assertFalse(self.post.likes.filter(id=self.user.id).exists())
    
    def test_user_has_liked_context(self):
        """Test user_has_liked context variable"""
        # Not logged in
        response = self.client.get(reverse(
            'post_detail', args=[self.post.slug]
        ))
        self.assertFalse(response.context['user_has_liked'])
        
        # Logged in but not liked
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse(
            'post_detail', args=[self.post.slug]
        ))
        self.assertFalse(response.context['user_has_liked'])
        
        # Like the post
        self.post.likes.add(self.user)
        
        response = self.client.get(reverse(
            'post_detail', args=[self.post.slug]
        ))
        self.assertTrue(response.context['user_has_liked'])
    
    def test_comment_delete_get_request_redirects(self):
        """Test that GET request to delete redirects with warning"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body="Test comment"
        )
        
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse(
            'comment_delete', args=[self.post.slug, comment.id]
        ), follow=True)
        
        # Should redirect with warning message
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('delete button', str(messages[0]))
        
        # Comment should still exist
        self.assertTrue(Comment.objects.filter(id=comment.id).exists())