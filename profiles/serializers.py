from rest_framework import serializers
from .models import Profile
from followers.models import Follower
from categories.models import Category


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    def validate_image(self, value):
        # 2MB
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Avatar size larger than 2MB!'
            )
        if value.image.width > 2048:
            raise serializers.ValidationError(
                'Avatar width larger than 2048px!'
            )
        if value.image.height > 2048:
            raise serializers.ValidationError(
                'Avatar height larger than 2048px!'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            # print(following)
            return following.id if following else None
        return None

    class Meta:
        model = Profile
        fields = [
            'id',
            'owner',
            'created_at',
            'updated_at',
            'name',
            'content',
            'image',
            'is_owner',
            'following_id',
            'posts_count',
            'followers_count',
            'following_count',
        ]
