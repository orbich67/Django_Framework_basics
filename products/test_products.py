from django.test import TestCase
from products.models import Product, ProductCategory


class ProductsTestCase(TestCase):
    def setUp(self):
        category = ProductCategory.objects.create(name="Обувь")
        self.product_1 = Product.objects.create(name="туфли 1",
                                                category=category,
                                                price=2100.5,
                                                quantity=50)

        self.product_2 = Product.objects.create(name="туфли 2",
                                                category=category,
                                                price=3998.1,
                                                quantity=25,
                                                is_active=False)

        self.product_3 = Product.objects.create(name="туфли 3",
                                                category=category,
                                                price=1098.1,
                                                quantity=45)

    def test_product_get(self):
        product_1 = Product.objects.get(name="туфли 1")
        product_2 = Product.objects.get(name="туфли 2")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_print(self):
        product_1 = Product.objects.get(name="туфли 1")
        product_2 = Product.objects.get(name="туфли 2")
        self.assertEqual(str(product_1), 'туфли 1 (Обувь)')
        self.assertEqual(str(product_2), 'туфли 2 (Обувь)')

    def test_product_get_items(self):
        product_1 = Product.objects.get(name="туфли 1")
        product_3 = Product.objects.get(name="туфли 3")
        products = product_1.get_items()

        self.assertEqual(list(products), [product_1, product_3])
