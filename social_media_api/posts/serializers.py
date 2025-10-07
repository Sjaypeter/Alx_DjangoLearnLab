from rest_framework import serializers
from . models import Post, Comment
from django.contrib.auth import get_user_model

user = get_user_model()

class PostSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField(read_only=True) # shows username instead of ID


    class Meta:
        model = Post
        fields =  ["__all__"]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_title(self, value):
        """Ensure title is not empty or too short."""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value

    def create(self, validated_data):
        """Automatically assign the logged-in user as the author."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    
    author = serializers.StringRelatedField(read_only=True) # shows username instead of ID
    post = serializers.PrimaryKeyRelatedField(read_only = True) # prevents manual post assignment in body

    class Meta:
        model = Comment
        fields = ["__all__"]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_content(self, value):
        """Ensure comment is not empty."""
        if not value.strip():
            raise serializers.ValidationError("Comment content cannot be empty.")
        return value