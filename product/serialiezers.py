from rest_framework.reverse import reverse
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'absolute_url',
            'description',
            'price',
            'get_image',
            'get_thumbnail',
        ]

    def get_absolute_url(self,obj):
        return reverse('product:detail',kwargs={'slug':obj.slug},request=self.context['request'])