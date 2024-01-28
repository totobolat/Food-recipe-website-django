from decimal import Decimal
from rest_framework import serializers
from .models import Category, Chef, Resipi, ResipiImage, ResipiRating, Review
from django.db.models.aggregates import Count, Avg

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'resipis_count']
    # def resipiInCategory(self, category:Category):
    #    return Category.objects.filter(id=collection.id).aggregate(Count('product'))
    # resipis_count = serializers.SerializerMethodField(method_name='resipiInCategory')
    resipis_count = serializers.IntegerField(read_only=True)

class ResipiImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        resipi_id = self.context['resipi_id']
        return ResipiImage.objects.create(resipi_id=resipi_id, **validated_data)
    class Meta:
        model = ResipiImage
        fields = ['id', 'image']

class ResipiSerializer(serializers.ModelSerializer):
    images = ResipiImageSerializer(many=True, read_only=True) 
    class Meta:
        model = Resipi
        fields = ['id', 'title', 'description', 'slug', 'ingredients',
         'how_to', 'category', 'images']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'title', 'date', 'description']
    
    def create(self, validated_data):
        resipi_id = self.context['resipi_id']
        validated_data['resipi_id'] = resipi_id
        return Review.objects.create(**validated_data)

class ChefSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Chef
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']