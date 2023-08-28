from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("classes/", views.classes, name="classes"),
    path("contact/", views.contact, name="contact"),
    path("profile/", views.profile, name="profile"),
    path("editprofile/",views.editprofile, name="editprofile"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path('payment/<str:choice>', views.payment, name="payment"),
    path("config/", views.stripe_config),
    path('create-checkout-session/<str:choice>', views.create_checkout_session),
    path('success/<str:session_id>', views.success), # new
    path('cancelled/', views.canceled), # new
    path('products/', views.products, name="products"),
    path('add_product/', views.add_product, name='add_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('remove_product/<int:item_id>/', views.remove_product, name='remove_product'),
    path('update_quantity/<int:item_id>/<int:new_quantity>/', views.update_quantity, name='update_quantity'),
    path('all-users/', views.users, name="all-users"),
    path('add-user/', views.add_user, name='add-user'),
    path('cart/', views.cart, name="cart"),
    path('add-to-cart/<int:choice>/', views.add_to_cart, name="add-to-cart"),
    path('order_checkout/<int:id>/', views.order_checkout, name="order_checkout"),
    path('ordersuccess/<int:id>/<str:session_id>', views.ordersuccess),
]
