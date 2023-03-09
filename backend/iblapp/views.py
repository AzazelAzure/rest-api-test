from django.shortcuts import render
from rest_framework.response import Response
from iblapp.serializers import GreetingSerializer as GS
from rest_framework import views, status
from iblapp.models import Greeting
from rest_framework_json_api.parsers import JSONParser
from json import JSONDecodeError
from django.http import JsonResponse
from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse
import json
import requests
import logging


logger = logging.getLogger(__name__)


class GreetingAPIView(views.APIView, ProtectedResourceView):
    """
    API to take a greeting, save, and log it
    """

    serializer_class = GS

    def get_serializer_context(self):
        return {
            'type': self.type,
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request):
        return self.save_greeting(request)

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello Worlds')

    def save_greeting(self, request):
        try:
            data = request.data
            logger.debug('Received data: %s', data)
            serializer = GS(data=data)
            if serializer.is_valid():
                message = serializer.validated_data['description']
                greeting = Greeting(message=message)
                greeting.save()
                logger.info('Saved greeting: %s', message)
                if data['message'] == 'hello':
                    data['message'] = 'goodbye'
                    logger.info('Data editted: %s', data)
                    updated_data = json.dumps(data)
                    response = requests.post(
                        'http://localhost:8000/iblapp/save_greeting/', data=updated_data)
                    logger.info(
                        'Called API again with updated data: %s', response.json())
                    return Response(serializer.data)
                return Response(serializer.data)
            else:
                logger.error('Invalid data: %s', serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            logger.error('Invalid data: JSON decoding error')
            return JsonResponse({"result": "error", "message": "Json decoding error"}, status=400)
