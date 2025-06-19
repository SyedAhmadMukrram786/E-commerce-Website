from django.contrib import admin
from django.urls import path
from . import views
from shop.views import JazzCash, success

urlpatterns = [
    path("",views.index, name="ShopHome"),
    path("about/",views.about, name="AboutUs"),
    path("contact/",views.contact, name="ContactUs"),
    path("tracker/",views.tracker, name="TrackingStatus"),
    path("search/",views.search, name="search"),
    path("productview/<int:id>",views.productview, name="product"),
    path("checkout/",views.checkout, name="Checkout"),
    path("products/",views.ProductsDetail, name="Product-Detail"),
    path("jazzcash/",JazzCash, name="jazzcash"),
    path("success/", success, name="success"),
]