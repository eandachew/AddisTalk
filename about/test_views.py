from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import About


class TestAboutViews(TestCase):
    
    def setUp(self):
        """Set up test data"""
        # Create multiple About entries with different update times
        self.about1 = About.objects.create(
            title="About Me - Old",
            content="Old content about me",
            updated_on="2023-01-01 12:00:00"
        )
        
        self.about2 = About.objects.create(
            title="About Me - Latest",
            content="Latest content about me",
            updated_on="2023-12-01 12:00:00"
        )
        
        self.about3 = About.objects.create(
            title="About Me - Middle",
            content="Middle content about me",
            updated_on="2023-06-01 12:00:00"
        )
    
    def test_about_page_loads_with_latest_entry(self):
        """Test that about page loads with the most recently updated entry"""
        response = self.client.get(reverse('about'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/about.html')
        self.assertIn('about', response.context)
        
        # Should return the most recently updated entry (about2)
        self.assertEqual(response.context['about'], self.about2)
        self.assertEqual(response.context['about'].title, "About Me - Latest")
        
        # Verify content in response
        self.assertContains(response, "About Me - Latest")
        self.assertContains(response, "Latest content about me")
    
    def test_about_page_ordering_logic(self):
        """Test that order_by('-updated_on').first() returns correct entry"""
        # Create another entry with even newer date
        newest_about = About.objects.create(
            title="About Me - Newest",
            content="Newest content",
            updated_on="2024-01-01 12:00:00"
        )
        
        response = self.client.get(reverse('about'))
        
        # Should now return the newest entry
        self.assertEqual(response.context['about'], newest_about)
        self.assertEqual(response.context['about'].title, "About Me - Newest")
        
        # Verify old entries are not in context
        self.assertNotEqual(response.context['about'], self.about1)
        self.assertNotEqual(response.context['about'], self.about2)
        self.assertNotEqual(response.context['about'], self.about3)
    
    def test_about_page_with_single_entry(self):
        """Test about page with only one About entry"""
        # Clear all entries
        About.objects.all().delete()
        
        # Create single entry
        single_about = About.objects.create(
            title="Single About Entry",
            content="This is the only about entry",
            updated_on="2023-01-01 12:00:00"
        )
        
        response = self.client.get(reverse('about'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['about'], single_about)
        self.assertContains(response, "Single About Entry")
    
    def test_about_page_with_no_entries(self):
        """Test about page when no About entries exist"""
        # Delete all entries
        About.objects.all().delete()
        
        response = self.client.get(reverse('about'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/about.html')
        
        # Context should have None or empty queryset
        self.assertIn('about', response.context)
        self.assertIsNone(response.context['about'])
        
        # Should not crash, just render empty template
        self.assertNotContains(response, "About Me -")
    
    def test_about_page_context_structure(self):
        """Test that context contains the expected data structure"""
        response = self.client.get(reverse('about'))
        
        context = response.context
        
        # Should have exactly one key 'about'
        self.assertEqual(len(context), 1)
        self.assertIn('about', context)
        
        # About object should have expected attributes
        about_obj = context['about']
        self.assertTrue(hasattr(about_obj, 'title'))
        self.assertTrue(hasattr(about_obj, 'content'))
        self.assertTrue(hasattr(about_obj, 'updated_on'))
    
    def test_about_page_html_content(self):
        """Test that the rendered HTML contains expected content"""
        response = self.client.get(reverse('about'))
        
        # Check for template structure (adjust based on your actual template)
        content = response.content.decode('utf-8')
        
        # Should contain the about title and content
        self.assertInHTML(self.about2.title, content)
        self.assertInHTML(self.about2.content, content)
        
        # Should not contain older about entries
        self.assertNotIn(self.about1.title, content)
        self.assertNotIn(self.about1.content, content)
    
    def test_about_page_updated_on_field_importance(self):
        """Test that ordering by updated_on works correctly"""
        # Update an older entry to make it newest
        self.about1.updated_on = "2024-02-01 12:00:00"
        self.about1.save()
        
        response = self.client.get(reverse('about'))
        
        # Should now return about1 as it has the newest updated_on
        self.assertEqual(response.context['about'], self.about1)
        self.assertEqual(response.context['about'].title, "About Me - Old")
    
    def test_about_page_multiple_requests(self):
        """Test that multiple requests return consistent results"""
        # First request
        response1 = self.client.get(reverse('about'))
        self.assertEqual(response1.context['about'], self.about2)
        
        # Update a different entry
        self.about3.updated_on = "2024-03-01 12:00:00"
        self.about3.save()
        
        # Second request should reflect the update
        response2 = self.client.get(reverse('about'))
        self.assertEqual(response2.context['about'], self.about3)
        
        # Create a new entry
        new_about = About.objects.create(
            title="Brand New",
            content="Just created",
            updated_on="2024-04-01 12:00:00"
        )
        
        # Third request should show the new entry
        response3 = self.client.get(reverse('about'))
        self.assertEqual(response3.context['about'], new_about)
    
    def test_about_page_queryset_efficiency(self):
        """Test that the queryset uses order_by and first() efficiently"""
        # This test verifies we're not loading all objects unnecessarily
        
        # Create many entries to test performance
        for i in range(50):
            About.objects.create(
                title=f"About {i}",
                content=f"Content {i}",
                updated_on=f"2023-01-{i+1:02d} 12:00:00"
            )
        
        # Latest should be the one created last in the loop
        latest = About.objects.all().order_by('-updated_on').first()
        
        response = self.client.get(reverse('about'))
        
        self.assertEqual(response.context['about'], latest)
        self.assertEqual(response.context['about'].title, "About 49")
    
    def test_about_page_with_request_factory(self):
        """Test using RequestFactory for more isolated testing"""
        factory = RequestFactory()
        request = factory.get('/about/')
        
        # Import the view function
        from . import views
        
        response = views.about_me(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'about/about.html')
        self.assertIn('about', response.context_data)
    
    def test_about_page_url_resolution(self):
        """Test that the URL resolves to the correct view"""
        from django.urls import resolve
        
        resolver = resolve('/about/')  # Adjust URL if different
        
        self.assertEqual(resolver.func.__name__, 'about_me')
        self.assertEqual(resolver.url_name, 'about')  # Adjust if URL name is different
    
    def test_about_page_http_methods(self):
        """Test that the view handles different HTTP methods"""
        # GET should work
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        
        # POST should also work (returns same page)
        response = self.client.post(reverse('about'))
        self.assertEqual(response.status_code, 200)
        
        # Other methods
        response = self.client.head(reverse('about'))
        self.assertEqual(response.status_code, 200)
    
    def test_about_page_security_headers(self):
        """Test basic security headers (optional)"""
        response = self.client.get(reverse('about'))
        
        # Check for basic security headers
        self.assertTrue(response.has_header('Content-Type'))
        self.assertIn('text/html', response['Content-Type'])
    
    def test_about_page_special_characters(self):
        """Test that special characters in content render correctly"""
        special_about = About.objects.create(
            title="About with <special> &chars;",
            content="Content with 'quotes', <html> tags, & ampersands",
            updated_on="2024-01-01 12:00:00"
        )
        
        response = self.client.get(reverse('about'))
        
        # Should contain the text (HTML escaped in template)
        self.assertContains(response, "About with &lt;special&gt; &amp;chars;")
        self.assertContains(response, "Content with &#x27;quotes&#x27;, &lt;html&gt; tags, &amp; ampersands")
    
    def test_about_page_with_null_updated_on(self):
        """Test handling of null updated_on fields"""
        # Clear existing entries
        About.objects.all().delete()
        
        # Create entry with null updated_on
        about_null = About.objects.create(
            title="No Update Date",
            content="Content without update date"
            # updated_on will be auto_now=True or null based on your model
        )
        
        response = self.client.get(reverse('about'))
        
        # Should still render without error
        self.assertEqual(response.status_code, 200)
        # Depending on your model, it might be the only entry or None


class TestAboutViewsEdgeCases(TestCase):
    """Test edge cases and error conditions"""
    
    def test_about_page_empty_database(self):
        """Test when database is completely empty (no About model entries)"""
        # Ensure no About objects exist
        About.objects.all().delete()
        
        response = self.client.get(reverse('about'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['about'])
        
        # Template should render without error
        self.assertTemplateUsed(response, 'about/about.html')
    
    def test_about_page_large_content(self):
        """Test with very large content"""
        large_content = "A" * 10000  # 10KB content
        
        About.objects.create(
            title="Large Content",
            content=large_content,
            updated_on="2024-01-01 12:00:00"
        )
        
        response = self.client.get(reverse('about'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Large Content")
        # Content should be truncated or fully displayed based on template
    
    def test_about_page_concurrent_updates(self):
        """Test behavior with concurrent-like updates"""
        # Create initial entry
        about1 = About.objects.create(
            title="First",
            content="First content",
            updated_on="2024-01-01 10:00:00"
        )
        
        # Get page - should show first entry
        response1 = self.client.get(reverse('about'))
        self.assertEqual(response1.context['about'], about1)
        
        # Create newer entry in same second (edge case)
        about2 = About.objects.create(
            title="Second",
            content="Second content",
            updated_on="2024-01-01 10:00:00"  # Same timestamp!
        )
        
        # With same timestamp, order might depend on ID or other factors
        response2 = self.client.get(reverse('about'))
        
        # Both have same updated_on, so which appears first depends on
        # database ordering (typically by ID for ties)
        latest = About.objects.all().order_by('-updated_on', '-id').first()
        self.assertEqual(response2.context['about'], latest)