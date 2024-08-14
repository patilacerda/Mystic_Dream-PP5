from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from home.models import Contact
from products.models import Product


class HomeViewsTestCase(TestCase):

    def setUp(self):
        # Create a test product for the index view
        self.product = Product.objects.create(
            name='Test Product',
            price=100,
            rating=4.5,
            description='A test product description.'
        )

    def test_index_view(self):
        """
        Test the index page view to ensure it loads correctly.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertIn('product_chunks', response.context)
        self.assertContains(response, self.product.name)

    def test_contact_page_view_get(self):
        """
        Test the contact page GET request to ensure it loads correctly.
        """
        response = self.client.get(reverse('contactus'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/contactus.html')
        self.assertIn('form', response.context)

    def test_contact_page_view_post_valid_data(self):
        """
        Test the contact page POST request with valid data.
        """
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Order Inquiry',
            'message': 'This is a test message.'
        }
        response = self.client.post(reverse('contactus'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('contactus'))

        # Check that the contact message was saved
        self.assertTrue(
            Contact.objects.filter(email='john@example.com').exists())

        # Check that a success message was sent
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
                str(messages[0]), 'Your message has been sent successfully!')

    def test_contact_page_view_post_invalid_data(self):
        """
        Test the contact page POST request with invalid data.
        """
        form_data = {
            'name': '',  # Name is required, so this should fail
            'email': 'john@example.com',
            'subject': 'Order Inquiry',
            'message': 'This is a test message.'
        }
        response = self.client.post(reverse('contactus'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/contactus.html')
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_faq_page_view(self):
        """
        Test the FAQ page view to ensure it loads correctly.
        """
        response = self.client.get(reverse('faq'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/faq.html')

    def test_privacy_page_view(self):
        """
        Test the Privacy page view to ensure it loads correctly.
        """
        response = self.client.get(reverse('privacy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/privacy.html')
