from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category =  models.CharField(max_length=50, default="")
    subcategory =  models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=300)
    price = models.IntegerField(default=0)
    published_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")
    
    def __str__(self):
        return self.product_name
    
class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    desc = models.CharField(max_length=5000)
    
    def __str__(self):
        return self.name


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(max_length=100,default=0)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=111)
    phone = models.CharField(max_length=30,default="")
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)

    def __str(self):
        return self.name
    
class Order_Update(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default=0)
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."