"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from shop import views as shop_views
from user_auth import views as user_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', shop_views.index,name='index'),
    path('signup/',user_views.register_view,name='signup'),
    path('login/', user_views.CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', user_views.CustomLogoutView.as_view(template_name='signup.html'), name='logout'),
    path('category/<cid>', shop_views.category_pro_list_view,name='category'),
    path('product/<pid>', shop_views.product_detail_view,name='detail'),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    path('reviewPost/<pid>/',shop_views.reviewPost,name='reviewPost'),
    path('shop/',shop_views.shopView,name='shop'),
    path('add-to-cart/',shop_views.add_to_cart,name='add-to-cart'),
    path('cart/',shop_views.cartView,name='cart'),
    path('delete-from-cart/',shop_views.delete_item_from_cart,name='delete-from-cart'),
    
]  

if settings.DEBUG:
        urlpatterns +=  static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
        urlpatterns +=  static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

