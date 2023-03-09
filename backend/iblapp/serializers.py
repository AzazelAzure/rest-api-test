from rest_framework.fields import CharField
from iblapp import models
from rest_framework import serializers
import logging

logger = logging.getLogger(__name__)


# class GreetingSerialize(serializers.ModelSerializer):
#     message = serializers.CharField(max_length=100)


class GreetingSerializer(serializers.ModelSerializer):
    message = serializers.CharField(source="description")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        logger.info('Message recieved: %s', data.get('message'))
        logger.info('Data recieved: %s', data)
        return {
            "data": {
                "id": instance.id,
                "attributes": data,
            }
        }

    class Meta:
        model = models.Greeting
        type = 'greetings'
        fields = (
            'message',
        )
