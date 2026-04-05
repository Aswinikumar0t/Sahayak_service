

from rest_framework import serializers
from .models import Category, SubCategory, RatePlan


class CategorySerializer(serializers.ModelSerializer):
    subcategories_count = serializers.IntegerField(source='sub_categories.count', read_only=True)
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'icon', 'image', 
            'is_active', 'created_at', 'subcategories_count'
        ]


class SubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_icon = serializers.CharField(source='category.icon', read_only=True)
    category_id = serializers.IntegerField(source='category.id', read_only=True)
    
    class Meta:
        model = SubCategory
        fields = [
            'id', 'category', 'category_id', 'category_name', 'category_icon',
            'name', 'image', 'is_active', 'created_at'
        ]


class RatePlanSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_icon = serializers.CharField(source='category.icon', read_only=True)
    sub_category_name = serializers.CharField(source='sub_category.name', read_only=True)
    
    class Meta:
        model = RatePlan
        fields = [
            'id', 'category', 'category_name', 'category_icon',
            'sub_category', 'sub_category_name',
            'name', 'plan_type', 'price', 'unit', 
            'min_hours', 'description', 'plan_for',
            'is_active', 'created_at'
        ]