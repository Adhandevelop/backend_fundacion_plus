from rest_framework import serializers
from apps.news.models import NewsArticle, NewsCategory


class NewsCategorySerializer(serializers.ModelSerializer):
    articles_count = serializers.IntegerField(source='articles.count', read_only=True)

    class Meta:
        model = NewsCategory
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'is_active',
            'articles_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'articles_count', 'created_at', 'updated_at']


class NewsArticleListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    related_initiative_name = serializers.CharField(source='related_initiative.name', read_only=True)
    related_initiative_slug = serializers.CharField(source='related_initiative.slug', read_only=True)

    class Meta:
        model = NewsArticle
        fields = [
            'id',
            'title',
            'slug',
            'summary',
            'cover_image',
            'category',
            'category_name',
            'related_initiative',
            'related_initiative_name',
            'related_initiative_slug',
            'author',
            'author_name',
            'publication_status',
            'is_featured',
            'published_at',
            'created_at',
        ]
        read_only_fields = fields


class NewsArticleDetailSerializer(NewsArticleListSerializer):
    class Meta(NewsArticleListSerializer.Meta):
        fields = NewsArticleListSerializer.Meta.fields + ['content', 'updated_at']
        read_only_fields = [
            'id',
            'slug',
            'category_name',
            'author',
            'author_name',
            'related_initiative_name',
            'related_initiative_slug',
            'published_at',
            'created_at',
            'updated_at',
        ]
