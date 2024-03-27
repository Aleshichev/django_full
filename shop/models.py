import random
import string

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def rand_slug():
    """
    Generates a random slug consisting of 3 characters from the set of lowercase letters and digits.
    """
    return "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(3)
    )


class Category(models.Model):
    """
    Model representing a category.

    """

    name = models.CharField("Category", max_length=250, db_index=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    slug = models.SlugField(
        "URL", max_length=250, unique=True, null=False, editable=True
    )
    created_at = models.DateTimeField("Create Date", auto_now_add=True)

    class Meta:
        unique_together = ["slug", "parent"]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        """
        Returns a string representation of the object.
        """
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return " -> ".join(full_path[::-1])

    def save(self, *args, **kwargs):
        """
        Saves the current instance of the database.

        """
        if not self.slug:
            self.slug = slugify(rand_slug() + "-pickBetter" + self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop:category_list", args=[str(self.slug)])


class Product(models.Model):
    """
    A model representing a product.

    """

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    title = models.CharField("Title", max_length=250)
    brand = models.CharField("Brand", max_length=250)
    description = models.TextField("Description", blank=True)
    slug = models.SlugField("URL", max_length=250)
    price = models.DecimalField("Price", max_digits=7, decimal_places=2, default=99.99)
    image = models.ImageField("Image", upload_to="product/products/%Y/%m/%d")
    available = models.BooleanField("Available", default=True)
    created_at = models.DateTimeField("Create Date", auto_now_add=True)
    updated_at = models.DateTimeField("Update Date", auto_now=True)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[str(self.slug)])


class ProductManager(models.Manager):
    def get_queryset(self):
        """
        Returns a queryset of available products.

        Returns:
            QuerySet: A queryset of available products.
        """
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):

    object = ProductManager()

    class Meta:
        proxy = True
