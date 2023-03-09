from django.db import models
from django_extensions.db.models import (
    TimeStampedModel,
    ActivatorModel,
    TitleDescriptionModel
)
from utils.model_abstracts import Model


class Greeting(TimeStampedModel,
               ActivatorModel,
               TitleDescriptionModel,
               models.Model,
               ):

    class Meta:
        verbose_name_plural = 'Greetings'

    type = 'greetings'
    id = Model
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.message

# Create your models here.
