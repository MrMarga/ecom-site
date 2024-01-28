from imp import reload
from django.shortcuts import redirect, render,get_object_or_404
from shop.models import Product,Category,Vendor,ProductImages,ProductReview,Product_price,Product_sizes,Product_colors
from .models import Product
from shop.forms import ProductReviewForm
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string


# Create your views here.


def index(request): 
    products = Product.objects.all()
    category = Category.objects.all()
    vendors = Vendor.objects.all()
  
    context={
        'products' :products,
        'category' :category,
        'vendors'  :vendors,
    }
    return render(request,'shop/index.html',context)
    

def category_pro_list_view(request,cid):
    category=Category.objects.get(cid=cid)
    products=Product.objects.filter(product_status="published",category=category)
    #getting all the published product using category foreign key and give it to the variable category here
    
    context = {
        'category' : category ,
        'products' : products , 
    }

    return render(request,'shop/category_pro_list.html',context)



def product_detail_view(request,pid):  
    
    product = Product.objects.get(pid=pid)
    
    sizes = Product_sizes.objects.all()
    colors = Product_colors.objects.all()
    
    products = Product.objects.filter(category=product.category)
    #this gives the product related the above product.
    #getting product by the category of the current product.
    #Related Product in model .
    
    p_imgs = product.p_images.all() #here product is from above pid 
    # this will bring all  the images related to specific product 
    # using "ProductImage" model by its foreign key 'product'  
    
    #getting all reviews
    reviews = ProductReview.objects.filter(product=product).order_by('-date')
    
    
    # to render form in the detail page that we created in form.py
    review_form = ProductReviewForm()
    
    
    # for making only one review for onr product if user is logged in .
    make_review = True
    
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
           make_review = False

    
    context = {
        'make_review' : make_review, 
        'product' : product,
        'products': products,
        'p_imgs'  : p_imgs,
        'reviews'  : reviews,
        'review_form' : review_form, 
        # 'colors': colors,
        'sizes' : sizes,     
    }
    return render(request,'shop/detail.html',context)


    
def reviewPost(request,pid):
    
    product = Product.objects.get(pid=pid)
    
    user = request.user # gets current logged in user
    
    review = ProductReview.objects.create(
        user = user ,
        product = product, 
        review = request.POST['review'],
        rating = request.POST['rating']
    )
    
    context = {
       
        'user' : user.username,
        'review' : request.POST['review'],
        'rating' : request.POST['rating']
    }
    
    return JsonResponse(
        
        {
        'bool':True,
        'context' : context,
        }
        
    )
    
    

def shopView(request):
    query = request.GET.get('q')

    sizes = Product_sizes.objects.all()
    prices = Product_price.objects.all()
    colors = Product_colors.objects.all()

    selected_color = request.GET.getlist('selected_color')
    selected_size = request.GET.getlist('selected_size')
    selected_price = request.GET.getlist('selected_price')

    # Start with all products
    products = Product.objects.all()

    if '1' in selected_color or '1' in selected_size:
        # Display all products if either selected_color or selected_size has the value '1'
        pass
    else:
        if selected_color:
            products = products.filter(color__in=selected_color)

        if selected_size:
            products = products.filter(size__in=selected_size)

    if selected_price:
        # Assuming price_range is a numeric field, you might want to adjust this logic accordingly
        # For example, if it's a ForeignKey, you may need to change the field used in the filter
        products = products.filter(price_range__in=selected_price)

    if not selected_color and not selected_size and not selected_price:
        products = Product.objects.all()

    if query:
        products = products.filter(title__icontains=query).order_by('-date')

    context = {
        'query': query,
        'products': products,
        'sizes': sizes,
        'prices': prices,
        'colors': colors,
        'selected_color': selected_color,
        'selected_size': selected_size,
        'selected_price': selected_price,
    }

    return render(request, 'shop/shop.html', context)




def add_to_cart(request):
    # Check if all required parameters are present
    required_parameters = ['id', 'title', 'qty', 'price', 'image', 'pid']
    if not all(param in request.GET for param in required_parameters):
        return JsonResponse({"error": "Required parameters are missing."}, status=400)

    # Create a dictionary for the new product
    new_product = {
        'title': request.GET['title'],
        'qty': int(request.GET['qty']),
        'price': float (request.GET['price']),
        'image': request.GET['image'],
        'pid': request.GET['pid']
    }

    # Get the existing cart data or create an empty dictionary
    cart_data = request.session.get('cart_data_obj', {})

    # Update or add the new product to the cart
    cart_data[str(request.GET['id'])] = new_product

    # Update the session with the modified cart data
    request.session['cart_data_obj'] = cart_data

    # Return the updated cart data and total cart items
    return JsonResponse({"cart_ data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})




def cartView(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float (item['price'])
        return render(request, 'shop/cart.html', {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    else:
        messages.warning(request,"Empty Cart.!!")
        return redirect("index")

    


def delete_item_from_cart(request):
    
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float (item['price'])
            
    context = render_to_string("shop/cart-list.html",{"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({
        'data':context,
        'totalcartitems': len(request.session['cart_data_obj']
        )})
    
    


