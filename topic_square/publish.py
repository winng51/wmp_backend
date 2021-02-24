from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

from rest_framework_jwt.utils import jwt_decode_handler

import json
from .models import Label, Topic, Picture, Comment, SubComment, User


def pub_topic(request):
    if request.method == 'POST':
        token = request.POST['token']
        labels_id = request.POST['labels']
        user_info = jwt_decode_handler(token)

        user = User.objects.get(id=user_info['user_id'])
        labels = Label.objects.get(id in labels_id)
        new_topic = Topic(labels=labels, title=request.POST['title'], content=request.POST['content'],
                          user=user, is_homework=request.POST['homework'])
        new_topic.save()

        response_data = {
            "topicId": new_topic.id,
        }

        response = json.dumps(response_data, cls=DjangoJSONEncoder)
        return HttpResponse(response, content_type="application/json")
