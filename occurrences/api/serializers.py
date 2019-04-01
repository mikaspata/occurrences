import datetime
from rest_framework import serializers

from django.contrib.auth.models import User

from api.models import Occurence, OccurenceState, \
    OccurenceCategory


class OccurenceCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField(max_length=20)
    description = serializers.CharField(max_length=200)


class OccurenceStateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    description = serializers.CharField(max_length=200)


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)


class OccurenceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    description = serializers.CharField(
        max_length=200, 
        required=False
    )
    geo_location = serializers.CharField(required=False)
    author_id = serializers.PrimaryKeyRelatedField(
        source='author', 
        queryset=User.objects.all(),
        required=False
    )
    author = AuthorSerializer(read_only=True)
    creation_date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", 
        required=False, 
        read_only=True
    )
    modified_date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", 
        required=False, 
        read_only=True
    )
    occurence_state_id = serializers.PrimaryKeyRelatedField(
        source='occurence_state', 
        queryset=OccurenceState.objects.all()
    )
    occurence_state = OccurenceStateSerializer(read_only=True)
    occurence_category_id = serializers.PrimaryKeyRelatedField(
        source='occurence_category', 
        queryset=OccurenceCategory.objects.all()
    )
    occurence_category = OccurenceCategorySerializer(read_only=True)

    def create(self, validated_data):
        validated_data.update({
            'creation_date': datetime.datetime.now(),
            'modified_date': datetime.datetime.now(),
            'occurence_state_id': OccurenceState.objects.get(description='por validar')\
                                                        .id,
        })
        return Occurence.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.modified_date = datetime.datetime.now()
        instance.occurence_state = validated_data.get('occurence_state')
        instance.save()
        return instance