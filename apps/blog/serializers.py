from rest_framework import serializers
from .models import Post, Category, Heading, PostView, CategoryAnalytics, PostAnalytics, PostInteraction, PostLike, PostShare, Comment
from apps.media.serializers import MediaSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name',
            'slug',
            'thumbnail'
        ]

class CategoryAnalyticsSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = CategoryAnalytics
        fields = [
            "id",
            "category_name",
            "views",
            "impressions",
            "clicks",
            "click_through_rate",
            "avg_time_on_page",
        ]

    def get_category_name(self, obj):
        return obj.category.name

class HeadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heading
        fields = [
            "title",
            "slug",
            "level",
            "order",
        ]

class PostViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostView
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    headings = HeadingSerializer(many=True)
    view_count = serializers.SerializerMethodField() #el nombre de esta variable debe ser igual a la funcion sin e get_ y se agrega view_count a all (en este caso por que es all se agrega automanticamente)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    thumbnail = MediaSerializer()
    user = serializers.StringRelatedField()
    class Meta:
        model = Post
        fields = "__all__"

    def get_view_count(self, obj):
        return obj.post_analytics.views if obj.post_analytics else 0

    def get_comments_count(self, obj):
        return obj.post_comments.filter(parent=None, is_active=True).count()

    def get_lkikes_count(self, obj):
        return obj.likes.filter().count()

    def get_has_liked(self, obj):
        """
        Verifica si el usuario autenticado ha dado 'like' al post.
        """
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return PostLike.objects.filter(post=obj, user=user).exists()
        return False

class PostListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()
    view_count = serializers.SerializerMethodField()
    thumbnail = MediaSerializer()
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "description",
            "thumbnail",
            "slug",
            "category",
            "view_count"
        ]

    def get_view_count(self, obj):
        return obj.post_analytics.views if obj.post_analytics else 0

class PostAnalyticsSerializer(serializers.ModelSerializer):
    post_title = serializers.SerializerMethodField()

    class Meta:
        model = PostAnalytics
        fields = [
            "id",
            "post_title",
            "impressions",
            "clicks",
            "click_through_rate",
            "avg_time_on_page",
            "views",
            "likes",
            "comments",
            "shares",
        ]

    def get_post_title(self, obj):
        return obj.post.title


class PostInteractionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField() # Devuelve el email del usuario; devuelve lo de la fucnion __STR__, que esta en models
    post_title = serializers.SerializerMethodField()
    comment_content = serializers.SerializerMethodField()

    def get_post_title(self, obj):
        return obj.post.title #recordar que en postinteraction post es llave foranea
    
    def get_comment_content(self, obj):
        return obj.comment.content if obj.comment else None
    
    class Meta:
        model = PostInteraction
        fields = [
            "id",
            "user",
            "post",
            "post_title", #definido en esta clase
            "interaction_type",
            "interaction_category",
            "weight",
            "timestamp",
            "device_type",
            "ip_address",
            "hour_of_day",
            "day_of_week",
            "comment_content", #definido en esta clase
        ]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    post_title = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()
    # replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "post",
            "post_title",
            "parent",
            "content",
            "created_at",
            "updated_at",
            "is_active",
            "replies_count",
            # "replies",
        ]

    def get_post_title(self, obj):
        return obj.post.title

    def get_replies(self, obj):
        replies = obj.replies.filter(is_active=True)
        return CommentSerializer(replies, many=True).data
    
    def get_replies_count(self, obj):
        return obj.replies.filter(is_active=True).count()


class PostLikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = PostLike
        fields = [
            "id",
            "post",
            "user",
            "timestamp",
        ]


class PostShareSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = PostShare
        fields = [
            "id",
            "post",
            "user",
            "platform",
            "timestamp",
        ]