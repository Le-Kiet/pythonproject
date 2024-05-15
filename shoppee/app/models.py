from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your models here.
#Change form register
class CreateUserForm(UserCreationForm):
    # """
    # A custom form that inherits from the Django UserCreationForm.
    # It adds additional fields to the user creation form, such as email, first name, and last name.
    
    # Inputs:
    #     None
    
    # Outputs:
    #     A form with the following fields: username, email, first_name, last_name, password1, password2
    # """
    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name','password1','password2' ]

class Category(models.Model):
    # """
    # A model that represents a category or subcategory for products.
    # It has fields for the subcategory, a boolean flag to indicate if it is a subcategory,
    # the category name, a slug for URL generation, and an optional image.
    
    # Inputs:
    #     sub_category (models.ForeignKey): The parent subcategory, if this is a subcategory.
    #     is_sub (models.BooleanField): A flag indicating if this is a subcategory.
    #     name (models.CharField): The name of the category.
    #     slug (models.SlugField): The slug for the category, used in URLs.
    #     image (models.ImageField): An optional image for the category.
        
    # Outputs:
    #     The string representation of the category name.
    # """
    sub_category=models.ForeignKey('self',on_delete=models.CASCADE,related_name='sub_categories',null=True,blank=True)
    is_sub=models.BooleanField(default=False)
    name = models.CharField(max_length=200,null=True)
    slug = models.SlugField(max_length=200,unique=True)
    image = models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url
class SubCategory(models.Model):
    # """
    # A model that represents a subcategory for a product.
    # It has a foreign key relationship with the Category model and a name field.
    
    # Inputs:
    #     category (models.ForeignKey): The parent category for this subcategory.
    #     name (models.CharField): The name of the subcategory.
        
    # Outputs:
    #     The string representation of the subcategory name.
    # """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='child_sub_categories')
    name = models.CharField(max_length=200, null=True, unique=True)

    def __str__(self):
        return self.name
    def get_all_sub_categories(self):
        return self.name
class Product(models.Model):
    # """
    # The Product class represents a product entity in the system.

    # Input:
    #     category (models.ManyToManyField): The category or categories the product belongs to.
    #     sub_category (models.ForeignKey): The sub-category the product belongs to.
    #     name (models.CharField): The name of the product.
    #     price (models.FloatField): The price of the product.
    #     digital (models.BooleanField): Indicates whether the product is digital or not.
    #     image (models.ImageField): The image of the product.
    #     detail (models.TextField): The detailed description of the product.
    #     discount (models.IntegerField): The discount percentage applied to the product.
    #     address (models.CharField): The address of the product.

    # Output:
    #     __str__(): Returns the name of the product.
    #     ImageURL: Returns the URL of the product image.
    #     get_total(): Calculates the total price of the product after applying the discount.
    # """
    category = models.ManyToManyField(Category,related_name="product")
    sub_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True,related_name="sub_products",limit_choices_to={"is_sub": True})
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True,blank=False)
    image = models.ImageField(null=True,blank=True)
    detail =models.TextField(null=True,blank=True)
    discount = models.IntegerField(default=0)
    address = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url
    def get_total(self):
        total = self.price
        if self.discount != 0:
            total = total * (100 - self.discount) / 100
        return total 
class Order(models.Model):
    # """
    # The Order class represents a customer order.

    # Input:
    #     customer (models.ForeignKey): The customer who placed the order.
    #     date_order (models.DateTimeField): The date and time the order was placed.
    #     complete (models.BooleanField): Indicates whether the order is complete or not.
    #     transaction_id (models.CharField): The unique identifier for the order transaction.

    # Output:
    #     __str__(): Returns the order ID.
    #     get_cart_items: Calculates the total number of items in the order.
    #     get_cart_total: Calculates the total price of the items in the order.
    # """
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)
    def __str__(self):
        return str(self.id)
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
class OrderItem(models.Model):
    # """
    # The OrderItem class represents an item in a customer order.

    # Input:
    #     product (models.ForeignKey): The product included in the order item.
    #     order (models.ForeignKey): The order the item belongs to.
    #     quantity (models.IntegerField): The quantity of the product in the order item.
    #     date_added (models.DateTimeField): The date and time the order item was added.

    # Output:
    #     get_total: Calculates the total price of the order item after applying the discount.
    # """
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        total =  self.product.price * self.quantity * (100-self.product.discount) /100
        return total
class ShippingAddress(models.Model):
    # """
    # The ShippingAddress class represents the shipping address for an order.

    # Input:
    #     customer (models.ForeignKey): The customer associated with the shipping address.
    #     order (models.ForeignKey): The order the shipping address belongs to.
    #     address (models.CharField): The shipping address.
    #     city (models.CharField): The city of the shipping address.
    #     state (models.CharField): The state of the shipping address.
    #     mobile (models.CharField): The mobile number associated with the shipping address.
    #     date_added (models.DateTimeField): The date and time the shipping address was added.

    # Output:
    #     __str__(): Returns the shipping address.
    # """
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    mobile = models.CharField(max_length=10,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address

class Province(models.Model):
    # """
    # The Province class represents a province or region.

    # Input:
    #     id (models.AutoField): The unique identifier for the province.
    #     name (models.CharField): The name of the province.

    # Output:
    #     __str__(): Returns the name of the province.
    #     get_all_sub_categories(): Returns the name of the province.
    # """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, unique=True)

    def __str__(self):
        return self.name

    def get_all_sub_categories(self):
        return self.name
    