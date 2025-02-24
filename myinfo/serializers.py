from rest_framework import serializers
from rest_framework import serializers

class GetPersonDataSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=100,
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Authorization code is required',
            'blank': 'Authorization code cannot be blank'
        }
    )
