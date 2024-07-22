from rest_framework import serializers
from .models import Comment, Post, Rating


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'text', 'created_date', 'user']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','post', 'author', 'text', 'created_date']

class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'text', 'created_date', 'user', 'average_rating', 'comments']

    def get_average_rating(self, obj):
        return obj.average_rating()


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['post', 'auth', 'mark_number']

