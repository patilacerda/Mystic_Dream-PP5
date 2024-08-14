from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Category


class ProductsViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username='admin',
            password='adminpassword',
            email='admin@example.com')
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10.00,
            category=self.category
        )

    def test_all_products_view(self):
        """
        Test the 'all products' view to ensure it loads correctly and displays
        the expected product.
        """
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertContains(response, 'Test Product')

    def test_product_detail_view(self):
        """
        Test the 'product detail' view to ensure it loads correctly and
        displays the correct product details.
        """
        response = self.client.get(
            reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertContains(response, 'Test Product')

    def test_add_product_view_by_superuser(self):
        """
        Test the 'add product' view to ensure a superuser can access the page
        and successfully add a product.
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('add_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/add_product.html')

        response = self.client.post(reverse('add_product'), {
            'name': 'New Product',
            'description': 'New Description',
            'price': 20.00,
            'category': self.category.id,
        })
        self.assertRedirects(
            response, reverse(
                'product_detail', args=[Product.objects.last().id]))
        self.assertEqual(Product.objects.count(), 2)

    def test_add_product_view_by_non_superuser(self):
        """
        Test the 'add product' view to ensure a non-superuser is redirected
        when trying to access the page.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('add_product'))
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(Product.objects.count(), 1)

    def test_edit_product_view_by_superuser(self):
        """
        Test the 'edit product' view to ensure a superuser can access the page
        and successfully edit a product.
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(
            reverse('edit_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/edit_product.html')

        response = self.client.post(
            reverse('edit_product', args=[self.product.id]), {
                'name': 'Updated Product',
                'description': 'Updated Description',
                'price': 15.00,
                'category': self.category.id,
            })
        self.assertRedirects(
            response, reverse('product_detail', args=[self.product.id]))
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')

    def test_edit_product_view_by_non_superuser(self):
        """
        Test the 'edit product' view to ensure a non-superuser is redirected
        when trying to access the page.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(
            reverse('edit_product', args=[self.product.id]))
        self.assertRedirects(response, reverse('home'))

    def test_delete_product_view_by_superuser(self):
        """
        Test the 'delete product' view to ensure a superuser can successfully
        delete a product.
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(
            reverse('delete_product', args=[self.product.id]))
        self.assertRedirects(response, reverse('products'))
        self.assertEqual(Product.objects.count(), 0)

    def test_delete_product_view_by_non_superuser(self):
        """
        Test the 'delete product' view to ensure a non-superuser is redirected
        when trying to delete a product.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('delete_product', args=[self.product.id]))
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(Product.objects.count(), 1)
