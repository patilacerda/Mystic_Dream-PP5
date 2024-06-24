from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product
from django.contrib.messages import get_messages

# Create your tests here.


class TestBagViews(TestCase):

    def setUp(self):
        """
        Setup method to create test data and authenticate a user
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
            )
        self.client.login(username='testuser', password='testpassword')
        self.product = Product.objects.create(name='Test Product', price=10.00)
        self.bag_url = reverse('view_bag')
        self.add_to_bag_url = reverse('add_to_bag', args=[self.product.id])
        self.adjust_bag_url = reverse('adjust_bag', args=[self.product.id])
        self.remove_from_bag_url = reverse(
            'remove_from_bag', args=[self.product.id]
        )

    def test_view_bag(self):
        """
        Test case to verify rendering of the bag contents page.
        """
        response = self.client.get(self.bag_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')

    def test_add_to_bag(self):
        """
        Test case to verify adding a product to the shopping bag.
        """
        response = self.client.post(self.add_to_bag_url, {
            'quantity': 1,
            'redirect_url': self.bag_url
        })
        self.assertRedirects(response, self.bag_url)
        bag = self.client.session['bag']
        self.assertIn(str(self.product.id), bag)
        self.assertEqual(bag[str(self.product.id)], 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Added" in str(message) for message in messages))

    def test_add_to_bag_with_size(self):
        """
        Test case to verify adding a product with a specified size
        to the shopping bag.
        """
        response = self.client.post(self.add_to_bag_url, {
            'quantity': 1,
            'product_size': 'M',
            'redirect_url': self.bag_url
        })
        self.assertRedirects(response, self.bag_url)
        bag = self.client.session['bag']
        self.assertIn(str(self.product.id), bag)
        self.assertIn('M', bag[str(self.product.id)]['items_by_size'])
        self.assertEqual(bag[str(self.product.id)]['items_by_size']['M'], 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Added" in str(message) for message in messages))

    def test_adjust_bag(self):
        """
        Test case to verify adjusting the quantity of a product
        in the shopping bag.
        """
        self.client.post(self.add_to_bag_url, {
            'quantity': 1,
            'redirect_url': self.bag_url
        })
        response = self.client.post(self.adjust_bag_url, {
            'quantity': 2
        })
        self.assertRedirects(response, self.bag_url)
        bag = self.client.session['bag']
        self.assertEqual(bag[str(self.product.id)], 2)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Updated" in str(message) for message in messages))

    def test_adjust_bag_with_size(self):
        """
        Test case to verify adjusting the quantity of a product
        with a specified size in the shopping bag.
        """
        self.client.post(self.add_to_bag_url, {
            'quantity': 1,
            'product_size': 'M',
            'redirect_url': self.bag_url
        })
        response = self.client.post(self.adjust_bag_url, {
            'quantity': 2,
            'product_size': 'M'
        })
        self.assertRedirects(response, self.bag_url)
        bag = self.client.session['bag']
        self.assertEqual(bag[str(self.product.id)]['items_by_size']['M'], 2)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Updated" in str(message) for message in messages))

    def test_remove_from_bag(self):
        """
        Test case to verify removing a product from the shopping bag.
        """
        self.client.post(self.add_to_bag_url, {
            'quantity': 1,
            'redirect_url': self.bag_url
        })
        response = self.client.post(self.remove_from_bag_url)
        self.assertEqual(response.status_code, 200)
        bag = self.client.session['bag']
        self.assertNotIn(str(self.product.id), bag)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Removed" in str(message) for message in messages))

    def test_remove_from_bag_with_size(self):
        """
        Test case to verify removing a product with a specified size from
        the shopping bag.
        """
        self.client.post(self.add_to_bag_url, {
            'quantity': 1,
            'product_size': 'M',
            'redirect_url': self.bag_url
        })
        response = self.client.post(self.remove_from_bag_url, {
            'product_size': 'M'
        })
        self.assertEqual(response.status_code, 200)
        bag = self.client.session['bag']
        self.assertNotIn('M', bag.get(str(self.product.id), {}).get(
            'items_by_size', {}))
        if not bag.get(str(self.product.id), {}).get('items_by_size', {}):
            self.assertNotIn(str(self.product.id), bag)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Removed" in str(message) for message in messages))
