from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from .question import Question
from .intentList import IntentList

try:
    from django.conf import settings

    if settings.AUTH_USER_MODEL:
        user_model = settings.AUTH_USER_MODEL
    else:
        user_model = User
except (ImportError, AttributeError):
    user_model = User


class Intent(models.Model):
    name = models.CharField(default='intent', max_length=25)
    created = models.DateTimeField(_("Creation date"), auto_now_add=True)
    updated = models.DateTimeField(_("Update date"), auto_now=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_("Question"), related_name="intents")
    intentList = models.ForeignKey(IntentList, on_delete=models.CASCADE, verbose_name=_("Intent List"), related_name="intents")
    user = models.ForeignKey(user_model, on_delete=models.SET_NULL, verbose_name=_("User"), null=True, blank=True)
    trainingPhrase = models.TextField()
    message = models.TextField()

def __str__(self):
         return f"{self.__class__.__name__} to '{self.intentList}' : '{self.question}'"   