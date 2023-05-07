from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=250)
    image = models.CharField(max_length=500, default='https://www.bonbonentertainment.nl/wp-content/uploads/2021/06/no-image.jpg')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        # ordering = ('name',)

    def to_json(self):
        return {
            'name': self.name,
            'image': self.image
        }

    def __str__(self):
        return f'{self.id}: {self.name}'


class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=1000)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    image = models.CharField(max_length=500, default='https://www.bonbonentertainment.nl/wp-content/uploads/2021/06/no-image.jpg')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ('-price',)

    def to_json(self):
        return {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category_id,
            'image': self.image
        }

    def __str__(self):
        return f'{self.id}: {self.name} {self.price}: {self.description}'


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order')
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ('-date',)

    def to_json(self):
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_price': self.product_price,
            'date': self.date
        }

    def __str__(self):
        return f'{self.id}:{self.product.name} - {self.date}'


class Comment(models.Model):
    nickname = models.CharField(max_length=250)
    text = models.TextField(max_length=1000)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment')
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('-date',)

    def to_json(self):
        return {
            'nickname': self.nickname,
            'text': self.text,
            'product': self.product_id,
            'date': self.date
        }

    def __str__(self):
        return f'{self.nickname}: {self.text}'


