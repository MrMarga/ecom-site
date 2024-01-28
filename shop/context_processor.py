from .models import Product,Category,Vendor,ProductImages,CartOrder,CartOrderItem,ProductReview,Wishlist,Address,Product_colors,Product_sizes,Product_price
 

def default(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    address = Address.objects.get(user=request.user)
    # This gets the user currently logged in .  
    sizes = Product_sizes.objects.all()
    prices = Product_price.objects.all()
    color = Product_colors.objects.all()
    j_ar = Product.objects.filter(just_arrived=True)  # to filter all the arrived products
    trendy = Product.objects.filter(is_trendy=True)  # to filter all the trendy products
    
    return {
        'categories' : categories ,
        'address'    : address , 
         'j_ar'     :j_ar,
        'trendy'   :trendy,
       'products'  : products,
        'sizes' :sizes,
        'prices' : prices,
        'color' : color
    }



