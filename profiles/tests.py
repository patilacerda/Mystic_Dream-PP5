from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import UserProfile, Wishlist
from checkout.models import Order, OrderLineItem
from products.models import Product


class ProfileViewsTestCase(TestCase):

    def setUp(self):
        """
        Set up the test user, profile, and other necessary objects.
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )
        self.client.login(username='testuser', password='testpassword')

        self.profile = UserProfile.objects.get(user=self.user)

        self.product = Product.objects.create(
            name='Test Product',
            price=100,
            description='A test product'
        )

        self.order = Order.objects.create(
            user_profile=self.profile,
            full_name='Test User',
            email=self.user.email,
            phone_number='1234567890',
            country='US',
            postcode='12345',
            town_or_city='Test City',
            street_address1='123 Test Street',
            county='Test County',
            grand_total=100
        )

        self.order_line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            lineitem_total=100
        )

    def test_profile_view(self):
        """
        Test the profile view, ensuring it loads correctly.
        """
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

        # Check for order number
        self.assertContains(response, self.order.order_number)

        # Check for product name in the order history
        self.assertContains(response, self.product.name)

    def test_add_to_wishlist(self):
        """
        Test adding a product to the wishlist.
        """
        response = self.client.post(
            reverse('add_to_wishlist', args=[self.product.id]))
        self.assertRedirects(
            response, reverse('product_detail', args=[self.product.id]))

        wishlist = Wishlist.objects.get(user=self.user, product=self.product)
        self.assertIsNotNone(wishlist)

    def test_view_wishlist(self):
        """
        Test viewing the wishlist.
        """
        Wishlist.objects.create(user=self.user, product=self.product)
        response = self.client.get(reverse('view_wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/wishlist.html')
        self.assertContains(response, self.product.name)

    def test_update_profile_info(self):
        """
        Test updating the profile's default delivery information.
        """
        response = self.client.post(reverse('profile'), {
            'default_phone_number': '0987654321',
            'default_street_address1': '456 New Street',
            'default_town_or_city': 'New City',
            'default_county': 'New County',
            'default_postcode': '54321',
            'default_country': 'US',
        })

        self.assertEqual(response.status_code, 200)

        # Refresh the profile instance from the database
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.default_phone_number, '0987654321')
        self.assertEqual(
            self.profile.default_street_address1, '456 New Street')
        self.assertEqual(self.profile.default_town_or_city, 'New City')
        self.assertEqual(self.profile.default_county, 'New County')
        self.assertEqual(self.profile.default_postcode, '54321')
        self.assertEqual(self.profile.default_country.code, 'US')

    def test_order_history_view(self):
        """
        Test viewing an order's history from the profile.
        """
        response = self.client.get(
                reverse('order_history', args=[self.order.order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertContains(response, self.order.order_number)
        self.assertContains(response, self.product.name)
