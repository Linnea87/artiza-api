from django.db import IntegrityError
from rest_framework import serializers
from bookmarks.models import Bookmark


# based on Like serializers provided by DRF-API walkthrough.
class BookmarkSerializer(serializers.ModelSerializer):
    """
    Serializer for the Bookmark model.
    The create method handles the unique constraint on 'owner' and 'post'
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Bookmark
        fields = [
            'id',
            'created_at',
            'owner',
            'post'
        ]

    def create(self, validated_data):
        """
        Bookmark validation.
        The create method handles the unique constraint on 'owner' and 'post'.
        """
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })