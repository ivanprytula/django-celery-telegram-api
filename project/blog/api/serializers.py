from rest_framework import serializers

from accounts.models import CustomUser
from blog.models import Comment
from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CommentSerializer(serializers.Serializer):
    post = PostSerializer()
    commenter_name = serializers.CharField()
    author = CustomUserSerializer()

    content = serializers.CharField()
    created_at = serializers.DateTimeField()
    active = serializers.BooleanField()

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.commenter_name = validated_data.get('commenter_name', instance.commenter_name)
        instance.content = validated_data.get('content', instance.content)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        return instance
