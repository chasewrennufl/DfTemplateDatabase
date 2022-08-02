from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
import os
from google.cloud import dialogflow


def make_published(modeladmin, request, queryset):
    """
    Mark the given survey as published
    """
    count = queryset.update(is_published=True)
    message = ngettext(
        "%(count)d survey was successfully marked as published.",
        "%(count)d surveys were successfully marked as published",
        count,
    ) % {"count": count}
    modeladmin.message_user(request, message)


make_published.short_description = _("Mark selected surveys as published")


def send_to_dialogflow(modeladmin, request, queryset):
    responses = queryset

    for response in responses.all():
        print(response)
        intents_client = dialogflow.IntentsClient()
        parent = dialogflow.AgentsClient.agent_path(response.project_id)
        prev_intents = intents_client.list_intents(request={"parent": parent})
        intents = response.intent_List.intents
        answers = response.answers
        intents.order_by('question')
        answers.order_by('question')
        for intent in intents.all():
            training_phrase = intent.trainingPhrase
            message = intent.message
            intent_attr = answers.filter(question = intent.question)
            for attr in intent_attr:
                display_name = 'intent for ' + attr.body
                training_phrase = training_phrase.replace('[*]', attr.body)
                message = message.replace('[*]', attr.body)
                training_phrases_parts = []
                training_phrases_parts.append(training_phrase)
                messages = []
                messages.append(message)
                try:
                    create_intent(response.project_id, display_name,  training_phrases_parts, messages)
                except:
                    print("Intent: " + display_name + " already exists" )
                
            

def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    

    intents_client = dialogflow.IntentsClient()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = response.auth.path
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


# for response in self.survey.responses.all():
# for question in self.survey.questions.all():
# Entry.objects.filter(pub_date__year=2005).order_by('-pub_date', 'headline')