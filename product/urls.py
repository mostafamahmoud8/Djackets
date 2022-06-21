from django.urls import path
from .views import (LatestProductListView, ProductDetailView
                    ,CategoryProductView)

app_name = 'product'

urlpatterns = [
    path('latest/', LatestProductListView.as_view(),name='latest_products'),
    path('products/<slug:slug>/', ProductDetailView.as_view(),name='detail'),
    path('products/<slug:c_slug>/<slug:p_slug>/', CategoryProductView.as_view(),name='Category_product'),

]