from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from .forms import ContactForm
from .models import ContactMessage


class TestContactViews(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.valid_form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message for the contact form.'
        }
    
    def test_contact_view_get(self):
        """Test GET request to contact page"""
        response = self.client.get(reverse('contact'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], ContactForm)
        # Check that form is empty on GET
        self.assertFalse(response.context['form'].is_bound)
    
    def test_contact_view_post_valid_data(self):
        """Test POST request with valid form data"""
        initial_count = ContactMessage.objects.count()
        
        response = self.client.post(
            reverse('contact'),
            data=self.valid_form_data,
            follow=True  # Follow redirect
        )
        
        # Check that message was saved
        final_count = ContactMessage.objects.count()
        self.assertEqual(final_count, initial_count + 1)
        
        # Check saved data
        saved_message = ContactMessage.objects.first()
        self.assertEqual(saved_message.name, 'John Doe')
        self.assertEqual(saved_message.email, 'john@example.com')
        self.assertEqual(saved_message.subject, 'Test Subject')
        self.assertEqual(saved_message.message, 'This is a test message for the contact form.')
        
        # Check redirection (should redirect to same page after success)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level_tag, 'success')
        self.assertIn('Thank you John Doe!', str(messages[0]))
        self.assertIn('Your message has been sent successfully', str(messages[0]))
        
        # Check that form is reset (unbound) after redirect
        self.assertIsInstance(response.context['form'], ContactForm)
        self.assertFalse(response.context['form'].is_bound)
    
    def test_contact_view_post_invalid_data(self):
        """Test POST request with invalid form data"""
        invalid_data = {
            'name': '',  # Empty name should be invalid
            'email': 'invalid-email',  # Invalid email format
            'subject': '',  # Empty subject
            'message': ''  # Empty message
        }
        
        initial_count = ContactMessage.objects.count()
        
        response = self.client.post(
            reverse('contact'),
            data=invalid_data,
            follow=False  # Don't follow, we want to check form errors
        )
        
        # Check no message was saved
        final_count = ContactMessage.objects.count()
        self.assertEqual(final_count, initial_count)
        
        # Check response status (should render form with errors, not redirect)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')
        
        # Check form is bound and has errors
        form = response.context['form']
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('subject', form.errors)
        self.assertIn('message', form.errors)
        
        # Check error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level_tag, 'error')
        self.assertIn('Please check your form', str(messages[0]))
        self.assertIn('There are errors', str(messages[0]))
    
    def test_contact_view_partial_invalid_data(self):
        """Test POST with some valid and some invalid fields"""
        partial_invalid_data = {
            'name': 'John Doe',  # Valid
            'email': '',  # Invalid - empty
            'subject': 'Test Subject',  # Valid
            'message': 'Valid message'  # Valid
        }
        
        initial_count = ContactMessage.objects.count()
        
        response = self.client.post(
            reverse('contact'),
            data=partial_invalid_data
        )
        
        # Check no message was saved
        final_count = ContactMessage.objects.count()
        self.assertEqual(final_count, initial_count)
        
        # Check form has errors
        form = response.context['form']
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        # Valid fields should not have errors
        self.assertNotIn('name', form.errors)
        self.assertNotIn('subject', form.errors)
        self.assertNotIn('message', form.errors)
    
    def test_contact_view_successful_submission_resets_form(self):
        """Test that after successful submission, form is reset"""
        # First submit valid data
        response = self.client.post(
            reverse('contact'),
            data=self.valid_form_data,
            follow=True
        )
        
        # Make another GET request to check form is fresh
        response = self.client.get(reverse('contact'))
        
        form = response.context['form']
        self.assertIsInstance(form, ContactForm)
        self.assertFalse(form.is_bound)
        # Check form fields are empty
        self.assertEqual(form.initial, {})
    
    def test_contact_view_form_instance_creation(self):
        """Test that form.save() creates ContactMessage instance correctly"""
        # Use the form directly to test model creation
        form = ContactForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        
        contact_message = form.save(commit=False)
        self.assertIsInstance(contact_message, ContactMessage)
        self.assertEqual(contact_message.name, 'John Doe')
        self.assertEqual(contact_message.email, 'john@example.com')
        
        # Save to database
        contact_message.save()
        self.assertTrue(ContactMessage.objects.filter(email='john@example.com').exists())
    
    def test_contact_view_empty_post(self):
        """Test POST request with empty data"""
        response = self.client.post(reverse('contact'), data={})
        
        self.assertEqual(response.status_code, 200)
        
        form = response.context['form']
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        
        # Should have errors for all required fields
        expected_errors = ['name', 'email', 'subject', 'message']
        for field in expected_errors:
            self.assertIn(field, form.errors)
    
    def test_contact_view_xss_protection(self):
        """Test that potentially malicious input is handled safely"""
        malicious_data = {
            'name': '<script>alert("xss")</script>',
            'email': 'test@example.com',
            'subject': '<b>Test</b>',
            'message': '<img src="x" onerror="alert(1)">'
        }
        
        response = self.client.post(
            reverse('contact'),
            data=malicious_data,
            follow=True
        )
        
        # Check message was saved (form should sanitize or accept as-is depending on your form setup)
        self.assertEqual(ContactMessage.objects.count(), 1)
        saved_message = ContactMessage.objects.first()
        
        # Depending on your form/widget configuration, HTML might be escaped or stripped
        # If using Django's default CharField/TextField, HTML will be stored as-is
        # If you want to test sanitization, you might need to check the template rendering
        
        # At minimum, ensure the data was saved
        self.assertEqual(saved_message.name, '<script>alert("xss")</script>')
        self.assertEqual(saved_message.message, '<img src="x" onerror="alert(1)">')
        
        # Check that response doesn't execute the script
        self.assertNotIn(b'<script>alert', response.content)
    
    def test_contact_view_long_input(self):
        """Test with very long input data"""
        long_message = 'A' * 1000  # 1000 character message
        
        long_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': long_message
        }
        
        response = self.client.post(
            reverse('contact'),
            data=long_data,
            follow=True
        )
        
        # Should save successfully if within field limits
        self.assertEqual(ContactMessage.objects.count(), 1)
        saved_message = ContactMessage.objects.first()
        self.assertEqual(len(saved_message.message), 1000)
    
    def test_contact_view_context(self):
        """Test that context contains the form"""
        response = self.client.get(reverse('contact'))
        
        self.assertIn('form', response.context)
        form = response.context['form']
        
        # Check form fields
        self.assertIn('name', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('subject', form.fields)
        self.assertIn('message', form.fields)
    
    def test_contact_view_success_redirect(self):
        """Test that successful POST redirects to contact page"""
        response = self.client.post(
            reverse('contact'),
            data=self.valid_form_data,
            follow=False  # Don't follow to check redirect
        )
        
        # Should redirect after successful form submission
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('contact'))
    
    def test_contact_view_form_validation_messages(self):
        """Test that form validation errors are displayed"""
        # Test with just email missing
        incomplete_data = {
            'name': 'John Doe',
            'email': '',  # Missing required field
            'subject': 'Test',
            'message': 'Test message'
        }
        
        response = self.client.post(reverse('contact'), data=incomplete_data)
        
        # Check form has email error
        form = response.context['form']
        self.assertIn('email', form.errors)
        self.assertIn('This field is required', str(form.errors['email']))
    
    def test_contact_view_database_integrity(self):
        """Test that multiple submissions work correctly"""
        # Submit first message
        self.client.post(reverse('contact'), data=self.valid_form_data)
        
        # Submit second message
        second_data = {
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'subject': 'Second Subject',
            'message': 'Second message'
        }
        self.client.post(reverse('contact'), data=second_data)
        
        # Check both messages saved
        self.assertEqual(ContactMessage.objects.count(), 2)
        
        messages = ContactMessage.objects.all()
        emails = [msg.email for msg in messages]
        self.assertIn('john@example.com', emails)
        self.assertIn('jane@example.com', emails)
    
    def test_contact_view_form_field_order(self):
        """Test form field order in rendered HTML (optional)"""
        response = self.client.get(reverse('contact'))
        
        # This test checks if form fields appear in expected order in HTML
        # You might need to adjust based on your actual template
        content = response.content.decode('utf-8')
        
        # Find positions of field labels (adjust based on your actual template)
        # This is a simple example - you might need to customize
        if 'name' in content and 'email' in content:
            name_pos = content.find('name')
            email_pos = content.find('email')
            # Assuming name comes before email in form
            self.assertLess(name_pos, email_pos)