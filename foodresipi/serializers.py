from decimal import Decimal
from rest_framework import serializers
from .models import Category, Chef, Resipi, ResipiImage, ResipiRating, Review
from django.db.models.aggregates import Count, Avg

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'resipis_count', 'slug']
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
class ChefSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Chef
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']


class ResipiSerializer(serializers.ModelSerializer):
    images = ResipiImageSerializer(many=True, read_only=True)
    chef_id = serializers.IntegerField()
    class Meta:
        model = Resipi
        fields = ['id', 'title', 'chef_id', 'description', 'slug', 'ingredients',
         'how_to', 'category', 'avg_rating', 'images']
    # def calculateAvg(self, ):
    #     Resipi.objects.filter(id=collection.id).aggregate(Count('product'))
    #     return 
    # avg_rating = serializers.SerializerMethodField(method_name='calculateAvg')

class CategoryResipiSerializer(serializers.ModelSerializer):
    images = ResipiImageSerializer(many=True, read_only=True) 
    class Meta:
        model = Resipi
        fields = ['id', 'title', 'category', 'avg_rating', 'images']

    # def create(self, validated_data):
    #     category_slug = self.context['resipis_slug']
    #     return Resipi.objects.create(category_slug=category_slug, **validated_data)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'title', 'date', 'description']
    
    def create(self, validated_data):
        resipi_id = self.context['resipi_id']
        validated_data['resipi_id'] = resipi_id
        return Review.objects.create(**validated_data)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResipiRating
        fields = ['stars']
    
    def create(self, validated_data):
        resipi_id = self.context['resipi_id']
        validated_data['resipi_id'] = resipi_id
        return Review.objects.create(**validated_data)