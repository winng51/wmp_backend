from django.http import HttpResponse
import json
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
from .models import Label, Topic, Picture, Comment, SubComment, User


# Create your views here.


def get_labels(request):
    if request.method == 'GET':
        all_topic_list = []
        for i in list(Topic.objects.order_by('-edit_time').values('id')):
            all_topic_list.append(i['id'])
        labels = {0: {"id": 0, "title": "全部", "topic_list": all_topic_list}}
        label_list = list(Label.objects.values('id', 'title'))
        for label in label_list:
            topic_list = []
            topics = list(Topic.objects.filter(labels__in=[label['id']]).values('id').order_by('-edit_time'))
            for key in topics:
                topic_list.append(key['id'])
            label['topic_list'] = topic_list
            labels[label['id']] = label
        response = json.dumps(labels, cls=DjangoJSONEncoder)
        return HttpResponse(response, content_type="application/json")


def get_homework_list(request):
    if request.method == 'GET':
        topic_list = []
        for i in list(Topic.objects.order_by('-create_time').filter(is_homework=True).values('id')):
            topic_list.append(i['id'])
        response = json.dumps(topic_list, cls=DjangoJSONEncoder)
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
                      .values('id', 'title', 'user__nickname', 'user__id', 'user__avatar', 'content', 'edit_time',
                              'create_time', 'like_count', 'view_count'))
        topics_dict = {}
        for topic in topics:
            # 添加标签
            label_dict_list = list(Topic.objects.filter(id=topic['id']).values('labels', 'labels__title'))
            topic['labels'] = label_dict_list
            # 添加照片
            image_list = []
            image_dict_list = list(Picture.objects.filter(topic=topic['id']).values('image'))
            for image_dict in image_dict_list:
                image_list.append(image_dict['image'])
            topic['user__avatar'] = 'https://wmp.winng51.cn/static/' + str(topic['user__avatar'])
            topic['images'] = ['https://wmp.winng51.cn/static/' + i for i in image_list if i != '']
            # 添加评论
            comment_list = Comment.objects.filter(topic=topic['id']).order_by('-like_count') \
                .values('content', 'like_count', 'user__nickname', 'user__id', 'user__avatar')
            comment_count = comment_list.count()
            topic['comments'] = list(comment_list)[:2]
            for comment in topic['comments']:
                comment['user__avatar'] = 'https://wmp.winng51.cn/static/' + str(comment['user__avatar'])
            topic['comment_count'] = comment_count
            topics_dict[topic['id']] = topic

        response = json.dumps(topics_dict, cls=DjangoJSONEncoder)
        return HttpResponse(response, content_type="application/json")


def get_topic(request):
    if request.method == 'POST':
        topic_id = request.POST['topic']
        print("id:", topic_id)
        topic = list(Topic.objects.filter(id=topic_id).
                     values('id', 'title', 'user__nickname', 'user__id', 'user__avatar', 'content', 'edit_time',
                            'create_time', 'like_count', 'star_count', 'view_count', 'stars'))[0]
        # 添加标签及头像
        label_dict_list = list(Topic.objects.filter(id=topic['id']).values('labels', 'labels__title'))
        topic['labels'] = label_dict_list
        topic['user__avatar'] = 'https://wmp.winng51.cn/static/' + str(topic['user__avatar'])
        # 添加照片
        image_list = []
        image_dict_list = list(Picture.objects.filter(topic=topic['id']).values('image'))
        for image_dict in image_dict_list:
            image_list.append(image_dict['image'])
        topic['images'] = ['https://wmp.winng51.cn/static/' + i for i in image_list if i != '']
        # 添加评论
        comment_list = Comment.objects.filter(topic=topic['id']).order_by('-like_count') \
            .values('content', 'like_count', 'user__nickname', 'user__id', 'user__avatar', 'id', 'create_time')
        comment_count = comment_list.count()
        topic['comments'] = list(comment_list)
        for comment in topic['comments']:
            comment['user__avatar'] = 'https://wmp.winng51.cn/static/' + str(comment['user__avatar'])
        topic['comment_count'] = comment_count
        response = json.dumps(topic, cls=DjangoJSONEncoder)
        return HttpResponse(response, content_type="application/json")
