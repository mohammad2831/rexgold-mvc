from django.db import models
from Account_Module.models import User, UserGroup
from Product_Data_Module.models import Product, ProductPrice




class Access_All(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    profit_sell=models.BigIntegerField(default=0)
    profit_buy=models.BigIntegerField(default=0)
    time = models.TimeField(auto_now=True)
    active_for_sell=models.BooleanField(default=True)
    active_for_buy=models.BooleanField(default=True)


    max_weight_buy = models.BooleanField(default=0)
    min_weight_buy = models.BooleanField(default=0)

    max_weight_sell = models.BooleanField(default=0)
    min_weight_sell = models.BooleanField(default=0)

    def __str__(self):
        return str(self.product)
    



#save profit for each user group
class Access_By_UserGroup(models.Model):
    group = models.ForeignKey(
        UserGroup, 
        on_delete=models.CASCADE,
        related_name='access_settings'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='group_access_settings'
    )

    profit_sell = models.BigIntegerField(default=0)
    profit_buy = models.BigIntegerField(default=0)
    time = models.DateTimeField(auto_now=True)  # بهتر از TimeField

    active_for_sell = models.BooleanField(default=True)
    active_for_buy = models.BooleanField(default=True)

    max_weight_buy = models.BigIntegerField(default=0)
    min_weight_buy = models.BigIntegerField(default=0)
    max_weight_sell = models.BigIntegerField(default=0)
    min_weight_sell = models.BigIntegerField(default=0)



    def __str__(self):
        return f"{self.group.name} - {self.product}"

#save profit for each user 
class Access_By_User(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    profit_sell=models.BigIntegerField(default=0)
    profit_buy=models.BigIntegerField(default=0)
    time = models.TimeField(auto_now=True)

    active_for_sell=models.BooleanField(default=True)
    active_for_buy=models.BooleanField(default=True)

    max_weight_buy = models.BigIntegerField(default=0)
    min_weight_buy = models.BigIntegerField(default=0)

    max_weight_sell = models.BigIntegerField(default=0)
    min_weight_sell = models.BigIntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product) + " - " + str(self.user)

