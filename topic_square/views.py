from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import Label, Topic, Picture

# Create your views here.


def get_labels(request):
    if request.method == 'GET':
        all_topic_list = []
        for i in list(Topic.objects.values('id')):
            all_topic_list.append(i['id'])
        labels = [{"id": -1, "title": "全部", "topic_list": all_topic_list}]
        label_list = list(Label.objects.values('id', 'title'))
        for label in label_list:
            topic_list = []
            topics = list(Topic.objects.filter(labels__in=[label['id']]).values('id'))
            for key in topics:
                topic_list.append(key['id'])
            label['topic_list'] = topic_list
        labels.extend(label_list)
        response = json.dumps(labels, cls=DjangoJSONEncoder)
        print(response)
        return HttpResponse(response, content_type="application/json")


def get_topics(request):
    if request.method == 'POST':
        post_list = request.POST['topics']
        if post_list == "":
            print("get_topics error: request got empty list")
            return HttpResponse("", content_type="application/json")
        elif "," in post_list:
            topic_id_list = post_list.split(',')
        else:
            topic_id_list = [post_list]
        print("list:", topic_id_list)
        topics = list(Topic.objects.filter(id__in=topic_id_list)
                      .values('id', 'title', 'user_name', 'user_id', 'content',
                              'create_time', 'comment_count', 'star_count', 'view_count'))
        for topic in topics:
            image_list = []
            image_dict_list = list(Picture.objects.filter(topic=topic['id']).values('image'))
            for image_dict in image_dict_list:
                image_list.append(image_dict['image'])
            topic['user_avatar'] = 'https://wmp.winng51.cn/static/' + str(Topic.objects.get(id=topic['id']).avatar)
            topic['images'] = ['https://wmp.winng51.cn/static/' + i for i in image_list if i != '']
            print(topic)
        response = json.dumps(topics, cls=DjangoJSONEncoder)
        return HttpResponse(response, content_type="application/json")
