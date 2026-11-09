from django.test import TestCase, Client
from rest_framework.test import APIClient

from .models import Product


class HealthCheckTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_health_endpoint(self):
        response = self.client.get("/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "status": "ok",
                "service": "cloudcart-python",
            },
        )


class ProductAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_products(self):
        Product.objects.create(
            name="Test Product",
            price="499.99",
        )

        response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["name"], "Test Product")

    def test_create_product(self):
        response = self.client.post(
            "/api/products/",
            {
                "name": "New CloudCart Product",
                "price": "299.99",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(
            Product.objects.first().name,
            "New CloudCart Product",
        )

    def test_create_product_without_name(self):
        response = self.client.post(
            "/api/products/",
            {"price": "299.99"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Product.objects.count(), 0)
