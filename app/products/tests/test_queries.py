from django.test import TestCase

from ..models import Category, Product
from ..queries import product_list, product_list_select_related


class ProductsTestMixin(object):
    def setUp(self):
        category = Category.objects.create(name="Test category")

        for num in range(1, 10):
            Product.objects.create(
                title=f"product_{num}",
                category=category
            )


class TestProductList(ProductsTestMixin, TestCase):
    def test_product_list_return_all_products(self):
        """Test product list return all products."""
        products = product_list()

        assert len(products) == Product.objects.count()

        for product in Product.objects.all():
            product_data = {
                "id": product.id,
                "title": product.title,
                "category": product.category.name
            }
            assert product_data in products

    def test_product_list_queries(self):
        """Test product list number of queries."""
        products_count = Product.objects.count()

        # Num queries is equal the number of products + 1
        # For each product we run one new query to get category
        # and we have the first query to get all products
        with self.assertNumQueries(products_count + 1):
            product_list()


class TestProductListSelectRelated(ProductsTestMixin, TestCase):
    def test_product_list_select_related_return_all_products(self):
        """Test product list return all products."""
        assert product_list() == product_list_select_related()

        products = product_list_select_related()

        assert len(products) > 1
        assert len(products) == Product.objects.count()

        for product in Product.objects.all():
            product_data = {
                "id": product.id,
                "title": product.title,
                "category": product.category.name
            }
            assert product_data in products

    def test_product_list_queries(self):
        """Test product list number of queries."""
        # Num queries is equal to 1 because we are using select related
        with self.assertNumQueries(1):
            product_list_select_related()
