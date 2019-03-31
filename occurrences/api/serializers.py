from rest_framework import serializers

from django.utils import timezone

from api.models import Occurence, OccurenceState, \
    OccurenceCategory


class OccurenceCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField(max_length=20)
    description = serializers.CharField(max_length=200)


class OccurenceStateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    description = serializers.CharField(max_length=200)


class OccurenceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    description = serializers.CharField(
        max_length=200, 
        required=False
    )
    geo_location = serializers.CharField()
    author = serializers.CharField(max_length=200)
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
            'creation_date': timezone.now(),
            'modified_date': timezone.now(),
            'occurence_state_id': OccurenceState.objects.get(description='por validar')\
                                                        .id
        })
        return Occurence.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.modified_date = timezone.now()
        instance.occurence_state = validated_data.get('occurence_state')
        instance.save()
        return instance