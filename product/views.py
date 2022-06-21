from django.http import Http404
from rest_framework.views import APIView 
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from .serialiezers import ProductSerializer
from .models import Product
# Create your views here.

class LatestProductListView(APIView):

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()[:5]
        serializer = ProductSerializer(products,many=True,context={'request':request})

        return Response(serializer.data)

class CategoryProductView(APIView):
    
    def get_object(self, category_slug, product_slug):
        try:
            product = Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
            return product
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, c_slug, p_slug):
        product = self.get_object(c_slug, p_slug)
        serializer = ProductSerializer(product,context={'request':request})
        return Response(serializer.data)

class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'