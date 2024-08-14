from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from checkout.models import Order
from products.models import Product
from profiles.models import UserProfile


class CheckoutViewsTestCase(TestCase):

    def setUp(self):
        """
        Set up a test user, test product, and log in the user.
        Set up the session data for the shopping bag.
        """

        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.profile = UserProfile.objects.get(user=self.user)

        self.product = Product.objects.create(
            name='Test Product',
            price=100,
            description='A test product'
        )

        session = self.client.session
        session['bag'] = {str(self.product.id): 1}
        session.save()

    def test_checkout_with_valid_data(self):
        """
        Test the checkout process with valid data..
        """
        response = self.client.post(reverse('checkout'), {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'country': 'US',
            'postcode': '12345',
            'town_or_city': 'Test City',
            'street_address1': '123 Test Street',
            'street_address2': '',
            'county': 'Test County',
            'client_secret': 'test_client_secret'
        })

        self.assertEqual(response.status_code, 302)  # Redirect to success page

        # Refresh the profile to check for any saved information updates
        self.profile.refresh_from_db()

    def test_checkout_with_invalid_data(self):
        """
        Test the checkout process with invalid data.
        The test ensures that the form submission fails,
        the user remains on the checkout page,
        the response contains an error message indicating invalid form data.
        """
        response = self.client.post(reverse('checkout'), {
            'full_name': '',  # Invalid data: empty full_name
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'country': 'US',
            'postcode': '12345',
            'town_or_city': 'Test City',
            'street_address1': '123 Test Street',
            'street_address2': '',
            'county': 'Test County',
            'client_secret': 'some_client_secret'
        })

        self.assertEqual(
            response.status_code, 200)  # Return to the checkout page
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertContains(response, 'There was an error with your form.')

    def test_checkout_success_view(self):
        """
        Test the checkout success page view.
        """
        order = Order.objects.create(
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            country='US',
            postcode='12345',
            town_or_city='Test City',
            street_address1='123 Test Street',
            county='Test County',
            user_profile=self.profile
        )
        response = self.client.get(
            reverse('checkout_success', args=[order.order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertContains(response, order.order_number)
