from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.sign_up),
    path('login', views.login),
    path('logout', views.logout),

    path('order', views.add_view_order),

    path('cart/<int:pk>', views.add_delete_in_cart),
    path('cart', views.cart_view),

    path('product/<int:pk>', views.product_detail),
    path('product', views.product_add),
    path('products', views.products_get),
]
