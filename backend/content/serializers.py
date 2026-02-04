from rest_framework import serializers
from .models import Post, Page

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('slug', 'author', 'created_at', 'updated_at')

class PageSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Page
        fields = '__all__'
        read_only_fields = ('slug', 'author', 'created_at', 'updated_at')

