from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

from datetime import datetime
import json
from .models import Label, Topic, Picture, Comment, SubComment, User


def get_add_labels(request):
    if request.method == 'GET':
        label_dict = {}
        label_list = list(Label.objects.filter(visible=True, selectable=True).values('id', 'title'))
        for label in label_list:
            label['select'] = False
            label_dict[label['id']] = label
        response = json.dumps(label_dict, cls=DjangoJSONEncoder)
        return HttpResponse(response, content_type="application/json")


def get_labels(request):
    if request.method == 'GET':
        all_topic_list = []
        for i in list(Topic.objects.order_by('-edit_time').values('id')):
            all_topic_list.append(i['id'])
        labels = {0: {"id": 0, "title": "全部", "topic_list": all_topic_list}}
        label_list = list(Label.objects.filter(visible=True).values('id', 'title'))
        for label in label_list:
            topic_list = []
            topics = list(Topic.objects.filter(labels__in=[label['id']]).values('id').order_by('-is_homework', '-edit_time'))
            if len(topics) == 0:
                continue
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
                      .values('id', 'title', 'user__username', 'user__id', 'user__avatar', 'content', 'edit_time',
                              'create_time', 'like_count', 'view_count'))
        topics_dict = {}
        dt = datetime.now()
        for topic in topics:
            print(dt - topic['create_time'])
            # 设置时间
            if (dt - topic['create_time']).days >= 180:
                topic['create_time'] = topic['create_time'].strftime('%Y-%m-%d')
            elif (dt - topic['create_time']).days >= 1:
                topic['create_time'] = topic['create_time'].strftime('%m-%d')
            else:
                topic['create_time'] = topic['create_time'].strftime('%H:%M:%S')
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
                .values('content', 'like_count', 'user__username', 'user__id', 'user__avatar')
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
        print("id:", topic_id, '被查看了')
        # 访问量+1
        t = Topic.objects.get(id=topic_id)
        t.view_count += 1
        t.save()
        topic = list(Topic.objects.filter(id=topic_id).
                     values('id', 'title', 'user__username', 'user__id', 'user__avatar', 'content', 'edit_time',
                            'create_time', 'like_count', 'star_count', 'view_count', 'stars', 'is_homework'))[0]
        # 添加标签及头像
        label_dict_list = list(Topic.objects.filter(id=topic['id']).values('labels', 'labels__title'))
        topic['labels'] = label_dict_list
        topic['user__avatar'] = 'https://wmp.winng51.cn/static/' + str(topic['user__avatar'])
        # 收藏数量只显示前十个
        if topic['stars'] != {}:
            new_list = []
            star_list = list(topic['stars'].items())[:10]
            for star_user in star_list:
                new_list.append({"avatar": star_user[1], "user_id": star_user[0]})
            topic['stars'] = new_list
        # 添加照片
        image_list = []
        image_dict_list = list(Picture.objects.filter(topic=topic['id']).values('image'))
        for image_dict in image_dict_list:
            image_list.append(image_dict['image'])
        topic['images'] = ['https://wmp.winng51.cn/static/' + i for i in image_list if i != '']
        # 添加评论
        comment_list = Comment.objects.filter(topic=topic['id']).order_by('-like_count') \
            .values('content', 'like_count', 'user__username', 'user__id', 'user__avatar', 'id', 'create_time')
        comment_count = comment_list.count()
        topic['comments'] = list(comment_list)
        for comment in topic['comments']:
            comment['user__avatar'] = 'https://wmp.winng51.cn/static/' + str(comment['user__avatar'])
        topic['comment_count'] = comment_count
        response = json.dumps(topic, cls=DjangoJSONEncoder)
        return HttpResponse(response, content_type="application/json")
