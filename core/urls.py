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
    path('cart/', views.cart, name="cart"),
    path('add-to-cart/<int:choice>/', views.add_to_cart, name="add-to-cart"),
    path('order_checkout/<int:id>/', views.order_checkout, name="order_checkout"),
    path('ordersuccess/<int:id>/<str:session_id>', views.ordersuccess),
]
