from django.urls import path
from .views import  product_detail_view, category_list, ProductListView,search_products

app_name = "shop"

urlpatterns = [
#   path("", products_view, name="products"),
    path("", ProductListView.as_view(), name="products"),
    path("search_products/", search_products, name="search-products"),
    path("search/<slug:slug>/", category_list, name="category_list"),
    path("<slug:slug>/", product_detail_view, name="product_detail"),
]
