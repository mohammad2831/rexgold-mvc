from django.db import models
from Account_Module.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    weight = models.BigIntegerField(default=0, null=True, blank=True)
    fee_percent = models.BigIntegerField(default=0)
    price = models.BigIntegerField(default=0)
    user_creator = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='NewProduct/images/', blank=True)

    SALE_TYPE_CHOICES = [
        ('by_weight', 'بر اساس وزن'),
        ('by_quantity', 'بر اساس تعداد'),
    ]
    type = models.CharField(max_length=20, choices=SALE_TYPE_CHOICES, default='by_quantity')

    def __str__(self):
        return f'{self.name}'
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)



class ProductPrice(models.Model):

    product=models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    base_price_sell=models.BigIntegerField(default=0)
    base_price_buy=models.BigIntegerField(default=0)
    time = models.TimeField(auto_now=True)
    is_exist=models.BooleanField(default=True)


    def __str__(self):
        return f'{self.product} - {self.is_exist}'
    