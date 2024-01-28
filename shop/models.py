from django.db import models

# Create your models here.

from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from user_auth.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


STATUS_CHOICE = (
    
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    
    ("draft", "Processing"),
    ("disabled", "disabled"),
    ("rejected", "rejected"),
    ("in_review", "in_review"),
    ("published", "published"),
)


RATING = (
    
    ( 1,  "⭐☆☆☆☆"),
    ( 2,  "⭐⭐☆☆☆"),
    ( 3,  "⭐⭐⭐☆☆"),
    ( 4,  "⭐⭐⭐⭐☆"),
    ( 5,  "⭐⭐⭐⭐⭐"),
)


 #This is a function named user_directory_path that seems to be generating a directory path for storing user-specific files
 
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

    #So, the final path would look something like ''user_123/filename.txt'', where 123 is the user's ID and filename.txt is the original filename

# Create your models here.

class Product_colors(models.Model):
   
   PRODUCT_COLOR= ( 
                  
        ('ALL' , 'ALL'),
         ('Black' , 'Black'),
         ('White' , 'White'),
         ('Red' , 'Red'),
         ('Blue' , 'Blue'),
         ('Green' , 'Green'),
         
         
        )
    
   color = models.CharField(choices=PRODUCT_COLOR,max_length=50)
   price = models.DecimalField(max_digits=9999999999, decimal_places=2, default='1.99')
   
   def __str__(self) -> str:
       return self.color


class Product_sizes(models.Model):
   
   PRODUCT_SIZE= ( 
         ('ALL' , 'ALL'),
         ('XS' , 'XS'),
         ('S' , 'S'),
         ('M' , 'M'),
         ('L' , 'L'),
         ('XL' , 'XL'),
         
        )
    
   size = models.CharField(choices=PRODUCT_SIZE,max_length=50)
   price = models.DecimalField(max_digits=9999999999, decimal_places=2, default='1.99')
   
   def __str__(self) -> str:
       return self.size

class Product_price(models.Model):
    
    PRODUCT_PRICE= ( 
         ('ALL' , 'ALL'),          
         ('$0 - $100' , '$0 - $100'),
         ('$100 - $200' , '$100 - $200'),
         ('$200 - $300' , '$200 - $300'),
         ('$300 - $400' , '$300 - $400'),
         ('$400 - $500' , '$400 - $500'),      
        )
    
    def __str__(self) -> str:
        return self.price
    
    price_range = models.CharField(choices=PRODUCT_PRICE,max_length=50)


class Category(models.Model):
    cid = ShortUUIDField(unique=True,length=10,max_length=20,prefix='cat',alphabet='marga1234')
    # makes the cid - 'cat46541....'
    
    title = models.CharField(max_length=100 , default='food')
    
    image = models.ImageField(upload_to='category',default='category.jpg')
    
    class Meta:
        verbose_name_plural = 'Categories' # for getting name categories rather categoyrs
    
    def __str__(self) -> str:
        return self.title

    def category_image(self):
        return mark_safe("<img src='%s' width='50' height='50' />" % self.image.url)

# class Tags(models.Model):
#         pass

class Vendor(models.Model):
        vid = ShortUUIDField(unique=True,length=10,max_length=20,prefix='ven',alphabet='abcd1234')
        title = models.CharField(max_length=100, default='Marga')
        image = models.ImageField(upload_to=user_directory_path)
        address = models.CharField(max_length=100, default='kathmandu-8 ,new-road')
        contact = models.CharField(max_length=100, default='+977-9845512345')
        shipping_on_time = models.CharField(max_length=100, default='100%')
        contact = models.CharField(max_length=100, default='100')
        days_return = models.CharField(max_length=100, default='30')
        warranty_period= models.CharField(max_length=100, default='100')
        chat_resp_time = models.CharField(max_length=100, default='100')
        authentic_rating = models.CharField(max_length=100, default='100')
        # description=models.TextField(null=True,blank=True,default="I am a amazing vendor")
        description=RichTextUploadingField(null=True,blank=True,default="I am a amazing vendor")
        user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
        # if cascade was chosen => When ever a user was delete the whole shop will be deleted. or Null don't delete it sets to null.
        
        
        class Meta:
            verbose_name_plural = 'vendors' # for getting name categories rather catogoyrs
        
        def __str__(self) -> str:
            return self.title

        def vendor_image(self):
         return mark_safe("<img src='%s' width='50' height='50' />" % self.image.url)
      

class Product(models.Model):
    
    pid = ShortUUIDField(unique=True,length=10,max_length=20,alphabet='abc1234')
    # makes the cid - 'cat46541....'
    
    title = models.CharField(max_length=40)
    
    # color = models.ManyToManyField(Product_colors,blank=True) 
    
    # size = models.ManyToManyField(Product_sizes,blank=True)
    
    price_range = models.ManyToManyField(Product_price,blank=True)
    
    image = models.ImageField(upload_to=user_directory_path, default='product.jpg')
    
    # description=models.TextField(null=True,blank=True,)
    
    description=RichTextUploadingField(null=True,blank=True,default="This is a product.")
 
    # When user that created the product is delete do you want to product -so
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True , related_name='category')  #related name for getting number of products for category
    # so that when category is delete product not deleted
    # each products are staying under one category 
    
    price = models.DecimalField(max_digits=9999999999, decimal_places=2, default='1.99')
    
    old_price = models.DecimalField(max_digits=9999999999, decimal_places=2, default='2.99')
    
    # specifications = models.TextField(null=True,blank=True)
    
    specifications=RichTextUploadingField(null=True,blank=True)
    
    tags = TaggableManager(blank=True)
    
    product_status = models.CharField(choices=STATUS, max_length=10 , default="in_review")
    
    pro_qty = models.IntegerField(null=True)
    
    just_arrived = models.BooleanField(default=False)
    
    is_trendy =  models.BooleanField(default=False)
    
    in_stock = models.BooleanField(default=True)
    
    featured = models.BooleanField(default=False)
    
    digital = models.BooleanField(default=False)
    
    sku = ShortUUIDField (unique=True, length=4 , max_length=10 , prefix="sku" , alphabet ="1234567890")  
    
    date = models.DateTimeField(auto_now_add=True)
    
    updated = models.DateTimeField(null=True, blank=True)  
    
    class Meta:
        verbose_name_plural = 'products' # for getting name categories rather product
        
    def __str__(self) -> str:
            return self.title

    def product_image(self):
     return mark_safe("<img src='%s' width='50' height='50' />" % self.image.url)
 
    def get_percentage(self):
        new_price_per = (self.price / self.old_price)* 100
        return new_price_per
    

class ProductImages(models.Model):
    
    images = models.ImageField(upload_to="product-images",default='product.jpg')
    
    #what ever images we upload here. we are linking it to the main class product
    
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='p_images')
    #related image is used to link images to the product
    
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'images' # for getting name categories rather product
        
        
       
       
        
######################  Cart , OrderItems   ############################
######################  Cart , OrderItems   ###########################
######################  Cart , OrderItems   ############################  
######################  Cart , OrderItems   ############################

class CartOrder(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
     
    price = models.DecimalField(max_digits=9999999999, decimal_places=2, default='1.99')

    paid_status = models.BooleanField(default=True)
    
    order_date = models.DateTimeField(auto_now_add=True)
    
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30 , default="processing")
    
    class Meta:
        verbose_name_plural = 'Cart Order'


class CartOrderItem(models.Model):
    
    invoice_no = models.CharField(max_length=200)
    
    order = models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    
    product_status = models.CharField(max_length=200)
    
    item = models.CharField(max_length=200)
    
    image = models.CharField(max_length=200)
    
    qty = models.IntegerField(default=0)
    
    price = models.DecimalField(max_digits=9999999999, decimal_places=2, default='1.99')
    
    total = models.DecimalField(max_digits=9999999999, decimal_places=2, default='1.99')
 
    

    class Meta:
        verbose_name_plural = 'Cart Order Items'
        
        
    def order_img(self):
            return mark_safe("<img src = '/media/%s' width=50px height='50' />" % (self.image))


         
######################  Product Review, Wishlist , Address  ############################
######################  Product Review, Wishlist , Address  ############################
######################  Product Review, Wishlist , Address  ############################
######################  Product Review, Wishlist , Address  ############################

class ProductReview(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True , related_name='pro_reviews',default='0')

    review = models.TextField()
    
    rating = models.IntegerField(choices=RATING, default=None)
    
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        
        verbose_name_plural = 'Product Reviews' # for getting name categories rather catogoyrs
        
    def __str__(self) -> str:
        
        return self.product.title

    def get_rating(self):
        return self.rating   
    
class Wishlist(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        
        verbose_name_plural = 'Wishlists' # for getting name categories rather catogoyrs
        
    def __str__(self) -> str:
        
        return self.product.title



class Address(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    address = models.CharField(max_length=100,null=True)
    
    status = models.BooleanField(default=False)
 
    class Meta:
        
        verbose_name_plural = 'Address'